import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FROM_EMAIL: str = ''
    SMTP_PORT: int = 456
    SMTP_HOST: str = 'smtp.yandex.ru'
    SMTP_PASSWORD: str = ''

    BROKER_URL: str = 'localhost:9092'
    EMAIL_CALLBACK_TOPIC: str = 'callback_email_topic'

settings = Settings()
