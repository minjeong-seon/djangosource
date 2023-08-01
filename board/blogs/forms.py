from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = "__all__" : 모델에 있는 모든 필드 사용하기
        # exclude = ["regdate", "updatedate"] : [] 안에 있는 필드만 빼고 다 포함
        fields = ["subject", "content", "image"]
