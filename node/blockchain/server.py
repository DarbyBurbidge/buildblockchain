import asyncio
from asyncio import StreamReader, StreamWriter

import structlog
from marshmallow.exceptions import MarshmallowError

from blockchain.messages import BaseSchema
from blockchain.utils import get_external_ip

logger = structlog.getLogger()


class Server:
    def __init__(self, blockchain, connection_pool, p2p_protocol):
        self.blockchain = blockchain
        self.connection_pool = connection_pool
        self.p2p_protocol = p2p_protocol
        self.external_ip = None
        self.external_port = None
        
        if not (blockchain and connection_pool and p2p_protocol):
            logger.error("'blockchain', 'connection_pool', and 'gossip_protocol' must all be instantiated")
            raise Exception("Could not start")
    
    async def get_external_ip(self):
        # Finds our external IP so we can advertize it
        self.external_ip = await get_external_ip()
        logger.info(f"Saved external IP: {self.external_ip}")

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        # Called when a new connection is received
        # the 'writer' is the connecting peer
        
        while True:
            try:
                # Handle/Reply to incoming data
                data = await reader.readuntil(b"\n")
                decoded_data = data.decode("utf-8").strip()
                
                try:
                    message = BaseSchema().loads(decoded_data)
                except MarshmallowError:
                    logger.info("received unreadable message", peer=writer)
                    break
                
                # Extract the address from the message amd add it to the writer
                writer.address = message["meta"]["address"]
                
                # Add peer to the connection_pool
                self.connection_pool.add_peer(writer)
                
                # Handle the message
                await self.p2p_protocol.handle_message(message, writer)
                
                await writer.drain()
                if writer.is_closing():
                    break
                
            except (asyncio.exceptions.IncompleteReadError, ConnectionError):
                # An error happened, break out of loop
                break
        
        # Connection is closed, Loop has ended
        writer.close()
        await writer.wait_closed()
        self.connection_pool.remove_peer(writer)
    
    async def listen(self, hostname="0.0.0.0", port=8888):
        # This listen method spawns the server
        
        server = await asyncio.start_server(self.handle_connection, hostname, port)
        
        logger.info(f"Server listening on {hostname}:{port}")
        
        await self.get_external_ip()
        self.external_port = port
        async with server:
            await server.serve_forever()