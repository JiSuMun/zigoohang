if (!isAuthenticated) {
  const cartTableBody = document.querySelector('#cart_table tbody')
  const cart = JSON.parse(localStorage.getItem('cart')) || []

  cart.forEach(item => {
    const tr = document.createElement('tr')

    const imgTd = document.createElement('td')
    const productTd = document.createElement('td')
    const quantityTd = document.createElement('td')
    const subtotalTd = document.createElement('td')

    imgTd.textContent = '이미지'
    productTd.textContent = item.id
    quantityTd.textContent = item.quantity
    subtotalTd.textContent = 'sub_total'

    tr.appendChild(imgTd)
    tr.appendChild(productTd)
    tr.appendChild(quantityTd)
    tr.appendChild(subtotalTd)


    cartTableBody.appendChild(tr)
  })
}