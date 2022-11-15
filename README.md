# Тестовое задание для Sber GoCloudCamp

## Distributed config
### Описание:
API для динамической конфигурации сервисов, реализованное на Django Rest Framework, в качестве базы данных подключена PostgreSQL.\
Используются две основные модели: Service и Config, а также модель ServiceConfig для m2m связи.\
У модели Service два поля: название и слаг, слаг является уникальным. У модели Config - название, сервис и статус. Сервис - m2m поле, ссылается на сервис. Состояние указывает на статус сервиса (active, stopped).\
Один конфиг может использоваться для нескольких сервисов, для этого при создании конфига или при его изменении в поле service необходимо добавить дополнительный слаг сервиса.\
Удаление конфига возможно только если он не используется никаким сервисом (поле service пусто).\
Фильтрация конфигов по сервисам, которые их используют возможна через передачу в запрос слага сервиса. Пример: ```http://localhost/api/configs?service=test1``` .\
Версионность конфигов реализована с помощью библиотеки django-reversion и плагина django-reversion-compare. Для просмотра прошлых версий необходимо зайти в админ-панель и перейти во вкладу Versions.

### Запуск:
#### 1. Скопировать проект на компьютер, перейти в папку disturbed_config.

- Создать файл ```.env``` и добавить в него следующие строки (в проде .env файл копируем на сервер с помощью GitHub workflow):
```
SECRET_KEY='#85r+v$gtn@yt*yzmewwtv)0dz(ohb2gj9ae1e=^ket5p*n6!x'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
- Выполнить команду для сборки:\
```docker-compose up -d```

#### 2. После сборки проекта в контейнеры выполнить миграции, создать начальные объекты версий, создать суперпользователя, собрать статику:

- ```docker-compose exec api python manage.py migrate```
- ```docker-compose exec api python manage.py createinitialrevisions```
- ```docker-compose exec api python manage.py createsuperuser```
- ```docker-compose exec api python manage.py collectstatic --no-input```

#### 3. Доступные эндпоинты:

- ```http://localhost/api/services/``` - POST, GET, DELETE, UPDATE запросы для сервисов. В качестве параметра для получения информации для конкретного сервиса передается слаг.
- ```http://localhost/api/configs/``` - POST, GET, DELETE, UPDATE. В качестве параметра для получения информации для конкретного конфига передается айди.
- ```http://localhost/admin/``` - админ-панель.
- ```http://localhost/swagger/``` - документация.

### Примеры запросов:
POST http://localhost/api/services/
```
{
    "name": "first test service",
    "slug": "test1"
}
```
POST http://localhost/api/configs/
```
{
    "name": "stopped test config",
    "service": [
        "test1",
        "test2"
    ],
    "status": "S"
}
```
PATCH http://localhost/api/configs/1/
```
{
    "name": "updated test config",
    "service": [
        "test2",
    ],
    "status": "A"
}
```
