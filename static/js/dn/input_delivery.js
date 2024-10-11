document.addEventListener('DOMContentLoaded', function () {
    const delivery_number = document.getElementById('delivery_number');
    const submitButton = document.querySelector('#submit'); 
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS');
    const addMoreBtn = document.getElementById('add-more'); 
    // const date = document.getElementById('date');
    const confirmationModal = document.getElementById('confirmationModal');
    const confirmSubmitButton = document.getElementById('confirmSubmit');
    const cancelSubmitButton = document.getElementById('cancelSubmit');
    const fgrnDisplay = document.getElementById('fgrnDisplay');
    const itemListDisplay = document.getElementById('itemListDisplay');
    const serial_no = document.getElementById('serial_no')

    submitButton.addEventListener('click', function(event) {
    event.preventDefault();

    // Populate the confirmation modal with delivery number and item list
    fgrnDisplay.textContent = "Delivery Number: " + delivery_number.value;

    // Clear previous items
    itemListDisplay.innerHTML = '';
    document.querySelectorAll('.item-list').forEach(function(form) {
        const itemName = form.querySelector('[name$=description]').value; // Select by name attribute
        const quantity = form.querySelector('[name$=quantity]').value; // Select by name attribute
        const listItem = document.createElement('li');
        listItem.textContent = `Item: ${itemName}, Quantity: ${quantity}`;
        itemListDisplay.appendChild(listItem);
    });

    // Show the confirmation modal
    confirmationModal.style.display = "block";
});

confirmSubmitButton.addEventListener('click', function() {
    confirmationModal.style.display = "none";

    const form1 = document.getElementById('form1');
    const formData = new FormData(form1);

    fetch(form1.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                const errorContainer = document.getElementById('error-container');
                errorContainer.innerHTML = ''; // Clear previous errors
                if (data.form_errors) {
                    const errorList = document.createElement('ul');
                    for (const key in data.form_errors) {
                        if (Object.prototype.hasOwnProperty.call(data.form_errors, key)) {
                            const errorItem = document.createElement('li');
                            errorItem.textContent = `${key}: ${data.form_errors[key].join(', ')}`; // Show all error messages
                            errorList.appendChild(errorItem);
                        }
                    }
                    errorContainer.appendChild(errorList);
                }
                throw new Error('Form submission failed');
            });
        } else {
            // Clear form and reload page only if submission is successful
            document.getElementById('form1').reset();
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle the error message display
        alert("An error occurred. Please check the form and try again.");
    });
});

    function add_new_form(args) {
        const currentForms = document.getElementsByClassName('item-list');
        let currentFormsCount = currentForms.length + 1;
        const copyFormTarget = document.getElementById('form-lists');
        const copyEmptyForm = document.getElementById('empty-form').cloneNode(true);
        copyEmptyForm.setAttribute('class', 'item-list form-group col-md-3 text-dark');
        copyEmptyForm.setAttribute('id', `form-${currentFormsCount}`);
        const regex = new RegExp('__prefix__', 'g');
        copyEmptyForm.querySelectorAll('input').forEach(function (input) {
            input.value = '';
        });
        copyEmptyForm.innerHTML = copyEmptyForm.innerHTML.replace(regex, currentFormsCount);
        totalNewForms.value = currentFormsCount;
        copyFormTarget.appendChild(copyEmptyForm);
    } 

     function updateTotalPrice(form) {
        var per_unit_kg = parseFloat(form.find('#per_unit_kg').val());
        var no_of_unit = parseFloat(form.find('#no_of_unit').val());
        var total = per_unit_kg * no_of_unit || 0;
        // var total_price = total + (total * 0.15)
        form.find('#quantity').val(total.toFixed(2));
        // form.find('.total_price').val(total_price.toFixed(2));
    }

    $(document).on('input', '.item-list #per_unit_kg, .item-list #no_of_unit', function () {
        var form = $(this).closest('.item-list');
        updateTotalPrice(form);
    });

    // Apply initial calculation for existing forms
    $('.item-list').each(function () {
        var form = $(this);
        updateTotalPrice(form);
    });
});
