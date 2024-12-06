document.addEventListener('DOMContentLoaded', function () {
    const MR_no = document.getElementById('MR_no');
    const submitButton = document.querySelector('#submits'); 
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS')
    const addMoreBtn = document.getElementById('add-more'); 
    const date = document.getElementById('date')
    addMoreBtn.addEventListener('click', add_new_form);
    const calculateTotalButton = document.querySelector('#calculate_total');

    calculateTotalButton.addEventListener('click', function (event) {
        event.preventDefault();
        calculateTotalPrice();
    });

    function calculateTotalPrice() {
        var total = 0
                      
        const formsets = $('.item-list');
        const priceFields = $('#total_price');
        const quantityFields = $('#total_quantity');
        
         $('.item-list').each(function() {
            const total_quantity_fields = $(this).find('#quantity');

            total_quantity_fields.each(function() {
            const quantity = parseFloat($(this).val()) || 0;
            total += quantity;
            });            
          console.log(total)

          quantityFields.val(total.toFixed(2))
          quantityFields.text(total.toFixed(2))
        });
    }
     
    calculateTotalPrice();

    submitButton.addEventListener('click', function(event){
        event.preventDefault();
    
        const formData = new FormData(form1);
    
        fetch(form1.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    // Display form errors in the error container
                    const errorContainer = document.getElementById('error-container');
                    errorContainer.innerHTML = ''; // Clear previous errors
                    if (data.form_errors) {
                        const errorList = document.createElement('ul');
                        for (const key in data.form_errors) {
                            if (Object.prototype.hasOwnProperty.call(data.form_errors, key)) {
                                const errorItem = document.createElement('li');
                                errorItem.textContent = `${key}: ${data.form_errors[key]}`;
                                errorList.appendChild(errorItem);
                            }
                        }
                        errorContainer.appendChild(errorList);
                    }
                    // Throw an error to trigger the catch block
                    throw new Error('Form submission failed');
                });
            } else {
                // Handle success or no error from the form submission
                document.getElementById('form1').reset();
    
                // Reload the page or perform other necessary actions
                window.location.reload();
            }
        })
    }); 
    
    function add_new_form(args) {
        // Your code to add a new form here
        const currentForms = document.getElementsByClassName('item-list')
        let currentFormsCount = currentForms.length + 1
        console.log(currentForms.length)
        console.log(totalNewForms);
        const copyFormTarget = document.getElementById('form-lists')
        const copyEmptyForm = document.getElementById('empty-form').cloneNode(true);
        copyEmptyForm.setAttribute('class', 'item-list form-group col-md-4 text-dark')
        copyEmptyForm.setAttribute('id', `form-${currentFormsCount}`)
        // Clear input values in the cloned form
        const regex = new RegExp('__prefix__', 'g')
        copyEmptyForm.querySelectorAll('input').forEach(function (input) {
            input.value = '';
        });
        copyEmptyForm.innerHTML = copyEmptyForm.innerHTML.replace(regex, currentFormsCount)
        // Append the cloned form to the form list
        totalNewForms.value = currentFormsCount + 1;
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
    
    

