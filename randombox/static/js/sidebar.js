// DOMContentLoaded : 웹페이지의 모든 html 요소 로드 후 발생하는 이벤트를 정의할 때 사용
document.addEventListener("DOMContentLoaded", function () {
  // 구매수량 input 태그 가져오기
  const qty = document.getElementById("quantity");
  const upButton = document.querySelector(".up");
  const downButton = document.querySelector(".down");
  const price = document.querySelector(".price");

  // 기본 가격 설정
  const defaultPrice = 20000;

  // 초기 가격 표시
  updatePrice(defaultPrice);

  // 수량 up == 구매금액도 up
  upButton.addEventListener("click", function () {
    incrementQuantity();
    updatePrice(defaultPrice * parseInt(qty.value));
  });

  // 수량 down == 구매금액도 down
  downButton.addEventListener("click", function () {
    decrementQuantity();
    updatePrice(defaultPrice * parseInt(qty.value));
  });

  // 수량 증가 시 가격 증가 함수
  function incrementQuantity() {
    const currentValue = parseInt(qty.value);
    const maxValue = parseInt(qty.max);
    if (currentValue < maxValue) {
      qty.value = currentValue + 1;
    }
  }

  // 수량 감소 시 가격 감소 함수
  function decrementQuantity() {
    const currentValue = parseInt(qty.value);
    const minValue = parseInt(qty.min);
    if (currentValue > minValue) {
      qty.value = currentValue - 1;
    }
  }

  // 최종 구매 가격 html에 업데이트
  function updatePrice(newPrice) {
    price.textContent = newPrice.toLocaleString() + "원";
  }

  // 구매 폼에 이벤트 리스너 추가
  const purchaseButton = document.getElementById("purchase-btn");
  const form = document.getElementById("purchase-form");

  purchaseButton.addEventListener("click", (e) => {
    e.preventDefault();
    const amount = parseInt(qty.value) * defaultPrice;
    document.getElementById("price_field").value = amount;

    const current = parseInt(document.querySelector("#p_amount").value);

    // console.log(current + amount);

    if (current + amount <= 100000) {
      alert("구매가 완료되었습니다.");
      form.submit();
    } else if (current + amount > 100000) {
      alert("구매 수량을 초과하였습니다.");
      return; // 함수 실행 중지
    }
  });
});
