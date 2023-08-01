// 좋아요 이미지 클릭 시
document.querySelector(".recommand button").addEventListener("click", (e) => {
  console.log(e.currentTarget.dataset.id);

  fetch(`/blogs/likes/${e.currentTarget.dataset.id}/`)
    .then((response) => {
      if (!response.ok) {
        return new Error("에러");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);

      // 좋아요 정리
      if (data["is_liked"]) {
        document.querySelector(".recommand img:nth-child(2)").classList.add("disabled");
        document.querySelector(".recommand img:nth-child(1)").classList.remove("disabled");
      } else {
        document.querySelector(".recommand img:nth-child(1)").classList.add("disabled");
        document.querySelector(".recommand img:nth-child(2)").classList.remove("disabled");
      }

      // 추천 전체 수
      document.querySelector(".like_count").innerHTML = data["likes"];
    })
    .catch((error) => console.log(error));
});
