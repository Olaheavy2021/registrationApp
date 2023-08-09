from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from users.models import Student

# A constant to define a common CSS class used in form widgets.
FORM_CLASS_NAME = "form-control border-0 bg-light rounded-end ps-1"


class UserStudentRegistrationForm(UserCreationForm):
    """
    Form for student registration. Inherits from Django's built-in UserCreationForm
    and adds additional fields specific to the Student model.
    """

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
    """
    Custom user login form
    """

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
    """
    Form to update user attributes like first name, last name, and email.
    """

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Satrya",
                "class": "form-control",
                "readonly": "readonly",
                "id": "firstName",
                "required": "required",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Satrya",
                "class": "form-control",
                "readonly": "readonly",
                "id": "firstName",
                "required": "required",
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
    """
    Form to update a student's profile,
    including their date of birth, address, city, country, and profile photo.
    """

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
                    'required': 'required'
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "id": "address",
                    "class": "form-control",
                    "placeholder": "78, Cross Bedford St.",
                    "required": "required",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "id": "city",
                    "class": "form-control",
                    "placeholder": "Sheffield",
                    "required": "required",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "id": "country",
                    "class": "form-control",
                    "placeholder": "United Kingdom",
                    "required": "required",
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
    """
    Custom form to change a user's password,
    inheriting from Django's built-in PasswordChangeForm.
    """

    old_password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password1 = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields["old_password"].label = "Old Password"
        self.fields["new_password1"].label = "New Password"
        self.fields["new_password2"].label = "Confirm New Password"
