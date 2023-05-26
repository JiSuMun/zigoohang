const addItemBtn = document.getElementById('addItem')

addItemBtn.addEventListener('click', () => {
  const productId = Number(addItemBtn.dataset.productId)
  const newQuantity = Number(addItemBtn.dataset.itemQuantity)
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
    // .then((response) => response.json())
    // .then((data) => {
    //   if (data.success) {
    //     console.log('Item added to cart')
    //   } else if (data.error) {
    //     console.error(data.error)
    //   }
    // })
    // .catch((error) => {
    //   console.error('Error:', error)
    // })
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
}
