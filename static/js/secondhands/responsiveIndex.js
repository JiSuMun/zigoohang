
function selectChange(value) {
  if (value === 'latest') {
    sortByLatest();
  } else if (value === 'lowcost') {
    sortByLowestCost();
  } else if (value === 'highcost') {
    sortByHighestCost();
  } else if (value === 'shortdistance') {
    sortByShortestDistance();
  } else {
    pass;
  }
}

function sortByLatest() {
  const productContainer = document.querySelector('.secondhands-page-content-product');
    const productCards = Array.from(productContainer.querySelectorAll('.product-card'));
    const sortedCards = productCards.sort(function(a, b) {
      const idA = parseInt(a.querySelector('.detail-product_id').textContent.replace(/[^0-9]/g, ''));
      const idB = parseInt(b.querySelector('.detail-product_id').textContent.replace(/[^0-9]/g, ''));
  
      return idB - idA;
    });
    
    productContainer.innerHTML = '';
    
    sortedCards.forEach(function(card) {
      productContainer.appendChild(card.parentNode);
    });
}

function sortByLowestCost() {
  const productContainer = document.querySelector('.secondhands-page-content-product');
    const productCards = Array.from(productContainer.querySelectorAll('.product-card'));
    const sortedCards = productCards.sort(function(a, b) {
      const priceA = parseInt(a.querySelector('.detail-product_price').textContent.replace(/[^0-9]/g, ''));
      const priceB = parseInt(b.querySelector('.detail-product_price').textContent.replace(/[^0-9]/g, ''));
      return priceA - priceB;
    });
  
    productContainer.innerHTML = ''; //기존 게시글 제거
  
    sortedCards.forEach(function(card) {
      productContainer.appendChild(card.parentNode);
    });
}

function sortByHighestCost() {
  const productContainer = document.querySelector('.secondhands-page-content-product');
  const productCards = Array.from(productContainer.querySelectorAll('.product-card'));
  const sortedCards = productCards.sort(function(a, b) {
    const priceA = parseInt(a.querySelector('.detail-product_price').textContent.replace(/[^0-9]/g, ''));
    const priceB = parseInt(b.querySelector('.detail-product_price').textContent.replace(/[^0-9]/g, ''));
    return priceB - priceA;
  });

  productContainer.innerHTML = '';

  sortedCards.forEach(function(card) {
    productContainer.appendChild(card.parentNode);
  });
}

function sortByShortestDistance() {
  const productContainer = document.querySelector('.secondhands-page-content-product');
    const productCards = Array.from(productContainer.querySelectorAll('.product-card'));
    const sortedCards = productCards.sort(function(a, b) {
      const distanceA = parseInt(a.querySelector('.detail-product_distance').textContent);
      const distanceB = parseInt(b.querySelector('.detail-product_distance').textContent);  
     
      return distanceA - distanceB;
    });
  
    productContainer.innerHTML = '';
  
    sortedCards.forEach(function(card) {
      productContainer.appendChild(card.parentNode);
    });
}

