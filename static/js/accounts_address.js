function search_address() {
  new daum.Postcode({
    oncomplete: function(data) {
      const addr = data.address;
      document.getElementById("address").value = addr;

    }
  }).open();
}