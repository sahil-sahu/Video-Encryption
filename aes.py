from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Generate a random key
key = get_random_bytes(16)  # AES-128, for AES-192 use 24 bytes, for AES-256 use 32 bytes

# Create a cipher object
cipher = AES.new(key, AES.MODE_EAX)

# Encrypt some data
data = b'Hello, World!'
# print(list(data).tobytes())
nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(data)

print(f'Ciphertext: {list(ciphertext)}')

# Decrypt the data
cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)

try:
    cipher.verify(tag)
    print(f'The message is authentic: {plaintext}')
except ValueError:
    print('Key incorrect or message corrupted')
