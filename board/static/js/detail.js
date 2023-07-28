// detail 클래스 명 이용
// a 태그 기능 중지
// 삭제 클릭 시 confirm 메시지 띄우기
// 확인 시 지정 경로로 이동

const deleteAll = document.querySelectorAll(".delete");
deleteAll.forEach((item) => {
  item.addEventListener("click", (e) => {
    e.preventDefault();

    if (confirm("질문을 삭제하시겠습니까?")) {
      location.href = e.target.href;
      alert("성공적으로 삭제되었습니다.");
    }
  });
});
