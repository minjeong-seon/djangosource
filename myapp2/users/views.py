from django.shortcuts import render, redirect

# django 에서 제공하는 User 생성폼과 모델 가져오기
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# 로그인 처리
from django.contrib.auth import authenticate, login, logout

# 비밀번호 변경
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .forms import UserForm


def index(request):
    return render(request, "index.html")


def user_main(request):
    return render(request, "users/main.html")


# def signup(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("users:login")
#     else:
#         form = UserCreationForm()

#     return render(request, "users/register.html", {"form": form})


def signup(request):
    """
    회원가입 시 UserForm 사용하는 방식
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = UserCreationForm()

    return render(request, "users/register.html", {"form": form})


def common_login(request):
    """
    (djnago-views 기능 안 쓰고)개발자가 로그인을 직접 구현할 때 사용
    """
    if request.method == "POST":
        # server에서 사용자 입력값 가져오기
        username = request.POST["username"]
        password = request.POST["password"]

        # 사용자가 존재한다면 권한을 가진 user 객체 리턴
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login() : session에 정보가 저장됨
            login(request, user)
            return redirect("index")

    return render(request, "users/login.html")


def common_logout(requset):
    """
    (djnago-views 기능 안 쓰고)개발자가 로그인을 직접 구현할 때 사용
    """
    logout(requset)
    return redirect("index")


def common_password_change(request):
    """
    (djnago-views 기능 안 쓰고)개발자가 로그인을 직접 구현할 때 사용
    """
    if request.method == "POST":
        form = PasswordChangeForm(requset.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
        else:
            form = PasswordChangeForm()

        return render(request, "users/password_change.html", {"form": form})


"""
django에서 USER 작업 시
django.contrib.auth.views 안에 정의된 여러 클래스들 사용 가능

login  => LoginView
logout => LogoutView
password 변경 => PasswordChangeView
password 초기화 => PasswordResetView
password 초기화를 위한 이메일 전송 => PasswordResetConfirm
"""


class CustomPasswordChangeView(PasswordChangeView):
    """
    PasswordChangeView 에서 정의한 template_name 은
    registration/password_chage_form.html 을 찾도록 되어 있음

    success_url 은 password_change_done 으로 이동함
    """

    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:login")
