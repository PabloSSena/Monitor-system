from pymongo import MongoClient


client=MongoClient("mongodb+srv://pablosena_db_user:KWi7Frw0Teq373NN@cluster0.qns5lfo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)

db = client.monitor_system

hosts_collection = db["hosts"]