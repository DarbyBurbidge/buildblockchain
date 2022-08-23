from hashlib import sha256

alices_message = "Hello Bob, Let's meet at the Kruger National Park on 2020-12-12 at 1pm.n"

alices_hash = "39aae6ffdb3c0ac1c1cc0f50bf08871a729052cf1133c4c9b44a5bab8fb66211"

hash_message = sha256(("p@55w0rd" + alices_message).encode()).hexdigest()

if hash_message == alices_hash:
    # print("Message has not been tampered with")
    pass
else:
    # print("Message does not match hash!")
    pass
    
    
from nacl.public import PrivateKey, Box

# Generate secret keys for Alice and Bob

alices_priv_key = PrivateKey.generate()
bobs_priv_key = PrivateKey.generate()

# Public keys are generated from private keys
alices_pub_key = alices_priv_key.public_key
bobs_pub_key = bobs_priv_key.public_key

# Bob sends Alice a message
# This means he makes a Box with his private key and alices public key
bobs_box = Box(bobs_priv_key, alices_pub_key)

# Encrypt Bob's secret message (bytes)
encrypted = bobs_box.encrypt(b"I am Satoshi")

# Alice creates a second box
alices_box = Box(alices_priv_key, bobs_pub_key)

# Alice now decrypts Bobs message
plaintext = alices_box.decrypt(encrypted)
# print(plaintext.decode('utf-8'))


import nacl.encoding
import nacl.signing

# Generate a new key-pair for Bob
bobs_private_key = nacl.signing.SigningKey.generate()
bobs_public_key = bobs_private_key.verify_key

# Since it's bytes, we'll need to serialize the key to a readable format before publishing
bobs_public_key_hex = bobs_public_key.encode(encoder=nacl.encoding.HexEncoder)

# Now let's sign a message
signed = bobs_private_key.sign(b"Send $37 to Alice")

print(bobs_public_key_hex)
print(signed)

# From the above
verify_key = nacl.signing.VerifyKey(bobs_public_key_hex, encoder=nacl.encoding.HexEncoder)

# Attempt to verify
print(verify_key.verify(signed).decode())