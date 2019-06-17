import tempfile

import pytest

from .factories import EpisodeFactory

pytestmark = pytest.mark.django_db


def test_episode_get_slug():
    episode = EpisodeFactory(title='Poxa vida ein uol')
    assert episode.get_slug() == 'poxa-vida-ein-uol'

    episode = EpisodeFactory(title='ikárâi$ ---- dã.top')
    assert episode.get_slug() == 'ikarai-datop'


def test_episode_cover_image_url():
    with tempfile.NamedTemporaryFile(suffix='.jpg') as fp:
        episode = EpisodeFactory(cover_image=fp.name)

    assert episode.cover_image_url
