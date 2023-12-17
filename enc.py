import sys
import math
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Check if public key file and input file are provided as command-line arguments
if len(sys.argv) < 3:
    print("Usage: python enc.py <public_key_file> <input_file>")
    sys.exit()

public_key_file = sys.argv[1]
input_file = sys.argv[2]

# Load public key from file
with open(public_key_file, "rb") as file:
    public_key = RSA.import_key(file.read())

# Generate a cipher object using the public key
cipher_rsa = PKCS1_OAEP.new(public_key)

# Open the input file and read its contents
with open(input_file, "rb") as file:
    plaintext = file.read()

blocks = math.ceil(len(plaintext)/256)
print(math.ceil(len(plaintext)/256))

encrypted_file = input_file
with open(encrypted_file, "wb") as file:
    for i in range(blocks):
        start = i * 256
        end = start + 256
        block = plaintext[start:end]
        encrypted_block = cipher_rsa.encrypt(block)
        file.write(encrypted_block)

print("File encrypted successfully.")