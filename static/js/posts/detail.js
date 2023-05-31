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