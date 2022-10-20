from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ServiceViewSet, ConfigViewSet

app_name = 'api'

router = SimpleRouter()

router.register('services', ServiceViewSet, basename='services')
router.register('config', ConfigViewSet, basename='config')

urlpatterns = [
    path('', include(router.urls)),
]
