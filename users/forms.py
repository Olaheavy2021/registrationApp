from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from users.models import Student

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


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Satrya",
                "class": "form-control",
                "id": "firstName",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Satrya",
                "class": "form-control",
                "id": "firstName",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "eg. mygeekyemail@cloudgeeks.com",
                "id": "exampleInputEmail1",
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["dob", "address", "city", "country", "photo"]
        widgets = {
            "dob": forms.DateInput(
                attrs={
                    "id": "dob",
                    "class": "form-control",
                    "placeholder": "DD-MM-YYYY",
                    "type": "date",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "id": "address",
                    "class": "form-control",
                    "placeholder": "78, Cross Bedford St.",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "id": "city",
                    "class": "form-control",
                    "placeholder": "Sheffield",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "id": "country",
                    "class": "form-control",
                    "placeholder": "United Kingdom",
                }
            ),
            "photo": forms.FileInput(
                attrs={
                    "class": "form-control d-none",
                    "id": "photo",
                    "onchange": "handleFileChange(this)",
                }
            ),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password1 = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
