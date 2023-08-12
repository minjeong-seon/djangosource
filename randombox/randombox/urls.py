from django.urls import path
from .views import main
from users.views import paid_amount

app_name = "random"

urlpatterns = [
    # http://127.0.0.1:8000/randombox/
    path("", main, name="main"),
    # http://127.0.0.1:8000/randombox/purchased
    path("purchased/", paid_amount, name="paid_amount"),
]
