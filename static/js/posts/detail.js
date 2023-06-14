function showAlert() {
  alert("이전 글이 없습니다.");
}



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
    button.innerHTML = "수정";
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
const reviewForms = document.querySelectorAll('[id^="review-likes-form-"]');

reviewForms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
    const reviewId = event.target.dataset.reviewId;
    console.log(postId, reviewId)

    axios({
      method: "POST",
      url: `/posts/${postId}/${reviewId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
      .then((response) => {
        const risLiked = response.data.r_is_liked;
        console.log(risLiked)
        const rlikeBtn = form.querySelector('#review-like');
        console.log(rlikeBtn)
        const rlikeCount = form.nextElementSibling;
        console.log(rlikeCount)
        const dreviewForms = document.querySelector(`#review-dislikes-form-${postId}-${reviewId}`);
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

// 댓글 싫어요 비동기
const dreviewForms = document.querySelectorAll('[id^="review-dislikes-form-"]');

dreviewForms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const dpostId = event.target.dataset.postId;
    const dreviewId = event.target.dataset.dreviewId;
    console.log(dpostId, dreviewId)

    axios({
      method: "POST",
      url: `/posts/${dpostId}/${dreviewId}/dislikes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
      .then((response) => {
        const rdisLiked = response.data.r_is_disliked;
        console.log(rdisLiked)
        const rdlikeBtn = form.querySelector('#review-dislike');
        console.log(rdlikeBtn)
        const rdlikeCount = form.nextElementSibling;
        console.log(rdlikeCount)
        const reviewForms = document.querySelector(`#review-likes-form-${dpostId}-${dreviewId}`);
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