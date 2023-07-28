from django.urls import path
from .views import index

app_name = "app2"

urlpatterns = [
    # http://127.0.0.1:8000/app2
    path("", index, name="detail")
]
