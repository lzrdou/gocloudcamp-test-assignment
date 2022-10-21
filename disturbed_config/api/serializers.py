from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers

from .models import Config, Service, ServiceConfig


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CustomServiceField(serializers.Field):
    def to_representation(self, value):
        return ServiceSerializer(value, many=True).data

    def to_internal_value(self, data):
        for item in data:
            try:
                if isinstance(item, bool):
                    raise TypeError
                Service.objects.get(slug=item)
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    f'slug of incorrect type={type(item).__name__}'
                )
        return data


class DetailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = (
            'name',
            'status'
        )


class ConfigListSerializer(serializers.ModelSerializer):
    service = CustomServiceField()

    class Meta:
        model = Config
        fields = (
            'id',
            'name',
            'service',
            'status'
        )


class ConfigSerializer(serializers.ModelSerializer):
    service = CustomServiceField()
    name = serializers.CharField()
    status = serializers.ChoiceField(
        choices=Config.CHOICES,
        allow_null=False,
    )

    class Meta:
        model = Config
        fields = (
            'name',
            'service',
            'status'
        )

    def _create_or_update(self, validated_data, instance):
        if instance is None:
            return Config.objects.create(**validated_data)
        return super().update(instance, validated_data)

    @transaction.atomic
    def _perform(self, validated_data, inst=None):
        services = validated_data.pop('service')
        config = self._create_or_update(validated_data, inst)
        services_id = [Service.objects.get(slug=slug).id for slug in services]
        if ServiceConfig.objects.filter(service__id__in=services_id).exists:
            ServiceConfig.objects.filter(service__id__in=services_id).delete()
        config.service.set(services_id)
        return config

    def create(self, validated_data):
        return self._perform(validated_data)

    def update(self, instance, validated_data):
        return self._perform(validated_data, instance)
