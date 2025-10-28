import aio_pika
from fastapi import FastAPI

rabbit_conn = None
rabbit_channel = None

async def init_rabbit(app: FastAPI):
    global rabbit_conn, rabbit_channel
    rabbit_conn = await aio_pika.connect_robust(
        "amqp://monitor:monitor@localhost/"
    )
    rabbit_channel = await rabbit_conn.channel()
    print("✓ Conectado ao RabbitMQ")

async def close_rabbit(app: FastAPI):
    global rabbit_conn
    if rabbit_conn:
        await rabbit_conn.close()
        print("✓ Desconectado do RabbitMQ")

def get_channel():
    return rabbit_channel