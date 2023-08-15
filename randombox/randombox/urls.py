from django.urls import path
from users.views import paid_amount

app_name = "random"

urlpatterns = [
    # http://127.0.0.1:8000/randombox/purchased --구매버튼 클릭 시 작동
    path("purchased/", paid_amount, name="paid_amount"),
]
