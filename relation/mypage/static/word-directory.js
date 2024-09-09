let currentElement = null; // 현재 선택된 단어 항목을 저장하는 변수

// 단어 세부 정보를 표시하는 함수
function showWordDetails(title, description, relatedWords, element) {
    // 단어 제목, 설명, 관련 단어를 세부 정보 영역에 업데이트
    document.getElementById("word-title").innerText = title;
    document.getElementById("word-description").innerText = description;
    document.getElementById("related-words").innerText = `관련 단어: ${relatedWords}`;

    // 현재 선택된 단어 항목을 저장
    currentElement = element;
    document.getElementById("delete-btn").style.display = "block"; // 삭제 버튼 표시
}

// 현재 선택된 단어 항목을 삭제하는 함수
function deleteCurrentWord() {
    // 선택된 단어가 있는 경우 삭제
    if (currentElement) {
        currentElement.remove(); // 단어 항목 삭제
        currentElement = null; // 현재 선택된 항목을 초기화

        // 세부 정보 영역을 기본 상태로 초기화
        document.getElementById("word-title").innerText = "저장된 단어 목록";
        document.getElementById("word-description").innerText = "단어의 자세한 설명이 필요하다면 단어를 클릭해주세요.";
        document.getElementById("related-words").innerText = "";
        document.getElementById("delete-btn").style.display = "none"; // 삭제 버튼 숨김
    }
}
