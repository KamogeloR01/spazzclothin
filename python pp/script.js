let cart = [];
try {
    cart = JSON.parse(localStorage.getItem("cart")) || [];
} catch (e) {
    cart = [];
}

const $ = (id) => document.getElementById(id);
const drawer = $("cart-drawer");
const overlay = $("overlay");
const toggle = $("cart-toggle");

function save() {
    try { localStorage.setItem("cart", JSON.stringify(cart)); } catch (e) {}
}

function total() {
    return cart.reduce((sum, i) => sum + i.price * i.qty, 0);
}

function openCart() {
    drawer.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    overlay.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    $("cart-close").focus();
}

function closeCart() {
    drawer.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    overlay.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    toggle.focus();
}

function addToCart(id, name, price) {
    const found = cart.find((i) => i.id === id);
    if (found) found.qty += 1;
    else cart.push({ id: id, name: name, price: price, qty: 1 });
    save();
    render();
}

function changeQty(id, delta) {
    const item = cart.find((i) => i.id === id);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) cart = cart.filter((i) => i.id !== id);
    save();
    render();
}

function removeItem(id) {
    cart = cart.filter((i) => i.id !== id);
    save();
    render();
}

function makeButton(label, text, onClick, className) {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = text;
    b.setAttribute("aria-label", label);
    if (className) b.className = className;
    b.addEventListener("click", onClick);
    return b;
}

function render() {
    const list = $("cart-items");
    list.innerHTML = "";

    cart.forEach((item) => {
        const li = document.createElement("li");

        const name = document.createElement("span");
        name.className = "name";
        name.textContent = item.name;

        const price = document.createElement("span");
        price.className = "line-price";
        price.textContent = "R" + (item.price * item.qty).toFixed(2);

        const qty = document.createElement("div");
        qty.className = "qty";
        const count = document.createElement("span");
        count.textContent = item.qty;
        qty.append(
            makeButton("Decrease quantity of " + item.name, "-", () => changeQty(item.id, -1)),
            count,
            makeButton("Increase quantity of " + item.name, "+", () => changeQty(item.id, 1))
        );

        const remove = makeButton("Remove " + item.name, "Remove", () => removeItem(item.id), "remove");

        li.append(name, price, qty, remove);
        list.appendChild(li);
    });

    const count = cart.reduce((n, i) => n + i.qty, 0);
    $("cart-count").textContent = count;
    $("cart-total").textContent = total().toFixed(2);
    $("cart-empty").hidden = cart.length > 0;
}

document.querySelectorAll(".add").forEach((btn) => {
    btn.addEventListener("click", () => {
        addToCart(btn.dataset.id, btn.dataset.name, Number(btn.dataset.price));
        const original = btn.textContent;
        btn.textContent = "Added";
        setTimeout(() => { btn.textContent = original; }, 900);
    });
});

toggle.addEventListener("click", openCart);
$("cart-close").addEventListener("click", closeCart);
overlay.addEventListener("click", closeCart);
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && drawer.classList.contains("open")) closeCart();
});

$("checkout").addEventListener("click", () => {
    const status = $("status");
    if (cart.length === 0) {
        status.textContent = "Your cart is empty. Add an item first.";
        return;
    }
    status.textContent = "Order placed. Total: R" + total().toFixed(2) + ". Thank you for your purchase.";
    cart = [];
    save();
    render();
});

render();
