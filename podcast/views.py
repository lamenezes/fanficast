from django.views.generic import ListView

from .models import Episode


class EpisodeSettingsMixin:
    context_object_name = 'episodes'
    queryset = Episode.objects.order_by('-publish_date')


class HomeView(EpisodeSettingsMixin, ListView):
    queryset = EpisodeSettingsMixin.queryset[:7]
    template_name = 'index.html'


class EpisodeListView(EpisodeSettingsMixin, ListView):
    paginate_by = 15
    template_name = 'episodes.html'
