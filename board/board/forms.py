from .models import Question, Answer
from django import forms

"""
django의 form 클래스 이용

"""


# class NameForm(forms.Form):
#     name = forms.CharField(
#         label="name", max_length=100, error_messages={"required": "이름 입력"}
#     )


class QuestionForm(forms.ModelForm):
    # Meta Class : 기본 정보 알려주기
    class Meta:
        model = Question
        fields = ["subject", "content"]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]
