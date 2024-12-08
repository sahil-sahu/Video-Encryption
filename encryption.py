from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
import time
import base64

class RSA_Hybrid_Encryptor:
    def key_create(self, key_size=2048):
        """Generate a new RSA key pair."""
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    def key_write(self, key, key_name):
        """Write an RSA key to a file."""
        with open(key_name, 'wb') as key_file:
            key_file.write(key)

    def key_load(self, key_name):
        """Load an RSA key from a file."""
        with open(key_name, 'rb') as key_file:
            key = key_file.read()
        return key
    
    def aes_key_generate(self, public_key):
        rsa_public_key = RSA.import_key(public_key)
        rsa_cipher = PKCS1_OAEP.new(rsa_public_key)
        aes_key = get_random_bytes(16)  # 256-bit key
        encrypted_key = rsa_cipher.encrypt(aes_key)
        return base64.b64encode(encrypted_key).decode('utf-8'), aes_key
    def Decrypt_aes_key(self, private_key, encrypted_key_str):
        rsa_private_key = RSA.import_key(private_key)
        rsa_cipher = PKCS1_OAEP.new(rsa_private_key)
        encrypted_key = base64.b64decode(encrypted_key_str)

        # Decrypt the AES key using RSA
        aes_key = rsa_cipher.decrypt(encrypted_key)
        return aes_key

    # def hybrid_encrypt(self, public_key, original_file, encrypted_file):
    #     """Encrypt a file using hybrid encryption (RSA + AES)."""
    #     rsa_public_key = RSA.import_key(public_key)
    #     rsa_cipher = PKCS1_OAEP.new(rsa_public_key)

    #     # Generate a random AES key
    #     aes_key = get_random_bytes(32)  # 256-bit key
    #     aes_cipher = AES.new(aes_key, AES.MODE_CBC)
    #     iv = aes_cipher.iv

    #     # Start encryption timing
    #     start_time = time.time()

    #     with open(original_file, 'rb') as file:
    #         original = file.read()

    #     # Encrypt file data using AES
    #     encrypted_data = aes_cipher.encrypt(pad(original, AES.block_size))

    #     # Encrypt AES key using RSA
    #     encrypted_key = rsa_cipher.encrypt(aes_key)

    #     # Save the encrypted AES key and IV at the beginning of the encrypted file
    #     with open(encrypted_file, 'wb') as file:
    #         file.write(encrypted_key + iv + encrypted_data)

    #     # Stop encryption timing
    #     encryption_time = time.time() - start_time

    #     # Calculate file size metrics
    #     original_size = os.path.getsize(original_file)
    #     encrypted_size = os.path.getsize(encrypted_file)
    #     file_size_overhead = ((encrypted_size - original_size) / original_size) * 100

    #     return encryption_time,original_size,encrypted_size,file_size_overhead

    # def hybrid_decrypt(self, private_key, encrypted_file, decrypted_file):
    #     """Decrypt a file using hybrid encryption (RSA + AES)."""
    #     rsa_private_key = RSA.import_key(private_key)
    #     rsa_cipher = PKCS1_OAEP.new(rsa_private_key)

    #     with open(encrypted_file, 'rb') as file:
    #         # Read the encrypted AES key
    #         encrypted_key = file.read(256)  # 2048 bits = 256 bytes
    #         iv = file.read(16)  # AES block size for IV
    #         encrypted_data = file.read()

    #     # Decrypt the AES key using RSA
    #     aes_key = rsa_cipher.decrypt(encrypted_key)

    #     # Decrypt the file data using AES
    #     aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)

    #     # Start decryption timing
    #     start_time = time.time()

    #     decrypted_data = unpad(aes_cipher.decrypt(encrypted_data), AES.block_size)

    #     with open(decrypted_file, 'wb') as file:
    #         file.write(decrypted_data)

    #     # Stop decryption timing
    #     decryption_time = time.time() - start_time

    #     return decryption_time

# Example usage
if __name__ == "__main__":
    rsa_encryptor = RSA_Hybrid_Encryptor()

    # File paths
    # original_file = "Interstellar.mkv"
    # encrypted_file = "enc_Interstellar.mkv"
    # decrypted_file = "dec_Interstellar.mkv"
    private_key_file = "rsa_private_key.pem"
    public_key_file = "rsa_public_key.pem"

    # Generate and write keys if not already created
    if not (os.path.exists(private_key_file) and os.path.exists(public_key_file)):
        private_key, public_key = rsa_encryptor.key_create()
        rsa_encryptor.key_write(private_key, private_key_file)
        rsa_encryptor.key_write(public_key, public_key_file)
    else:
        private_key = rsa_encryptor.key_load(private_key_file)
        public_key = rsa_encryptor.key_load(public_key_file)
    # Encrypt the file and measure performance
    # enc_time, orig_size, enc_size, overhead = rsa_encryptor.hybrid_encrypt(public_key, original_file, encrypted_file)
    # print("Hybrid Encryption Metrics:")
    # print(f"Encryption Time: {enc_time:.4f} seconds")
    # print(f"Original File Size: {orig_size} bytes")
    # print(f"Encrypted File Size: {enc_size} bytes")
    # print(f"File Size Overhead: {overhead:.2f}%")

    # # Decrypt the file and measure performance
    # dec_time = rsa_encryptor.hybrid_decrypt(private_key, encrypted_file, decrypted_file)
    # print("Hybrid Decryption Metrics:")
    # print(f"Decryption Time: {dec_time:.4f} seconds")