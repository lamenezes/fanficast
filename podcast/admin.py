from copy import deepcopy
from django.contrib import admin
from mezzanine.blog.admin import BlogPostAdmin

from .models import Episode

fields = ('short_description', 'cover_image', 'episode_link', 'length', 'cover_image_square')
episode_extra_fieldsets = [(None, {'fields': fields})]


class EpisodeAdmin(BlogPostAdmin):
    fieldsets = deepcopy(BlogPostAdmin.fieldsets) + episode_extra_fieldsets


admin.site.register(Episode, EpisodeAdmin)
