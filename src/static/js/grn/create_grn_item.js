document.addEventListener('DOMContentLoaded', function() {
    const formset = document.querySelectorAll('.card-body');
    formset.forEach(function(item, index) {
        console.log('index')
        // const quantityInput = item.querySelector('input[name$="quantity"]');
        // const beforeVatInput = item.querySelector('input[name$="before_vat"]');
        // const totalPriceOutput = item.querySelector('output[name$="total_price"]');
        const priceInput = document.getElementById('price');
        const finalPriceOutput = document.getElementById('final_price');
    
        // Add input event listeners to calculate the total price
        // quantityInput.addEventListener('input', updateTotalPrice);
        // beforeVatInput.addEventListener('input', updateTotalPrice);
        
        // function updateTotalPrice() {
        //     const quantity = parseFloat(quantityInput.value) || 0;
        //     const beforeVat = parseFloat(beforeVatInput.value) || 0;
        //     const total = quantity * beforeVat;
        //     totalPriceOutput.textContent = total.toFixed(2);
        //     const price = parseFloat(priceInput.value) || 0;
        // }
        priceInput.addEventListener('input', updateFinalPrice);
        function updateFinalPrice() {
        let totalSum = 0.00;

        formsets.forEach(function(formset) {
            const price = parseFloat(formset.querySelector('input[name$="price"]').value) || 0;
            
            totalSum += price;
        });

        finalPriceOutput.textContent = totalSum.toFixed(2);
    }
    });
});