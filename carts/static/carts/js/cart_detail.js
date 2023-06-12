if (!isAuthenticated) {
  let storedCart = localStorage.getItem('cart');

  // JSON 문자열을 객체로 변환합니다.
  let cart = JSON.parse(storedCart);

  

  // 상품 정보를 가져온 후 '#cart-table > tbody'에 정보 저장
  function getProductInfoAndRender(product_id, quantity) {
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
      const tr = document.createElement('tr')
      const imgTd = document.createElement('td')
      const productTd = document.createElement('td')
      const productPriceTd = document.createElement('td')
      const quantityTd = document.createElement('td')
      const subtotalTd = document.createElement('td')

      const imgTag = document.createElement('img')
      imgTag.src = data.image
      imgTag.width = 100

      imgTd.appendChild(imgTag)
      productTd.textContent = data.name
      productPriceTd.textContent = data.price
      quantityTd.textContent = quantity
      subtotalTd.textContent = data.price * quantity

      tr.appendChild(imgTd)
      tr.appendChild(productTd)
      tr.appendChild(productPriceTd)
      tr.appendChild(quantityTd)
      tr.appendChild(subtotalTd)

      const cartTableBody = document.querySelector('#cart_table tbody')
      cartTableBody.appendChild(tr)
    });
  }

  // 저장된 'cart'에서 각 상품 ID와 수량을 가져옵니다.
  for (let i = 0; i < cart.length; i++) {
    getProductInfoAndRender(cart[i].id, cart[i].quantity);
  }
}
