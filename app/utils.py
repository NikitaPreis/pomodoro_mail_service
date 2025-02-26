import asyncio
import json

import aio_pika
from aiokafka import AIOKafkaConsumer

from app.client import MailClient
from app.settings import Settings
from app.service import MailService


consumer: AIOKafkaConsumer = AIOKafkaConsumer(
    'email_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda message: json.loads(message.decode('utf-8')),
    # loop=asyncio.get_event_loop()
)


async def get_mail_service() -> MailService:
    return MailService(
        mail_client=MailClient(settings=Settings())
    )


async def consume_message():
    mail_service = await get_mail_service()
    await consumer.start()
    try:
        async for message in consumer:
            print(message)
            await mail_service.consume_mail(message.value)
    finally:
        await consumer.stop()
