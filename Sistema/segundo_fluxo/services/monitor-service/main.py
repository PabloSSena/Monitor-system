from fastapi import FastAPI

from api.routes.router import router
from api.routes.websocket import websocketRouter
from rabbitmq.rabbitmq import init_rabbit, close_rabbit
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_rabbit(app)
    yield
    await close_rabbit(app)

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(websocketRouter)


