from dataclasses import dataclass
import json

import aio_pika

from app.client import MailClient
from app.schemas import UserMessageBody


@dataclass
class MailService:
    mail_client: MailClient

    async def consume_mail(self, message: aio_pika.IncomingMessage):
        async with message.process():
            email_body = UserMessageBody(**json.loads(message.body.decode()))
            correlation_id = message.correlation_id

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
        from app.utils import get_amqp_connection

        connection = await get_amqp_connection()
        channel = await connection.channel()
        message = aio_pika.Message(
            body=f'User email: {email} failed with exception: {exception}'.encode(),
            correlation_id=correlation_id,
        )
        await channel.default_exchange.publish(
            message=message,
            routing_key='callback_mail_queue'
        )
