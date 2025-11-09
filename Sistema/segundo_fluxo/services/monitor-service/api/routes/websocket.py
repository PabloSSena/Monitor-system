import json
import logging
from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from schemas.schemas import list_hosts
from services.monitor import monitor_host
import asyncio
logger = logging.getLogger(__name__)
from config.database import hosts_collection

websocketRouter = APIRouter()

@websocketRouter.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    monitor_tasks: Dict[str, asyncio.Task] = {}
    try:
        while True:
            current_hosts = set(list_hosts(hosts_collection.find()))
            existing_hosts = set(monitor_tasks.keys())
            new_hosts = current_hosts - existing_hosts
            for host in new_hosts:
                if host not in monitor_tasks:
                    task = asyncio.create_task(monitor_host(websocket, host, 5))
                    monitor_tasks[host] = task
                    logger.info(f"Novo host adicionado: {host}")
            
            removed_hosts =  existing_hosts - current_hosts
            for host in removed_hosts:
                if host in monitor_tasks:
                    monitor_tasks[host].cancel()
                    await monitor_tasks[host]
                    del monitor_tasks[host]
                    logger.info(f"Host removido: {host}")        

            await asyncio.sleep(10)

    except WebSocketDisconnect:
        logger.info("Cliente desconectou")
        for task in monitor_tasks.values():
            task.cancel()

@websocketRouter.get("/", response_class=HTMLResponse)
async def get_index():
    with open("app/templates/index.html") as f:
        return f.read()