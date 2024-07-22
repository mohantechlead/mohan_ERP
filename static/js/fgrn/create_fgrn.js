document.addEventListener('DOMContentLoaded', function () {
    const FGRN_no = document.getElementById('FGRN_no');
    const submitButton = document.querySelector('#submits'); 
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS')
    const addMoreBtn = document.getElementById('add-more'); 
    const recieved_from = document.getElementById('recieved_from')
    const recieved_by = document.getElementById('recieved_by')
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
        const quantityFields = $('#quantity');
        
         $('.item-list').each(function() {
            const total_quantity_fields = $(this).find('#quantity');

            total_quantity_fields.each(function() {
            const quantity = parseFloat($(this).val()) || 0;
            total += quantity;
            });            
          console.log(total)

          priceFields.val(total.toFixed(2))
          priceFields.text('Total Price: ' + total.toFixed(2))
        });
    }
     
    calculateTotalPrice();

    submitButton.addEventListener('click', function(event){
        event.preventDefault();
        validateInputs();
        
        const formData1 = new FormData(form1);
        const formData2 = new FormData(form2);
        const prNoValue = formData1.get('FGRN_no');
        const amount = 1
        console.log(prNoValue)
        formData2.append('FGRN_no', prNoValue)
    
        fetch(form1.action, {
            method: 'POST',
            body: formData1
        })
        .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                // Display form 1 errors in the error container
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
                throw new Error('Form 1 submission failed');
            });
        } else {
            // If the response is successful, proceed to the next form submission
            return fetch(form2.action, {
                method: 'POST',
                body: formData2
            });
        }
        })
        .then(response => {
        if (!response.ok) {
            // Handle errors from the second form submission, if any
            return response.json().then(data => {
                // Display form 2 errors in the UI
                console.log('Form 2 errors:', data.form_errors);
                // Handle the errors in the UI without reloading the page
            });
        } else {
            // Handle success or no error from the second form submission
            // Reload the page or perform other necessary actions
            document.getElementById('form1').reset();
            document.getElementById('form2').reset();

            // Remove the code below if you don't want the page to reload
            window.location.reload();
        }
        })
        .catch(error => {
        console.error('Error:', error);
                    });
            });
            // });
        
    
    const setError = (element, message) => {
        const inputControl = element.parentElement;
        const errorDisplay = inputControl.querySelector('.error');
    
        errorDisplay.innerText = message;
        inputControl.classList.add('error');
        inputControl.classList.remove('success');
    }

    const setSuccess = element => {
        const inputControl = element.parentElement;
        const errorDisplay = inputControl.querySelector('.error');
    
        errorDisplay.innerText = '';
        inputControl.classList.add('success');
        inputControl.classList.remove('error');
    };
    
    const validateInputs = () => {
        const FGRN_noValue = FGRN_no.value.trim();
        const recieved_fromValue = recieved_from.value.trim();
        const recieved_byValue = recieved_by.value.trim();
        const dateValue = date.value.trim();
    
        if(FGRN_noValue === '' || FGRN_noValue === null) {
            setError(FGRN_no, 'FGRN Number is required');
        } else{
            setSuccess(FGRN_no)
        }
        if(recieved_fromValue === ''|| recieved_fromValue === null){
            setError(recieved_from, 'Recieved From is required')
        }else{
            setSuccess(recieved_from)
        }
        if(recieved_byValue === ''|| recieved_byValue === null){
            setError(recieved_by, 'Recieved By is required')
        }else{
            setSuccess(recieved_by)
        }
        if(dateValue === '' || dateValue === null){
            setError(date, 'Date is required')
        }else{
            setSuccess(date)
        }
    };
    
    
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
    
    