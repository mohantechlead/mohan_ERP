document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.querySelector('#submit');
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS');
    const addMoreBtn = document.getElementById('add-more');
    const calculateTotalButton = document.querySelector('#calculate_total');

    addMoreBtn.addEventListener('click', add_new_form);
    if (window.initItemDescriptionComboboxes) {
        window.initItemDescriptionComboboxes();
    }

    calculateTotalButton.addEventListener('click', function (event) {
        event.preventDefault();
        calculateTotalPrice();
    });

    function calculateTotalPrice() {
        var total = 0;
        const quantityFields = $('#total_quantity');
        $('.item-list').each(function () {
            $(this).find('[id$="-quantity"], #quantity').each(function () {
                total += parseFloat($(this).val()) || 0;
            });
            quantityFields.val(total.toFixed(2));
            quantityFields.text(total.toFixed(2));
        });
    }

    calculateTotalPrice();
    order_items_list();

    submitButton.addEventListener('click', function (event) {
        event.preventDefault();

        const formData1 = new FormData(form1);
        const formData2 = new FormData(form2);
        formData2.append('delivery_number', formData1.get('delivery_number'));
        formData2.append('serial_no', formData1.get('serial_no'));

        fetch(form1.action, {
            method: 'POST',
            body: formData1
        })
            .then(function (response) {
                if (!response.ok) {
                    return response.json().then(function (data) {
                        const errorContainer = document.getElementById('error-container');
                        errorContainer.innerHTML = '';
                        if (data.form_errors) {
                            const errorList = document.createElement('ul');
                            for (const key in data.form_errors) {
                                if (Object.prototype.hasOwnProperty.call(data.form_errors, key)) {
                                    const errorItem = document.createElement('li');
                                    errorItem.textContent = key + ': ' + data.form_errors[key];
                                    errorList.appendChild(errorItem);
                                }
                            }
                            errorContainer.appendChild(errorList);
                        }
                        throw new Error('Form 1 submission failed');
                    });
                }
                return fetch(form2.action, {
                    method: 'POST',
                    body: formData2
                });
            })
            .then(function (response) {
                if (!response.ok) {
                    return response.json().then(function (data) {
                        console.log('Form 2 errors:', data.form_errors);
                    });
                }
                document.getElementById('form1').reset();
                document.getElementById('form2').reset();
                window.location.reload();
            });
    });

    function add_new_form() {
        const currentForms = document.getElementsByClassName('item-list');
        const newIndex = currentForms.length;
        const copyFormTarget = document.getElementById('form-lists');
        const copyEmptyForm = document.getElementById('empty-form').cloneNode(true);
        copyEmptyForm.classList.remove('hidden');
        copyEmptyForm.classList.add('item-list', 'form-group', 'col-md-4', 'text-dark');
        copyEmptyForm.id = 'form-' + (newIndex + 1);

        const regex = new RegExp('__prefix__', 'g');
        copyEmptyForm.querySelectorAll('input').forEach(function (input) {
            input.value = '';
            delete input.dataset.comboboxInit;
        });
        copyEmptyForm.innerHTML = copyEmptyForm.innerHTML.replace(regex, newIndex);
        totalNewForms.value = newIndex + 1;
        copyFormTarget.appendChild(copyEmptyForm);
        if (window.initItemDescriptionComboboxes) {
            window.initItemDescriptionComboboxes(copyEmptyForm);
        }
    }

    function order_items_list() {
        const serialNoInput = document.querySelector('input[name="serial_no"]');
        if (!serialNoInput) {
            return;
        }

        function loadOrderItems() {
            const serialNo = serialNoInput.value.trim();
            if (!serialNo) {
                return;
            }
            fetch('/DN/get_order_items/?serial_no=' + encodeURIComponent(serialNo))
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if (data.items && data.items.length && window.setItemDescriptionOptions) {
                        window.setItemDescriptionOptions(data.items);
                    }
                })
                .catch(function (error) {
                    console.error('Error fetching items:', error);
                });
        }

        serialNoInput.addEventListener('change', loadOrderItems);
        serialNoInput.addEventListener('blur', loadOrderItems);
    }

    function updateTotalPrice(form) {
        var per_unit_kg = parseFloat(form.find('[id$="-per_unit_kg"], #per_unit_kg').val());
        var no_of_unit = parseFloat(form.find('[id$="-no_of_unit"], #no_of_unit').val());
        var total = per_unit_kg * no_of_unit || 0;
        form.find('[id$="-quantity"], #quantity').val(total.toFixed(2));
    }

    $(document).on('input', '.item-list [id$="-per_unit_kg"], .item-list [id$="-no_of_unit"], .item-list #per_unit_kg, .item-list #no_of_unit', function () {
        updateTotalPrice($(this).closest('.item-list'));
    });

    $('.item-list').each(function () {
        updateTotalPrice($(this));
    });
});
