
// 올라가기 버튼
window.onscroll = function() {
  scrollFunction();
};

function scrollFunction() {
  var scrollBtn = document.getElementById("scrollBtn");
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    scrollBtn.style.display = "flex";
  } else {
    scrollBtn.style.display = "none";
  }
}

function scrollToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

// login required
function loginRequired() {
  let result = confirm("로그인이 필요합니다. 로그인 하시겠습니까?")

  if (result) {
    window.location.href = '/accounts/login/';
  }
}