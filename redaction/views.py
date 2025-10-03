from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from redaction.models import Topic, Redactor, Newspaper
from redaction.form import RedactorForm, NewspaperForm, UpdateYearsOfExperienceForm


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


class TopicCreateView(generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("redaction:topic-list")


class TopicUpdateView(generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("redaction:topic-list")


class TopicDeleteView(generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("redaction:topic-list")


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 10


class RedactorCreateView(generic.CreateView):
    model = Redactor
    form_class = RedactorForm
    success_url = reverse_lazy("redaction:redactor-list")


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspapers__topic", "newspapers__sub_topic")


class RedactorUpdateYearsOfExperience(generic.UpdateView):
    model = Redactor
    form_class = UpdateYearsOfExperienceForm
    template_name = "redaction/redactor_update_experience.html"
    success_url = reverse_lazy("redaction:redactor-list")


class RedactorDeleteView(generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("redaction:redactor-list")


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 10


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("redaction:newspaper-list")


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
    queryset = Newspaper.objects.prefetch_related("publishers", "sub_topic").select_related("topic")


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("redaction:newspaper-list")
