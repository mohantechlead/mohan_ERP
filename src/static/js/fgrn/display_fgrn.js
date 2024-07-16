document.addEventListener('DOMContentLoaded', function () {
    const orderLinks = document.querySelectorAll('.order-link');
    console.log("p1")
    orderLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            console.log("p2")
            const orderID = this.getAttribute('data-order-id');
            window.location.href = `/cosmic/display_single_order?order_no=${orderID}`;
        });
    });
    const orderLinks2 = document.querySelectorAll('.order-link2');
    console.log("p1")
    orderLinks2.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            console.log("p2")
            const orderID = this.getAttribute('data-order-id');
            window.location.href = `/GRN/display_single_order?PR_no=${orderID}`;
        });
    });
});