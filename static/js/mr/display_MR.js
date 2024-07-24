document.addEventListener('DOMContentLoaded', function () {
    const orderLinks = document.querySelectorAll('.order-link');
    console.log("p1")
    orderLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            console.log("p2")
            const MRID = this.getAttribute('data-order-id');
            window.location.href = `/MR/display_single_mr?MR_no=${MRID}`;
        });
    });
});