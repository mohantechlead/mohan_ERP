from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, render

from FGRN.models import FGRN, FGRN_item
from MR.models import MR, MR_item

from .forms import WIPForm, WIPItemForm
from .models import WIP, WIP_item


def _aggregate_lines_by_item(queryset):
    """Sum quantity per item (case-insensitive key). Returns (totals_dict, label_by_key)."""
    totals = defaultdict(float)
    labels = {}
    for row in queryset:
        raw = (getattr(row, 'item_name', None) or '').strip()
        if not raw or raw == '-':
            continue
        key = raw.casefold()
        q = getattr(row, 'quantity', None)
        q = float(q) if q is not None else 0.0
        totals[key] += q
        if key not in labels:
            labels[key] = raw
    return dict(totals), labels


def _merge_display_labels(*label_maps_in_order):
    out = {}
    for labels in label_maps_in_order:
        for key, label in labels.items():
            if key not in out:
                out[key] = label
    return out


def _flow_scoped_line_querysets(mr_no, wip_no, fgrn_no):
    """
    Line-item querysets for MR / WIP / FGRN variance scope.
    Global mode when no document numbers are set; otherwise only the requested documents.
    """
    use_global = not (mr_no or wip_no or fgrn_no)
    if use_global:
        return (
            MR_item.objects.all(),
            WIP_item.objects.all(),
            FGRN_item.objects.all(),
        )
    mr_qs = MR_item.objects.none()
    wip_qs = WIP_item.objects.none()
    fgrn_qs = FGRN_item.objects.none()
    if mr_no:
        try:
            mr_obj = MR.objects.get(MR_no=mr_no)
            mr_qs = MR_item.objects.filter(MR_no=mr_obj)
        except MR.DoesNotExist:
            pass
    if wip_no:
        try:
            wip_obj = WIP.objects.get(WIP_no=wip_no)
            wip_qs = WIP_item.objects.filter(WIP_no=wip_obj)
        except WIP.DoesNotExist:
            pass
    if fgrn_no:
        try:
            fgrn_obj = FGRN.objects.get(FGRN_no=fgrn_no)
            fgrn_qs = FGRN_item.objects.filter(FGRN_no=fgrn_obj)
        except FGRN.DoesNotExist:
            pass
    return mr_qs, wip_qs, fgrn_qs


@login_required(login_url='login_user')
def create_wip(request):
    ItemFormSet = formset_factory(WIPItemForm, extra=1)

    if request.method == 'POST':
        form = WIPForm(request.POST)
        formset = ItemFormSet(request.POST, prefix='items')

        if form.is_valid() and formset.is_valid():
            wip_instance = form.save()
            saved = 0
            for form_item in formset:
                cd = form_item.cleaned_data
                if not cd:
                    continue
                inv = cd.get('inventory_pick')
                qty = cd.get('quantity')
                if inv is None or qty is None or qty == '':
                    continue
                obj = form_item.save(commit=False)
                obj.WIP_no = wip_instance
                obj.item_name = inv.item_name
                obj.per_unit_kg = cd.get('per_unit_kg')
                obj.measurement_type = cd.get('measurement_type') or ''
                obj.save()
                saved += 1

            if saved == 0:
                wip_instance.delete()
                return JsonResponse(
                    {'form_errors': {'items': ['Add at least one line item with item and quantity.']}},
                    status=400,
                )

            return redirect('display_WIP')

        form_errors = dict(form.errors.items())
        formset_errors = {
            f'formset_{i}': dict(f.errors)
            for i, f in enumerate(formset)
            if f.errors
        }
        return JsonResponse(
            {'form_errors': {**form_errors, **formset_errors}},
            status=400,
        )

    return render(
        request,
        'wip/create_wip.html',
        {'form': WIPForm(), 'formset': ItemFormSet(prefix='items')},
    )


@login_required(login_url='login_user')
def display_wip(request):
    wip_list = WIP.objects.all().order_by('WIP_no')
    rows = []
    for w in wip_list:
        items = WIP_item.objects.filter(WIP_no=w.WIP_no)
        rows.append(
            {
                'WIP_no': w.WIP_no,
                'date': w.date,
                'work_center': w.work_center,
                'notes': w.notes,
                'wip_items': items,
            }
        )
    return render(
        request,
        'wip/display_wip.html',
        {'my_order': rows, 'wip_list': wip_list},
    )


@login_required(login_url='login_user')
def mrfwip_fgrn_flow_difference(request):
    """
    Compare line quantities for MR / WIP / FGRN (MR → WIP → FGRN).
    With no filters, aggregates all line items system-wide so the table loads immediately.

    With MR/WIP/FGRN numbers in the query string, each category is limited to that document.
    Optional ``item`` query narrows the result grid to item names containing that substring
    (case-insensitive). Items are matched by name (case-insensitive); duplicate lines on one document are summed.
    """
    mr_no = (request.GET.get('mr') or '').strip()
    wip_no = (request.GET.get('wip') or '').strip()
    fgrn_no = (request.GET.get('fgrn') or '').strip()
    item_q = (request.GET.get('item') or '').strip()

    errors = []
    mr_obj = wip_obj = fgrn_obj = None
    mr_agg, wip_agg, fgrn_agg = {}, {}, {}
    mr_lab, wip_lab, fgrn_lab = {}, {}, {}

    use_global = not (mr_no or wip_no or fgrn_no)

    mr_qs, wip_qs, fgrn_qs = _flow_scoped_line_querysets(mr_no, wip_no, fgrn_no)
    mr_agg, mr_lab = _aggregate_lines_by_item(mr_qs)
    wip_agg, wip_lab = _aggregate_lines_by_item(wip_qs)
    fgrn_agg, fgrn_lab = _aggregate_lines_by_item(fgrn_qs)

    if mr_no:
        try:
            mr_obj = MR.objects.get(MR_no=mr_no)
        except MR.DoesNotExist:
            errors.append(f'MR "{mr_no}" was not found.')
    if wip_no:
        try:
            wip_obj = WIP.objects.get(WIP_no=wip_no)
        except WIP.DoesNotExist:
            errors.append(f'WIP "{wip_no}" was not found.')
    if fgrn_no:
        try:
            fgrn_obj = FGRN.objects.get(FGRN_no=fgrn_no)
        except FGRN.DoesNotExist:
            errors.append(f'FGRN "{fgrn_no}" was not found.')

    display_labels = _merge_display_labels(mr_lab, wip_lab, fgrn_lab)
    all_keys = set(mr_agg) | set(wip_agg) | set(fgrn_agg)
    rows = []
    for key in sorted(all_keys):
        if use_global:
            mr_sel = wip_sel = fgrn_sel = True
        else:
            mr_sel = mr_obj is not None
            wip_sel = wip_obj is not None
            fgrn_sel = fgrn_obj is not None
        mq = float(mr_agg.get(key, 0.0)) if mr_sel else None
        wq = float(wip_agg.get(key, 0.0)) if wip_sel else None
        fq = float(fgrn_agg.get(key, 0.0)) if fgrn_sel else None

        d_mr_wip = (mq - wq) if (mr_sel and wip_sel) else None
        d_wip_fgrn = (wq - fq) if (wip_sel and fgrn_sel) else None

        rows.append(
            {
                'item': display_labels.get(key, key),
                'mr_qty': mq,
                'wip_qty': wq,
                'fgrn_qty': fq,
                'd_mr_wip': d_mr_wip,
                'd_wip_fgrn': d_wip_fgrn,
            }
        )

    if item_q:
        needle = item_q.casefold()
        rows = [r for r in rows if needle in (r.get('item') or '').casefold()]

    mr_list = MR.objects.order_by('MR_no').values_list('MR_no', flat=True)
    wip_list = WIP.objects.order_by('WIP_no').values_list('WIP_no', flat=True)
    fgrn_list = FGRN.objects.order_by('FGRN_no').values_list('FGRN_no', flat=True)

    return render(
        request,
        'wip/mrfwip_fgrn_flow_difference.html',
        {
            'rows': rows,
            'errors': errors,
            'mr_no': mr_no,
            'wip_no': wip_no,
            'fgrn_no': fgrn_no,
            'item_q': item_q,
            'mr_obj': mr_obj,
            'wip_obj': wip_obj,
            'fgrn_obj': fgrn_obj,
            'mr_list': mr_list,
            'wip_list': wip_list,
            'fgrn_list': fgrn_list,
            'use_global': use_global,
        },
    )


_FLOW_ITEM_SUGGEST_MAX_Q = 120


@login_required(login_url='login_user')
def mrfwip_flow_item_suggestions(request):
    """
    JSON: item names whose text contains ``q`` (minimum 3 characters, case-insensitive).
    Scoped to the same MR/WIP/FGRN line items as the variance page.
    """
    q = (request.GET.get('q') or '').strip()
    if len(q) < 3:
        return JsonResponse({'items': []})
    if len(q) > _FLOW_ITEM_SUGGEST_MAX_Q:
        q = q[:_FLOW_ITEM_SUGGEST_MAX_Q]

    mr_no = (request.GET.get('mr') or '').strip()
    wip_no = (request.GET.get('wip') or '').strip()
    fgrn_no = (request.GET.get('fgrn') or '').strip()

    mr_qs, wip_qs, fgrn_qs = _flow_scoped_line_querysets(mr_no, wip_no, fgrn_no)
    seen = {}
    for qs in (mr_qs, wip_qs, fgrn_qs):
        for name in qs.filter(item_name__icontains=q).values_list('item_name', flat=True).distinct():
            raw = (name or '').strip()
            if not raw or raw == '-':
                continue
            key = raw.casefold()
            if key not in seen:
                seen[key] = raw
    items = sorted(seen.values(), key=str.casefold)[:50]
    return JsonResponse({'items': items})
