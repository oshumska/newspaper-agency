from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from redaction.form import TopicSearchForm
from redaction.models import Topic

TOPIC_URL = reverse("redaction:topic-list")
TOPIC_CREATE_URL = reverse("redaction:topic-create")


def update_topic_url(topic_id: int):
    return reverse("redaction:topic-update", args=[topic_id])


def delete_topic_url(topic_id: int):
    return reverse("redaction:topic-delete", args=[topic_id])


class PublicTopicTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(name="test")

    def test_login_required(self):
        res = self.client.get(TOPIC_URL)
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(TOPIC_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)
        update_url = update_topic_url(self.topic.id)
        res = self.client.get(update_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateTopicTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_topic(self):
        Topic.objects.create(name="topic 1")
        Topic.objects.create(name="topic 2")
        res = self.client.get(TOPIC_URL)
        self.assertEqual(res.status_code, 200)
        topic = Topic.objects.all()
        self.assertEqual(list(res.context["topic_list"]), list(topic))

    def test_get_topic_context_data(self):
        Topic.objects.create(name="topic 1")
        Topic.objects.create(name="topic 2")
        res = self.client.get(TOPIC_URL)
        search_form = TopicSearchForm(initial={"name": ""})
        self.assertEqual(str(res.context["search_form"]), str(search_form))

    def test_topic_get_queryset(self):
        Topic.objects.create(name="topic 1")
        Topic.objects.create(name="topic 2")
        res = self.client.get(TOPIC_URL, data={"name": "1"})
        topic = Topic.objects.filter(name__icontains="1")
        self.assertEqual(
            list(res.context["topic_list"]),
            list(topic),
        )

    def test_topic_create(self):
        res = self.client.post(TOPIC_CREATE_URL, data={"name": "test"})
        self.assertRedirects(res, TOPIC_URL)
        try:
            Topic.objects.get(name="test")
        except Topic.DoesNotExist:
            self.assertTrue(False)

    def test_topic_update(self):
        topic = Topic.objects.create(name="topic 1")
        topic_id = topic.id
        url = update_topic_url(topic_id)
        res = self.client.post(url, data={"name": "change 1"})
        self.assertRedirects(res, TOPIC_URL)
        topic = Topic.objects.get(name="change 1")
        self.assertEqual(topic.id, topic_id)

    def test_topic_delete(self):
        topic = Topic.objects.create(name="topic 1")
        url = delete_topic_url(topic.id)
        res = self.client.post(url)
        self.assertRedirects(res, TOPIC_URL)
        topic = Topic.objects.filter(name="topic 1")
        self.assertEqual(len(topic), 0)
