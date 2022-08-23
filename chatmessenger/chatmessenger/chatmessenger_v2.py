import asyncio
from textwrap import dedent

class ConnectionPool:
    def __init__(self):
        self.connection_pool = set()
        
    def send_welcome_message(self, writer):
        """
        Sends Welcome Message to new connected client
        Args:
            writer (_type_): new client
        """
        message = dedent(f"""
        ===
        Welcome {writer.nickname}!
        
        There are {len(self.connection_pool) - 1} user(s) here beside you
        
        Help:
         - Type anything to chat
         - /list will list all connected users
         - /quit will disconnect you
        ===
        """)
        
        writer.write(f"{message}\n".encode())
    
    def broadcast(self, writer, message):
        """
        Broadcasts a general message to the entire pool
        Args:
            writer (_type_): client sender
            message (_type_): message to broadcast
        """
        for user in self.connection_pool:
            if user != writer:
                # We don't need to also broadcast to the user sending the message
                user.write(f"{message}\n".encode())
    
    def broadcast_user_join(self, writer):
        """
        Calls broadcast method with a "user joined" message
        Args:
            writer (_type_): client that joined
        """
        self.broadcast(writer, f"{writer.nickname} just joined")
    
    def broadcast_user_quit(self, writer):
        """
        Calls the broadcast method with a "user quitting" message
        Args:
            writer (_type_): client that quit
        """
        self.broadcast(writer, f"{writer.nickname} just left")
    
    def broadcast_user_message(self, writer, message):
        """
        Calls the broadcast method with a user's chat message
        Args:
            writer (_type_): client sender
            message (_type_): user's message
        """
        self.broadcast(writer, f"[{writer.nickname}]: {message}")
    
    def list_users(self, writer):
        """
        Lists all users in the pool
        Args:
            writer (_type_): client requesting all users
        """
        message = "===\n"
        message += "Currently connected users:"
        for user in self.connection_pool:
            if user == writer:
                message += f"\n - {user.nickname} (you)"
            else:
                message += f"\n - {user.nickname}"
                
        message += "\n==="
        writer.write(f"{message}\n".encode())
    
    def add_new_user_to_pool(self, writer):
        """
        Adds new user to existing pool of clients
        Args:
            writer (_type_): client to add
        """
        self.connection_pool.add(writer)
        
    def remove_user_from_pool(self, writer):
        """
        Removes an existing user from the pool
        Args:
            writer (_type_): client to remove
        """
        self.connection_pool.remove(writer)
        
async def handle_connection(reader, writer):
    """

    Args:
        reader (_type_): _description_
        writer (_type_): _description_
    """
    writer.write("> Choose your nickname: ".encode())
    
    response = await reader.readuntil(b"\n")
    writer.nickname = response.decode().strip()
    connection_pool.add_new_user_to_pool(writer)
    connection_pool.send_welcome_message(writer)
    
    # Announce new user
    connection_pool.broadcast_user_join(writer)
    
    while True:
        try:
            data = await reader.readuntil(b"\n")
        except asyncio.exceptions.IncompleteReadError:
            connection_pool.broadcast_user_quit(writer)
            break
        message = data.decode().strip()
        if message == "/quit":
            connection_pool.broadcast_user_quit(writer)
            break
        elif message == "/list":
            connection_pool.list_users(writer)
        else:
            connection_pool.broadcast_user_message(writer, message)
        
        await writer.drain()
    
        if writer.is_closing():
            break
    
    # We're now outside the message loop, the user has quit. Cleanup...
    writer.close()
    await writer.wait_closed()
    connection_pool.remove_user_from_pool(writer)
        
async def main():
    server = await asyncio.start_server(handle_connection, "0.0.0.0", 8888)
    
    async with server:
        await server.serve_forever()
        
connection_pool = ConnectionPool()

asyncio.run(main())
        