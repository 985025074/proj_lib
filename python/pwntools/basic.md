<!-- 基本样板 -->
```py
import pwn

from pwnlib.tubes import ssh
import logging

shell = pwn.ssh('hacker', host="pwn.college", keyfile="~/key", )
# logging.info("success ssh!")
# run process

process_challenge = shell.process("/challenge/pwntools-tutorials-level1.1")
assert isinstance(process_challenge,ssh.ssh_process)
# wait here until things
while True:
    data = process_challenge.recv(timeout=1)
    if data==b"":
        break
    print(data.decode("utf-8"))
# read is over
print("read is over")
final_bytes = b'p' + (0x15).to_bytes() + (123456789).to_bytes(4,"little")+b"Bypass Me:)"
process_challenge.sendline(final_bytes)

try:
    while True:
        data = process_challenge.recv(timeout=5)
        if data=="":
            break
        print(data.decode("utf-8"))
except EOFError:
    print("program ends.")

```
# ssh 负责链接，process 负责进成通信,p1632可以包裹数字
# 记得加上conext 影响汇编表现：
context(arch="amd64", os="linux", log_level="info")

# pwntools 重定向：
```py
import pwn
import os
def main():
    fd = os.open("/tmp/wmzcob",os.O_RDONLY)
    p = pwn.process(["/challenge/run","plefmckxwa"],env={"gsizpd":"tmkvmfzsik"},stdin=fd)
    p.interactive()
    while True:
        try:
            data = p.recvline()
            print(data.decode())
        except:
            break
main()

```


## 特殊重定向
stdin=PIPE 意思是让其他人来作为管道