#!/usr/bin/python3

import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Check if passphrase is provided as command-line argument
if len(sys.argv) < 2:
    print("Passphrase key missing as command-line argument")
    sys.exit()

passphrase = sys.argv[1]

# Generate RSA key
key = RSA.generate(4096)

# Save private key to file with encryption
encrypted_private_key = key.export_key(passphrase=passphrase, pkcs=8,
                                       protection="scryptAndAES256-CBC")

with open("private_key.pem", "wb") as file:
    file.write(encrypted_private_key)

# Save public key to file
public_key = key.publickey().export_key()
with open("public_key.pem", "wb") as file:
    file.write(public_key)