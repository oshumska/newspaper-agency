from django.urls import path
from redaction.views import index, TopicListView, RedactorListView

urlpatterns = [
    path("", index, name="index"),
    path("topic/", TopicListView.as_view(), name="topic-list"),
    path("redactor/", RedactorListView.as_view(), name="redactor-list"),
]

app_name = "redaction"
