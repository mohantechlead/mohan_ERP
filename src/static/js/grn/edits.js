document.addEventListener('DOMContentLoaded', function () {
       
    //const totalPriceField = $('#total-price');
    const submitButton = document.querySelector('#submits');
    const form1 = document.querySelector('#form1');

    
    //const quantityFields = $('.quantity');

    submitButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Serialize form data
        const formData1 = new FormData(form1);


        // Use fetch to submit both forms asynchronously
        fetch(form1.action, {
            method: 'POST',
            body: formData1
        })
            .then(response => {
                // Handle the response if needed
                console.log('Form 1 submitted:', response);

                // Submit the second form asynchronously
                
            })
           
            .catch(error => {
                console.error('Error:', error);
            });
    });


  
    console.log("try")

    

    // Apply initial calculation for existing forms
    
    



// Bind a change event to the price fields to recalculate on input change
//priceFields.change(calculateTotalPrice);
//quantityFields.change(calculateTotalPrice);

    
});