from unicodedata import normalize
import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.blog.models import BlogPost

from .fields import CompressedImageField


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

    # Best resolutions (from best to worst): 1080x600, 810x450, 540x300
    cover_image = CompressedImageField(
        verbose_name=_('Cover Image (810x450)'),
        resize_to=(0, 300),
        image_quality=90,
    )

    cover_image_square = CompressedImageField(
        verbose_name=_('Square Cover Image (600x600)'),
        resize_to=(0, 300),
        image_quality=90,
        blank=True,
    )

    episode_link = models.URLField(blank=True)

    length = models.DurationField()

    is_episode = True

    @property
    def cover_image_url(self):
        return os.path.join(settings.MEDIA_URL, self.cover_image.url)

    def get_slug(self):
        slug = super(Episode, self).get_slug()
        normalized_slug = normalize('NFKD', slug)
        return normalized_slug.encode('ASCII', 'ignore').decode()
