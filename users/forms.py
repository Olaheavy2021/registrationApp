from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

FORM_CLASS_NAME = "form-control border-0 bg-light rounded-end ps-1"


class StudentRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "C2065612",
                "class": FORM_CLASS_NAME,
                "id": "studentId",
            }
        ),
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Satrya",
                "class": FORM_CLASS_NAME,
                "id": "firstName",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Fajri",
                "class": FORM_CLASS_NAME,
                "id": "lastName",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "eg. mygeekyemail@cloudgeeks.com",
                "id": "exampleInputEmail1",
                "class": FORM_CLASS_NAME,
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "********",
                "class": FORM_CLASS_NAME,
                "id": "inputPassword1",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "********",
                "class": FORM_CLASS_NAME,
                "id": "inputPassword2",
            }
        )
    )
    course = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select Course",
        widget=forms.Select(
            attrs={
                "class": FORM_CLASS_NAME,
                "id": "course",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "course",
            "password1",
            "password2",
        ]


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "eg. C2065612",
                "id": "exampleInputUsername",
                "class": FORM_CLASS_NAME,
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "********",
                "class": FORM_CLASS_NAME,
                "id": "inputPassword1",
            }
        )
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
