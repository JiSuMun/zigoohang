function execDaumPostcode() {
  new daum.Postcode({
    oncomplete: function(data) {
      var roadAddr = data.roadAddress; // 도로명 주소 변수

      document.getElementById('order_address_postcode').value = data.zonecode;
      document.getElementById("order_address").value = roadAddr;

    }
  }).open();
}


// 사용할 포인트
const pointInput = document.getElementById('use_points');
let pointTemp = 0
const paymentsData = document.getElementById('payments_data')
const totalAmount = paymentsData.dataset.totalAmount

pointInput.addEventListener('input', function(e) {
  userPoints = parseInt(pointInput.dataset.userPoints)
  if (e.target.value > userPoints) {
    alert('보유 포인트를 초과할 수 없습니다.')
    e.target.value = pointTemp;
  } else if (e.target.value < 0){
    alert('0 이상의 값을 입력해주세요.')
    e.target.value = pointTemp;
  } else if (e.target.value > totalAmount*0.5) { 
    alert('총 결제금액의 50%를 넘을 수 없습니다.')
    e.target.value = pointTemp;
  } else {
    pointTemp = e.target.value
  }
})