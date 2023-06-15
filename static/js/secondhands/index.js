
document.addEventListener('DOMContentLoaded', function() {

  // 전체 버튼 클릭 이벤트 처리
  const allButton = document.querySelector('[data-filter="all"]');
  const allButtonClick = function() {
    // 모든 게시글 보이게 설정
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(function(card) {
      card.style.display = 'block';
    });
  };

  allButton.addEventListener('click', allButtonClick);

  // 최신순 버튼 클릭 이벤트 처리
  const latestButton = document.querySelector('[data-filter="latest"]');

  const latestButtonClick = function() {
    
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
  };

  latestButton.addEventListener('click', latestButtonClick);

  // 가격 낮은순 버튼 클릭 이벤트 처리
  const lowPriceButton = document.querySelector('[data-filter="lowcost"]');

  lowPriceButton.addEventListener('click', function() {
  
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
  });

  // 가격 높은 순 버튼 클릭 이벤트 처리
  const highPriceButton = document.querySelector('[data-filter="highcost"]');
  highPriceButton.addEventListener('click', function() {

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
  });

  //가까운 거리 순 버튼 클릭 이벤트
  const shortDistanceButton = document.querySelector('[data-filter="shortdistance"]');

  shortDistanceButton.addEventListener('click', function() {

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
  });

  // 전체 버튼 초기 활성화
  allButton.click();
});

