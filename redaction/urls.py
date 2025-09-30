from django.urls import path
from redaction.views import (
    index,
    TopicListView,
    RedactorListView,
    NewspaperListView,
    TopicCreateView,
    TopicUpdateView,
    RedactorCreateView,
    NewspaperCreateView, RedactorDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("topic/", TopicListView.as_view(), name="topic-list"),
    path("topic/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topic/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),
    path("redactor/", RedactorListView.as_view(), name="redactor-list"),
    path("redactor/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
    path("redactor/create/", RedactorCreateView.as_view(), name="redactor-create"),
    path("newspaper/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspaper/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
]

app_name = "redaction"
