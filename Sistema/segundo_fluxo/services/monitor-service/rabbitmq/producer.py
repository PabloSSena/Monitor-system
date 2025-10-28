import aio_pika
from .rabbitmq import get_channel, get_exchange

async def send_message(message: str):
    try:
        exchange = get_exchange()        
        msg = aio_pika.Message(body=message.encode())
        await exchange.publish(msg, routing_key='monitor_routing_key')
        
        return {"status": "enviado", "message": message}
    except Exception as e:
        return {"error": str(e)}