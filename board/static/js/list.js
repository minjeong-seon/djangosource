// 페이지 나누기 영역 클릭 시 href 값 가져오기
document.querySelector(".pagination").addEventListener("click", (e) => {
  e.preventDefault();

  let href = e.target.getAttribute("href");
  console.log(href);

  // href 값을 actionForm의 page value 값에 대입
  document.querySelector("#page").value = href;
  document.querySelector("#actionForm").submit();
});

// 검색창
// 찾기 버튼 클릭 시
// 검색어 입력여부 확인(없으면 alert창 띄우기)+focus
// 검색어 있으면 하단 actionForm 안 keyword value 값에 검색어 삽입
document.querySelector("#btn_search").addEventListener("click", (e) => {
  e.preventDefault();

  const search_bar = document.querySelector("#top_keyword");

  if (search_bar.value == "") {
    alert("검색어를 입력해 주세요.");
    search_bar.focus();
    return;
  }

  document.querySelector("#keyword").value = search_bar.value;
  document.querySelector("#actionForm").submit();
});

// 정렬 기준 변화 시 값을 가져와서
// 페이지는 기본 1로 변경
// actionForm 안 sort에 값 변경 후 actionForm 전송

document.querySelector(".so").addEventListener("change", (e) => {
  document.querySelector("#page").value = 1;
  document.querySelector("#sort").value = e.target.value;
  document.querySelector("#actionForm").submit();
});

// 제목 클릭 시, a태그 중지 + href 값 가져오기
// actionForm의 action 값을 href로 변경후 submit
const titles = document.querySelectorAll(".text-decoration-none");
titles.forEach((title) => {
  title.addEventListener("click", (e) => {
    e.preventDefault();

    let actionForm = document.querySelector("#actionForm");
    actionForm.action = e.target.href;
    actionForm.submit();
  });
});
