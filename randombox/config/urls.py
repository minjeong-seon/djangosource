from django.contrib import admin
from django.urls import path, include
from randombox.views import main, master

urlpatterns = [
    path("admin/", admin.site.urls),
    path("randombox/", include("randombox.urls")),
    path("users/", include("users.urls")),
    path("qna/", include("qna.urls")),
    # http://127.0.0.1:8000/ -메인페이지 설정하기
    path("", main, name="main"),
    # http://127.0.0.1:8000/master -관리자 페이지
    path("master/", master, name="master"),
]
