const addItemBtn = document.getElementById('addItem')

addItemBtn.addEventListener('click', () => {
  const productId = Number(addItemBtn.dataset.productId)
  const newQuantity = count
  if (isAuthenticated) {
    user_add_item_cart(productId, newQuantity)
  } else {
    guest_add_item_cart(productId, newQuantity)
  }
})

function user_add_item_cart(product, quantity) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  axios({
    method: 'POST',
    url: '/carts/add_item/',
    headers: {
      'X-CSRFToken': csrftoken, 
    },
    data: JSON.stringify({
      product, 
      quantity,
    }),
  })
    .then((response) => {
      const countBadge = document.getElementById('count_badge')

      countBadge.textContent = response.data.cart_count
      countBadge.style.setProperty('display', 'block')

      alert('장바구니에 추가되었습니다.')
    })
}

function guest_add_item_cart(product, quantity) {
  let cart = JSON.parse(localStorage.getItem('cart')) || []

  const existingItem = cart.find((item) => item.id === product);

  if (existingItem) {
    existingItem.quantity += quantity
  } else {
    const newItem = { id: product, quantity: quantity }
    cart.push(newItem)
  }

  localStorage.setItem('cart', JSON.stringify(cart))

  const countBadge = document.getElementById('count_badge')

  countBadge.textContent = cart.length
  countBadge.style.setProperty('display', 'block')

  alert('장바구니에 추가되었습니다.')
}
