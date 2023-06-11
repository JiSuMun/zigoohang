
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

// console.log(totalAmount);
// console.log(orderId);
// console.log(orderItem);
// console.log(new Date().getTime());

function pay_type(pg) {
  $("#pg").val(pg);
  // console.log(pg);

  // $("#method").val(method);
}

function test() {
  // const pgTest = document.getElementById('pg')
  console.log(pg);
  console.log($("#pg").val());
  // console.log(pgTest);
  // console.log($("#pg").val());
  // console.log(method);
}

const IMP = window.IMP; 
IMP.init("imp21474003");  // 가맹점 식별코드

function requestPay() {

  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  
  const pg = $("#pg").val()
  console.log(pg);
  const paymentsData = document.getElementById('payments_data')
  const totalAmount = paymentsData.dataset.totalAmount
  const orderId = paymentsData.dataset.orderId
  const orderItem = paymentsData.dataset.orderItem
  const userName = paymentsData.dataset.userName

  const receiver = document.getElementById('receiver').value;
  const orderAddress = document.getElementById('order_address').value;
  const orderPhone = document.getElementById('order_phone').value;
  // const orderEmail = document.getElementById('order_email').value;
  const usePoints = parseInt(document.getElementById('use_points').value);
  const orderMsg = document.getElementById('order_msg').value;
  
  console.log(orderPhone);
  IMP.request_pay({
    pg: pg,
    // pay_method: "card",
    // merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount - usePoints,                         // 숫자 타입
    // buyer_email: orderEmail,
    buyer_name: receiver,
    buyer_tel: orderPhone,
    buyer_addr: orderAddress,
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    if ( rsp.success ) {
      var msg = '결제가 완료되었습니다.';
      // msg += '고유ID : ' + rsp.imp_uid;
      // msg += '상점 거래ID : ' + rsp.merchant_uid;
      // msg += '\n결제 금액 : ' + rsp.paid_amount;
      msg += '\n결제 금액 : ' + rsp.paid_amount;
      console.log(rsp);
      // msg += '카드 승인번호 : ' + rsp.apply_num;
      axios({
        method: 'POST',
        url: '/carts/payments/approval/',
        headers: {
          'X-CSRFToken': csrftoken, 
        },
        data: JSON.stringify({
          orderId,
          totalAmount,
          receiver,
          orderAddress,
          // orderEmail,
          usePoints,
          orderPhone,
          orderMsg,
        }),
      })
        .then(function(response) {
          if (response.data.result === 'success') {
            window.location.href = "/carts/payments/show_approval/";
          }
        })
      // .catch((error) => {
      //   console.error('Error:', error)
      // })
    }
    else {
        var msg = '결제에 실패하였습니다.\n에러내용 : ' + rsp.error_msg
    }
  alert(msg);
  // location.href = '/'
  });
}
