
raw_data = "c7cc3e0fe41f7fd7b812f87653a8c3b25f9d1f54fe6dd40dd12cddd435c38692"
bytes_ = bytes.fromhex(raw_data)
iv = bytes_[:16]
ciphertext = bytes_[16:]
int_cipher = int.from_bytes(ciphertext, 'big')
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

key = open("/challenge/.key", "rb").read()
cipher = AES.new(key=key, mode=AES.MODE_CBC)
ciphertext = cipher.iv + cipher.encrypt(pad(b"sleep", cipher.block_size))

print(f"TASK: {ciphertext.hex()}")