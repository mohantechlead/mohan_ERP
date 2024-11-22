document.addEventListener('DOMContentLoaded', function() {
    //const radioButtons = document.querySelectorAll('input[type="radio"]');
    const radioButtons = document.querySelectorAll('.measurement_type');
    const submitButton = document.querySelector('#submits');
    const submitsButton = document.querySelector('#submitss');
    const addMoreBtn = document.getElementById('add-more');
    const priceFields = document.querySelectorAll('.price');
    const totalPriceField = $('#total-price');
    const totalVatField = $('#total-vat');
    const radioButtons2 = document.querySelectorAll('.payment_type');
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS')
    let vat_checked = document.getElementById('vat_is_checked')
    console.log(totalNewForms)
    console.log("try")
    const quantityFields = $('.quantity');
    const withholding_checkbox = document.getElementById("withholdingCheckbox");
    const discount_checkbox = document.getElementById("discountCheckbox");
    const vat_checkbox = document.getElementById("vatCheckbox");
    var excise = false
    var discount = false

    submitsButton.addEventListener('click', function (event) {
        event.preventDefault(); 
        calculateTotalPrice();
        console.log("calc")
    });
    addMoreBtn.addEventListener('click', add_new_form);
    
    var univ_total = 0
    var univ_vat = 0
    function calculateTotalPrice() {
    var total = 0
    var total_vat = 0
    var originalTotal = 0;
    var originalVat = 0;

    const formsets = $('.item-list');
    const total_price_fields = document.querySelectorAll('.total_price');
    const total_vat_fields = document.querySelectorAll('.before_vat');
    const withholdingApplied = withholding_checkbox.checked;
    const discountApplied = discount_checkbox.checked;
    
    $('.item-list').each(function() {
        
    
        // Within each formset, select the 'total_price' fields
        const totalFields = $(this).find('.total_price');
        const vatFields = $(this).find('.before_vat');
        totalFields.each(function() {
        const price = parseFloat($(this).val()) || 0;
     
        total += price;
        originalTotal += price; 
        });
        vatFields.each(function() {
        const vat_price = parseFloat($(this).val()) || 0;
        total_vat += vat_price;
        originalVat += vat_price;
      
        });
        
        console.log(total)
       
        // Update the total for this formset
        univ_total = total;
        univ_vat = total_vat;
        totalPriceField.val(total.toFixed(2));  // Update the 'value' of the field
        totalPriceField.text('Total Price: $' + total.toFixed(2)); 
        totalVatField.val(total_vat.toFixed(2));  // Update the 'value' of the field
        totalVatField.text('Before VAT Price: $' + total_vat.toFixed(2));  // Update the displayed text
    });
    withholding_checkbox.addEventListener("change", function () {
    console.log("The withholding checkbox was clicked.");

    const withholdingApplied = withholding_checkbox.checked;
    
    if (withholdingApplied) {
        const withholding_amount = total_vat * 0.05;
        total = (total_vat + withholding_amount) + (0.15 * (total_vat + withholding_amount));
        excise = true
    } else {
        total = originalTotal;
        excise = false// Reset to the original total price
    }
    univ_total = total;
    console.log(univ_total,total,"tots")

    // Update the displayed and input fields
    totalPriceField.val(total.toFixed(2));
    totalPriceField.text('Total Price: $' + total.toFixed(2));
});

discount_checkbox.addEventListener("change", function () {
    console.log("The discount checkbox was clicked.");

    const discountApplied = discount_checkbox.checked;
    console.log(total_vat)
    if (discountApplied) {
        const discount_amount = total_vat * 0.05;
        total_vat = (total_vat - discount_amount) ;
        total = (total_vat ) + (0.15 * (total_vat ))
        discount = true
    } else {
        total_vat = originalVat;
        total = originalTotal;
        discount = false// Reset to the original total price
    }
    univ_vat = total_vat;
    univ_total = total;
    console.log(univ_vat,univ_total,"vats")
    // Update the displayed and input fields
    totalVatField.val(univ_vat.toFixed(2));
    totalVatField.text('Before VAT Price: $' + univ_vat.toFixed(2));
    totalPriceField.val(univ_total.toFixed(2));
    totalPriceField.text('Total Price: $' + univ_total.toFixed(2));
});

vat_checkbox.addEventListener("change", function () {
    console.log("The vat checkbox was clicked.");
    vat_checked = !(vat_checked);
    const vatApplied = vat_checkbox.checked;
    console.log(total_vat,vat_checked)
    if (vatApplied) {
        const vat_removed_amount = total_vat * 0.05;
        without_vat = univ_vat;
        
    } else {
        without_vat = univ_total;
    }
    console.log(univ_vat,univ_total,"vats")
    // Update the displayed and input fields
    totalVatField.val(without_vat.toFixed(2));
    totalVatField.text('Before VAT Price: $' + without_vat.toFixed(2));
    totalPriceField.val(without_vat.toFixed(2));
    totalPriceField.text('Total Price: $' + without_vat.toFixed(2));
});
        }

// Call the calculation function when the page loads
calculateTotalPrice();
    
    
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
/* radioButtons2.forEach(button => {
    button.addEventListener('change', function() {
        // Hide all input elements
        hideAllInputs2();
        console.log("trys")
        // Show the input element corresponding to the selected radio button
        const inputId = 'input_' + this.value;
        const inputElement = document.getElementById(inputId);
        if (inputElement) {
            inputElement.style.display = 'block';
        }
    });
}); */
    function hideAllInputs() {
    const inputElements = document.querySelectorAll('[id^="input_"]');
    inputElements.forEach(element => {
        element.style.display = 'none';
    });
}
    function hideAllInputs2() {
        const inputElements = document.querySelectorAll('[id^="input2_"]');
        inputElements.forEach(element => {
            element.style.display = 'none';
        });
    }
    submitButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Serialize form data
        const formData1 = new FormData(form1);
        const formData2 = new FormData(form2);

        const freightPrice = formData1.get('freight1');
        const prNoValue = formData1.get('PR_no');

        
        formData1.set('PR_before_vat', univ_vat.toFixed(2));
        if (vat_checkbox.checked) {
                // If checkbox is checked, set PR_total_price based on some condition
                formData1.set('PR_total_price', (univ_vat ).toFixed(2)); // Example logic
            } else {
                // If checkbox is not checked, set PR_total_price based on default logic
                formData1.set('PR_total_price', univ_total.toFixed(2)); // Default logic
            }
        if (freightPrice) {
            formData1.append('freight', freightPrice)
        }
        else{
            const freightPrice = formData1.get('freight2');
            if (freightPrice) {
                formData1.append('freight', freightPrice)
        }
        }
        console.log(formData1,"ex")
        const amount = 1
        if (excise) {
            formData1.append('excise_tax',amount)
            
            console.log(formData1,"data")
            console.log("inside")
        }
        console.log(prNoValue)
        formData2.append('PR_no', prNoValue)
        formData2.append('vat_is_checked',vat_checked)
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
                //console.log('Form 2 submitted:', response);
                document.getElementById('form1').reset();
                document.getElementById('form2').reset();

                // Reload the page
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
        var total_price = total  + (total * 0.15)
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
        updateTotalPrice(form);
    });
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
                }
            });