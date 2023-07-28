from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserForm(UserCreationForm):
    """
    UserCreationForm 은 username(id), password1, password2 만 들어있음
    다른 정보를 받기 원하면 추가 필요함 ==> 새로운 클래스 작성
    """

    # 부모가 내려줄 때 email은 null이 가능한 상태로 상속 ==> required 상태로 사용하기 위해서 선언
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        # 모델(테이블)에서 사용할 필드 지정
        fields = ["username", "email"]
