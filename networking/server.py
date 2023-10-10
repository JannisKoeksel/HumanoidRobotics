import asyncio
from websockets.server import serve


class Server:
    
    def __init__(self,port:int, handler) -> None:
        self.handler = handler
        self.port = port
    

    async def runner(self,websocket):
        async for message in websocket:
            
            await websocket.send(message)

    async def start(self):
        async with serve(self.runner, "localhost", self.port):
            await asyncio.Future()  

