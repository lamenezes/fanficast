from django.views.generic import TemplateView

from models import Episode


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['episodes'] = Episode.objects.all().order_by('-publish_date')
        return context
