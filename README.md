# WebTronicsTestTask

## Тестовое задание WebTronics

### Установка и настройка

1. Склонируйте репозиторий при помощи команды `git clone https://github.com/meetinger/WebTronicsTestTask` 
и перейдите в директорию репозитория
2. Установите виртуальное окружение(venv или conda) Python(рекомендую установить Python 3.10,
   т.к. на 3.11 есть проблемы с отображением стека вызовов FastAPI,
   [GitHub Issue](https://github.com/tiangolo/fastapi/issues/5740))
3. Установите нужные зависимости `pip install -r requirements.txt`
4. Установите контейнеры docker `docker-compose up -d`
   (перед этим проверьте конфигурацию контейнеров в файле `docker-compose.yml`,
   если у Вас уже заняты те или иные параметры(порты, имена контейнеров) тогда измените их)
    1. В случае того, если Вы изменили конфигурацию `docker-compose.yml`, отредактируйте
       файл `core/settings.py` в соответствии с изменёнными параметрами
5. В файле `core/settings.py` измените параметр `ROOT_URL` в соответствии с вашим IP-адресом или доменом
6. Примените миграции для базы данных `alembic upgrade head`
7. Запустите сервер из корня репозитория при помощи команды `uvicorn main:app --host 0.0.0.0`
    1. Если Вы хотите запустить сервер на другом порте, то команда будет следующей:
       `uvicorn main:app --host 0.0.0.0 --port <номер порта>`

### Тестирование API

1. Из корня репозитория запустите команду `pytest tests/`
2. Для того чтобы посмотреть покрытие кода тестами(на момент написания README 95%), команда будет следующей:
   `pytest --cov=../ tests/`

### Задания из Google-Формы

1. Юнит-тесты для функции:

```python
async def logs(cont, name):
    conn = aiohttp.UnixConnector(path="/var/run/docker.sock")
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(f"http://xx/containers/{cont}/logs?follow=1&stdout=1") as resp:
            async for line in resp.content:
                print(name, line)
```

Находятся в директории `form_tasks/unittests`

2. Эндпоинты для кодирования URL находятся в директории `form_tasks/endpoints`

### Замечания по поводу моего кода

1. В структуре БД была применена примесь `db/models/mixins_models.py`, что в будущем позволит легко добавить возможность
   реакций для других сущностей
2. В задании с юнит-тестами для функции логов докера были применены костыли в связи с тем,
   что в исходной функции у line не был вызван метод `.decode()`
3. В задании с эндпоинтом для кодирования URL я сделал два эндпоинта GET и POST


### Бонусная секция:
1. https://hunter.io/ не верифицирует webmail, так что делать проверку с помощью этого сервиса бессмысленно
Модуль с клиентом на aiohttp Вы можете найти по пути `core/utils/hunter_io.py` (токен, найденный на GitHub прилагается)
2. https://clearbit.com/ также не ищет людей с webmail адресами, так что нет смысла интегрировать этот сервис
Модуль с клиентом на aiohttp Вы можете найти по пути `core/utils/clearbit_com.py` (токены, найденные на GitHub прилагаются)
# P.S. Репозиторий не мёртв на данный момент, я буду продолжать делать бонусную секцию)
