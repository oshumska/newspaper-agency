from django.contrib.auth import get_user_model
from django.test import TestCase

from redaction.models import Topic, Redactor, Newspaper


class ModelsTests(TestCase):

    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEqual(str(topic), topic.name)

    def test_redactor_str(self):

        redactor = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            first_name="test",
            last_name="test",
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username} ({redactor.first_name} {redactor.last_name})",
        )

    def test_newspaper_str(self):
        topic = Topic.objects.create(name="test")
        redactor = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            first_name="test",
            last_name="test",
        )
        newspaper = Newspaper.objects.create(
            title="test",
            content="test content",
            topic=topic,
        )
        self.assertEqual(str(newspaper), f"{newspaper.topic.name}: {newspaper.title}")
