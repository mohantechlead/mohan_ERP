document.addEventListener('DOMContentLoaded', function () {
    const form1 = document.getElementById('form1');
    const submitButton = document.querySelector('#submits');
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS');
    const addMoreBtn = document.getElementById('add-more');
    const calculateTotalButton = document.querySelector('#calculate_total');
    const postUrl = form1 ? form1.getAttribute('action') : '';
    const nextUrl = form1 ? form1.getAttribute('data-next-url') || '' : '';

    if (addMoreBtn) {
        addMoreBtn.addEventListener('click', add_new_form);
    }

    if (calculateTotalButton) {
        calculateTotalButton.addEventListener('click', function (event) {
            event.preventDefault();
            calculateTotalPrice();
        });
    }

    function quantityInputInRow(row) {
        if (!row) return null;
        return row.querySelector('input[name*="quantity"]');
    }

    function calculateTotalPrice() {
        let total = 0;
        const formsets = document.querySelectorAll('.item-list');
        const quantityFields = document.getElementById('total_quantity');

        formsets.forEach(function (formset) {
            const q = quantityInputInRow(formset);
            if (q) {
                total += parseFloat(q.value) || 0;
            }
        });

        if (quantityFields) {
            quantityFields.textContent = total.toFixed(2);
        }
    }

    function updateRowQuantityFromKg(row) {
        if (!row) return;
        var pkgEl = row.querySelector('input[name*="per_unit_kg"]');
        var nouEl = row.querySelector('input[name*="no_of_unit"]');
        var qtyEl = quantityInputInRow(row);
        if (!qtyEl) return;
        var pkg = parseFloat((pkgEl && pkgEl.value) || '0') || 0;
        var nou = parseFloat((nouEl && nouEl.value) || '0') || 0;
        if (!pkg && !nou) return;
        qtyEl.value = (pkg * nou).toFixed(2);
    }

    const formLists = document.getElementById('form-lists');
    if (formLists) {
        formLists.addEventListener('input', function (e) {
            var name = e.target.getAttribute('name') || '';
            if (name.indexOf('per_unit_kg') === -1 && name.indexOf('no_of_unit') === -1) {
                return;
            }
            var row = e.target.closest('.item-list');
            updateRowQuantityFromKg(row);
            calculateTotalPrice();
        });
    }

    calculateTotalPrice();

    document.querySelectorAll('.item-list').forEach(function (row) {
        var pkgEl = row.querySelector('input[name*="per_unit_kg"]');
        var nouEl = row.querySelector('input[name*="no_of_unit"]');
        if ((pkgEl && String(pkgEl.value).trim()) || (nouEl && String(nouEl.value).trim())) {
            updateRowQuantityFromKg(row);
        }
    });

    if (submitButton && form1) {
        submitButton.addEventListener('click', function (event) {
            event.preventDefault();
            const formData = new FormData(form1);

            fetch(postUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(function (response) {
                    if (!response.ok) {
                        return response.json().then(function (data) {
                            const errorContainer = document.getElementById('error-container');
                            errorContainer.innerHTML = '';
                            if (data.form_errors) {
                                const errorList = document.createElement('ul');
                                Object.keys(data.form_errors).forEach(function (key) {
                                    if (Object.prototype.hasOwnProperty.call(data.form_errors, key)) {
                                        const err = data.form_errors[key];
                                        const errorItem = document.createElement('li');
                                        errorItem.textContent =
                                            key +
                                            ': ' +
                                            (typeof err === 'object' ? JSON.stringify(err) : err);
                                        errorList.appendChild(errorItem);
                                    }
                                });
                                errorContainer.appendChild(errorList);
                            }
                            throw new Error('Form submission failed');
                        });
                    }
                    if (nextUrl) {
                        window.location.href = nextUrl;
                    } else {
                        window.location.reload();
                    }
                })
                .catch(function () {});
        });
    }

    function add_new_form() {
        const currentForms = document.getElementsByClassName('item-list');
        const currentFormsCount = currentForms.length;
        const copyFormTarget = document.getElementById('form-lists');
        const emptyEl = document.getElementById('empty-form');
        if (!emptyEl || !copyFormTarget || !totalNewForms) {
            return;
        }
        const copyEmptyForm = emptyEl.cloneNode(true);
        copyEmptyForm.classList.remove('hidden');
        copyEmptyForm.setAttribute('class', 'card-body row item-list form-group col-md-3 text-dark');
        copyEmptyForm.setAttribute('id', 'form-' + String(currentFormsCount));
        const regex = new RegExp('__prefix__', 'g');
        copyEmptyForm.innerHTML = copyEmptyForm.innerHTML.replace(regex, String(currentFormsCount));
        copyEmptyForm.querySelectorAll('input, select, textarea').forEach(function (el) {
            if (el.type !== 'hidden') {
                el.value = '';
            }
        });
        totalNewForms.value = String(currentFormsCount + 1);
        copyFormTarget.appendChild(copyEmptyForm);
    }
});
