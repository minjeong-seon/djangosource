from django.contrib import admin
from django.urls import path, include
from randombox.views import main, master
from users.modal_view import manage_stock, quantity_control
from users.views import customer

urlpatterns = [
    path("admin/", admin.site.urls),
    path("randombox/", include("randombox.urls")),
    path("users/", include("users.urls")),
    path("qna/", include("qna.urls")),
    # http://127.0.0.1:8000/ -메인페이지 설정하기
    path("", main, name="main"),
    # http://127.0.0.1:8000/master -관리자 페이지
    path("master/", master, name="master"),
    # http://127.0.0.1:8000/master/stock/선택분류 -재고관리
    path("master/stock/<int:selectedValue>/", manage_stock, name="manage_stock"),
    # http://127.0.0.1:8000/master/stock/선택분류/상품id -품절처리
    path(
        "master/stock/<int:selectedValue>/<int:pid>/",
        quantity_control,
        name="quantity_control",
    ),
    # http://127.0.0.1:8000/master/customer/ -회원관리
    path("master/customer/", customer, name="customer"),
]
