from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from redaction.form import NewspaperSearchForm
from redaction.models import Newspaper, Topic

NEWSPAPER_URL = reverse("redaction:newspaper-list")
NEWSPAPER_CREATE_URL = reverse("redaction:newspaper-create")


def detail_newspaper_url(newspaper_id: int):
    return reverse("redaction:newspaper-detail", args=[newspaper_id])


def update_newspaper_url(newspaper_id: int):
    return reverse("redaction:newspaper-update", args=[newspaper_id])


def delete_newspaper_url(newspaper_id: int):
    return reverse("redaction:newspaper-delete", args=[newspaper_id])


class PublicNewspapersTest(TestCase):

    def setUp(self):
        self.client = Client()
        topic = Topic.objects.create(name="test 1")
        self.newspaper = Newspaper.objects.create(
            title="test 1", content="test content", topic=topic
        )

    def test_login_require(self):
        urls = [
            NEWSPAPER_URL,
            NEWSPAPER_CREATE_URL,
            detail_newspaper_url(self.newspaper.id),
            update_newspaper_url(self.newspaper.id),
            delete_newspaper_url(self.newspaper.id),
        ]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateNewspaperTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="user 1",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_newspaper(self):
        topic = Topic.objects.create(name="test 1")
        Newspaper.objects.create(title="test 1", content="test content", topic=topic)
        Newspaper.objects.create(title="test 2", content="test content", topic=topic)
        res = self.client.get(NEWSPAPER_URL)
        self.assertEqual(res.status_code, 200)
        redactors = Newspaper.objects.all()
        self.assertEqual(list(res.context["newspaper_list"]), list(redactors))

    def test_get_newspaper_context_data(self):
        topic = Topic.objects.create(name="test 1")
        Newspaper.objects.create(title="test 1", content="test content", topic=topic)
        Newspaper.objects.create(title="test 2", content="test content", topic=topic)
        res = self.client.get(NEWSPAPER_URL)
        search_form = NewspaperSearchForm(initial={"title": ""})
        self.assertEqual(str(res.context["search_form"]), str(search_form))

    def test_get_newspaper_queryset(self):
        topic = Topic.objects.create(name="test 1")
        Newspaper.objects.create(title="test 1", content="test content", topic=topic)
        Newspaper.objects.create(title="test 2", content="test content", topic=topic)
        res = self.client.get(NEWSPAPER_URL, data={"title": "1"})
        newspaper = Newspaper.objects.filter(title__icontains="1")
        self.assertEqual(list(res.context["newspaper_list"]), list(newspaper))

    def test_newspaper_details(self):
        topic = Topic.objects.create(name="test 1")
        newspaper = Newspaper.objects.create(
            title="test 1", content="test content", topic=topic
        )
        url = detail_newspaper_url(newspaper.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, newspaper.title)
        self.assertContains(res, newspaper.content)
        self.assertContains(res, newspaper.topic.name)

    def test_newspaper_create(self):
        topic = Topic.objects.create(name="test 1")
        data = {
            "title": "test create",
            "content": "test content",
            "topic": topic.id,
        }
        res = self.client.post(NEWSPAPER_CREATE_URL, data)
        self.assertEqual(res.status_code, 200)

    def test_newspaper_delete(self):
        topic = Topic.objects.create(name="test 1")
        newspaper = Newspaper.objects.create(
            title="test delete", content="test content", topic=topic
        )
        url = delete_newspaper_url(newspaper.id)
        res = self.client.post(url)
        self.assertRedirects(res, NEWSPAPER_URL)
        newspaper = Newspaper.objects.filter(title="test delete")
        self.assertEqual(newspaper.count(), 0)
