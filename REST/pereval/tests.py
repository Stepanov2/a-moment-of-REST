import os
from copy import deepcopy

from django.conf import settings
from django.test import TestCase
import requests
import json

from pereval.models import Added, User, Image, PEREVAL_PHOTO_UPLOAD_DIR
from pereval.views import PerevalViewSet

from rest_framework.test import APIRequestFactory
# Create your tests here.

class AnimalTestCase(TestCase):
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, 'pereval', 'test_data.json'), 'r', encoding='utf-8') as data:
            self.create_data = json.load(data)
        self.endpoint = "http://localhost:8000/api/products/"
        self.get_list = PerevalViewSet.as_view({'get': 'list'})
        self.get_details = PerevalViewSet.as_view({'get': 'retrieve'})
        self.post = PerevalViewSet.as_view({'post': 'create'})
        self.put = PerevalViewSet.as_view({'put': 'update'})
        self.patch = PerevalViewSet.as_view({'patch': 'partial_update'})

    def test_hello_world(self):

        self.assertEqual(1, 2 - 1)


    def test_create(self):
        factory = APIRequestFactory()
        data = deepcopy(self.create_data)
        # print(self.create_data['level'])

        # Первый отчёт
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        pereval_1 = Added.objects.get(pk=response.data['id'])

        # Второй отчёт от этого же пользователя с другой фамилией.
        data['user']['fam'] = "Другой"
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        pereval_2 = Added.objects.get(pk=response.data['id'])

        self.assert_(pereval_1.user == pereval_2.user)  # новый пользователь не создался
        self.assert_(pereval_1.user.fam == 'Другой') # но у пользователя поменялась фамилия

        # Теперь должен создаться новый пользователь.
        data['user']['email'] = 'different@email.com'
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        pereval_3 = Added.objects.get(pk=response.data['id'])
        self.assert_(pereval_3.user != pereval_2.user)

        # Удаляем все обязательные поля.
        data.pop('title')
        data.pop('add_time')
        data['user'].pop('email')
        data['coords'] = {}
        data.pop('images')
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        # print(response.data['message'])
        # print(len(response.data['message']))
        self.assert_(len(response.data['message']) == 5)  # This should rase 5 errors exactly.

        # пустой список картинок
        data = deepcopy(self.create_data)
        data['images'] = []
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        self.assert_(response.data['message']['non_field_errors'])

    def tearDown(self):
        """Removing all newly created images."""
        for image in Image.objects.all():
            full_path = os.path.join(settings.MEDIA_ROOT, str(image.path))
            os.remove(full_path)
