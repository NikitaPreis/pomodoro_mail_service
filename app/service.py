import asyncio
from dataclasses import dataclass
import json

from aiokafka import AIOKafkaProducer

from app.client import MailClient
from app.schemas import UserMessageBody
from app.settings import Settings


settings = Settings()


event_loop = asyncio.get_event_loop()


producer = AIOKafkaProducer(
    bootstrap_servers=settings.BROKER_URL,
    loop=event_loop
)


@dataclass
class MailService:
    mail_client: MailClient

    async def consume_mail(self, message: dict):
        email_body = UserMessageBody(**message)
        correlation_id = email_body.correlation_id

        try:
            self.send_email(
                subject=email_body.subject,
                text=email_body.message,
                to=email_body.user_email
            )
            print('success')
        except Exception as e:
            await self.send_mail_fail_callback(
                email=email_body.user_email,
                correlation_id=correlation_id,
                exception=e
            )
            print(f'Exception: {e}')

    def send_email(self, subject, text, to):
        self.mail_client.send_email_task(
            subject=subject, text=text, to=to
        )

    async def send_mail_fail_callback(
        self, email: str, correlation_id: str, exception: Exception
    ) -> None:
        callback_email_data = {
            'exception': str(exception),
            'email': email,
            'correlation_id': correlation_id
        }
        encode_email_data = json.dumps(callback_email_data).encode()

        producer = AIOKafkaProducer(
            bootstrap_servers=settings.BROKER_URL,
            loop=event_loop
        )

        await producer.start()
        try:
            await producer.send(
                topic=settings.EMAIL_CALLBACK_TOPIC,
                value=encode_email_data
            )
        finally:
            await producer.close()

        print(f'error: {exception}')
