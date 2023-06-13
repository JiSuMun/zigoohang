const quantityBtn = document.querySelectorAll('button[name="quantity_btn"]')
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value

quantityBtn.forEach(function(e) {
  e.addEventListener('click', function(event) {
    event.preventDefault()
    const productId = e.dataset.productId
    const quantityValue = e.dataset.quantityValue
    if (isAuthenticated) {
      user_modify_quantity(productId, quantityValue)
    } else {
      guest_modify_quantity()
    }
  })
})


function user_modify_quantity(productId, quantityValue) {
  console.log(Number(quantityValue))
  axios({
    method: 'POST',
    url: '/carts/modify_quantity/',
    headers: {'X-CSRFToken': csrfToken},
    data: JSON.stringify({
      productId,
      quantityValue,
    })
  })
    .then((response) => {
      const productQuantityDiv = document.getElementById(`product_count-${productId}`)
      const productQuantityInput = document.getElementById(`product_quantity-${productId}`)
      const subTotalSpan = document.getElementById(`sub_total-${productId}`)
      const totalSpan = document.getElementById('total')
      // console.log(response)
      // console.log(response.data.subTotal)
      // console.log(response.data.total)
      // subTotalSpan.innerHTML = response.data.subTotal
      productQuantityDiv.textContent = response.data.quantity
      productQuantityInput.value = response.data.quantity
      subTotalSpan.innerHTML = response.data.subTotal.toLocaleString()
      totalSpan.innerHTML = response.data.total.toLocaleString()
    })
}


function guest_modify_quantity() {

}

function dicreaseItem(id) {
  let cart = JSON.parse(localStorage.getItem('cart'))
  const existingItem = cart.find((item) => item.id === id);

  if (existingItem) {
    if (existingItem.quantity > 1) {
      existingItem.quantity -= 1
      const productCountDiv = document.getElementById(`product_count-${id}`)
      const cartSubTotalSpan = document.getElementById(`sub_total-${id}`)
      const cartTotalSpan = document.getElementById(`total`)
      
      const productDataDiv = document.getElementById(`product_data-${id}`)
      const productPrice = productDataDiv.dataset.productPrice
      cartTotalAmount -= productPrice

      productCountDiv.textContent = existingItem.quantity
      cartSubTotalSpan.textContent = (existingItem.quantity * productPrice).toLocaleString()
      cartTotalSpan.textContent = cartTotalAmount.toLocaleString()
    }
  }

  localStorage.setItem('cart', JSON.stringify(cart))
}

function increaseItem(id) {
  let cart = JSON.parse(localStorage.getItem('cart'))
  const existingItem = cart.find((item) => item.id === id);

  if (existingItem) {
    existingItem.quantity += 1
    const productCountDiv = document.getElementById(`product_count-${id}`)
    const cartSubTotalSpan = document.getElementById(`sub_total-${id}`)
    const cartTotalSpan = document.getElementById(`total`)
    
    const productDataDiv = document.getElementById(`product_data-${id}`)
    const productPrice = productDataDiv.dataset.productPrice
    cartTotalAmount += parseInt(productPrice)

    productCountDiv.textContent = existingItem.quantity
    cartSubTotalSpan.textContent = (existingItem.quantity * productPrice).toLocaleString()
    cartTotalSpan.textContent = cartTotalAmount.toLocaleString()
  }

  localStorage.setItem('cart', JSON.stringify(cart))
}