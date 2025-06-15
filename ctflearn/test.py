raw = """
 2e6e7770 6c6c6f63 7b656765 484c4330
 7a695975 6e666c44 5a6f4b53 4c775977
 61554268 2e6e4949 4e544e64 4d697778
 4d6a6332 577a4579 00000a7d
"""
raw = raw.replace(" ","").replace("\n","")
print(raw)
raw = bytes.fromhex(raw)
print(raw)
print(raw.decode("latin1",errors="ignore")[::-1])