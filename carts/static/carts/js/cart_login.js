// // const loginBtn = document.getElementById('login_btn')
// // console.log(loginBtn);
// const loginForm = document.getElementById('login-form');

// function fetchCartFromLocalStorage() {
//   const cart = localStorage.getItem("cart");
//   return JSON.parse(cart) || [];
// }

// loginForm.addEventListener('submit', function (event) {
//   // event.preventDefault();
//   onUserLoggedIn()
// })

// function onUserLoggedIn() {
//   const cart = fetchCartFromLocalStorage();
//   console.log(123);
//   console.log(123);
//   console.log(123);
//   console.log(123);
//   console.log(123);
//   console.log(123);
//   if (cart.length > 0) {
//     axios({
//       method: 'POST',
//       url: '/accounts/login/',
//       data: JSON.stringify(cart),
//       // contentType: 'application/json',
//       // dataType: 'json',
//     })
//   //     success: (data) => {
//   //       if (data.status === "success") {
//   //         // 장바구니 데이터가 성공적으로 전송되고 서버에서 처리 완료되면 Local Storage의 데이터를 지웁니다.
//   //         // localStorage.removeItem("cart");
//   //       }
//   //     },
//   //     error: (xhr, status, errorThrown) => {
//   //       console.error("Error: " + errorThrown);
//   //     }
//   //   });
//   // }
//   }
// }


// import axios from 'axios';

// async function login(username, password) {
//   // localStorage에서 cart 데이터 가져오기
//   const cartData = localStorage.getItem('cart');
//   const parsedCartData = cartData ? JSON.parse(cartData) : [];

//   // 로그인 요청하기 (localStorage의 cart 데이터를 포함시킴)
//   const response = await axios.post('/accounts/login/', {
//     username: username,
//     password: password,
//     cart_data: parsedCartData
//   });
// }

window.addEventListener('DOMContentLoaded', (event) => {
  const loginForm = document.getElementById('login-form');
  
  loginForm.addEventListener('submit', (e) => {
    // 기본 폼 제출 행위를 막음
    e.preventDefault();

    // localStorage에서 cart 데이터 가져오기
    const cartData = localStorage.getItem('cart');
    
    // cart_data 필드를 생성함
    const cartDataInput = document.createElement('input');
    cartDataInput.type = 'hidden';
    cartDataInput.name = 'cart_data';
    cartDataInput.value = cartData || '[]';
    
    // cart_data 필드를 폼에 추가함
    loginForm.appendChild(cartDataInput);
    
    // 폼을 제출함
    loginForm.submit();
  });
});
