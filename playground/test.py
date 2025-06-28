# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pycrypto",
# ]
# ///
def int_to_bytes(integer:int):
    return integer.to_bytes(1, 'big')
def bytes_to_int(byte_data:bytes):
    return int.from_bytes(byte_data, 'big')

# for every byte
from Crypto.Utils.strxor import strxor
test_byte = b"ab"
temp = 1
result_byte = 0
for i in range(7):
    byte_temp = int_to_bytes(temp)
