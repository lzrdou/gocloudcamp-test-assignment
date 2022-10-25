import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Config, Service, ServiceConfig


class ServiceTests(APITestCase):
    def test_create_service(self):
        url = reverse('api:services-list')
        data = {'name': 'test name', 'slug': 'test-slug'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(Service.objects.get().name, 'test name')
        self.assertEqual(Service.objects.get().slug, 'test-slug')

    def test_get_service(self):
        Service.objects.create(name='test name', slug='test-slug')
        url_get = reverse('api:services-detail', args=['test-slug'])
        data = {'name': 'test name', 'slug': 'test-slug'}
        response = self.client.get(url_get)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_patch_service(self):
        Service.objects.create(name='test name', slug='test-slug')
        url_patch = reverse('api:services-detail', args=['test-slug'])
        data_patch = {'name': 'patched_name'}
        response = self.client.patch(url_patch, data_patch, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Service.objects.get(slug='test-slug').name,
            'patched_name'
        )

    def test_delete_service(self):
        Service.objects.create(name='test name', slug='test-slug')
        self.assertEqual(Service.objects.count(), 1)
        url_delete = reverse('api:services-detail', args=['test-slug'])
        response = self.client.delete(url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Service.objects.count(), 0)


class ConfigTests(APITestCase):
    def test_create_config(self):
        Service.objects.create(name='test name 1', slug='first-slug')
        Service.objects.create(name='test name 2', slug='second-slug')
        url = reverse('api:configs-list')
        data = {
            'name': 'test name',
            'service': [
                'first-slug',
                'second-slug'
            ],
            'status': 'A'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Config.objects.count(), 1)
        self.assertEqual(ServiceConfig.objects.count(), 2)
        self.assertEqual(Config.objects.get().name, 'test name')
        self.assertEqual(Config.objects.get().status, 'A')

    def test_get_config(self):
        Service.objects.create(name='test name 1', slug='first-slug')
        Config.objects.create(
            name='test name', status='A'
        )
        ServiceConfig.objects.create(service_id=1, config_id=1)
        url = reverse('api:configs-list') + '?service=first-slug'
        data = {'name': 'test name', 'status': 'A'}
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(json.dumps(response.data))[0], data)

    def test_patch_config(self):
        Service.objects.create(name='test name 1', slug='first-slug')
        Service.objects.create(name='test name 2', slug='second-slug')
        Config.objects.create(
            name='test name', status='A'
        )
        ServiceConfig.objects.create(service_id=1, config_id=1)
        url_patch = reverse('api:configs-detail', args=[1])
        data_patch = {
            "name": "patched name",
            "service": [
                'second-slug'
            ],
            "status": "S"
        }
        response = self.client.patch(url_patch, data_patch, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        config = Config.objects.get(id=1)
        self.assertEqual(config.name, data_patch['name'])
        self.assertEqual(config.status, data_patch['status'])
        self.assertFalse(
            ServiceConfig.objects.filter(
                service_id=1, config_id=1).exists()
        )
        self.assertTrue(
            ServiceConfig.objects.filter(
                service_id=2, config_id=1).exists()
        )

    def test_delete_config(self):
        Service.objects.create(name='test name 1', slug='first-slug')
        Config.objects.create(
            name='test name', status='A'
        )
        ServiceConfig.objects.create(service_id=1, config_id=1)
        url_delete = reverse('api:configs-detail', args=[1])
        response = self.client.delete(url_delete)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        Service.objects.get(slug='first-slug').delete()
        response = self.client.delete(url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
