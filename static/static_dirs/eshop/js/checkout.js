const form = document.getElementById("id_checkout_form");
const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const validateFormAndCheckout = () => {
    const url = '/orders/checkout/';
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfmiddlewaretoken
        },
        body: new FormData(form)
    }).then(response => {
        return response.json();
    }).then(data => {
        if (data.success) {
            console.log("Success Submitted");
            window.location.href = '/shop/product-list/';
        }
        else {
            console.log(data);
        }
    }).catch(error => {
        console.log(error);
    })
}

form.addEventListener('submit', (event) => {
    event.preventDefault();
    validateFormAndCheckout();
})