from django.urls import path
from .views import detail, info

# app의 namespace 지정
app_name = "app1"

urlpatterns = [
    # http://127.0.0.1:8000/app1/
    path("", detail, name="detail"),
    # http://127.0.0.1:8000/app1/info/
    path("info/", info, name="info"),
]
