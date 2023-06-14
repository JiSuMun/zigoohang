const orderAllBtn = document.getElementById('order_all')

orderAllBtn.addEventListener('click', function(event){
  const checkItems = document.querySelectorAll("input[name='item_check']")
  if (checkItems.length > 0) {
    checkItems.forEach(function(e){
      e.checked = true
    })
    const form = document.getElementById('order_form')
    form.submit()
  } else {
    alert("주문할 상품을 선택해주세요.")
  }
})

const orderCheckBtn = document.getElementById('order_check')

orderCheckBtn.addEventListener('click', function(event){
  const checkItems = document.querySelectorAll("input[name='item_check']")
  if (checkItems.length > 0) {
    checkItems.forEach(function(e){
      e.checked = true
    })
    const form = document.getElementById('order_form')
    form.submit()
  } else {
    alert("주문할 상품을 선택해주세요.")
  }
})