import socket
import asyncio

async def tcp_check(host: str, port: int = 80, timeout: float = 5) -> bool:
    port = port 
    timeout = timeout or 5
    
    loop = asyncio.get_running_loop()
    
    def _connect():
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False
    
    return await loop.run_in_executor(None, _connect)