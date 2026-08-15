from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import VendorPayment, purchase_orders


def _admin_approvals(user):
    return user.is_authenticated and user.is_superuser


def _all_non_cancelled_completed_for_pr(pr: purchase_orders) -> bool:
    """True when every non-cancelled installment for this PR is completed."""
    active = VendorPayment.objects.filter(pr=pr).exclude(status="cancelled")
    if not active.exists():
        return False
    return all(p.status == "completed" for p in active)


def _payment_totals_for_pr(pr: purchase_orders, exclude_vp_id=None):
    """All non-cancelled installments count toward PR balance (pending + approved + completed)."""
    purchase_total = Decimal(str(pr.PR_before_vat or 0))
    qs = VendorPayment.objects.filter(
        pr=pr, status__in=("pending", "approved", "completed")
    )
    if exclude_vp_id is not None:
        qs = qs.exclude(id=exclude_vp_id)
    total_applied = sum(Decimal(str(v.amount)) for v in qs)
    remaining = purchase_total - total_applied
    if remaining < Decimal("0"):
        remaining = Decimal("0")
    completion = "full" if remaining == Decimal("0") else "partial"
    return purchase_total, total_applied, remaining, completion


def vp_detail_dict(vp: VendorPayment):
    pr = vp.pr
    purchase_total, applied_without_me, _, _ = _payment_totals_for_pr(pr, exclude_vp_id=vp.id)
    amt = Decimal(str(vp.amount))
    if vp.status == "cancelled":
        total_incl_this = applied_without_me
    else:
        total_incl_this = applied_without_me + amt
    remaining = purchase_total - total_incl_this
    if remaining < Decimal("0"):
        remaining = Decimal("0")
    completion = "full" if remaining == Decimal("0") else "partial"
    return {
        "id": str(vp.id),
        "vp": vp,
        "payment_number": vp.payment_number,
        "installment_number": vp.installment_number,
        "payment_date": vp.payment_date,
        "purchase_number": pr.PR_no,
        "supplier_name": vp.supplier_name,
        "payment_type": vp.payment_type,
        "amount": float(vp.amount),
        "status": vp.status,
        "approved_by": vp.approved_by.get_username() if vp.approved_by else None,
        "approval_date": vp.approval_date,
        "completed_by": vp.completed_by.get_username() if vp.completed_by else None,
        "completed_date": vp.completed_date,
        "cancelled_by": vp.cancelled_by.get_username() if vp.cancelled_by else None,
        "cancelled_date": vp.cancelled_date,
        "reference_number": vp.reference_number,
        "status_remark": vp.status_remark,
        "purchase_total": float(purchase_total),
        "total_paid": float(total_incl_this),
        "remaining_amount": float(remaining),
        "payment_completion_status": completion,
        "remark": vp.remark,
        "linked_actual_purchase_id": (
            str(vp.actual_purchase_id) if vp.actual_purchase_id else None
        ),
    }


def _normalize_payment_type(raw: str) -> str:
    pt = (raw or "").strip().lower()
    if pt == "paritial":
        pt = "partial"
    return pt


def _group_rows(row_dicts):
    """Group payment rows by purchase (PR); mirrors dd-frontend display page."""
    by_pr = {}
    for p in row_dicts:
        key = p["purchase_number"]
        if key not in by_pr:
            by_pr[key] = {
                "purchase_number": key,
                "supplier_name": p["supplier_name"],
                "total_amount": float(p["amount"]),
                "remaining_amount": float(p["remaining_amount"]),
                "completion_status": p["payment_completion_status"],
                "payments": [p],
            }
        else:
            cur = by_pr[key]
            cur["total_amount"] += float(p["amount"])
            cur["remaining_amount"] = min(
                cur["remaining_amount"],
                float(p["remaining_amount"]),
            )
            if (
                cur["completion_status"] == "full"
                or p["payment_completion_status"] == "full"
            ):
                cur["completion_status"] = "full"
            else:
                cur["completion_status"] = "partial"
            cur["payments"].append(p)
    for g in by_pr.values():
        g["payments"].sort(key=lambda x: x["installment_number"] or 0)
    return list(by_pr.values())


@login_required(login_url="login_user")
def create_vendor_payment(request):
    existing = VendorPayment.objects.select_related("pr").all()
    existing_details = [vp_detail_dict(v) for v in existing]

    purchase_options = []
    for pr in purchase_orders.objects.all().order_by("PR_no"):
        _, _, rem, _ = _payment_totals_for_pr(pr)
        purchase_options.append(
            {
                "pr_no": pr.PR_no,
                "vendor_name": pr.vendor_name or "",
                "remaining": float(rem),
            }
        )

    if request.method == "POST":
        pr_no = (request.POST.get("pr_no") or "").strip()
        payment_date = request.POST.get("payment_date")
        payment_type = _normalize_payment_type(request.POST.get("payment_type"))
        amount_raw = request.POST.get("amount")
        remark = (request.POST.get("remark") or "").strip() or None

        ctx = {
            "purchase_options": purchase_options,
            "existing_rows": existing_details,
            "post": request.POST,
        }
        if not pr_no:
            messages.error(request, "Purchase (PR) is required.")
            return render(request, "vendor_payments/create_vendor_payment.html", ctx)

        pr = get_object_or_404(purchase_orders, PR_no__iexact=pr_no)
        _, _, remaining, _ = _payment_totals_for_pr(pr)

        if remaining <= Decimal("0"):
            messages.error(request, "This purchase is already fully paid.")
            return render(request, "vendor_payments/create_vendor_payment.html", ctx)

        if payment_type not in ("partial", "full"):
            messages.error(request, "Payment type must be Partial or Full.")
            return render(request, "vendor_payments/create_vendor_payment.html", ctx)

        if payment_type == "full":
            amount = remaining
        else:
            if not amount_raw:
                messages.error(request, "Amount is required for partial payment.")
                return render(request, "vendor_payments/create_vendor_payment.html", ctx)
            amount = Decimal(str(amount_raw))
            if amount <= Decimal("0"):
                messages.error(request, "Amount must be greater than 0.")
                return render(request, "vendor_payments/create_vendor_payment.html", ctx)
            if amount > remaining:
                messages.error(
                    request,
                    f"Partial amount cannot exceed remaining amount ({remaining}).",
                )
                return render(request, "vendor_payments/create_vendor_payment.html", ctx)

        last_installment = (
            VendorPayment.objects.filter(pr=pr)
            .order_by("-installment_number")
            .values_list("installment_number", flat=True)
            .first()
            or 0
        )
        next_installment = int(last_installment) + 1
        generated_payment_number = f"{pr.PR_no}-PAY-{next_installment}"

        VendorPayment.objects.create(
            payment_number=generated_payment_number,
            installment_number=next_installment,
            payment_date=payment_date,
            pr=pr,
            supplier_name=(pr.vendor_name or "")[:255] or "-",
            payment_type=payment_type,
            amount=amount,
            remark=remark,
            status="pending",
        )
        messages.success(request, "Vendor payment created.")
        return redirect("display_vendor_payments")

    return render(
        request,
        "vendor_payments/create_vendor_payment.html",
        {
            "purchase_options": purchase_options,
            "existing_rows": existing_details,
            "prefill_pr": (request.GET.get("pr_no") or "").strip(),
        },
    )


@login_required(login_url="login_user")
def display_vendor_payments(request):
    rows = VendorPayment.objects.select_related("pr").all().order_by(
        "-payment_date", "-installment_number"
    )
    detail_rows = [vp_detail_dict(vp) for vp in rows]
    grouped = _group_rows(detail_rows)
    return render(
        request,
        "vendor_payments/display_vendor_payments.html",
        {"grouped": grouped, "rows": rows},
    )


@login_required(login_url="login_user")
def vendor_payments_completed(request):
    rows = VendorPayment.objects.select_related("pr").filter(status="completed").order_by(
        "-payment_date"
    )
    detail_rows = [vp_detail_dict(vp) for vp in rows]
    return render(
        request,
        "vendor_payments/vendor_payments_list.html",
        {
            "title": "Completed Vendor Payments",
            "detail_rows": detail_rows,
            "list_type": "completed",
        },
    )


@login_required(login_url="login_user")
def vendor_payments_rejected(request):
    rows = VendorPayment.objects.select_related("pr").filter(status="cancelled").order_by(
        "-payment_date"
    )
    detail_rows = [vp_detail_dict(vp) for vp in rows]
    return render(
        request,
        "vendor_payments/vendor_payments_list.html",
        {
            "title": "Rejected (Cancelled) Vendor Payments",
            "detail_rows": detail_rows,
            "list_type": "rejected",
        },
    )


@login_required(login_url="login_user")
@user_passes_test(_admin_approvals, login_url="login_user")
def vendor_payment_approvals(request):
    rows = (
        VendorPayment.objects.select_related("pr")
        .filter(status="pending")
        .order_by("payment_date", "installment_number")
    )
    detail_rows = [vp_detail_dict(vp) for vp in rows]
    by_pr = defaultdict(list)
    for d in detail_rows:
        by_pr[d["purchase_number"]].append(d)
    approval_groups = []
    for pr_no in sorted(by_pr.keys()):
        payments = sorted(by_pr[pr_no], key=lambda x: x["installment_number"])
        total_amt = sum(Decimal(str(p["amount"])) for p in payments)
        approval_groups.append(
            {
                "purchase_number": pr_no,
                "supplier_name": payments[0]["supplier_name"],
                "count": len(payments),
                "total_amount": total_amt,
                "payments": payments,
            }
        )
    return render(
        request,
        "vendor_payments/vendor_payment_approvals.html",
        {"approval_groups": approval_groups},
    )


@login_required(login_url="login_user")
@user_passes_test(_admin_approvals, login_url="login_user")
def vendor_payment_status(request):
    """All approved installments that can be marked completed or cancelled."""
    rows = (
        VendorPayment.objects.select_related("pr")
        .filter(status="approved")
        .order_by("pr_id", "installment_number")
    )
    detail_rows = [vp_detail_dict(vp) for vp in rows]
    by_pr = defaultdict(list)
    for d in detail_rows:
        by_pr[d["purchase_number"]].append(d)
    status_groups = []
    for pr_no in sorted(by_pr.keys()):
        payments = sorted(by_pr[pr_no], key=lambda x: x["installment_number"])
        total_amt = sum(Decimal(str(p["amount"])) for p in payments)
        status_groups.append(
            {
                "purchase_number": pr_no,
                "supplier_name": payments[0]["supplier_name"],
                "count": len(payments),
                "total_amount": total_amt,
                "payments": payments,
            }
        )
    return render(
        request,
        "vendor_payments/vendor_payment_status.html",
        {
            "status_groups": status_groups,
            "actual_purchase_prompt_pr": request.session.pop(
                "vendor_payment_prompt_actual_purchase", None
            ),
        },
    )


@login_required(login_url="login_user")
def vendor_payment_purchase_summary(request, pr_no: str):
    pr = get_object_or_404(purchase_orders, PR_no__iexact=pr_no.strip())
    payments = VendorPayment.objects.filter(pr=pr).order_by("installment_number")
    detail_rows = [vp_detail_dict(vp) for vp in payments]
    purchase_total, total_applied, remaining, completion = _payment_totals_for_pr(pr)
    return render(
        request,
        "vendor_payments/vendor_payment_purchase_summary.html",
        {
            "pr": pr,
            "detail_rows": detail_rows,
            "purchase_total": float(purchase_total),
            "total_applied": float(total_applied),
            "remaining": float(remaining),
            "completion": completion,
        },
    )


@login_required(login_url="login_user")
def vendor_payment_detail(request, payment_number: str):
    vp = get_object_or_404(VendorPayment, payment_number__iexact=payment_number.strip())
    return render(
        request,
        "vendor_payments/vendor_payment_detail.html",
        {"detail": vp_detail_dict(vp)},
    )


@login_required(login_url="login_user")
def edit_vendor_payment(request, payment_number: str):
    vp = get_object_or_404(VendorPayment, payment_number__iexact=payment_number.strip())
    if vp.status != "pending":
        messages.error(request, "Only pending vendor payments can be edited.")
        return redirect("vendor_payment_detail", payment_number=vp.payment_number)

    detail = vp_detail_dict(vp)
    max_for_partial = Decimal(str(detail["remaining_amount"])) + Decimal(str(vp.amount))

    if request.method == "POST":
        payment_date = request.POST.get("payment_date")
        payment_type = _normalize_payment_type(request.POST.get("payment_type"))
        amount_raw = request.POST.get("amount")
        remark = (request.POST.get("remark") or "").strip() or None

        _, _, remaining_without_me, _ = _payment_totals_for_pr(vp.pr, exclude_vp_id=vp.id)

        if payment_type not in ("partial", "full"):
            messages.error(request, "Payment type must be Partial or Full.")
            return render(
                request,
                "vendor_payments/edit_vendor_payment.html",
                {"detail": detail, "max_for_partial": float(max_for_partial)},
            )

        if payment_type == "full":
            amount = remaining_without_me
        else:
            if not amount_raw:
                messages.error(request, "Amount is required for partial payment.")
                return render(
                    request,
                    "vendor_payments/edit_vendor_payment.html",
                    {"detail": detail, "max_for_partial": float(max_for_partial)},
                )
            amount = Decimal(str(amount_raw))
            if amount <= Decimal("0"):
                messages.error(request, "Amount must be greater than 0.")
                return render(
                    request,
                    "vendor_payments/edit_vendor_payment.html",
                    {"detail": detail, "max_for_partial": float(max_for_partial)},
                )
            if amount > remaining_without_me:
                messages.error(
                    request,
                    f"Partial amount cannot exceed remaining amount ({remaining_without_me}).",
                )
                return render(
                    request,
                    "vendor_payments/edit_vendor_payment.html",
                    {"detail": detail, "max_for_partial": float(max_for_partial)},
                )

        vp.payment_date = payment_date
        vp.payment_type = payment_type
        vp.amount = amount
        vp.remark = remark
        vp.save()
        messages.success(request, "Vendor payment updated.")
        return redirect("vendor_payment_detail", payment_number=vp.payment_number)

    return render(
        request,
        "vendor_payments/edit_vendor_payment.html",
        {"detail": detail, "max_for_partial": float(max_for_partial)},
    )


@login_required(login_url="login_user")
def delete_vendor_payment(request, payment_number: str):
    vp = get_object_or_404(VendorPayment, payment_number__iexact=payment_number.strip())
    if request.method != "POST":
        return redirect("display_vendor_payments")
    if vp.status != "pending":
        messages.error(request, "Only pending vendor payments can be deleted.")
        return redirect("display_vendor_payments")
    vp.delete()
    messages.success(request, "Vendor payment deleted.")
    return redirect("display_vendor_payments")


@login_required(login_url="login_user")
@user_passes_test(_admin_approvals, login_url="login_user")
def approve_vendor_payment(request, payment_number: str):
    vp = get_object_or_404(VendorPayment, payment_number__iexact=payment_number.strip())
    if request.method != "POST":
        return redirect("vendor_payment_approvals")
    if vp.status != "pending":
        messages.error(request, "Only pending vendor payments can be approved.")
        return redirect("vendor_payment_approvals")
    vp.status = "approved"
    vp.approved_by = request.user
    vp.approval_date = timezone.now()
    vp.save()
    messages.success(request, "Vendor payment approved.")
    return redirect("vendor_payment_approvals")


@login_required(login_url="login_user")
@user_passes_test(_admin_approvals, login_url="login_user")
def approve_vendor_payments_bulk(request):
    if request.method != "POST":
        return redirect("vendor_payment_approvals")
    purchase_number = (request.POST.get("purchase_number") or "").strip()
    numbers = [n.strip() for n in request.POST.getlist("payment_number") if n.strip()]
    if not numbers:
        messages.error(request, "Select at least one payment to approve.")
        return redirect("vendor_payment_approvals")
    pr = get_object_or_404(purchase_orders, PR_no__iexact=purchase_number)
    approved_count = 0
    now = timezone.now()
    seen = set()
    with transaction.atomic():
        for pn in numbers:
            if pn in seen:
                continue
            seen.add(pn)
            vp = (
                VendorPayment.objects.select_for_update()
                .filter(
                    payment_number__iexact=pn,
                    pr=pr,
                    status="pending",
                )
                .first()
            )
            if vp:
                vp.status = "approved"
                vp.approved_by = request.user
                vp.approval_date = now
                vp.save(
                    update_fields=[
                        "status",
                        "approved_by",
                        "approval_date",
                    ]
                )
                approved_count += 1
    if approved_count:
        messages.success(
            request,
            f"Approved {approved_count} payment(s) for PR {pr.PR_no}.",
        )
    else:
        messages.warning(
            request,
            "No matching pending payments were approved (wrong PR or already processed).",
        )
    return redirect("vendor_payment_approvals")


@login_required(login_url="login_user")
@user_passes_test(_admin_approvals, login_url="login_user")
def update_vendor_payment_status(request, payment_number: str):
    vp = get_object_or_404(VendorPayment, payment_number__iexact=payment_number.strip())
    if request.method != "POST":
        return redirect("vendor_payment_status")

    new_status = (request.POST.get("status") or "").strip().lower()
    ref = (request.POST.get("reference_number") or "").strip()
    remark = (request.POST.get("remark") or "").strip()

    if vp.status != "approved":
        messages.error(
            request,
            "Only approved vendor payments can be marked as completed or cancelled.",
        )
        return redirect("vendor_payment_status")
    if new_status not in ("completed", "cancelled"):
        messages.error(request, "Status must be completed or cancelled.")
        return redirect("vendor_payment_status")
    if new_status == "completed" and not ref:
        messages.error(
            request,
            "Reference number is required when completing a vendor payment.",
        )
        return redirect("vendor_payment_status")
    if new_status == "cancelled" and not remark:
        messages.error(request, "Remark is required when cancelling a vendor payment.")
        return redirect("vendor_payment_status")

    vp.status = new_status
    if new_status == "completed":
        vp.completed_by = request.user
        vp.completed_date = timezone.now()
        vp.reference_number = ref
        vp.status_remark = None
        vp.cancelled_by = None
        vp.cancelled_date = None
    else:
        vp.cancelled_by = request.user
        vp.cancelled_date = timezone.now()
        vp.status_remark = remark
        vp.reference_number = None
        vp.completed_by = None
        vp.completed_date = None
    vp.save()
    messages.success(request, f"Vendor payment marked as {new_status}.")
    if new_status == "completed" and _all_non_cancelled_completed_for_pr(vp.pr):
        request.session["vendor_payment_prompt_actual_purchase"] = vp.pr.PR_no
    return redirect("vendor_payment_status")
