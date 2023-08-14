from django.urls import path
from .views import main
from users.views import paid_amount

app_name = "random"

urlpatterns = [
    # http://127.0.0.1:8000/randombox/ --메인 페이지(랜덤박스 이벤트)
    path("", main, name="main"),
    # http://127.0.0.1:8000/randombox/purchased --구매버튼 클릭 시 작동
    path("purchased/", paid_amount, name="paid_amount"),
]
