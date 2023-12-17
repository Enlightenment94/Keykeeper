import tkinter as tk
import os
import subprocess
import math
from getpass import getpass
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def dec(private_key_file, encrypted_file, passphrase):
	with open(private_key_file, "rb") as file:
	    private_key = RSA.import_key(file.read(), passphrase=passphrase)

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

	return plaintext

def enc(public_key_file, plaintext, input_file):
	# Load public key from file
	with open(public_key_file, "rb") as file:
	    public_key = RSA.import_key(file.read())

	# Generate a cipher object using the public key
	cipher_rsa = PKCS1_OAEP.new(public_key)

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

def list_files(folder):
    files = os.listdir(folder)
    for file in files:
        if file.endswith('.txt'):
            listbox.insert(tk.END, file)

def show_file_content(entry):
	selected_file = listbox.get(tk.ACTIVE)
	file_path = selected_file
	with open(file_path, 'rb') as f:
		content = f.read()

		pharsekey = entry.get()
		content = dec("private_key.pem", file_path, pharsekey)

		text.delete('1.0', tk.END)
		text.insert(tk.END, content)

def button_click(text):
	selected_file = listbox.get(tk.ACTIVE)
	area = text.get("1.0", "end-1c").rstrip()
	encoded_bytes = area.encode()
	enc("public_key.pem", encoded_bytes, selected_file)

root = tk.Tk()
root.title("Keykeeper")

entry = tk.Entry(root, show="*")
entry.pack()

listbox = tk.Listbox(root)
listbox.pack()

text = tk.Text(root)
text.pack()

selected_folder = os.getcwd()  # Aktualny folder roboczy
entry.insert(tk.END, "")
list_files(selected_folder)

listbox.bind('<<ListboxSelect>>', lambda event: show_file_content(entry))

button = tk.Button(root, text="Save", command=lambda: button_click(text))
button.pack()

root.mainloop()