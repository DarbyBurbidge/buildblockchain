import json
import random

from datetime import datetime
from hashlib import sha256

class Blockchain(object):
    def __init__(self):
        self._chain = []
        self._pending_txns = []
        
        # Create genesis block
        print("generating genesis block")
        self._chain.append(self.new_block())
        
    def new_block(self, previous_hash=None):
        # Generates a new block and adds it to chain
        block = {
            "index": len(self._chain),
            "timestamp": datetime.utcnow().isoformat(),
            "transactions": self._pending_txns,
            "previous_hash": self.last_block["hash"] if self.last_block else None,
            "nonce": format(random.getrandbits(64), "x")
        }
        # Hash the new block and add it to the chain
        block_hash = self.hash(block)
        block["hash"] = block_hash
        
        # Reset list of pending_txns
        self._pending_txns = []
        # Add the block to the chain
        #self._chain.append(block)
        
        #print(f"Created block {block['index']}")
        return block
    
    @staticmethod
    def hash(block):
        # Ensure the dict is sorted or hashes will be inconsistent
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()
    
    @staticmethod
    def is_valid_hash(block):
        return block["hash"].startswith("0000")
    
    @property
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
        
    def proof_of_work(self):
        while True:
            new_block = self.new_block()
            if self.is_valid_hash(new_block):
                break
        
        self._chain.append(new_block)
        print("Found a new block: ", new_block)