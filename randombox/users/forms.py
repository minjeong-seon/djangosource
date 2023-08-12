from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser  # CustomUser 모델을 import


class UserForm(UserCreationForm):
    """
    UserCreationForm 은 username(id), password1, password2 만 들어있음
    다른 정보를 받기 원하면 추가 필요함 ==> 새로운 클래스 작성
    """

    email = forms.EmailField(label="이메일")
    address = forms.CharField(max_length=255, label="주소")

    class Meta:
        model = CustomUser  # CustomUser 모델로 변경
        fields = ["username", "email", "address"]
