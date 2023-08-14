document.addEventListener("DOMContentLoaded", function () {
  const openModalButton = document.getElementById("openModalButton");
  const category = document.getElementById("category");
  const tbody = document.getElementById("stockTableBody");
  const prevButton = document.getElementById("prevButton");
  const nextButton = document.getElementById("nextButton");

  const PAGE_ITEMS = 15; // 한 페이지당 아이템 수
  let currentPage = 1;
  let dataList = [];
  let totalPages = 1;

  // ---------------------------------------------------------------
  // selectedValue + keyword 같이 manage_stock 함수에 넘겨서 데이터 받아야 함

  document.getElementById("btn_search").addEventListener("click", function () {
    let selectedCategory = document.getElementById("category");
    let keyword = document.getElementById("top_keyword").value;
    let selectedValue = selectedCategory.value;
    if (selectedValue === "상품 분류") {
      alert("분류를 선택해주세요.");
      selectedCategory.focus();
    } else {
      currentPage = 1;
      console.log("검색어: ", keyword, "선택분류: ", selectedValue);
      fetch(`/master/stock/${selectedValue}/?keyword=${encodeURIComponent(keyword)}`)
        .then((response) => response.json())
        .then((responseData) => {
          dataList = [];

          if (selectedValue === "1" && responseData.general_list) {
            try {
              dataList = JSON.parse(responseData.general_list);
              console.log("검색결과: ", dataList);

              if (dataList.length === 0) {
                tbody.textContent = "일치하는 결과가 없습니다.";

                return;
              }
            } catch (error) {
              console.error("Error parsing JSON:", error);
            }
          } else if (selectedValue === "2" && responseData.brand_list) {
            try {
              dataList = JSON.parse(responseData.brand_list);
              console.log("검색결과: ", dataList);

              if (dataList.length === 0) {
                tbody.textContent = "일치하는 결과가 없습니다.";

                return;
              }
            } catch (error) {
              console.error("Error parsing JSON:", error);
            }
          }

          totalPages = Math.ceil(dataList.length / PAGE_ITEMS);
          updateTable(currentPage);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }
  });

  // ---------------------------------------------------------------
  const quantityInput = document.getElementById("quantity");
  const upButton = document.querySelector(".up");
  const downButton = document.querySelector(".down");
  var isPressed = false;
  upButton.addEventListener("mouseup", function (event) {
    isPressed = false;
  });
  upButton.addEventListener("mousedown", function (event) {
    isPressed = true;
    doInterval("1");
  });
  downButton.addEventListener("mouseup", function (event) {
    isPressed = false;
  });
  downButton.addEventListener("mousedown", function (event) {
    isPressed = true;
    doInterval("-1");
  });
  function doInterval(action) {
    if (isPressed) {
      quantityInput.value = parseInt(quantityInput.value) + parseInt(action);

      setTimeout(function () {
        doInterval(action);
      }, 200);
    }
  }
  // ---------------------------------------------------------------

  // ---------------------------------------------------------------
  // 재고 수량 0으로 업데이트(품절처리)

  document.body.addEventListener("click", (e) => {
    if (e.target.classList.contains("qty-ctrl")) {
        e.preventDefault();
        const row = e.target.closest("tr");
        const productName = row.querySelector(".pname").innerText;
        // const stockQuantity = parseInt(row.querySelector(".stock").innerText);

        const pid = e.target.getAttribute("data-id");
        const selectedValue = document.getElementById("category").value;
        const modified_qty = parseInt(document.getElementById(`quantity-${pid}`).value);

        console.log("수정입력: ",modified_qty)
        const confirmResult = confirm(productName + " 상품의 재고수량을 조절하시겠습니까?");
        if (!confirmResult) {
            return; // 사용자가 취소를 선택한 경우 요청을 중단
        }

        // CSRF 토큰 추출 및 헤더 설정
        const csrfToken = document.querySelector("#csrf-token").value;
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        headers.append("X-CSRFToken", csrfToken);

        var data = {
            quantity: parseInt(modified_qty),
        };

        fetch(`/master/stock/${encodeURIComponent(selectedValue)}/${encodeURIComponent(pid)}/`, {
          method: "POST",
          body: JSON.stringify(data),
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
          
        })
        .then((response) => response.json())
        .then((responseData) => {
            dataList = [];
            if (selectedValue === "1" && responseData.general_list) {
                try {
                    dataList = JSON.parse(responseData.general_list);
                } catch (error) {
                    console.error("Error parsing JSON:", error);
                }
            } else if (selectedValue === "2" && responseData.brand_list) {
                try {
                    dataList = JSON.parse(responseData.brand_list);
                } catch (error) {
                    console.error("Error parsing JSON:", error);
                }
            }

            totalPages = Math.ceil(dataList.length / PAGE_ITEMS);
            updateTable(currentPage);

            alert("처리되었습니다."); // 요청이 성공적으로 처리된 후에 알림 표시
        })
        .catch((error) => {
            console.error("Error fetching data:", error);
        });
    }
});

  // ---------------------------------------------------------------
  // 페이징 처리 -번호 업데이트(페이지 Prev, Next 클릭 시 태그 값 변동)

  function updatePageNumber() {
    const currentPageElement = document.getElementById("currentPage");
    currentPageElement.textContent = currentPage.toString();
  }

  // ---------------------------------------------------------------
  // 분류 선택 변경 감지 -selectedValue으로 view 함수에서 JSON 데이터 parsing

  category.addEventListener("change", (event) => {
    const selectedValue = event.target.value;
    console.log("selectedValue", selectedValue);
    openModalButton.href = `/master/stock/${selectedValue}/`;

    if (selectedValue === "1" || selectedValue === "2") {
      fetch(`/master/stock/${selectedValue}/`)
        .then((response) => response.json())
        .then((responseData) => {
          dataList = [];

          if (selectedValue === "1" && responseData.general_list) {
            try {
              dataList = JSON.parse(responseData.general_list);
            } catch (error) {
              console.error("Error parsing JSON:", error);
            }
          } else if (selectedValue === "2" && responseData.brand_list) {
            try {
              dataList = JSON.parse(responseData.brand_list);
            } catch (error) {
              console.error("Error parsing JSON:", error);
            }
          } else {
            tbody.textContent = "일치하는 결과가 없습니다.";
            return;
          }

          console.log(dataList);

          totalPages = Math.ceil(dataList.length / PAGE_ITEMS);
          updateTable(currentPage);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    } else {
      dataList = [];
      tbody.innerHTML = `
        <tr>
            <td>None</td>
            <td>None</td>
            <td>None</td>
            <td>None</td>
        </tr>
      `;
    }

    updatePageNumber();
  });

  // ---------------------------------------------------------------
  // 페이징 처리 - 이전 버튼 클릭 시 현재 페이지 번호 -1

  prevButton.addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      updateTable(currentPage);
    }
  });

  // ---------------------------------------------------------------
  // 페이징 처리 - 다음 버튼 클릭 시 현재 페이지 번호 +1

  nextButton.addEventListener("click", () => {
    if (currentPage < totalPages) {
      currentPage++;
      updateTable(currentPage);
    }
  });

  // ---------------------------------------------------------------
  // 페이징 처리 -페이지 번호 시작/끝 비활성화 처리

  function updateTable(pageNumber) {
    const totalPages = Math.ceil(dataList.length / PAGE_ITEMS);

    tbody.innerHTML = generateTableRows(dataList, pageNumber, PAGE_ITEMS);
    prevButton.disabled = pageNumber === 1;
    nextButton.disabled = pageNumber === totalPages;

    currentPage = pageNumber;
    updatePageNumber(); // currentPage 업데이트
  }

  // ---------------------------------------------------------------
  // 템플릿에 출력할 내용 가져오기
  // toLocaleString() : 세 단위마다 `,` 표시

  function generateTableRows(dataList, pageNumber, itemsPerPage) {
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, dataList.length);
    let selectedValue = document.getElementById("category").value;

    console.log("제발...", selectedValue);
    return dataList
      .slice(startIndex, endIndex)
      .map(
        (item) => `
        <tr class="text-center">
            <td >${item.pk}</td>
            <td class="pname">${decodeUnicodeEscape(item.fields.pname)}</td>
            <td>${item.fields.price.toLocaleString()}<span>원</span></td>
            <td class="d-flex" style="display: flex !important;
            justify-content: flex-end !important;
            align-items: baseline !important;">
              <span class="stock mg-r">${item.fields.stock_qty}</span> 
              <div class="custom_input_group">
                <div class="input-group" id="custom_input">
                  <input type="hidden" id="csrf-token" name="csrfmiddlewaretoken" value="${csrfToken}">
                  <input type="number" name="quantity" id="quantity-${item.pk}" class="form-control" value="0" min="1" step="1">
                  <button class="qty-ctrl btn btn-outline-warning ms-1" data-id="${item.pk}">확인</button>
                </div>
              </div>
            </td>
        </tr>
      `
      )
      .join("");
  }

  // ---------------------------------------------------------------

  function decodeUnicodeEscape(str) {
    return str.replace(/\\u[\dA-Fa-f]{4}/g, (match) => String.fromCharCode(parseInt(match.slice(2), 16)));
  }
});
