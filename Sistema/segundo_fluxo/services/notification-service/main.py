from fastapi import FastAPI
from dotenv import load_dotenv
from rabbitmq.consumer import start_consumer, stop_consumer
from contextlib import asynccontextmanager
from telegram_service.telegram_register import start_bot
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_bot()
    await start_consumer()
    yield
    await stop_consumer()

app = FastAPI(lifespan=lifespan)



