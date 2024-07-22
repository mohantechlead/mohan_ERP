document.addEventListener('DOMContentLoaded', function () {
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS')
    const submitButton = document.querySelector('#submits');
    const addMoreBtn = document.getElementById('add-more');
    const MR_no = document.getElementById('MR_no')
   
    addMoreBtn.addEventListener('click', add_new_form);

    submitButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default form submission

        validateInputs();
       
        // Serialize form data
        const formData1 = new FormData(form1);
        const formData2 = new FormData(form2);

        const prNoValue = formData1.get('MR_no');


        const amount = 1

       

        console.log(prNoValue)
        formData2.append('MR_no', prNoValue)

        // Use fetch to submit both forms asynchronously
        fetch(form1.action, {
            method: 'POST',
            body: formData1
            
        })
            .then(response => {
                if (!response.ok) {
                    // console.log(form_errors)
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
                if (response && !response.ok) {
                    // Handle errors from the second form submission, if any
                    return response.json().then(data => {
                        // 'data' will contain the form errors returned from the server
                        // Update the UI to display these errors to the user
                        console.log('Form 2 errors:', data.form_errors);
                        // Display the errors in the UI
                    });
                } else {
                    // Handle success or no error from the second form submission
                    // Reload the page or do any other necessary action
                    document.getElementById('form1').reset();
                    document.getElementById('form2').reset();

                    window.location.reload();
                }
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

    const setError = (element, message) => {
        const inputControl = element.parentElement;
        const errorDisplay = inputControl.querySelector('.error');
    
        errorDisplay.innerText = message;
        inputControl.classList.add('error');
        inputControl.classList.remove('success')
    }
    
    const setSuccess = element => {
        const inputControl = element.parentElement;
        const errorDisplay = inputControl.querySelector('.error');
    
        errorDisplay.innerText = '';
        inputControl.classList.add('success');
        inputControl.classList.remove('error');
    };
    
    const validateInputs = () => {
        const MR_noValue = MR_no.value.trim()
    
        if (MR_noValue === null || MR_noValue === ''){
            setError(MR_no, 'MR_noValue is required');
        } else {
            setSuccess(MR_no);
        }
    }

});



