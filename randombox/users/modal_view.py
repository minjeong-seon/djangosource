from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.serializers import serialize
from .models import General, Brand
from django.http import HttpResponseBadRequest
import json


# 재고 관리 모달창 데이터 전달(JsonResponse)
def manage_stock(request, selectedValue):
    keyword = request.GET.get("keyword", "")
    sort = request.GET.get("sort", "recent")

    print("검색어: ", keyword)
    print("sort: ", sort)

    general_list = General.objects.order_by("-price")
    brand_list = Brand.objects.order_by("-price")

    data = {}  # data 변수 초기화
    
    print("selectedValue: ", selectedValue)

    # selectedValue = 1 : 일반 상품군
    if selectedValue == 1:
        if keyword:
            general_list = general_list.filter(
                Q(pname__icontains=keyword) | Q(id__icontains=keyword)
            ).distinct()

        # Ajax로 작업하기 위해 Json으로 직렬화해서 데이터 보내기
        serialized_general_list = serialize("json", general_list)

        data = {
            "general_list": serialized_general_list,
            "keyword": keyword,
            "sort": sort,
        }

    # selectedValue = 2 : 브랜드 상품군
    elif selectedValue == 2:
        if keyword:
            brand_list = brand_list.filter(
                Q(pname__icontains=keyword) | Q(id__icontains=keyword)
            ).distinct()

        serialized_brand_list = serialize("json", brand_list)

        data = {
            "brand_list": serialized_brand_list,
            "keyword": keyword,
            "sort": sort,
        }

    # Json 데이터 보내기(url에서 경로 지정 필수: config/urls.py에 설정함)
    return JsonResponse(data, content_type="application/json; charset=utf-8")


# 모달창에서 재고 수량 조절
def quantity_control(request, selectedValue, pid):
    # 템플릿에서 넘겨받는 값은 문자열이므로 int 값으로 변환
    selectedValue = int(selectedValue)

    data = {}  # data 변수 초기화

    # 넘겨받는 값에 따라 변수에 모델 담기
    if selectedValue == 1:
        model = General
    elif selectedValue == 2:
        model = Brand
    else:
        return HttpResponseBadRequest("잘못된 선택 값입니다.")

    # 담은 모델 써먹기(템플릿에서 유저가 선택한 데이터 가져오기)
    obj = get_object_or_404(model, id=pid)
    print("선택한 품목: ", obj)


    if request.method == "POST":
        # Ajax 에서 json 으로 넘겨받은 quantity 데이터 int 값으로 파싱
        request_data = json.loads(request.body)
        modified_qty = int(request_data.get("quantity"))

        print("수정 입력: ", modified_qty)

        if modified_qty is None:
            return HttpResponseBadRequest("데이터 값 확인 필요")

        # 선택한 데이터에 입력받은 값 업데이트(재고수량 조절)
        obj.stock_qty = modified_qty
        obj.save()


        if selectedValue == 1:
            general_list = General.objects.order_by("-price")
            serialized_general_list = serialize("json", general_list)
            data["general_list"] = serialized_general_list

        elif selectedValue == 2:
            brand_list = Brand.objects.order_by("-price")
            serialized_brand_list = serialize("json", brand_list)
            data["brand_list"] = serialized_brand_list

    return JsonResponse(data, content_type="application/json; charset=utf-8")
