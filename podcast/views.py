from django.views.generic import ListView

from .models import Episode


class HomeView(ListView):
    template_name = 'index.html'
    paginate_by = 10
    queryset = Episode.objects.order_by('-publish_date')
    context_object_name = 'episodes'
