from tokenize import cookie_re

import requests

from requests import *
url = 'http://127.0.0.1:8787/dar/user/login'

content_type = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}


data = {
"user_name": "test01",
"passwd": "admin123"
}

res = requests.post(url=url , data=data, headers=content_type)

print(res.text)
#
# print(type(res.text))
#
# print(res.json())

seesion = requests.session()
res2 = seesion.request(method='post' ,url=url, data=data, headers=content_type)

cookie = requests.utils.dict_from_cookiejar(res2.cookies)

print(cookie)
print(res2.text
      )

