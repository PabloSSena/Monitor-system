import asyncio
import websockets
import json

async def run_client():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as ws:
        # Solicita monitoramento do Google
        await ws.send(json.dumps({"cmd": "monitor", "host": "google.com"}))
        
        # Fica recebendo mensagens do servidor
        async for msg in ws:
            data = json.loads(msg)
            print(f"Status: {data['host']} TCP={data['tcp']} ")
    await asyncio.Future()
if __name__ == "__main__":
    asyncio.run(run_client())
