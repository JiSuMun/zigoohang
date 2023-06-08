const checkAll = document.getElementById('check_all')

checkAll.addEventListener('change', function() {
  const checkItems = document.querySelectorAll("input[name='item_check']")
  checkItems.forEach(function(checkbox) {
    checkbox.checked = checkAll.checked
  })
})