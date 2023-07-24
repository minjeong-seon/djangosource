from django import forms
from .models import Photo


class PhotoForm(forms.ModelForm):
    """
    forms.ModelForm : form 은 Model 과 연결된 상태
    """

    class Meta:
        model = Photo
        fields = ["title", "author", "image", "description", "price"]
