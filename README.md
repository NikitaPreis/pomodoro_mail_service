# pomodoro_mail_service

### Описание

Проект «pomodoro_mail_service » — это микросервис, реализующий отправку сообщений на почту. Сервис слушает брокер сообщений (RabbitMQ) и отправляет email по протоколу SMTP на основе задания, полученного из брокера (SMTP + Яндекс Почта, RabbitMQ + Microservice).

### Стек:

* Python
* FastAPI
* Pydantic
* RabbitMQ
* aio-pika


### Ссылка на core сервис:

Основной сервис с полной инструкцией по тому, как развернуть проект, находится по ссылке (HTTPS):
* https://github.com/NikitaPreis/pomodoro-tracker.git


### Как развернуть проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git@github.com:NikitaPreis/pomodoro_mail_service.git
cd pomodoro_mail_service
```

Создать и активировать виртуальное окружение:
```
# Команды для Windows
python -m venv .venv
source venv/Scripts/activate
```

Установить зависимости:
```
pip install -r requirements.txt
```

Установить переменные окружения в файле .env:
```
FROM_EMAIL=<your.sender.email.yandex.ru>
SMTP_PORT=465
SMTP_HOST=smtp.yandex.ru
SMTP_PASSWORD=<your.special.yandex.email.password.for.app>
```

Запустить сервис:
```
python -m app.main
```

**ВАЖНО:** убедитесь, что брокер сообщений (RabbitMQ) запущен с корретными учетными данными. Кроме того, убедитесь, что producer-service, подключен к RabbitMQ и использует корретный топики.

### Направления для доработки:
1. Настроить алертинг;
2. Провести рефакторинг, чтобы отвязать методы сервиса от семантической связи с конкретными брокером сообщений (RabbitMQ);
3. Вынести названия очередей в константы для удобства дальнейшего деплоя;
4. Подготовить тесты (unit, component, integration).
