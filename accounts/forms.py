from django import forms
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']


class SetAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'profile',
            'province',
            'cityfrom django import forms',
        ]

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']


class SetAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'profile',
            'province',
            'city',
            'complete_address',
            'postal_code',
            'receiver',
        ]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'mobile',
            'phone',
            'card_number',
            'id_code',
            'is_edited',
        ]


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=150, label='Email')


class ResetPasswordConfirmForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput, label='New Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, label='Confirm Password'
    )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput, label='Old Password'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput, label='New Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, label='Confirm Password'
    )

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'mobile',
            'phone',
            'card_number',
            'id_code',
            'is_edited',
        ]


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=150, label='Email')


class ResetPasswordConfirmForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput, label='New Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, label='Confirm Password'
    )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput, label='Old Password'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput, label='New Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, label='Confirm Password'
    )
