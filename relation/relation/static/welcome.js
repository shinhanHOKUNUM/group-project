// 메뉴 버튼 클릭 시 메뉴를 토글하는 함수
function toggleMenu() {
    const menuItems = document.getElementById('menu-items');
    menuItems.style.display = menuItems.style.display === 'flex' ? 'none' : 'flex';
}

// 로그인 페이지 이동 함수
function navigateToLogin() {
    window.location.href = loginUrl;  // HTML에서 정의된 loginUrl을 사용
}