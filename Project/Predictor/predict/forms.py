from django import forms
from .models import Img


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Img
        fields = ('image',)