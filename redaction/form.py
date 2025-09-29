from django import forms
from django.contrib.auth.forms import UserCreationForm

from redaction.models import Redactor


class RedactorForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "years_of_experience",
        )

    def clean_years_of_experience(self):
        if self.cleaned_data["years_of_experience"]:
            return self.cleaned_data["years_of_experience"] >= 0
        return True
