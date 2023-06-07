function toggleReviewUpdateForm(review_id) {
  const form = document.getElementById("reviewUpdateForm" + review_id);
  const box = document.querySelector(".review--box");
  const button = document.getElementById("reviewUpdateButton" + review_id);
  
  if (form.style.display === "none") {
    form.style.display = "block";
    box.style.display = "none";
    button.innerHTML = "취소";
  } else {
    form.style.display = "none";
    box.style.display = "block";
    button.innerHTML = "리뷰 수정";
  }
}


const reviewButton = document.getElementById('create-review');
const rCreate = document.querySelector('.r-create');

reviewButton.addEventListener('click', () => {
  if (rCreate.style.display === 'block') {
    rCreate.style.display = 'none';
  } else {
    rCreate.style.display = 'block';
  }
});


// 좋아요 비동기
const forms = document.querySelectorAll('.like-forms');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

forms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
       
    axios({
      method: "POST",
      url: `/posts/${postId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
      .then((response) => {
        const isLiked = response.data.is_liked;
        const likeBtn = document.querySelector(`#like-${postId}`)
        const likeCount = document.querySelector(`#likes_count`)
        
        if (isLiked === true) {
          likeBtn.classList.remove('fa-regular')
          likeBtn.classList.add('fa-solid')
        } else {
          likeBtn.classList.remove('fa-solid')
          likeBtn.classList.add('fa-regular')
        }
        likeCount.innerText = response.data.likes_count;
      })
      .catch((error) => {
        console.log(error.response);
      });
  });
});

// 댓글 좋아요 비동기
const reviewForms = document.querySelectorAll('.review-like-form');

reviewForms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
    const reviewId = event.target.dataset.reviewId
       
    axios({
      method: "POST",
      url: `/posts/${postId}/${reviewId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
      .then((response) => {
        const risLiked = response.data.r_is_liked;
        const rlikeBtn = document.querySelector(`#review-like-${reviewId}`)
        const rlikeCount = document.querySelector(`#review_likes_count-${reviewId}`)
        
        if (risLiked === true) {
          rlikeBtn.classList.add('r-like-color')
          rlikeBtn.classList.remove('r-like-color-gray')
        } else {
          rlikeBtn.classList.add('r-like-color-gray')
          rlikeBtn.classList.remove('r-like-color')

        }
        rlikeCount.innerText = response.data.review_likes_count;
      })
      .catch((error) => {
        console.log(error.response);
      });
  });
});

// 댓글 싫어요 비동기
const dreviewForms = document.querySelectorAll('.review-dislike-form');

dreviewForms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
    const dreviewId = event.target.dataset.dreviewId
       
    axios({
      method: "POST",
      url: `/posts/${postId}/${dreviewId}/dislikes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
      .then((response) => {
        const rdisLiked = response.data.r_is_disliked;
        const rdlikeBtn = document.querySelector(`#review-dislike-${dreviewId}`)
        const rdlikeCount = document.querySelector(`#review_dislikes_count-${dreviewId}`)
        
        if (rdisLiked === true) {
          rdlikeBtn.classList.add('r-like-color')
          rdlikeBtn.classList.remove('r-like-color-gray')
        } else {
          rdlikeBtn.classList.add('r-like-color-gray')
          rdlikeBtn.classList.remove('r-like-color')

        }
        rdlikeCount.innerText = response.data.review_dislikes_count;
      })
      .catch((error) => {
        console.log(error.response);
      });
  });
});