
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

// 테마 버튼
document.getElementById('set_btn').addEventListener('click', function () {
  var menuContainer = document.getElementById('theme_btn_box');
  menuContainer.classList.toggle('theme_hidden');

  // this.textContent = menuContainer.classList.contains('theme_hidden') ? '메뉴 열기' : '메뉴 닫기';
});



// 테마
function getStoredTheme() {
  return localStorage.getItem("theme");
}

function setStoredTheme(theme) {
  localStorage.setItem("theme", theme);
}

function getPreferredTheme() {
  const storedTheme = getStoredTheme();
  if (storedTheme) {
    return storedTheme;
  }
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function setTheme(theme) {
  document.documentElement.setAttribute("data-bs-theme", theme);
}

function toggleTheme() {
  const currentTheme = getPreferredTheme();
  const newTheme = currentTheme === "light" ? "dark" : "light";
  setStoredTheme(newTheme);
  setTheme(newTheme);
}

const lightThemeBtn = document.getElementById("lightThemeBtn");
const darkThemeBtn = document.getElementById("darkThemeBtn");

lightThemeBtn.addEventListener("click", () => {
  stylesheet.href = '/static/css/main/theme-light.css'
  setStoredTheme("light");
  lightThemeBtn.querySelector('img').classList.add('theme_icon_active')
  darkThemeBtn.querySelector('img').classList.remove('theme_icon_active')
  userPrefThemeBtn.querySelector('img').classList.remove('theme_icon_active')
});

darkThemeBtn.addEventListener("click", () => {
  stylesheet.href = '/static/css/main/theme-dark.css'
  setStoredTheme("dark");
  lightThemeBtn.querySelector('img').classList.remove('theme_icon_active')
  darkThemeBtn.querySelector('img').classList.add('theme_icon_active')
  userPrefThemeBtn.querySelector('img').classList.remove('theme_icon_active')

});
function applyOSTheme() {
  stylesheet.href = '/static/css/main/theme-os.css'
  localStorage.removeItem("theme"); // 기존 사용자 지정 테마 정보 삭제
}

const userPrefThemeBtn = document.getElementById("userPrefThemeBtn");

userPrefThemeBtn.addEventListener("click", () => {
  applyOSTheme();
  lightThemeBtn.querySelector('img').classList.remove('theme_icon_active')
  darkThemeBtn.querySelector('img').classList.remove('theme_icon_active')
  userPrefThemeBtn.querySelector('img').classList.add('theme_icon_active')
});

// 초기 테마 설정 및 적용 (수정)
if (getStoredTheme() === null) {
  applyOSTheme();
  userPrefThemeBtn.querySelector('img').classList.add('theme_icon_active')
} else {
  setTheme(getPreferredTheme());
  if (getPreferredTheme() === 'light') {
    lightThemeBtn.querySelector('img').classList.add('theme_icon_active')
  } else if (getPreferredTheme() === 'dark') {
    darkThemeBtn.querySelector('img').classList.add('theme_icon_active')
  }
}
// 초기 테마 설정 및 적용
// setTheme(getPreferredTheme());


// login required
function loginRequired() {
  let result = confirm("로그인이 필요합니다. 로그인 하시겠습니까?")

  if (result) {
    window.location.href = '/accounts/login/';
  }
}

// document.addEventListener("DOMContentLoaded", function () {
//   const svgElement = document.getElementById("sun_svg");
//   const svgFillColor = "orange"; // 원하는 색상을 여기에 입력하세요.

//   svgElement.addEventListener("load", function () {
//     const svg = svgElement.contentDocument;
//     const elements = svg.getElementsByTagName("path");
//     console.log(elements, elements.length)
//     for (let i = 0; i < elements.length; i++) {
//       elements[i].setAttribute("fill", svgFillColor);
//     }
//   });
// });