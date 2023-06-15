// 팔로워
const modal1 = document.querySelector(".modal-body1");
const openModalBtn1 = document.getElementById("open-modal-btn1");

// 팔로잉
const modal2 = document.querySelector(".modal-body2");
const openModalBtn2 = document.getElementById("open-modal-btn2");

// 모달 열고 닫기
function toggleModal1() {
  if (modal1.style.display === "none") {
    modal1.style.display = "block";
    openModalBtn1.innerHTML = "더보기 취소";
  } else {
    modal1.style.display = "none";
    openModalBtn1.innerHTML = "더보기";
  }
}
function toggleModal2() {
  if (modal2.style.display === "none") {
    modal2.style.display = "block";
    openModalBtn2.innerHTML = "더보기 취소";
  } else {
    modal2.style.display = "none";
    openModalBtn2.innerHTML = "더보기";
  }
}

const form = document.querySelector('#follow-form');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const personData = document.getElementById('person_data')
const personId = personData.dataset.userId;
const personUsername = personData.dataset.username;
const followingsCountTag = document.querySelector('#followings-count');
const followersCountTag = document.querySelector('#followers-count');
const followingList = document.querySelector('#following-ul');
const followerList = document.querySelector('#follower-ul');




openModalBtn1.addEventListener("click", toggleModal1);
openModalBtn2.addEventListener("click", toggleModal2);

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const userId = event.target.dataset.userId;

  axios({
    method: 'post',
    url: `/accounts/${userId}/follow/`,
    headers: { 'X-CSRFToken': csrftoken },
  })
    .then((response) => {
      const isFollowed = response.data.is_followed;
      const followBtn = document.querySelector('#follow-form > input[type=submit]');
      if (isFollowed === true) {
        followBtn.value = 'Unfollow';
      } else {
        followBtn.value = 'Follow';
      }
      const followingsCountData = response.data.followings_count;
      const followersCountData = response.data.followers_count;
      followingsCountTag.textContent = followingsCountData;
      followersCountTag.textContent = followersCountData;

      // 업데이트된 팔로잉 목록을 가져와서 템플릿에 반영
      updateFollowingList(personUsername);

      // 업데이트된 팔로워 목록을 가져와서 템플릿에 반영
      updateFollowerList(personUsername);
    })
    .catch((error) => {
      console.error(error);
    });
});

// 팔로잉 리스트 업데이트 함수
function updateFollowingList(username) {
  axios.get(`/accounts/profile/${username}/following-list/`)
    .then((response) => {
      followingList.innerHTML = response.data;
    })
    .catch((error) => {
      console.error(error);
    });
}

// 팔로워 리스트 업데이트 함수
function updateFollowerList(username) {
  axios.get(`/accounts/profile/${username}/followers-list/`)
    .then((response) => {
      followerList.innerHTML = response.data;
    })
    .catch((error) => {
      console.error(error);
    });
}

// 페이지 로드 시 팔로잉/팔로워 목록 초기화
window.addEventListener('DOMContentLoaded', () => {
  const username = personUsername;
  updateFollowingList(username);
  updateFollowerList(username);
});




