from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import UserForm

"""
django 가 제공하는 users 테이블 사용
from django.contrib.auth.models import User

UserCreationForm 을 이용한 회원가입
from django.contrib.auth.forms import UserCreationForm
"""


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # 회원가입 후 user가 로그인 직접 하기
            # return redirect("users:login")

            # 회원가입 후 로그인 처리 해주기
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # 세션에 정보가 담기게 됨
                login(request, user)
                return redirect("index")
    else:
        form = UserForm()
    return render(request, "users/register.html", {"form": form})
