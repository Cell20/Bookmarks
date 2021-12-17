from django import forms
from django.contrib.auth.models import User
from .models import Profile
import os


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
# MY CODE
    # def save(self, commit=True):
    #     profile = super().save(commit=True) # try if error
    #     photo = self.cleaned_data['photo']  # cleaned_data.get('photo')

    #     if photo:
    #         if photo.url.startswith('/media/h') == True:
    #             photo.path
    #             photo.url = '/media/2021/12/16/'


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'There is already an account associated with this email address. Try Logging in.')
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
