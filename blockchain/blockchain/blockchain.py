import json

from datetime import datetime
from hashlib import sha256

class Blockchain(object):
    def __init__(self):
        self._chain = []
        self._pending_txns = []
        
        # Create genesis block
        print("generating genesis block")
        self.new_block()
        
    def new_block(self, previous_hash=None):
        # Generates a new block and adds it to chain
        block = {
            "index": len(self._chain),
            "timestamp": datetime.utcnow().isoformat(),
            "transactions": self._pending_txns,
            "previous_hash": previous_hash
        }
        block_hash = self.hash(block)
        block["hash"] = block_hash
        
        # Reset list of pending_txns
        self._pending_txns = []
        # Add the block to the chain
        self._chain.append(block)
        
        print(f"Created block {block['index']}")
        return block
    
    @staticmethod
    def hash(block):
        # Ensure the dict is sorted or hashes will be inconsistent
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()
    
    def last_block(self):
        # Gets the latest block in the chain if there is one
        return self._chain[-1] if self._chain else None
    
    def new_txn(self, sender, receiver, amt):
        # Adds a new txn to the list of pending_txns
        self._pending_txns.append({
            "receiver": receiver,
            "sender": sender,
            "amount": amt
        })