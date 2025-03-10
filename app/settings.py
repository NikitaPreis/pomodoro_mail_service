from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TESTING: str = 'False'
    AMQP_URL: str = 'amqp://guest:guest@rabbitmq:5672//'

    FROM_EMAIL: str = ''
    SMTP_PORT: int = 456
    SMTP_HOST: str = 'smtp.yandex.ru'
    SMTP_PASSWORD: str = ''

    @property
    def amqp_url(self):
        if self.TESTING == 'True':
            return 'amqp://guest:guest@localhost:5672//'
        return 'amqp://guest:guest@rabbitmq:5672//'

settings = Settings()
