import asyncio
import socket
import websockets
import json
from typing import Dict

# -------------------------
# Funções utilitárias
# -------------------------

async def tcp_check(host: str, port: int = 443, timeout: float = 3.0) -> bool:
    """
    Verifica se a porta TCP do host está aberta.
    Retorna True se conseguiu conectar, False caso contrário.
    """
    loop = asyncio.get_running_loop()

    def _connect():
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False

    return await loop.run_in_executor(None, _connect)


# -------------------------
# Monitor de hosts
# -------------------------

async def monitor_host(ws, host: str, interval: int = 5):
    """
    Monitora um host periodicamente e envia status via WebSocket.
    """
    print(f"[+] Task de monitoramento criada para {host} (intervalo {interval}s)")
    while True:
        up_tcp = await tcp_check(host)
        payload = {
            "host": host,
            "tcp": up_tcp,
        }
        try:
            await ws.send(json.dumps(payload))
        except websockets.ConnectionClosed:
            print(f"[!] Conexão fechada, parando monitor de {host}")
            break
        await asyncio.sleep(interval)


# -------------------------
# Handler de WebSocket
# -------------------------

async def handler(ws):
    """
    Recebe comandos do cliente para monitorar hosts.
    Permite enviar hosts em momentos separados:
    {"cmd": "monitor", "host": "google.com", "interval": 5}
    """
    monitor_tasks: Dict[str, asyncio.Task] = {}

    try:
        while True:
            msg = await ws.recv()
            req = json.loads(msg)
            print(f"[+] Mensagem recebida: {req}")

            cmd = req.get("cmd")
            if cmd != "monitor":
                await ws.send(json.dumps({"error": "comando invalido"}))
                continue
            
            host = req.get("host")
            interval = req.get("interval", 5)
            if not host:
                await ws.send(json.dumps({"error": "nenhum host fornecido"}))
                continue

            if host in monitor_tasks:
                await ws.send(json.dumps({"info": f"{host} ja está sendo monitorado"}))
                continue

            # Cria uma task de monitoramento
            task = asyncio.create_task(monitor_host(ws, host, interval))
            monitor_tasks[host] = task
            await ws.send(json.dumps({"info": f"Iniciando monitoramento de {host}"}))

    except websockets.ConnectionClosed:
        print("[!] Cliente desconectou, cancelando tasks...")
        for host, task in monitor_tasks.items():
            task.cancel()
        monitor_tasks.clear()
    except Exception as e:
        print(f"[ERRO] {e}")
        for task in monitor_tasks.values():
            task.cancel()
        monitor_tasks.clear()


# -------------------------
# Servidor principal
# -------------------------

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("[*] Servidor WebSocket rodando em ws://localhost:8765")
        await asyncio.Future()  # loop infinito

if __name__ == "__main__":
    asyncio.run(main())
