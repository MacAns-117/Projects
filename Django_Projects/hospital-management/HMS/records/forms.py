from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Nurse, Patient


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css)


class PatientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["name", "blood_group", "age", "disease", "location"]


class NurseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Nurse
        fields = [
            "name",
            "gender",
            "department",
            "shift",
            "care",
            "experience",
            "certifications",
            "contact_number",
            "email",
            "address",
            "profile_picture",
        ]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
