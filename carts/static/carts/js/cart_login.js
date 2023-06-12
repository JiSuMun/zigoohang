window.addEventListener('DOMContentLoaded', (event) => {
  const loginForm = document.getElementById('login-form')
  
  loginForm.addEventListener('submit', async (e) => {
    // 기본 폼 제출 행위를 막음
    e.preventDefault()

    // localStorage에서 cart 데이터 가져오기
    const cartData = localStorage.getItem('cart')
    
    // FormData 객체 생성
    const formData = new FormData(loginForm)
    formData.set('cart_data', cartData || '[]')
    
    // 로그인 요청(POST)을 보냄
    const response = await fetch(loginForm.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
      },
      credentials: 'same-origin', // 로그인한 사용자에 대한 쿠키를 전송
    })

    // 서버에서 반환한 JSON 데이터
    const json = await response.json()

    if (json.status === 'success') {
      // 로컬 스토리지의 카트 데이터를 삭제하고
      localStorage.removeItem('cart')
      // 지정된 URL로 리디렉션
      window.location.replace(json.redirect_url)
    } else {
      // 에러 메시지 표시 (실패한 경우)
      alert(json.message)
    }
  })
})