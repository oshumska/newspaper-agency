from django.urls import path
from redaction.views import index, TopicListView

urlpatterns = [
    path("", index, name="index"),
    path("topic/", TopicListView.as_view(), name="topic-list")
]

app_name = "redaction"
