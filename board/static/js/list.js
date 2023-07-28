// 페이지 나누기 영역 클릭 시 href 값 가져오기
document.querySelector(".pagination").addEventListener("click", (e) => {
  e.preventDefault();

  let href = e.target.getAttribute("href");
  console.log(href);

  // href 값을 actionForm의 page value 값에 대입
  document.querySelector("#page").value = href;
  document.querySelector("#actionForm").submit();
});
