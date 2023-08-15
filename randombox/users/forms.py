from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser  # CustomUser 모델을 import
from django.contrib.auth.forms import AuthenticationForm

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



class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "로그인 정보가 올바르지 않습니다. 다시 시도해주세요.",
        'inactive': "비활성화된 계정입니다.",
    }