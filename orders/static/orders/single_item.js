// Select sections to show based on dish type
var dishtype = document.querySelector('#dish-type').innerHTML;
var dishname = document.querySelector('#dish-name').innerHTML;
var subx = document.querySelector('#subx');
if (dishtype === 'Pizza') {
    var dishsplit = dishname.split(" ");
    var topping = document.querySelector('#id_topping');

    if (dishsplit.includes("1") || dishsplit.includes("2") || dishsplit.includes("3")) {
        document.querySelector('#topping').style.display = "block";
        // Allow a certain number of selected options for Topping
        document.querySelector('#form').onsubmit = event => {
            event.preventDefault();
            if (dishsplit.includes("1") && topping.selectedOptions.length != 1) {
                alert("Must choose 1 topping");
            }
            else if (dishsplit.includes("2") && topping.selectedOptions.length != 2) {
                alert("Must choose 2 toppings");
            }
            else if (dishsplit.includes("3") && topping.selectedOptions.length != 3) {
                alert("Must choose 3 toppings");
            }
            else {
                document.querySelector('#form').submit();
            }            
        }
    }
    document.querySelector('#size').style.display = "block";
}


else if (dishtype === 'Sub') {
    document.querySelector('#subX').style.display = "block";
    document.querySelector('#size').style.display = "block";

    // If Steak, enable all subX for click. Else, only 'Extra Cheese'
    if (dishname != 'Steak') {
        for (let i = 0; i < 3; i++) {
            document.querySelector('#id_subx_' + [i]).disabled = true;
            document.querySelector('label[for="id_subx_' + [i] +'"]').className = "text-muted";
        }
    }
    checked_count = 0
    document.querySelectorAll('input[name=subx]').forEach(input => {
        input.onclick = () => {
            if (input.checked) {
                // Refer to price & final_price variable below
                final_price += 0.5 * parseInt(quantity_value);
                checked_count += 1;
            }
            else {
                final_price -= 0.5 * parseInt(quantity_value);
                checked_count -= 1;
            }
            price.innerHTML = final_price.toFixed(2);
        }
    })
}

else if (dishtype === 'Dinner Platter') {
    document.querySelector('#size').style.display = "block";
}
else {
    // Deselect default size Small for Pasta and Salad
    document.querySelector('#id_size').selectedIndex = -1;
}
// Display price based on size and quantity
var size = document.querySelector('#id_size');
var size_value = size.options[size.selectedIndex].value;

var quantity = document.querySelector('#id_quantity');
var quantity_value = quantity.options[quantity.selectedIndex].value;

var price = document.querySelector('#id_price');
var price_from_size = price.getAttribute('value');
var final_price = parseFloat(price_from_size);

// Change price when size changes
size.onchange = () => {
    size_value = size.options[size.selectedIndex].value;

    if (size_value == 'l') {
        price.setAttribute('value', localStorage.getItem("price_large"));
        price_from_size = price.getAttribute('value');
        
    }
    else {
        price.setAttribute('value', localStorage.getItem("price_small"));
        price_from_size = price.getAttribute('value');
    }
    
    final_price = (parseFloat(price_from_size) + checked_count * 0.5) * parseInt(quantity_value);
    price.innerHTML = final_price.toFixed(2);
}

// Change price when quantity changes
quantity.onchange = () => {
    quantity_value = quantity.options[quantity.selectedIndex].value;
    final_price = (parseFloat(price_from_size) + checked_count * 0.5) * parseInt(quantity_value);
    
    // Show price with 2 decimal places, toFixed also convert number to string
    price.innerHTML = final_price.toFixed(2);
}

// Change cart number whenever a new item is added to cart
// var current_num, updated_num;
// document.querySelector('#form').onsubmit = event => {
//     event.preventDefault();
//     current_num = parseInt(document.querySelector('#cart-num').innerHTML);
//     updated_num = current_num + 1;
//     await sleep(2000);
//     document.querySelector('#form').submit();

// }