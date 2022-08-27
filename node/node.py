import asyncio

from blockchain.blockchain import Blockchain
from blockchain.connections import ConnectionPool
from blockchain.peers import P2PProtocol
from blockchain.server import Server

# Instantiate Blockchain and our pool of peers
blockchain = Blockchain()
connection_pool = ConnectionPool()

 # Instantiate the server and attach our modules
server = Server(blockchain, connection_pool, P2PProtocol)

# Start the server


async def main():
    await server.listen()
    
asyncio.run(main())