const stylesheet = document.getElementById('stylesheet');
function getStoredTheme() {
  return localStorage.getItem("theme");
}
if (getStoredTheme() === null) {
  stylesheet.href = '/static/css/main/theme-os.css'
} else {
  if (getStoredTheme() === 'light') {
    stylesheet.href = '/static/css/main/theme-light.css'
  } else {
    stylesheet.href = '/static/css/main/theme-dark.css'
  }
  // setTheme(getPreferredTheme());
}