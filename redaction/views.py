from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from redaction.models import Topic, Redactor, Newspaper


def index(request: HttpRequest) -> HttpResponse:
    num_topic = Topic.objects.count()
    num_redactor = Redactor.objects.count()
    num_newspaper = Newspaper.objects.count()
    context = {
        "num_topic": num_topic,
        "num_redactor": num_redactor,
        "num_newspaper": num_newspaper,
    }
    return render(request, "redaction/index.html", context=context)


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 10


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 10
