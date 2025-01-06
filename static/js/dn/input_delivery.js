document.addEventListener('DOMContentLoaded', function () {
    const FGRN_no = document.getElementById('FGRN_no');
    const submitButton = document.querySelector('#submit'); 
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS')
    const addMoreBtn = document.getElementById('add-more'); 
    const recieved_from = document.getElementById('recieved_from')
    const recieved_by = document.getElementById('recieved_by')
    const date = document.getElementById('date')
    addMoreBtn.addEventListener('click', add_new_form);
    const calculateTotalButton = document.querySelector('#calculate_total');
    const orderInput = document.querySelector('input[name="serial_no"]');  // The order number input field
    const descriptionSelect = document.querySelector('#description');  // The description dropdown

   


    calculateTotalButton.addEventListener('click', function (event) {
        event.preventDefault();
        calculateTotalPrice();
    });

    function calculateTotalPrice() {
        var total = 0
        var price = 0          
        const formsets = $('.item-list');
        const quantityFields = $('#total_quantity');
         $('.item-list').each(function() {
            const total_quantity_fields = $(this).find('#quantity');
            const total_price_fields = $(this).find('#total_price');

            total_quantity_fields.each(function() {
            const quantity = parseFloat($(this).val()) || 0;
            total += quantity;
            }); 

            total_price_fields.each(function() {
                const total_price = parseFloat($(this).val()) || 0;
                price += total_price;
            });

        quantityFields.val(total.toFixed(2))
        quantityFields.text(total.toFixed(2))
        });
    }
     
    calculateTotalPrice();
    order_items_list();

    submitButton.addEventListener('click', function(event){
        event.preventDefault();
        // validateInputs();
        
        const formData1 = new FormData(form1);
        const formData2 = new FormData(form2);
        const prNoValue = formData1.get('delivery_number');
        const orderValue = formData1.get('serial_no');
        const amount = 1
        console.log(prNoValue)
        formData2.append('delivery_number', prNoValue)
        formData2.append('serial_no',orderValue)
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

    function order_items_list(){
        const serialNoInput = document.querySelector('input[name="serial_no"]'); // Adjust based on input's name
        const descriptionSelect = document.querySelectorAll('select[name$="-description"]'); // For all description fields in formset
    
        if (serialNoInput) {
            serialNoInput.addEventListener('change', function () {
                const serialNo = serialNoInput.value;
    
                // Fetch updated items based on the serial_no
                fetch(`/DN/get_order_items/?serial_no=${serialNo}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.items) {
                            descriptionSelect.forEach(select => {
                                select.innerHTML = ''; // Clear existing options
    
                                // Add new options
                                data.items.forEach(item => {
                                    const option = document.createElement('option');
                                    option.value = item;
                                    option.textContent = item;
                                    select.appendChild(option);
                                });
                            });
                        } else {
                            descriptionSelect.forEach(select => {
                                select.innerHTML = '<option value="">No items available</option>';
                            });
                        }
                    })
                    .catch(error => console.error('Error fetching items:', error));
            });
        }
    }

    function updateTotalPrice(form) {
        var per_unit_kg = parseFloat(form.find('#per_unit_kg').val());
        // var unit_price = parseFloat(form.find('#unit_price').val());
        var no_of_unit = parseFloat(form.find('#no_of_unit').val());
        // var quantity = parseFloat(form.find('#quantity').val());

             
        var total = per_unit_kg * no_of_unit  || 0;
        // var final_price = unit_price * quantity || 0;   
        

        form.find('#quantity').val(total.toFixed(2));
        // form.find('#total_price').val(final_price.toFixed(2));
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
    
    