document.addEventListener('DOMContentLoaded', function () {
const FGRN_no = document.getElementById('FGRN_no');
const submitButton = document.querySelector('#submits'); 
const totalNewForms = document.getElementById('id_items-TOTAL_FORMS')
const addMoreBtn = document.getElementById('add-more'); 
addMoreBtn.addEventListener('click', add_new_form);

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
    }).then(response => {
            return fetch(form2.action, {
                method: 'POST',
                body: formData2
            });
            
    }).catch(error => {
        console.error('Error:', error);
    });
});
    

const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
}

const validateInputs = () => {
    const FGRN_noValue = FGRN_no.value.trim();

    if(FGRN_noValue === '' || FGRN_noValue === null) {
        setError(FGRN_no, 'FGRN Number is required');
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

});



