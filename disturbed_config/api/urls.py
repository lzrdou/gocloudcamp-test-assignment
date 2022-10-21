from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ConfigViewSet, ServiceViewSet

app_name = 'api'

router = SimpleRouter()

router.register('services', ServiceViewSet, basename='services')
router.register('configs', ConfigViewSet, basename='configs')

urlpatterns = [
    path('', include(router.urls)),
]
