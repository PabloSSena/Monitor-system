import aio_pika
from emails.email import send_email
from app import send_message
from telegram_service.telegram_notifier import send_notification

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f"Mensagem recebida: {message.body.decode()}")
        await send_notification(message.body.decode())
        # send_email('pablosilvasena@gmail.com', 'Nova Mensagem Recebida', f'<strong>{message.body.decode()}</strong>')
        # send_message()

async def start_consumer():
    global connection, channel, queue
    
    try:
        connection = await aio_pika.connect_robust("amqp://monitor:monitor@localhost/")
        channel = await connection.channel()
        
        exchange = await channel.declare_exchange(
            "monitor_exchange",
            aio_pika.ExchangeType.DIRECT,
            durable=True
        )
        
        queue = await channel.declare_queue(
            "monitor_queue",
            durable=True, 
        )
        
        await queue.bind(exchange,routing_key="monitor_routing_key") 
        
        await queue.consume(process_message)
        
        print("Consumidor iniciado e aguardando mensagens...")
    
    except Exception as e:
        print(f"Erro ao iniciar consumidor: {e}")


async def stop_consumer():
    global connection
    
    if connection:
        await connection.close()
        print("Consumidor encerrado")