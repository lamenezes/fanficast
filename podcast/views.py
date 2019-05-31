from django.views.generic import TemplateView

from .models import Episode


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        episodes = Episode.objects.all().order_by('-publish_date')
        if episodes:
            context['last_episode'] = episodes[0]
            context['episodes'] = episodes[1:]
        return context
