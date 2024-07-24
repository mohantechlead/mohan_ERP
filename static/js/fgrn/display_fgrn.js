document.addEventListener('DOMContentLoaded', function () {
    const orderLinks = document.querySelectorAll('.order-link');
    console.log("p1")
    orderLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            console.log("p2")
            const fgrnID = this.getAttribute('data-order-id');
            window.location.href = `/FGRN/display_single_fgrn?FGRN_no=${fgrnID}`;
        });
    });
    // const orderLinks2 = document.querySelectorAll('.order-link2');
    // console.log("p1")
    // orderLinks2.forEach(function (link) {
    //     link.addEventListener('click', function (event) {
    //         event.preventDefault();
    //         console.log("p2")
    //         const orderID = this.getAttribute('data-order-id');
    //         window.location.href = `/FGRN/display_single_fgrn?PR_no=${orderID}`;
    //     });
    // });
});