// drawer 메뉴 복사

const navInner = document.querySelector('.nav-inner');
const drawer = document.querySelector('.drawer');

function addMClass(element) {
  const childElements = element.querySelectorAll('*');

  childElements.forEach(childElement => {
    const classNames = childElement.classList;
    const newClassNames = [];

    classNames.forEach(className => {
      const newClassName = 'm-' + className;
      newClassNames.push(newClassName);
    });

    childElement.classList.remove(...classNames);
    childElement.classList.add(...newClassNames);
  });
}

function copyNavInner() {
  const navInnerCopy = navInner.cloneNode(true);
  navInnerCopy.querySelector('.logo').remove();
  navInnerCopy.querySelector('.drawer_icon').remove();
  

  addMClass(navInnerCopy);
  drawer.appendChild(navInnerCopy);
}

copyNavInner();

// 드롭다운시 클래스 추가
function mini() {
  const hover = document.querySelectorAll(".m-nav-hover .m-nav-link");
  hover.forEach(link => {
    link.removeAttribute("href");
  });

  const mNavDrops = document.querySelectorAll(".m-nav-drop");
  mNavDrops.forEach(drop => {
    const img = document.createElement("img");
    img.setAttribute("src", "../../static/img/base/drawer.svg");
    img.classList.add("m-nav-icon");
    drop.appendChild(img);
  });
}

mini();

// mini 메뉴 안 dropdown 추가
function drawerMenuClick() {
  const mNavHover = document.querySelectorAll(".m-nav-hover");

  mNavHover.forEach(link => {
    const dropdown = link.querySelector(".m-nav-drop");
    if (!dropdown) return;

    link.addEventListener("click", function() {
      dropdown.classList.toggle("open");

      const siblings = Array.from(link.parentNode.children).filter(element =>
        element !== link
      );
      siblings.forEach(sibling => {
        const siblingDropdown = sibling.querySelector(".m-nav-drop");
        if (siblingDropdown) siblingDropdown.classList.remove("open");
      });
    });
  });
}

drawerMenuClick();
