from django.db import models


class Service(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=64,
        verbose_name='Slug',
        unique=True
    )

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return f'{self.name}'


class Config(models.Model):
    CHOICES = (
        ('A', 'active'),
        ('S', 'stopped')
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Название'

    )
    service = models.ManyToManyField(
        Service,
        through='ServiceConfig',
        verbose_name='Сервис'
    )
    status = models.CharField(
        max_length=128,
        choices=CHOICES,
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Конфигурация'
        verbose_name_plural = 'Конфигурации'

    def __str__(self):
        return f'{self.name}'


class ServiceConfig(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Сервис'
    )
    config = models.ForeignKey(
        Config,
        on_delete=models.CASCADE,
        verbose_name='Конфигурация'
    )

    class Meta:
        verbose_name = 'Конфигурация сервиса'
        verbose_name_plural = 'Конфигурации рецептов'
        constraints = [
            models.UniqueConstraint(
                name='service_config_unique',
                fields=['service', 'config']
            )
        ]

    def __str__(self):
        return f'{self.service} {self.config}'
