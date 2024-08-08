document.addEventListener('DOMContentLoaded', function() {
    //const radioButtons = document.querySelectorAll('input[type="radio"]');
   
    const submitButton = document.querySelector('#submits');
    const addMoreBtn = document.getElementById('add-more');
   
    const totalNewForms = document.getElementById('id_GRN_items-TOTAL_FORMS')
    console.log(totalNewForms)
    
    addMoreBtn.addEventListener('click', add_new_form);

    submitButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Serialize form data
        const formData1 = new FormData(form1);
        const formData2 = new FormData(form2);

       
        // const prNoValue = formData1.get('PR_no');
        const grnNoValue = formData1.get('GRN_no');
       
        // console.log(prNoValue)
        // formData2.append('PR_no', prNoValue)
        formData2.append('GRN_no', grnNoValue)
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
                document.getElementById('form1').reset();
                document.getElementById('form2').reset();

                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
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
        


