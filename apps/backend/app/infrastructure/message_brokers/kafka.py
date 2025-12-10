# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from collections.abc import AsyncGenerator
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from orjson import orjson

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    async def start(self) -> None:
        await self.producer.start()
        await self.consumer.start()

    async def close(self) -> None:
        await self.consumer.stop()
        await self.producer.stop()

    async def send_message(self, key: str, topic: str, value: bytes) -> None:
        await self.producer.send(topic, key=key, value=value)

    async def start_consuming(self, topic: str) -> AsyncGenerator:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self) -> None:
        self.consumer.unsubscribe()
