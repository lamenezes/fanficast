from __future__ import unicode_literals

from django.db import models
from mezzanine.blog.models import BlogPost


class Episode(BlogPost):
    """
    Represents are a specific type of blog post that represent an podcast episode.
    Episodes show up in the homepage and in the blog.
    An episode has:
        - Short description
        - Cover image
        - Download link to the episode
    """

    short_description = models.CharField(max_length=256)

    cover_image = models.ImageField()

    episode_link = models.URLField(blank=True)
