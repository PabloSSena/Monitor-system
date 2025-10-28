from pymongo import MongoClient
import os

client=MongoClient(os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)

db = client.monitor_system

hosts_collection = db["hosts"]