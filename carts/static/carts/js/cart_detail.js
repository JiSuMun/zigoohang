let cartTotalAmount = 0

if (!isAuthenticated) {
  let storedCart = localStorage.getItem('cart');

  // JSON 문자열을 객체로 변환합니다.
  let cart = JSON.parse(storedCart);

  cartDiv = document.getElementById('cart_div');

  async function getProductInfoAndRender(product_id, quantity) {
    return new Promise((resolve) => {
      $.get(`/carts/api/products/${product_id}/`, function(data) {
      // const productInfo = `
      //   <tr>
      //     <td><img src="${data.image}" alt="" width="100px"></td>
      //     <td>${data.name}</td>
      //     <td>${data.price}</td>
      //     <td>${quantity}</td>
      //     <td>${data.price * quantity}</td>
      //   </tr>
      //   `
      // document.querySelector('#cart_table > tbody').innerHTML += productInfo;

      // const cartDiv = document.createElement("div");
      // cartDiv.id = "cart_div";

      const productDataDiv = document.createElement("div");
      productDataDiv.id = `product_data-${data.id}`
      productDataDiv.setAttribute("data-product-price", data.price);


      const content = document.createElement("div");
      content.className = "cart_list_content";

      const checkboxCol = document.createElement("div");
      checkboxCol.className = "cart_checkbox_col";

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.name = "item_check";
      checkbox.value = `${data.id}`;

      // const hiddenInput = document.createElement("input");
      // hiddenInput.type = "hidden";
      // hiddenInput.name = "input_quantity";
      // hiddenInput.value = "1";
      // hiddenInput.id = "product_quantity-2";

      checkboxCol.appendChild(checkbox);
      // checkboxCol.appendChild(hiddenInput);

      const link = document.createElement("a");
      link.href = `/stores/${data.storeId}/${data.id}/`;
      link.className = "cart_product";

      const imgContainer = document.createElement("div");
      imgContainer.className = "cart_img_container";

      const image = document.createElement("img");
      image.src = `${data.image}`;
      image.alt = "";

      imgContainer.appendChild(image);

      const productText = document.createElement("div");
      productText.className = "cart_list_product_text";

      const productName = document.createElement("div");
      productName.className = "cart_list_name";
      productName.textContent = `${data.name}`;

      const productPrice = document.createElement("div");
      productPrice.className = "cart_list_price";
      productPrice.textContent = `${data.price.toLocaleString()}`;

      productText.appendChild(productName);
      productText.appendChild(productPrice);

      link.appendChild(imgContainer);
      link.appendChild(productText);

      const quantityCol = document.createElement("div");
      quantityCol.className = "cart_quantity_col";

      const quantityContainer = document.createElement("div");
      quantityContainer.className = "cart_quantity_container";

      const minusButton = document.createElement("button");
      minusButton.className = "cart_quantity_button";
      // minusButton.name = "quantity_btn";
      minusButton.setAttribute("type", "button");
      minusButton.setAttribute("onclick", `dicreaseItem(${data.id})`);
      minusButton.setAttribute("data-quantity-value", "-1");
      // minusButton.setAttribute("data-product-id", data.id);
      minusButton.textContent = "-";

      const quantityDisplay = document.createElement("div");
      quantityDisplay.className = "cart_quantity";
      quantityDisplay.id = `product_count-${data.id}`;
      quantityDisplay.textContent = quantity;

      const plusButton = document.createElement("button");
      plusButton.className = "cart_quantity_button";
      // plusButton.name = "quantity_btn";
      plusButton.setAttribute("type", "button");
      plusButton.setAttribute("onclick", `increaseItem(${data.id})`);
      plusButton.setAttribute("data-quantity-value", "1");
      // plusButton.setAttribute("data-product-id", data.id);
      plusButton.textContent = "+";

      quantityContainer.appendChild(minusButton);
      quantityContainer.appendChild(quantityDisplay);
      quantityContainer.appendChild(plusButton);

      quantityCol.appendChild(quantityContainer);

      const subtotal = document.createElement("div");
      subtotal.className = "cart_subtotal";
      subtotal.innerHTML = `<span id=\"sub_total-${data.id}\">${(data.price * quantity).toLocaleString()}</span> 원`;

      content.appendChild(productDataDiv);
      content.appendChild(checkboxCol);
      content.appendChild(link);
      content.appendChild(quantityCol);
      content.appendChild(subtotal);

      
      cartDiv.appendChild(content);

      



      // const tr = document.createElement('tr')
      // const imgTd = document.createElement('td')
      // const productTd = document.createElement('td')
      // const productPriceTd = document.createElement('td')
      // const quantityTd = document.createElement('td')
      // const subtotalTd = document.createElement('td')

      // const imgTag = document.createElement('img')
      // imgTag.src = data.image
      // imgTag.width = 100

      // imgTd.appendChild(imgTag)
      // productTd.textContent = data.name
      // productPriceTd.textContent = data.price
      // quantityTd.textContent = quantity
      // subtotalTd.textContent = data.price * quantity

      // tr.appendChild(imgTd)
      // tr.appendChild(productTd)
      // tr.appendChild(productPriceTd)
      // tr.appendChild(quantityTd)
      // tr.appendChild(subtotalTd)

      // const cartTableBody = document.querySelector('#cart_table tbody')
      // cartTableBody.appendChild(tr)
      cartTotalAmount += data.price * quantity
      
      resolve();
    });
  });
}

  // 저장된 'cart'에서 각 상품 ID와 수량을 가져옵니다.
  async function displayCart() {
    for (let i = 0; i < cart.length; i++) {
      await getProductInfoAndRender(cart[i].id, cart[i].quantity);

      if (i === cart.length - 1) {
        const cartTotal = document.createElement('div');
        cartTotal.className = 'cart_total';
        cartTotal.innerHTML = `합계 : <span id="total" class="pointColor">${cartTotalAmount.toLocaleString()}</span> 원`;

        cartDiv.appendChild(cartTotal);
      }
    }
  }
  (async () => {
    await displayCart();
    console.log(cartTotalAmount); // test
  })();
  }
  // displayCart();
// }
console.log(cartTotalAmount);

// login required
function loginRequired() {
  let result = confirm("로그인이 필요합니다. 로그인 하시겠습니까?")

  if (result) {
    const form = document.getElementById('order_form');
    form.submit();
  }
}