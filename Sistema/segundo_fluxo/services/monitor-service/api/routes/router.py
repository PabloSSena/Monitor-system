from fastapi import APIRouter
from models.hosts import Hosts
from config.database import hosts_collection
from schemas.schemas import list_serial
from bson import ObjectId

router = APIRouter()

@router.get('/')
async def get_hosts():
    hosts = list_serial(hosts_collection.find())
    return hosts

@router.post('/')
async def create_hosts(host:Hosts):
    hosts_collection.insert_one(dict(host))



