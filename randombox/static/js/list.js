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
  console.log("검색어: ", search_bar.value);
  if (search_bar.value == "") {
    alert("검색어를 입력해 주세요.");
    search_bar.focus();
    return;
  }

  document.querySelector("#keyword").value = search_bar.value;
  document.querySelector("#actionForm").submit();
});
