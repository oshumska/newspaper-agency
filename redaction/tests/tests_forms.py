from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from redaction.form import RedactorForm, UpdateYearsOfExperienceForm, NewspaperForm
from redaction.models import Topic


class FormsTests(TestCase):

    def test_redactor_form(self):
        form_data = {
            "username": "test_user",
            "password1": "<PASSWORD1>",
            "password2": "<PASSWORD1>",
            "email": "testuser@gmail.com",
            "first_name": "test",
            "last_name": "user",
            "years_of_experience": 10,
        }
        form = RedactorForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_redactor_years_of_exp_must_be_positive(self):
        form_data = {
            "username": "test_user",
            "password1": "<PASSWORD1>",
            "password2": "<PASSWORD1>",
            "email": "testuser@gmail.com",
            "first_name": "test",
            "last_name": "user",
            "years_of_experience": -1,
        }
        form = RedactorForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["years_of_experience"], None)

    def test_redactor_update_years_of_exp(self):
        """test that user can't enter negative number"""
        redactor = get_user_model().objects.create_user(
            username="user_create",
            password="<PASSWORD>",
        )
        form_data = {
            "years_of_experience": -1,
        }
        form = UpdateYearsOfExperienceForm(data=form_data, instance=redactor)
        self.assertFalse(form.is_valid())
        """test that user can enter positive number"""
        form_data = {
            "years_of_experience": 2,
        }
        form = UpdateYearsOfExperienceForm(data=form_data, instance=redactor)
        self.assertTrue(form.is_valid())
        """test that user can't reduce years of experience"""
        redactor.years_of_experience = 2
        redactor.save()
        form_data = {
            "years_of_experience": 1,
        }
        form = UpdateYearsOfExperienceForm(data=form_data, instance=redactor)
        self.assertFalse(form.is_valid())

    def test_newspaper_form(self):
        topic = Topic.objects.create(name="test topic")
        publisher = get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD1>",
        )
        form_data = {
            "title": "test",
            "content": "test content",
            "topic": topic.id,
            "publishers": (publisher.id,),
            "published_date": datetime.now(),
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], form_data["title"])
        self.assertEqual(form.cleaned_data["content"], form_data["content"])
        self.assertEqual(form.cleaned_data["topic"].id, form_data["topic"])
        self.assertEqual(form.cleaned_data["publishers"].first().id, publisher.id)
        self.assertEqual(
            form.cleaned_data["published_date"].replace(tzinfo=None),
            form_data["published_date"].replace(tzinfo=None),
        )
