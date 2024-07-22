document.addEventListener('DOMContentLoaded', function() {
        
    const addMoreBtn = document.getElementById('add-more');
    const totalNewForms = document.getElementById('id_items-TOTAL_FORMS')
    console.log("try")
    
    addMoreBtn.addEventListener('click', add_new_form);
    
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