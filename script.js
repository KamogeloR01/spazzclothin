let cart = JSON.parse(localStorage.getItem("cart")) || [];
let totalPrice = 0;

function addToCart(product) {

    cart.push(name,price);
    totalPrice += price;

    document.getElementById("cart-count").innerText = `Cart: R{cart.length} items - Total: RR{totalPrice.toFixed(2)}`;
    updateCartDisplay();

    {
function updateCartDisplay() {
    const cartItemsContainer = document.getElementById("cart-items");
    cartItemsContainer.innerHTML = "";     
    const cartItems = JSON.parse(localStorage.getItem("cart")) || [];   
    cartItems.forEach((item, index) => {
        const li = document.createElement("li");
        li.textContent = item.name + " - R" + item.price.toFixed(2);
        cartItemsContainer.appendChild(li);
    });

    document.getElementById("cart-count").innerText = `Cart: R{cartItems.length} items - Total: RR{totalPrice.toFixed(2)}`;
}

function checkoutt() {
    alert("Thank you for your purchase! Total: R" + totalPrice.toFixed(2));
}
