from django.views.generic import ListView

from .models import Episode


class EpisodeSettingsMixin:
    template_name = 'index.html'
    context_object_name = 'episodes'
    queryset = Episode.objects.order_by('-publish_date')


class HomeView(EpisodeSettingsMixin, ListView):
    queryset = EpisodeSettingsMixin.queryset[:10]


class EpisodeListView(EpisodeSettingsMixin, ListView):
    paginate_by = 10
