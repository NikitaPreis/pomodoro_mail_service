import aio_pika

from app.client import MailClient
from app.settings import Settings
from app.service import MailService


async def get_amqp_connection() -> aio_pika.abc.AbstractConnection:
    settings = Settings()
    return await aio_pika.connect_robust(settings.amqp_url)


async def get_mail_service() -> MailService:
    return MailService(
        mail_client=MailClient(settings=Settings())
    )


async def make_amqp_consumer():
    mail_service = await get_mail_service()
    connection = await get_amqp_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue('mail_queue', durable=True)
    await queue.consume(mail_service.consume_mail)
