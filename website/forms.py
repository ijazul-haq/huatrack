from django import forms
from django.contrib.auth.models import User
from .models import Artwork, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ArtworkForm(forms.ModelForm):

    class Meta:
        model = Artwork
        fields = ['title', 'created', 'path']
        widgets = {
            'created': forms.DateInput(attrs={'id': 'date', 'class': 'datepicker'})
        }

    def __init__(self, *args, **kwargs):
        super(ArtworkForm, self).__init__(*args, **kwargs)
        self.fields['path'].widget.attrs.update({'class': 'file-path validate'})


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['public_key', 'private_key']


class ArtworkTransferForm(forms.ModelForm):

    class Meta:
        model = Artwork
        fields = ['txid']
