# Generated by Django 4.1.2 on 2022-10-20 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('status', models.CharField(choices=[('A', 'active'), ('S', 'stopped')], max_length=128, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Конфигурация',
                'verbose_name_plural': 'Конфигурации',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Сервис',
                'verbose_name_plural': 'Сервисы',
            },
        ),
        migrations.CreateModel(
            name='ServiceConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.config', verbose_name='Конфигурация')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.service', verbose_name='Сервис')),
            ],
            options={
                'verbose_name': 'Конфигурация сервиса',
                'verbose_name_plural': 'Конфигурации рецептов',
            },
        ),
        migrations.AddField(
            model_name='config',
            name='service',
            field=models.ManyToManyField(through='api.ServiceConfig', to='api.service', verbose_name='Сервис'),
        ),
        migrations.AddConstraint(
            model_name='serviceconfig',
            constraint=models.UniqueConstraint(fields=('service', 'config'), name='service_config_unique'),
        ),
    ]
