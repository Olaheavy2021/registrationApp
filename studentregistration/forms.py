from django import forms


class ContactForm(forms.Form):
    """
    A Django form for the contact-us page.
    It captures essential details like name, email, subject,
    and the message from the page visitor.
    """

    name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg"}),
    )
    email = forms.EmailField(
        required=True,
        max_length=255,
        widget=forms.EmailInput(attrs={"class": "form-control form-control-lg"}),
    )
    subject = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg"}),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"class": "form-control form-control-lg", "rows": "4"}
        ),
    )
