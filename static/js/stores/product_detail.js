// swiper

var swiper = new Swiper(".mySwiper", {
  spaceBetween: 10,
  slidesPerView: 4,
  freeMode: true,
  watchSlidesProgress: true,
});
var swiper2 = new Swiper(".mySwiper2", {
  spaceBetween: 10,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  thumbs: {
    swiper: swiper,
  },
});


//  가격 수량 버튼
const incrementBtn = document.getElementById("increment_btn")
const decrementBtn = document.getElementById("decrement_btn")
const countDiv = document.getElementById("product_count")
const price = countDiv.dataset.productPrice
const subTotalPriceSpan = document.getElementById("sub_total_price")
const totalPriceSpan = document.getElementById("total_price")
const totalCount = document.getElementById("total_count")
const buyQuantity = document.querySelector("input[name='input_quantity']")

let count = 1
let subTotalPrice = price
let totalPrice = price

// + 버튼 클릭 시 count 숫자 증가
incrementBtn.addEventListener("click", () => {
  count++;
  countDiv.textContent = count
  totalCount.textContent = count
  buyQuantity.value = count

  subTotalPrice = count * price
  totalPrice = count * price

  console.log(subTotalPrice)
  console.log(totalPrice)

  subTotalPriceSpan.textContent = subTotalPrice.toLocaleString()
  totalPriceSpan.textContent = totalPrice.toLocaleString()
})

// - 버튼 클릭 시 count 숫자 감소
decrementBtn.addEventListener("click", () => {
  if (count > 1) { // 현재 숫자가 1보다 큰 경우에만 감소
    count--;
    countDiv.textContent = count
    totalCount.textContent = count
    buyQuantity.value = count

    subTotalPrice = count * price
    totalPrice = count * price

    subTotalPriceSpan.textContent = subTotalPrice.toLocaleString()
    totalPriceSpan.textContent = totalPrice.toLocaleString()
  }
})

// 리뷰 별
const ratingStars = document.querySelectorAll('.rating-star');

ratingStars.forEach((ratingStar) => {
  const rating = ratingStar.textContent;
  ratingStar.innerHTML = '';

  for (let i = 1; i <= 5; i++) {
    const star = document.createElement('i');
    star.classList.add('fas', 'fa-star');
    if (i > rating) {
      star.classList.remove('fas');
      star.classList.add('far');
    }
    ratingStar.appendChild(star);
  }
});

// 리뷰 좋아요 비동기
const reviewForms = document.querySelectorAll('[id^="review-likes-form-"]');
console.log(reviewForms)
const r_csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

reviewForms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const storeId = event.target.dataset.storeId;
    const productId = event.target.dataset.productId;
    const reviewId = event.target.dataset.reviewId;
    console.log(storeId, productId, reviewId)

    axios({
      method: "POST",
      url: `/stores/${storeId}/${productId}/${reviewId}/likes/`,
      headers: {'X-CSRFToken': r_csrftoken},
    })
      .then((response) => {
        const risLiked = response.data.r_is_liked;
        console.log(risLiked)
        const rlikeBtn = form.querySelector('#review-like');
        console.log(rlikeBtn)
        const rlikeCount = form.nextElementSibling;
        console.log(rlikeCount)
        const dreviewForms = document.querySelector(`#review-dislikes-form-${storeId}-${productId}-${reviewId}`);
        console.log(dreviewForms)
        
        if (risLiked) {
          rlikeBtn.classList.remove('r-like-color-gray')
          rlikeBtn.classList.add('r-like-color')
          dreviewForms.querySelector('button').disabled = true;
        } else {
          rlikeBtn.classList.remove('r-like-color')
          rlikeBtn.classList.add('r-like-color-gray')
          dreviewForms.querySelector('button').disabled = false;
        }
        rlikeCount.textContent = response.data.review_likes_count;
      })
      .catch((error) => {
        console.log(error.response);
      });
  });
});

// 리뷰 싫어요 비동기
const dreviewForms = document.querySelectorAll('[id^="review-dislikes-form-"]');
console.log(dreviewForms)

dreviewForms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const storeId = event.target.dataset.storeId;
    const productId = event.target.dataset.productId;
    const dreviewId = event.target.dataset.dreviewId;
    console.log(storeId, productId, dreviewId)
    
    axios({
      method: "POST",
      url: `/stores/${storeId}/${productId}/${dreviewId}/dislikes/`,
      headers: {'X-CSRFToken': r_csrftoken},
    })
      .then((response) => {
        const rdisLiked = response.data.r_is_disliked;
        console.log(rdisLiked)
        const rdlikeBtn = form.querySelector('#review-dislike');
        console.log(rdlikeBtn)
        const rdlikeCount = form.nextElementSibling;
        console.log(rdlikeCount)
        const reviewForms = document.querySelector(`#review-likes-form-${storeId}-${productId}-${dreviewId}`);
        console.log(reviewForms)
        
        if (rdisLiked) {
          rdlikeBtn.classList.remove('r-like-color-gray')
          rdlikeBtn.classList.add('r-like-color')
          reviewForms.querySelector('button').disabled = true;
        } else {
          rdlikeBtn.classList.remove('r-like-color')
          rdlikeBtn.classList.add('r-like-color-gray')
          reviewForms.querySelector('button').disabled = false;
        }
        rdlikeCount.textContent = response.data.review_dislikes_count;
      })
      .catch((error) => {
        console.log(error.response);
      });
  });
});