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
    ## To-do:Loop infinito de monitoramento
    ## To-do: Checar status TCP
    ## To-do:: Construir payload JSON (corpo a enviar para o cliente) 
    ## To-do: Enviar resultado via WebSocket
    ## To_do: Tratar exceção de conexão fechada
    ## To-do: Aguardar intervalo antes de nova checagem


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

        #To-do: Loop infinito para receber mensagens do cliente
            #To-do: Aguardar mensagem do cliente
            #To-do: Parsear JSON
            #To-do: Validar comando
            #To-do: Extrair host e intervalo
            #To-do: Monitorar sistema
            # Cria uma task de monitoramento
    #To-do: Tratar exceção de conexão fechada



# -------------------------
# Servidor principal
# -------------------------

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("[*] Servidor WebSocket rodando em ws://localhost:8765")
        await asyncio.Future()  # loop infinito

if __name__ == "__main__":
    asyncio.run(main())
