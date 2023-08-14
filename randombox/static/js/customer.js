// 페이지 나누기 영역 클릭 시 href 값 가져오기
document.querySelector(".pagination").addEventListener("click", (e) => {
  e.preventDefault();

  let href = e.target.getAttribute("href");
  console.log(href);

  document.querySelector("#page").value = href;
  document.querySelector("#actionForm").submit();
});

// 검색창
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

// 정렬 기준 변화 시: 페이지는 기본 1로 변경
// actionForm 안 sort에 값 변경 후 actionForm 전송
document.querySelector(".so").addEventListener("change", (e) => {
  document.querySelector("#page").value = 1;
  document.querySelector("#sort").value = e.target.value;
  document.querySelector("#actionForm").submit();
});

// 당첨여부 다시 클릭 시 서랍 닫기
// 당첨여부 다시 클릭 시 서랍 닫기
const collapseLinks = document.querySelectorAll(".drawer");
collapseLinks.forEach((drawer) => {
  drawer.addEventListener("click", (e) => {
    e.preventDefault();

    const target = drawer.getAttribute("href");
    console.log("타겟: ", target);

    // 클릭한 요소의 서랍 영역 가져오기
    const drawer_contents = document.querySelector(target);
    console.log("서랍내용:", drawer_contents);
    console.log("서랍 classList:", drawer_contents.classList);

    if (drawer_contents.classList.contains("show")) {
      console.log("안녕");
      drawer_contents.classList.remove("show");
    } else {
      console.log("Hello");
      drawer_contents.classList.add("show");
    }
  });
});
