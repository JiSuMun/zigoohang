const addItemBtn = document.getElementById('addItem')
const quantityElem = document.getElementById('quantity')

addItemBtn.addEventListener('click', () => {
  const productId = Number(addItemBtn.dataset.productId)
  const newQuantity = Number(quantityElem.value)

  let cart = JSON.parse(localStorage.getItem('cart')) || []

  const existingItem = cart.find((item) => item.id === productId);

  if (existingItem) {
    existingItem.quantity += newQuantity
  } else {
    const newItem = { id: productId, quantity: newQuantity }
    cart.push(newItem)
  }

  localStorage.setItem('cart', JSON.stringify(cart))
})
