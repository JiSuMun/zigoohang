const stars = document.querySelectorAll('.starRating i');
const ratingInput = document.getElementById('rating_input');

stars.forEach(star => {
  star.addEventListener('click', function() {
    const rating = this.getAttribute('data-rating');

    stars.forEach(s => {
      s.classList.remove('fas');
      s.classList.add('far');
    });

    for (let i = 0; i < rating; i++) {
      stars[i].classList.remove('far');
      stars[i].classList.add('fas');
    }

    ratingInput.value = rating;
  });
});