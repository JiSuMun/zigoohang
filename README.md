# KDT_Final_PJT

## 프로젝트 개요

| 프로젝트 목적 | 웹 프레임워크 Django와 HTML / CSS / JavaScript를 활용한 콘텐츠 기반 커뮤니티 웹 플랫폼 개발 |
| --- | --- |
| 프로젝트 기간 | 2023.05.22 ~ 2023.06.15 |
| 발표 날짜 | 2023.06.16 |
| 팀명 | 핫6 |
| 주제 | 환경 보호에 관심 있는 사용자들을 대상으로 환경뉴스 등 소식을 알리는 서비스를 제공하고, 중고거래, 친환경제품 등을 판매하는 서비스를 제공 |


## 기술 스택

<div style="text-align: center;">
<img src="https://img.shields.io/badge/git-F05032?style=for-plastic&logo=git&logoColor=white"><img src="https://img.shields.io/badge/github-181717?style=for-plastic&logo=github&logoColor=white"><img src="https://img.shields.io/badge/python-3776AB?style=for-plastic&logo=python&logoColor=white"><img src="https://img.shields.io/badge/django-092E20?style=for-plastic&logo=django&logoColor=white"><br>
<img src="https://img.shields.io/badge/html5-E34F26?style=for-plastic&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/css3-1572B6?style=for-plastic&logo=css3&logoColor=white"><img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-plastic&logo=javascript&logoColor=white"><img src="https://img.shields.io/badge/axios-5A29E4?style=for-plastic&logo=axios&logoColor=white"><img src="https://img.shields.io/badge/sqlite-003B57?style=for-plastic&logo=sqlite&logoColor=white">
</div>


## 개발 역할 분담

| 이름 | 역할 |
| --- | --- |
| [문지수](https://github.com/JiSuMun) | 조장, 백엔드 |
| [박은정](https://github.com/Dreamofheaven) | 프론트엔드 |
| [서유영](https://github.com/syuyoung) | 프론트엔드 |
| [방한영](https://github.com/hany0829) | 백엔드 |
| [정광배](https://github.com/iblug) | 백엔드 |


## 주제 사전 조사 & 분석

[그린피스](https://www.greenpeace.org/korea/)

[모레상점](https://morestore.co.kr/MoreBrands.html)

[리뉴어스](https://www.renuers.com/)

[지구랭](https://jigoorang.com/shop)


## 서비스 주요 기능
<details>
<summary>회원관리</summary>

- 회원가입
  - 회원가입 약관
  - 회원가입 인증
  - 판매자/일반회원 가입
  
- 로그인
  - 소셜 로그인
  - 아이디/비밀번호 찾기
  
- 로그아웃

- 회원 프로필

- 팔로잉
  - 팔로우/언팔로우
  - 팔로워/팔로잉 목록

- 포인트

</details>
<details>
<summary>장바구니</summary>

- 장바구니

- 결제

</details>
<details>
<summary>챌린지</summary>

- 챌린지 게시글
  - 생성, 조회, 수정, 삭제
  - 참가/미참가 등록

- 챌린지 인증
  - 생성, 조회, 수정, 삭제
- 챌린지 참가

</details>
<details>
<summary>게시판 - 환경 보호 정보 제공</summary>

- 게시글
  - 생성, 조회, 수정, 삭제
  - 좋아요
- 리뷰
  - 생성, 조회, 수정, 삭제
  - 좋아요/싫어요
- 친환경 지도
- 에코 뉴스

</details>
<details>
<summary>중고거래</summary>

- 중고거래 게시글
  - 생성, 조회, 수정, 삭제
  - 거래장소 지도
  - 예약중/거래완료
- 필터링(전체,최신,거리순)
  
</details>

<details>
<summary>상점</summary>

- 상점 게시글
  - 생성, 조회, 수정, 삭제
- 상품 리뷰
  - 좋아요/싫어요
- 관심상품 등록
  
</details>

<details>
<summary>채팅</summary>

- 나와의 채팅
- 사용자와 채팅
- 채팅 알림
  
</details>

<details>
<summary>검색</summary>
</details>


## 모델(Model) 설계

![Alt text](image/erd.png)

## 화면(Template) 설계

<details>
<summary>메인</summary>

![Alt text](image/main.png)

</details>

<details>
<summary>회원가입</summary>

- 약관동의
![Alt text](image/agreements.PNG)
- 회원가입 폼
![Alt text](image/signup.PNG)
- 이메일 인증

</details>

<details>
<summary>로그인</summary>

- 로그인
![Alt text](image/login.PNG)

</details>

<details>
<summary>프로필</summary>

![Alt text](image/MYPAGE.png)

</details>

<details>
<summary>행성상점</summary>

- 상점 목록
![Alt text](image/stores.jpeg)
- 각 상점 페이지
![Alt text](image/store_index.jpeg)
- 상품
![Alt text](image/product-detail.jpeg)

</details>

<details>
<summary>장바구니</summary>

![Alt text](image/carts.png)
</details>

<details>
<summary>결제하기</summary>

- 주문하기
![Alt text](image/order.png)
- 결제하기
![Alt text](image/kakaopay.jpeg)
- 결제완료
![Alt text](image/approval.png)

</details>

<details>
<summary>중고거래</summary>

![Alt text](image/secondhands_index.jpeg)
![Alt text](image/secondhands_detail.png)

</details>

<details>
<summary>채팅</summary>

![Alt text](image/inbox.png)
![Alt text](image/room.png)
</details>

<details>
<summary>챌린지</summary>

![Alt text](image/challenge_index.png)
![Alt text](image/challenge_detail.png)
</details>

<details>
<summary>환경</summary>

![Alt text](image/posts_index.png)
![Alt text](image/zero_map.png)
![Alt text](<image/ECO NEWS.png>)
![Alt text](image/FORUM.png)

</details>

<details>
<summary>검색</summary>

![Alt text](image/search.png)
</details>

## 프로젝트 후기
<details>
<summary>문지수</summary>
이번 프로젝트를 통해 많이 성장한 것 같습니다. 그리고 첫 번째 프로젝트에서 실패했던 채팅 배포도 이번 프로젝트를 통해 성공할 수 있었고, 많은 js코드를 작성하며 js에 대한 이해도도 높아졌습니다. 지쳤던 한 달이었지만 무사히 프로젝트를 마칠 수 있음에 뿌듯했습니다.
조장의 의견을 잘 따라준 팀원분들께 감사하다는 말씀 드리고 싶습니다.
</details>


<details>
<summary>서유영</summary>
기획 단계에서 구현하고자 한 목표가 많아 긴 기간에도 불구하고 매일 새벽까지 작업을 해서 체력적으로 아주 힘들었지만, 덕분에 애정이 많이 가는 프로젝트가 된 것 같습니다.
각자 자신 있는 부분에서 최대한의 능력을 발휘하기 위해 밤낮 가리지 않고 열심히 한 팀원들을 보며 자신도 많은 자극이 되어 앞으로 좀 더 개발을 열심히 할 수 있는 계기가 되었습니다.
많은 것을 배우게 된 프로젝트였습니다.
</details>


<details>
<summary>박은정</summary>
이번 프로젝트를 통해서 장고가 어떻게 작동하는지 이해하게 되었다.
또한, 내가 무엇이 부족하고, 필요한지 그리고 중요한 부분이 무엇인지 
파악할 수 있었다. 덕분에 앞으로의 공부 방향성에 대해서도 생각해볼 수 있었다.
몰아치면서 직접 개발을 할 때는 안보이고 생각하지 못했던 것들이
서비스를 만들고나서 직접 사용을 해볼 때 많이 보였다. 
개발자로서 사용자 경험이 많이 필요하다는 것을 느꼈고, 
깃버전 관리를 경험할 수 있어서 좋았다.  
함께 고생해준 팀원분들 모두에게 정말 감사합니다.  
</details>


<details>
<summary>정광배</summary>
한 달이라는 긴 기간 동안 많은 것을 시도해 보면서 달리다 보니 시간이 너무 빨리 간 것 같습니다.
함께 달려준 팀원분들께 너무 감사하고 좋은 완성물이 나와서 뿌듯합니다.
결제 API나 로컬스토리지로 장바구니를 구현하면서 많은 어려움이 있었지만, 관련 자료를 찾아보면서 많이 배울 기회가 되었습니다. 앞으로도 더 성장해서 팀에 더 많이 기여할 수 있는 실력을 갖추고 싶습니다.
</details>


<details>
<summary>방한영</summary>
처음 프로젝트를 시작 할 때 과연 한달짜리 프로젝트는 어떻게 해야 할 지 감도 오지 않았는데 벌써 이렇게 끝난 것 같습니다. 좋은 팀원분들과 함께 할 수 있어 영광이었고 평소에 생각하지 않던 주제였기에 좀 더 배울 수 있고 새로운 경험이었던 것 같습니다. 내일로 프로젝트는 끝나지만 끝이 아닌 새로운 시작으로 앞으로도 개발자로서 자질을 갖추는데 시간을 더욱 더 가졌으면 좋겠습니다.
</details>

## 프로젝트 회고

<details>
<summary>Keep</summary>

- 밤늦게까지 열심히 하는 모습
- 문제가 생길때마다 백, 프론트 상관없이 해결
- 제 위치에서 최선을 다함
- 매일매일 각자 한 작업들의 리뷰를 해서 팀원들간의 소통이 원활했던 것
- 광배님이 문제 해결 잘 해주셔서 광배님이랑 프로젝트 하고 싶음 - 팀원 모두 같이 해결하였습니다.
- 서로 존중하고 칭찬해주는 모습들
- 부트스트랩 등 사용하지 않고 순수 css, js만 사용해서 구현 한 것
</details>

<details>
<summary>Problem</summary>

- 기간, 능력에 비해 기획을 크게 잡음
- 부족한체력, 건강 고려하지 않았음
- 미적 감각의 부족으로 인해 디자인에 시간이 많이 소요됨
- 서로의 낯가림 때문에 친해지는데 시간이 많이 소요
- 촘촘한 기획에 익숙하지 못했던 것
- 나의 부족한 지식과 능력
- 자바스크립트 지식 부족
- css 컨벤션 정하지 않고 진행하여 복잡해짐
</details>

<details>
<summary>Try</summary>

- 프로젝트 시작 전 기획 단단히 잡기
- 디자이너 외주 (전문적인 인력을 통한 퀄리티 향상)
- 운동을 통한 체력관리
- 아이스브레이킹 필요
- 바닐라 js, react.js 공부하기
- 프로젝트 했던 코드들을 회고하면서 따로 정리해놓기
- css 컨벤션 미리 정하고 시작하기
</details>