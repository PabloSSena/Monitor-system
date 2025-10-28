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
    list_of_hosts =list_hosts(hosts_collection.find())
    for host in list_of_hosts:
        task = asyncio.create_task(monitor_host(websocket, host, 5))
        monitor_tasks[host] = task    
    
    try:
        while True:
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        logger.info("Cliente desconectou")
        for task in monitor_tasks.values():
            task.cancel()

@websocketRouter.get("/", response_class=HTMLResponse)
async def get_index():
    with open("app/templates/index.html") as f:
        return f.read()