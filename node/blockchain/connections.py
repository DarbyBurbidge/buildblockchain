import structlog
from more_itertools import take

logger = structlog.getLogger(__name__)

class ConnectionPool:
    def __init__(self):
        self.connection_pool = dict()
    
    def broadcast(self, message):
        # Method to broadcast message to all peers
        for user in self.connection_pool:
            user.write(f"{message}".encode())
    
    @staticmethod
    def get_address_string(writer):
        # Get a peer's ip:port (address)
        ip = writer.address["ip"]
        port = writer.address["port"]
        return f"{ip}:{port}"
    
    def add_peer(self, writer):
        # Add a peer to the connection pool
        address = self.get_address_string(writer)
        self.connection_pool[address] = writer
        logger.info("Added new peer to pool", address=address)
    
    def remove_peer(self, writer):
        # Remove a peer from the connection pool
        address = self.get_address_string(writer)
        self.connection_pool.pop(address)
        logger.info("Removed peer from pool", address=address)
    
    def get_living_peers(self, count):
        # Return some connected peers
        # TODO (Reader): Sort these by most active, but for now just get the first *count* of them
        return take(count, self.connection_pool.items())
    