# coding=utf-8
# @Time : 2018/1/2 9:47
# @Author : 李飞
import requests
import time, json
import hmac
from hashlib import sha1
from PIL import Image
import os


def getg(time):
    key = 'd1b964811afb40118a12068ff74a12f4'
    h1 = hmac.new(key.encode('utf-8'), ''.encode('utf-8'), sha1)
    h1.update("password".encode('utf-8'))
    h1.update("c3cef7c66a1843f8b3a9e6a1e3160e20".encode('utf-8'))
    h1.update("com.zhihu.web".encode('utf-8'))
    h1.update(time.encode('utf-8'))
    h1.hexdigest()
    return h1.hexdigest()


Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
header = {
    'host': 'www.zhihu.com',
    'User-Agent': Agent,
    'Referer': 'https://www.zhihu.com/',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
}
session = requests.session()

captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
response = session.get(captcha_url, headers=header, verify=False)

show_captcha = json.loads(response.text)['show_captcha']
if not show_captcha:
    captcha = ''
else:
    with open('captcha.jpg', 'wb') as f:
        f.write(response.content)
        f.close()
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
t = str(int(time.time() * 1000))
form_data = {
    'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
    'grant_type': 'password',
    'timestamp': t,
    'source': 'com.zhihu.web',
    'signature': getg(t),
    'username': '+myusername',
    'password': 'mypassword',
    'captcha': captcha,
    'lang': 'en',
    'ref_source': 'homepage',
    'utm_source': 'baidu',
}
login_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
result = session.post(login_url, data=form_data, headers=header, verify=False)
print(result)
