from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "users"

urlpatterns = [
    # http://127.0.0.1:8000/users/
    path("", views.user_main, name="main"),
    # http://127.0.0.1:8000/users/register
    path("register/", views.signup, name="register"),
    # # http://127.0.0.1:8000/users/login
    # path("login/", views.common_login, name="login"),
    # # http://127.0.0.1:8000/users/logout
    # path("logout/", views.common_logout, name="logout"),
    # django 가 제공하는 views 사용하기
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
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
]
