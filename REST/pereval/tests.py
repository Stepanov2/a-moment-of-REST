import os
from copy import deepcopy

from django.conf import settings
from django.test import TestCase
import json

from django.urls import reverse

from pereval.models import Added, Image, PEREVAL_POSSIBLE_STATUSES
from pereval.views import PerevalViewSet

from rest_framework.test import APIRequestFactory, APIClient
# Create your tests here.


class PerevalTestCase(TestCase):
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, 'pereval', 'test_data.json'), 'r', encoding='utf-8') as data:
            self.create_data = json.load(data)  # Эти данные копируются в каждый тест через deepcopy
        self.get_list = PerevalViewSet.as_view({'get': 'list'})
        self.get_details = PerevalViewSet.as_view({'get': 'retrieve'})
        self.post = PerevalViewSet.as_view({'post': 'create'})
        self.put = PerevalViewSet.as_view({'put': 'update'})
        self.patch = PerevalViewSet.as_view({'patch': 'partial_update'})

    def test_create(self):
        """Проверяем POST"""
        factory = APIRequestFactory()
        data = deepcopy(self.create_data)

        # Создаём первый отчёт.
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        pereval_1 = Added.objects.get(pk=response.data['id'])

        # Второй отчёт от этого же пользователя с другой фамилией.
        data['user']['fam'] = "Другой"
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        pereval_2 = Added.objects.get(pk=response.data['id'])

        self.assert_(pereval_1.user == pereval_2.user)  # новый пользователь не создался
        self.assert_(pereval_1.user.fam == 'Другой')  # но у пользователя поменялась фамилия

        # Теперь должен создаться новый пользователь.
        data['user']['email'] = 'different@email.com'
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        pereval_3 = Added.objects.get(pk=response.data['id'])
        self.assert_(pereval_3.user != pereval_2.user)

        # Удаляем из запроса все обязательные поля.
        data.pop('title')
        data.pop('add_time')
        data['user'].pop('email')
        data['coords'] = {}
        data.pop('images')
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        self.assert_(len(response.data['message']) == 5)  # This should raise 5 errors exactly.

        # пустой список картинок
        data = deepcopy(self.create_data)
        data['images'] = []
        request = factory.post('/submitData/', data, format='json')
        response = self.post(request)
        self.assert_(response.data['message']['non_field_errors'])

    def test_update(self):
        """Проверяем PATCH и PUT"""
        factory = APIRequestFactory()
        data = deepcopy(self.create_data)

        # Создаём два поста и берём их id.
        request = factory.post('/submitData/', data, format='json')
        put_id = self.post(request).data['id']

        request = factory.post('/submitData/', data, format='json')
        patch_id = self.post(request).data['id']

        # Меняем все возможные значения в данных запроса.
        for key, value in data.items():
            if isinstance(value, str) and key != 'add_time':
                data[key] += 'aaaa'
            if value is None:
                data[key] = 'some'

        for key, value in data['level'].items():
            data['level'][key] = '1-Б'

        for key, value in data['coords'].items():
            data['coords'][key] -= 50

        cleaned_data = deepcopy(data)

        # Убираем из запроса информацию о user и картинках.
        cleaned_data.pop('user')
        cleaned_data.pop('images')

        # Делаем PUT
        client = APIClient()
        url = reverse('added-detail', kwargs={'pk': put_id})

        response_put = client.put(url, cleaned_data, format='json')
        self.assert_(response_put.status_code == 200)

        # Делаем PATCH по одному полю за раз.
        url = reverse('added-detail', kwargs={'pk': patch_id})
        for key, _ in cleaned_data.items():
            response = client.patch(url, {key: cleaned_data[key]}, format='json')
            self.assert_(response.status_code == 200)

        # Проверяем, что данные в базе совпадают с данными в запросе
        pereval_put = Added.objects.get(pk=put_id)
        pereval_patch = Added.objects.get(pk=patch_id)
        for key, value in cleaned_data.items():
            if key not in ('add_time', 'coords', 'level'):  # todo Надо получать данные от сериализатора, а не от модели
                self.assert_(value == pereval_put.__dict__[key], msg=f'{key}: {value}, {pereval_put.__dict__[key]}')
                self.assert_(value == pereval_patch.__dict__[key], msg=f'{key}: {value}, {pereval_patch.__dict__[key]}')

        # Проверяем, что нельзя исправить перевал, который взяли в работу
        for i in range(1, 4):
            pereval_patch.status = PEREVAL_POSSIBLE_STATUSES[i][0]
            pereval_patch.save()
            response = client.patch(url, {'title': 'Новое'}, format='json')
            self.assert_(response.status_code == 400)

    def tearDown(self):
        """Removing all newly created images."""
        for image in Image.objects.all():
            full_path = os.path.join(settings.MEDIA_ROOT, str(image.path))
            os.remove(full_path)
