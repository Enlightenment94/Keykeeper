import sys
import math
from getpass import getpass
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Check if private key file and encrypted file are provided as command-line arguments
if len(sys.argv) < 3:
    print("Usage: python decrypt_file.py <private_key_file> <encrypted_file>")
    sys.exit()

private_key_file = sys.argv[1]
encrypted_file = sys.argv[2]

# Prompt the user to enter the passphrase
passphrase = getpass("Enter the passphrase for the private key: ")

# Load private key from file with passphrase
with open(private_key_file, "rb") as file:
    private_key = RSA.import_key(file.read(), passphrase=passphrase)

# Create cipher object using private key
cipher_rsa = PKCS1_OAEP.new(private_key)

# Open encrypted file and read its contents
with open(encrypted_file, "rb") as file:
    ciphertext = file.read()

size = 256 * 2
blocks = math.ceil(len(ciphertext)/size)
print(math.ceil(len(ciphertext)/size))

plaintext = b""
for i in range(blocks):
    start = i * size
    end = start + size
    block = ciphertext[start:end]
    plaintext += cipher_rsa.decrypt(block)

print (plaintext.decode())

print("File decrypted successfully.\n")