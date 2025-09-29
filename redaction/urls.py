from django.urls import path
from redaction.views import index, TopicListView, RedactorListView, NewspaperListView, TopicCreateView

urlpatterns = [
    path("", index, name="index"),
    path("topic/", TopicListView.as_view(), name="topic-list"),
    path("topic/create/", TopicCreateView.as_view(), name="topic-create"),
    path("redactor/", RedactorListView.as_view(), name="redactor-list"),
    path("newspaper/", NewspaperListView.as_view(), name="newspaper-list"),
]

app_name = "redaction"
