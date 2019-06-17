import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

from podcast.models import Episode


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')


class EpisodeFactory(DjangoModelFactory):
    class Meta:
        model = Episode

    length = factory.Faker('time_delta')
    short_description = factory.Faker('sentence', nb_words=12)
    title = factory.Faker('sentence', nb_words=3)
    user = factory.SubFactory(UserFactory)
