from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from redaction.models import Redactor
from redaction.form import RedactorForm, RedactorSearchForm, UpdateYearsOfExperienceForm

REDACTOR_URL = reverse("redaction:redactor-list")
REDACTOR_CREATE_URL = reverse("redaction:redactor-create")


def redactor_detail_url(redactor_id):
    return reverse("redaction:redactor-detail", args=[redactor_id])


def update_redactor_experience_url(redactor_id):
    return reverse("redaction:update-experience", args=[redactor_id])


def redactor_delete_url(redactor_id):
    return reverse("redaction:redactor-delete", args=[redactor_id])


class PublicRedactorTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.redactor = get_user_model().objects.create_user(
            username="user1",
            password="<PASSWORD>",
        )

    def test_login_require(self):
        urls = [
            REDACTOR_URL,
            REDACTOR_CREATE_URL,
            redactor_detail_url(self.redactor.id),
            update_redactor_experience_url(self.redactor.id),
            redactor_delete_url(self.redactor.id),
        ]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateRedactorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="user 1",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_redactors(self):
        get_user_model().objects.create_user(
            username="user 2",
            password="<PASSWORD>",
        )
        get_user_model().objects.create_user(
            username="user 3",
            password="<PASSWORD>",
        )
        res = self.client.get(REDACTOR_URL)
        self.assertEqual(res.status_code, 200)
        redactors = Redactor.objects.all()
        self.assertEqual(list(res.context["redactor_list"]), list(redactors))

    def test_get_redactors_context_data(self):
        get_user_model().objects.create_user(
            username="user 2",
            password="<PASSWORD>",
        )
        get_user_model().objects.create_user(
            username="user 3",
            password="<PASSWORD>",
        )
        res = self.client.get(REDACTOR_URL)
        search_form = RedactorSearchForm(initial={"username": ""})
        self.assertEqual(str(res.context["search_form"]), str(search_form))

    def test_get_redactors_queryset(self):
        get_user_model().objects.create_user(
            username="user 2",
            password="<PASSWORD>",
        )
        get_user_model().objects.create_user(
            username="user 3",
            password="<PASSWORD>",
        )
        res = self.client.get(REDACTOR_URL, data={"username": "2"})
        redactor = Redactor.objects.filter(username__icontains="2")
        self.assertEqual(
            list(res.context["redactor_list"]),
            list(redactor),
        )

    def test_redactor_create(self):
        data = {
            "username": "user_create",
            "first_name": "user",
            "last_name": "user",
            "email": "email@gmail.com",
            "years_of_experience": 2,
            "password1": "<PASSWORD>",
            "password2": "<PASSWORD>",
        }
        res = self.client.post(REDACTOR_CREATE_URL, data=data)
        self.assertEqual(res.status_code, 200)

    def test_redactor_detail(self):
        redactor = get_user_model().objects.create_user(
            username="user_create",
            password="<PASSWORD>",
        )
        url = redactor_detail_url(redactor.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Delete")
        self.assertContains(res, "Newspapers")
        self.assertContains(res, "Add experience +")

    def test_update_experience_url(self):
        redactor = get_user_model().objects.create_user(
            username="user_create",
            password="<PASSWORD>",
        )
        url = update_redactor_experience_url(redactor.id)
        res = self.client.post(url, data={"years_of_experience": 2})
        self.assertRedirects(res, REDACTOR_URL)
        redactor.refresh_from_db()
        self.assertEqual(redactor.years_of_experience, 2)
        res = self.client.post(url, data={"years_of_experience": 1})
        redactor.refresh_from_db()
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(redactor.years_of_experience, 1)
        res = self.client.post(url, data={"years_of_experience": 3})
        self.assertRedirects(res, REDACTOR_URL)
        redactor.refresh_from_db()
        self.assertEqual(redactor.years_of_experience, 3)

    def test_redactor_delete(self):
        redactor = get_user_model().objects.create_user(
            username="user_create", password="<PASSWORD>"
        )
        url = redactor_delete_url(redactor.id)
        res = self.client.post(url)
        self.assertRedirects(res, REDACTOR_URL)
        redactor = Redactor.objects.filter(username="user_create")
        self.assertEqual(redactor.count(), 0)
