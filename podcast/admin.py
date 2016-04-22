from copy import deepcopy
from django.contrib import admin
from mezzanine.blog.admin import BlogPostAdmin

from models import Episode

episode_extra_fieldsets = [
    (None, {'fields': ('short_description', 'cover_image', 'episode_link', 'length')}),
]


class EpisodeAdmin(BlogPostAdmin):
    fieldsets = deepcopy(BlogPostAdmin.fieldsets) + episode_extra_fieldsets


admin.site.register(Episode, EpisodeAdmin)
