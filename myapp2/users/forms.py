from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    """
    form.ModelForm
        ▽
    BaseUserCreationForm
        ▽
    UserCreationForm
        ▽
    UserForm : User 테이블 모든 필드 + 상속
        ▽
    UserCreationForm 클래스를 상속받는 Form
    """

    # 부모가 넘겨주는 email은 필수 입력 요소가 아님 ==> 필수입력요소로 만들기 : 재정의
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        # fields = "__all__" + 상속
        fields = ["username", "email"]  # + 상속(password1, password2)
