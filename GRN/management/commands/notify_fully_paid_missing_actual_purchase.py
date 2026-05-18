"""
Notify when vendor payments for a PR are fully completed but no Actual Purchase
was filed within FULLY_PAID_MISSING_ACTUAL_GRACE_DAYS after the last completion.

Schedule (example):
    python manage.py notify_fully_paid_missing_actual_purchase

Run daily via Task Scheduler / cron.
"""

from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Max, Q
from django.utils import timezone

from GRN.models import ActualPurchase, VendorPayment, purchase_orders


def fully_paid_anchor(pr: purchase_orders):
    payments = VendorPayment.objects.filter(pr=pr).exclude(status="cancelled")
    if not payments.exists():
        return None
    if payments.filter(~Q(status="completed")).exists():
        return None
    anchor = payments.aggregate(m=Max("completed_date"))["m"]
    return anchor


def has_actual_purchase_after(pr: purchase_orders, anchor):
    if anchor is None:
        return False
    return ActualPurchase.objects.filter(pr_no=pr, created_at__gte=anchor).exists()


class Command(BaseCommand):
    help = (
        "Email when a PR is fully paid (all vendor installments completed) but "
        "no Actual Purchase exists within the grace period after last completion."
    )

    def handle(self, *args, **options):
        grace_days = getattr(
            settings,
            "FULLY_PAID_MISSING_ACTUAL_GRACE_DAYS",
            2,
        )
        to_email = getattr(
            settings,
            "FULLY_PAID_MISSING_ACTUAL_REMINDER_EMAIL",
            "mekdi1610@gmail.com",
        )
        from_email = getattr(
            settings,
            "DEFAULT_FROM_EMAIL",
            settings.EMAIL_HOST_USER,
        )

        now = timezone.now()
        threshold = now - timedelta(days=grace_days)
        sent = 0
        cleared = 0

        for pr in purchase_orders.objects.all().iterator():
            anchor = fully_paid_anchor(pr)

            if anchor is None:
                if pr.fully_paid_missing_actual_notified_at:
                    purchase_orders.objects.filter(pk=pr.pk).update(
                        fully_paid_missing_actual_notified_at=None
                    )
                    cleared += 1
                continue

            if has_actual_purchase_after(pr, anchor):
                if pr.fully_paid_missing_actual_notified_at:
                    purchase_orders.objects.filter(pk=pr.pk).update(
                        fully_paid_missing_actual_notified_at=None
                    )
                    cleared += 1
                continue

            if anchor > threshold:
                continue

            if pr.fully_paid_missing_actual_notified_at:
                continue

            subject = f"[Mohan ERP] Actual Purchase needed for PR {pr.PR_no}"
            body = (
                f"Purchase request {pr.PR_no} has all vendor payments completed "
                f"(last completed at {anchor.isoformat()}), but no Actual Purchase "
                f"has been recorded since then (grace period: {grace_days} day(s)).\n\n"
                f"Please create an Actual Purchase in the ERP.\n"
            )
            send_mail(
                subject,
                body,
                from_email,
                [to_email],
                fail_silently=False,
            )
            purchase_orders.objects.filter(pk=pr.pk).update(
                fully_paid_missing_actual_notified_at=now
            )
            sent += 1
            self.stdout.write(self.style.SUCCESS(f"Sent reminder for PR {pr.PR_no}"))

        self.stdout.write(
            self.style.NOTICE(
                f"Done. Reminders sent: {sent}, notification flags cleared: {cleared}."
            )
        )
