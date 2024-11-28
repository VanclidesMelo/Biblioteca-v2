import factory
from django.contrib.auth.models import User
from .models import Colecao


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class ColecaoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Colecao

    nome = factory.Sequence(lambda n: f"Coleção {n}")
    colecionador = factory.SubFactory(UserFactory)
