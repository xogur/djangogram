from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

class SignUpForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name','username','password']

        # labels = {
        #     'email' : '이메일 주소',
        #     'name' : '성명',
        #     'username' : '사용자 이름',
        #     'password' : '비밀번호',

        # }

        widgets = {
            'email': django_forms.TextInput(attrs={'placeholder': '이메일 주소'}),
            'name': django_forms.TextInput(attrs={'placeholder': '성명'}),
            'username': django_forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password': django_forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user