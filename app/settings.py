import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AMQP_URL: str = 'amqp://guest:guest@localhost:5672//'

    FROM_EMAIL: str = ''
    SMTP_PORT: int = 456
    SMTP_HOST: str = 'smtp.yandex.ru'
    SMTP_PASSWORD: str = ''

settings = Settings()
