const paymentsData = document.getElementById('payments_data')
const totalAmount = paymentsData.dataset.totalAmount
const orderId = paymentsData.dataset.orderId
const orderItem = paymentsData.dataset.orderItem
const userName = paymentsData.dataset.userName
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

console.log(totalAmount);
console.log(orderId);
console.log(orderItem);
console.log(new Date().getTime());

const IMP = window.IMP; 
IMP.init("imp21474003");  // 가맹점 식별코드

function requestPay() {
  IMP.request_pay({
    pg: "html5_inicis.INIBillTst",
    pay_method: "card",
    merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount,                         // 숫자 타입
    customer_uid : '1',
    buyer_email: "gildong@gmail.com",
    buyer_name: "홍길동",
    buyer_tel: "010-4242-4242",
    // buyer_addr: "서울특별시 강남구 신사동",
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
    if ( rsp.success ) {
      var msg = '결제가 완료되었습니다.';
      // msg += '고유ID : ' + rsp.imp_uid;
      // msg += '상점 거래ID : ' + rsp.merchant_uid;
      // msg += '\n결제 금액 : ' + rsp.paid_amount;
      msg += '\n결제 금액 : ' + rsp.paid_amount;
      console.log(rsp);
      // msg += '카드 승인번호 : ' + rsp.apply_num;
  }
  else {
      var msg = '결제에 실패하였습니다.\n에러내용 : ' + rsp.error_msg
  }
  alert(msg);
  });
}
function requestPay2() {
  IMP.request_pay({
    pg: "kcp.A52CY",
    // pay_method: "card",
    // merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount,                         // 숫자 타입
    // buyer_email: "gildong@gmail.com",
    // buyer_name: "홍길동",
    // buyer_tel: "010-4242-4242",
    // buyer_addr: "서울특별시 강남구 신사동",
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
    if ( rsp.success ) {
      var msg = '결제가 완료되었습니다.';
      // msg += '고유ID : ' + rsp.imp_uid;
      // msg += '상점 거래ID : ' + rsp.merchant_uid;
      // msg += '\n결제 금액 : ' + rsp.paid_amount;
      msg += '\n결제 금액 : ' + rsp.paid_amount;
      console.log(rsp);
      // msg += '카드 승인번호 : ' + rsp.apply_num;
  }
  else {
      var msg = '결제에 실패하였습니다.\n에러내용 : ' + rsp.error_msg
  }
  alert(msg);
  });
}
function kakaoPay() {
  const receiver = document.getElementById('receiver').value;
  const orderAddress = document.getElementById('order_address').value;
  const orderPhone = document.getElementById('order_phone').value;
  const orderEmail = document.getElementById('order_email').value;
  const usePoints = parseInt(document.getElementById('use_points').value);
  console.log(orderPhone);
  IMP.request_pay({
    pg: "kakaopay",
    // pay_method: "card",
    // merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount - usePoints,                         // 숫자 타입
    buyer_email: orderEmail,
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
          orderEmail,
          usePoints,
          orderPhone,
        }),
      })
        .then(function(response) {
          if (response.data.result === 'success') {
            window.location.href = "/carts/payments/show_approval/";
          }
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
    else {
        var msg = '결제에 실패하였습니다.\n에러내용 : ' + rsp.error_msg
    }
  alert(msg);
  // location.href = '/'
  });
}
function eximbayPay() {
  IMP.request_pay({
    pg: "eximbay",
    // pay_method: "card",
    // merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount,                         // 숫자 타입
    // buyer_email: "gildong@gmail.com",
    // buyer_name: "홍길동",
    // buyer_tel: "010-4242-4242",
    // buyer_addr: "서울특별시 강남구 신사동",
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
  });
}
function danalPay() {
  IMP.request_pay({
    pg: "danal",
    // pay_method: "card",
    // merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount,                         // 숫자 타입
    // buyer_email: "gildong@gmail.com",
    // buyer_name: "홍길동",
    // buyer_tel: "010-4242-4242",
    // buyer_addr: "서울특별시 강남구 신사동",
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
  });
}
function danalPay2() {
  IMP.request_pay({
    pg: "danal_tpay",
    // pay_method: "card",
    // merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount,                         // 숫자 타입
    // buyer_email: "gildong@gmail.com",
    // buyer_name: "홍길동",
    // buyer_tel: "010-4242-4242",
    // buyer_addr: "서울특별시 강남구 신사동",
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
  });
}
function tossPay() {
  IMP.request_pay({
    pg: "tosspay",
    // pay_method: "card",
    // merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount,                         // 숫자 타입
    // buyer_email: "gildong@gmail.com",
    // buyer_name: "홍길동",
    // buyer_tel: "010-4242-4242",
    // buyer_addr: "서울특별시 강남구 신사동",
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
  });
}
function paycoPay() {
  IMP.request_pay({
    pg: "payco",
    // pay_method: "card",
    // merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount,                         // 숫자 타입
    // buyer_email: "gildong@gmail.com",
    // buyer_name: "홍길동",
    // buyer_tel: "010-4242-4242",
    // buyer_addr: "서울특별시 강남구 신사동",
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
  });
}
function paypalPay() {
  IMP.request_pay({
    pg: "paypal",
    // pay_method: "card",
    // merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount,                         // 숫자 타입
    // buyer_email: "gildong@gmail.com",
    // buyer_name: "홍길동",
    // buyer_tel: "010-4242-4242",
    // buyer_addr: "서울특별시 강남구 신사동",
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
  });
}
function smilePay() {
  IMP.request_pay({
    pg: "smilepay",
    // pay_method: "card",
    merchant_uid: "merchant_" + new Date().getTime(),   // 주문번호
    name: orderItem,
    amount: totalAmount,                         // 숫자 타입
    // buyer_email: "gildong@gmail.com",
    // buyer_name: "홍길동",
    // buyer_tel: "010-4242-4242",
    // buyer_addr: "서울특별시 강남구 신사동",
    // buyer_postcode: "01181"
  }, function (rsp) { // callback
    //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
  });
}