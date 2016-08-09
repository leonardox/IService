# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class IserviceUser(User):
    """
    This class represents a system user.
    """

    name = models.CharField(max_length=100)
    picture = models.CharField(null=True, max_length=150)
    favorites_services = models.ManyToManyField('Service')

    def add_favorite_service(self, service):
        """
        This functions adds a service into favorite list.
        """
        self.favorites_services.add(service)

    @staticmethod
    def create_user(**kwargs):
        """
        This fuction inserts an user on database.
        :param kwargs:
        :return: User instance.
        """
        user = IserviceUser()
        if 'name' in kwargs:
            user.name = kwargs['name']
        if 'email' in kwargs:
            user.email = kwargs['email']
            user.username = user.email
        if 'picture' in kwargs:
            user.picture = kwargs['picture']
        if 'password' in kwargs:
            user.set_password(kwargs['password'])

        user.save()

        if 'phone' in kwargs:
            for phone_number in kwargs['phone']:
                phone = PhoneNumber(phone=str(phone_number), user=user, service=None)
                phone.save()

        return user


class State(models.Model):
    """
    This class represents a state.
    """
    uf = models.CharField(max_length=2)
    name = models.CharField(max_length=20)


class City(models.Model):
    """
    This class represents a city
    """
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State)


class Service(models.Model):
    """
    This class represents a Iservice Service.
    """
    ALIMENTACAO = "ALIMENTACAO"
    ANIMAIS = "ANIMAIS"
    AULAS = "AULAS"
    AUTOMOTIVO = "AUTOMOTIVO"
    BELEZA_E_BEM_ESTAR = "BELEZA_E_BEM_ESTAR"
    CASA_E_CONSTRUCAO = "CASA_E_CONSTRUCAO"
    COMUNICACAO_E_ARTES = "COMUNICACAO_E_ARTES"
    CONSULTORIA = "CONSULTORIA"
    DELIVERY = "DELIVERY"
    EVENTOS_E_MUSICA = "EVENTOS_E_MUSICA"
    SAUDE = "SAUDE"
    TECNOLOGIA = "TECNOLOGIA"
    TRANSPORTE = "TRANSPORTE"
    SEGURANCA = "SEGURANCA"
    OUTROS = "OUTROS"

    CATEGORIES = (
        (ALIMENTACAO, ("Alimentação")),
        (ANIMAIS, ("Animais")),
        (AULAS, ("Aulas")),
        (AUTOMOTIVO, ("Automotivo")),
        (BELEZA_E_BEM_ESTAR, ("Beleza e bem-estar")),
        (CASA_E_CONSTRUCAO, ("Casa e construção")),
        (COMUNICACAO_E_ARTES, ("Comunicação e artes")),
        (CONSULTORIA, ("Consultoria")),
        (DELIVERY, ("Delivery")),
        (EVENTOS_E_MUSICA, ("Eventos e Música")),
        (SAUDE, ("Saúde")),
        (TECNOLOGIA, ("Tecnologia")),
        (TRANSPORTE, ("Transporte")),
        (SEGURANCA, ("Segurança")),
        (OUTROS, ("Outros"))
    )

    name = models.CharField(max_length=60)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(IserviceUser)
    category = models.CharField(max_length=60, choices=CATEGORIES)
    city_db = models.ForeignKey(City)

    @staticmethod
    def create_service(**kwargs):
        """
        This fuction inserts a service on database.
        :param kwargs:
        :return: Service instance.
        """
        service = Service()
        if 'name' in kwargs:
            service.name = kwargs['name']
        if 'description' in kwargs:
            service.description = kwargs['description']
        if 'user' in kwargs:
            service.user = kwargs['user']
        if 'category' in kwargs:
            service.category = kwargs['category']

        if 'city' in kwargs and 'state' in kwargs and 'uf' in kwargs:
            try:
                state_data = State.objects.get(name=kwargs['state'])
            except State.DoesNotExist:
                state_data = _save_new_state(kwargs['uf'], kwargs['state'])
            try:
                city_data = City.objects.get(name=kwargs['city'], state=state_data)
                service.city_db = city_data
            except City.DoesNotExist:
                service.city_db = _save_new_city(state_data, kwargs['city'])

        service.save()

        if 'phones' in kwargs:
            for phone_number in kwargs['phones']:
                phone = PhoneNumber(phone=str(phone_number), user=None, service=service)
                phone.service = service
                phone.save()

        if 'tags' in kwargs:
            for tag in kwargs['tags']:
                tag_db = Tag(tag=tag, service=service)
                tag_db.save()

        return service


class PhoneNumber(models.Model):
    """
    This class is a phone from an user or a service.
    """
    phone = PhoneNumberField(null=True)
    user = models.ForeignKey(IserviceUser, null=True)
    service = models.ForeignKey(Service, null=True)


class Tag(models.Model):
    """
    This class is a tag from a service.
    """
    tag = models.CharField(max_length=50)
    service = models.ForeignKey(Service, null=True)


def _save_new_city(state, city):
    """
    This function adds a new city into database.
    """
    city = City(name=city, state=state)
    city.save()
    return city


def _save_new_state(uf, state):
    """
    This function adds a new state into database.
    """
    state = State(uf=uf.upper(), name=state)
    state.save()
    return state
