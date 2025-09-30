import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from redaction.models import Redactor, Newspaper, Topic


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


class NewspaperForm(forms.ModelForm):
    published_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects,
        widget=forms.CheckboxSelectMultiple(),
    )
    topic = forms.ModelChoiceField(
        queryset=Topic.objects,
        widget=forms.RadioSelect()
    )
    sub_topic = forms.ModelMultipleChoiceField(
        queryset=Topic.objects,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Newspaper
        fields = "__all__"
