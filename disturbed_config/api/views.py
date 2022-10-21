from rest_framework import status, viewsets
from rest_framework.response import Response
from reversion.views import RevisionMixin

from .models import Config, Service, ServiceConfig
from .serializers import (ConfigSerializer, ConfigListSerializer,
                          DetailConfigSerializer, ServiceSerializer)


class ServiceViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'slug'


class ConfigViewSet(RevisionMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ConfigSerializer

    def destroy(self, request, *args, **kwargs):
        config = self.get_object()
        if ServiceConfig.objects.filter(config=config).exists():
            return Response(
                {'Невозможно удалить конфигурацию, которая '
                 'используется сервисами'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            config.delete()
        except Exception as e:
            return Response(
                {f'Не удалось удалить конфигурацию, ошибка:{e}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = Config.objects.all()
        service_f = self.request.query_params.get('service')
        if service_f:
            queryset = queryset.filter(config__service__slug=service_f)
        return queryset

    def get_serializer_class(self):
        if 'service' in self.request.query_params:
            return DetailConfigSerializer
        elif self.action == 'list':
            return ConfigListSerializer
        return ConfigSerializer
