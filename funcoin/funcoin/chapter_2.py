import hashlib

input_bytes = b"bacjpack"

output = hashlib.sha256(input_bytes)

#print(output.hexdigest())

from hashlib import sha256

file = open("my_image.png", "rb")

hash = sha256(file.read()).hexdigest()
file.close()

#print(f"The hash of my file is: {hash}")

secret_phrase = "bolognese"

def get_hash_with_secret_phrase(input_data, secret_phrase):
    combined = input_data + secret_phrase
    return sha256(combined.encode()).hexdigest()

email_body = "Hey Bob, I think you should learn about blockchains!" \
    "I've been investing in Bitcoin and currently have exactly 12.03 BTC in my account."
    
print(get_hash_with_secret_phrase(email_body, secret_phrase))