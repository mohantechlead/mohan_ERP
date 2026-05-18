document.addEventListener('DOMContentLoaded', function () {
    const prInput = document.getElementById('actual_pr_no');
    const tbody = document.getElementById('actual_purchase_items_body');
    const paymentsSection = document.getElementById('actual_purchase_payments_section');
    const paymentsBody = document.getElementById('actual_purchase_payments_body');
    const paymentsHint = document.getElementById('actual_purchase_payments_hint');

    function escapeHtml(s) {
        if (s === null || s === undefined) return '';
        const d = document.createElement('div');
        d.textContent = String(s);
        return d.innerHTML;
    }

    function renderRows(items) {
        if (!items.length) {
            tbody.innerHTML = '<tr><td colspan="3">No PR items found.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        items.forEach((item) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <input type="hidden" name="pr_item_id[]" value="${item.pr_item_id}">
                    <input type="text" name="item_name[]" class="form-control readonly-cell" value="${item.item_name}" readonly>
                </td>
                <td>
                    <input type="number" step="0.01" name="requested_quantity[]" class="form-control readonly-cell" value="${item.requested_quantity}" readonly>
                </td>
                <td>
                    <input type="number" step="0.01" min="0" name="actual_quantity[]" class="form-control" value="${item.requested_quantity}">
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderPayments(payments) {
        if (!paymentsBody || !paymentsSection) return;
        if (!payments || !payments.length) {
            paymentsBody.innerHTML =
                '<tr><td colspan="8" class="text-muted text-center">No vendor payments recorded for this PR yet.</td></tr>';
            paymentsSection.style.display = 'block';
            if (paymentsHint) {
                paymentsHint.textContent =
                    'When vendor payments are completed, saving Actual Purchase can link them here.';
            }
            return;
        }
        paymentsBody.innerHTML = payments
            .map(
                (p) => `
            <tr>
                <td>${escapeHtml(p.installment_number)}</td>
                <td><a href="/GRN/vendor-payments/${encodeURIComponent(p.payment_number)}">${escapeHtml(p.payment_number)}</a></td>
                <td>${escapeHtml(p.payment_date)}</td>
                <td class="text-right">${Number(p.amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                <td>${escapeHtml(p.payment_type)}</td>
                <td>${escapeHtml(p.status)}</td>
                <td>${escapeHtml(p.reference_number || '—')}</td>
                <td>${p.linked ? '<span class="label label-default">Linked</span>' : '<span class="text-muted">—</span>'}</td>
            </tr>`
            )
            .join('');
        paymentsSection.style.display = 'block';
        if (paymentsHint) {
            paymentsHint.textContent =
                'Completed vendor payments that are not yet linked will be associated when you save.';
        }
    }

    function clearPayments() {
        if (paymentsBody) paymentsBody.innerHTML = '';
        if (paymentsSection) paymentsSection.style.display = 'none';
        if (paymentsHint) paymentsHint.textContent = 'Select a PR to load vendor payments.';
    }

    prInput.addEventListener('change', function () {
        const prNo = prInput.value.trim();
        if (!prNo) {
            tbody.innerHTML =
                '<tr><td colspan="3" class="text-center text-muted">Select PR to auto-populate items.</td></tr>';
            clearPayments();
            return;
        }

        fetch(`/GRN/get_actual_purchase_pr_items?pr_no=${encodeURIComponent(prNo)}`)
            .then((response) => response.json())
            .then((data) => {
                renderRows(data.items || []);
                renderPayments(data.payments || []);
            })
            .catch(() => {
                tbody.innerHTML = '<tr><td colspan="3">Failed to load PR items.</td></tr>';
                clearPayments();
            });
    });

    if (prInput.value.trim()) {
        prInput.dispatchEvent(new Event('change'));
    }
});
