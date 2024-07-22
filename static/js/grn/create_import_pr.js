document.addEventListener('DOMContentLoaded', function () {
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    const totalPriceField = $('#total-price');
    const submitButton = document.querySelector('#submits');
    const submitsButton = document.querySelector('#submitss');
    const form1 = document.querySelector('#form1');
    const form2 = document.querySelector('#form2');
    const freight1 = document.getElementById('#freight1');
    const freight2 = document.getElementById('#freight2');
    const priceFields = document.querySelectorAll('.price');
    const addMoreBtn = document.getElementById('add-more');
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS')
    console.log(totalNewForms)
    console.log("try")
    
    addMoreBtn.addEventListener('click', add_new_form);

    for (var priceField of priceFields) {
        priceField.addEventListener('input', function() {
            // Update the final_price field
            console.log("yes")
        });
    }
    const quantityFields = $('.quantity');

    submitsButton.addEventListener('click', function (event) {
        event.preventDefault(); 
        calculateTotalPrice();
        console.log("calc")
    });
    submitButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Serialize form data
        const formData1 = new FormData(form1);
        const formData2 = new FormData(form2);

        const freightPrice = formData1.get('freight1');
        const prNoValue = formData1.get('PR_no');

        if (freightPrice) {
            formData1.append('freight', freightPrice)
            console.log(freightPrice,"1")
        }
        else{
            const freightPrice = formData1.get('freight2');
            if (freightPrice) {
                formData1.append('freight', freightPrice)
                console.log(freightPrice,"2")
        }
        }
        console.log(prNoValue)
        formData2.append('PR_no', prNoValue)

        // Use fetch to submit both forms asynchronously
        fetch(form1.action, {
            method: 'POST',
            body: formData1
        })
            .then(response => {
                // Handle the response if needed
                console.log('Form 1 submitted:', response);

                // Submit the second form asynchronously
                return fetch(form2.action, {
                    method: 'POST',
                    body: formData2
                });
            })
            .then(response => {
                // Handle the response for the second form if needed
                console.log('Form 2 submitted:', response);
                //document.getElementById('form1').reset();
                //document.getElementById('form2').reset();

                // // Reload the page
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });


    function updateTotalPrice(form) {
        var quantity = parseFloat(form.find('.quantity').val());
        var price = parseFloat(form.find('.price').val());
        var total = quantity * price || 0;
        var total_price = quantity * price || 0;
        form.find('.before_vat').val(total.toFixed(2));
        form.find('.total_price').val(total_price.toFixed(2));
    }

    $(document).on('input', '.item-list .quantity, .item-list .price', function () {
        var form = $(this).closest('.item-list');
        updateTotalPrice(form);
    });

    // Apply initial calculation for existing forms
    $('.item-list').each(function () {
        var form = $(this);
        console.log("lists")
        updateTotalPrice(form);
        
    });
    radioButtons.forEach(button => {
    button.addEventListener('change', function() {
        // Hide all input elements
        hideAllInputs();
        console.log("trys")
        // Show the input element corresponding to the selected radio button
        const inputId = 'input_' + this.value;
        const inputElement = document.getElementById(inputId);
        if (inputElement) {
            inputElement.style.display = 'block';
        }
    });
});

function hideAllInputs() {
    const inputElements = document.querySelectorAll('[id^="input_"]');
    inputElements.forEach(element => {
        element.style.display = 'none';
    });
}

function calculateTotalPrice() {
    var total = 0
   
    const formsets = $('.item-list');
    const priceFields = $('.total_price');
    const quantityFields = $('.quantity');
    const total_price_fields = document.querySelectorAll('.total_price');
    $('.item-list').each(function() {
        
    
        // Within each formset, select the 'total_price' fields
        const totalFields = $(this).find('.total_price');
        
        totalFields.each(function() {
        const price = parseFloat($(this).val()) || 0;
        console.log(price,"price")
        total += price;
        console.log(total,"loop")
        });
        console.log(total)

        // Update the total for this formset
        totalPriceField.val(total.toFixed(2));  // Update the 'value' of the field
        totalPriceField.text('Total Price: $' + total.toFixed(2));  // Update the displayed text
    });
        }

// Call the calculation function when the page loads
calculateTotalPrice();

// Bind a change event to the price fields to recalculate on input change
//priceFields.change(calculateTotalPrice);
//quantityFields.change(calculateTotalPrice);


function add_new_form(args) {
        // Your code to add a new form here
        const currentForms = document.getElementsByClassName('item-list')
        let currentFormsCount = currentForms.length + 1
        console.log(currentForms.length)
        console.log(totalNewForms);
        const copyFormTarget = document.getElementById('form-lists')
        const copyEmptyForm = document.getElementById('empty-form').cloneNode(true);
        copyEmptyForm.setAttribute('class', 'item-list form-group col-md-5 text-dark')
        copyEmptyForm.setAttribute('id', `form-${currentFormsCount}`)
// Clear input values in the cloned form
        const regex = new RegExp('__prefix__','g')
        copyEmptyForm.querySelectorAll('input').forEach(function(input) {
            input.value = '';
        });
        copyEmptyForm.innerHTML = copyEmptyForm.innerHTML.replace(regex,currentFormsCount)
        // Append the cloned form to the form list
        totalNewForms.value = currentFormsCount + 1;
        copyFormTarget.appendChild(copyEmptyForm);
        const priceFields = document.querySelectorAll('.price');
        const totalFields = document.querySelectorAll('.total_price');
        const quantityFields = document.querySelectorAll('.quantity');
        
        
        
    }
});
