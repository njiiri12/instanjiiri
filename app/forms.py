from .models import Image, Profile
from django import forms


class NewImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['date_created', 'likes', 'user']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'bio', 'profile_photo')
        exclude = ['user']
        