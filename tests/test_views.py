import pytest
from django.core.urlresolvers import reverse

from podcast.views import EpisodeListView, HomeView

from .factories import EpisodeFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def home_view():
    return HomeView.as_view()


@pytest.fixture
def episode_list_view():
    return EpisodeListView.as_view()


def test_home_view(rf, home_view):
    EpisodeFactory.create_batch(8)
    request = rf.get(reverse('home'))

    response = home_view(request)

    assert response.status_code == 200
    assert response.context_data['is_paginated'] is False
    assert response.context_data['episodes'].count() == 7


def test_episodes_view(rf, episode_list_view):
    EpisodeFactory.create_batch(16)
    request = rf.get(reverse('episodes'))

    response = episode_list_view(request)

    assert response.status_code == 200
    assert response.context_data['is_paginated'] is True
    assert response.context_data['episodes'].count() == 15


def test_episodes_view_second_page(rf, episode_list_view):
    EpisodeFactory.create_batch(16)
    request = rf.get(reverse('episodes'), {'page': 2})

    response = episode_list_view(request)

    assert response.status_code == 200
    assert response.context_data['is_paginated'] is True
    assert response.context_data['episodes'].count() == 1
