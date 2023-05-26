const userAuth = document.getElementById("user-auth")
const isAuthenticated = userAuth.dataset.authenticated === "true"

window.onload = function() {
  // localStorage에 cart key 값 확인
  let cart = localStorage.getItem("cart")

  if (cart === null || cart === "null") {
      // localStorage에 cart key 값이 없는 경우 (빈 배열 생성)
      cart = []
      localStorage.setItem("cart", JSON.stringify(cart))
  }
  else {
      // localStorage에 cart key 값이 있는 경우, JSON 문자열을 객체로 변환
      cart = JSON.parse(cart)
  }
  // 추가 작업 코드 작성
}