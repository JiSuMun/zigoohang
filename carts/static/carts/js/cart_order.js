const orderAllBtn = document.getElementById('order_all')

orderAllBtn.addEventListener('click', function(event){
  event.preventDefault()
  const checkItems = document.querySelectorAll("input[name='item_check']")
  checkItems.forEach(function(e){
    e.checked = true
  })
  const form = document.getElementById('order_form')
  // console.log(form)
  form.submit()
})