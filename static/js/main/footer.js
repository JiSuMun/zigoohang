function toggleInfo() {
  var infoWrap = document.getElementById("infoWrap");
  var footerIcon = document.getElementById("icon");

  infoWrap.classList.toggle("show");
  footerIcon.classList.toggle("rotate");
}