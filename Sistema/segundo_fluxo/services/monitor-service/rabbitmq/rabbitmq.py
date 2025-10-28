import aio_pika
from fastapi import FastAPI

rabbit_conn = None
rabbit_channel = None
exchange = None

async def init_rabbit(app: FastAPI):
    global rabbit_conn, rabbit_channel, exchange
    rabbit_conn = await aio_pika.connect_robust(
        "amqp://monitor:monitor@localhost/"
    )
    rabbit_channel = await rabbit_conn.channel()
    print("✓ Conectado ao RabbitMQ")
    exchange = await rabbit_channel.declare_exchange(
        'monitor_exchange', 
        aio_pika.ExchangeType.DIRECT, 
        durable=True,
        passive=False
    )
    queue = await rabbit_channel.declare_queue('monitor_queue', durable=True, passive=True)
    await queue.bind(exchange, 'monitor_routing_key')

async def close_rabbit(app: FastAPI):
    global rabbit_conn
    if rabbit_conn:
        await rabbit_conn.close()
        print("✓ Desconectado do RabbitMQ")

def get_channel():
    return rabbit_channel

def get_exchange():
    return exchange 