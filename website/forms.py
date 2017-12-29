from django import forms
from .models import User


class UserReg(forms.ModelForm):
    # name = forms.CharField()
    # username = forms.CharField()
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'
