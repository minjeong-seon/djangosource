from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

# reverse_lazy(앱이름:url 패턴이름) : url 지연 평가 -- view 함수 실행 성공 시 이동할 리다이렉션 경로 지정

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            # 비번 변경 후 로그인 페이지 이동
            success_url=reverse_lazy("users:login"),
        ),
        name="password_change",
    ),
]
