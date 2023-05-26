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