import asyncio
import logging
from fastapi import WebSocket
from utils.tcp_check import tcp_check
from rabbitmq.producer import send_message
logger = logging.getLogger(__name__)

async def monitor_host(websocket: WebSocket, host: str, interval: int = 5):
    logger.info(f"Iniciando monitoramento de {host}")
    
    try:
        while True:
            up_tcp = await tcp_check(host)
            print('up_tcp', up_tcp)
            await websocket.send_json({
                "host": host,
                "tcp": up_tcp,
            })
            if(up_tcp == False):
                await send_message(f'{host}')
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        logger.info(f"Monitoramento de {host} cancelado")
    except Exception as e:
        logger.error(f"Erro em monitor_host({host}): {e}")