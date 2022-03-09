import time
from urllib import parse

import requests
import re

from requests.utils import dict_from_cookiejar

username = ""
password = ""

href_patten = r"href='(.*)'"
# publicKeyModulus_patten = """<input id="publicKeyModulus" name="publicKeyModulus" value="(.+)" type="hidden">"""
# publicKeyExponent_patten = """<input id="publicKeyExponent" name="publicKeyExponent" value="(.+)" type="hidden">"""
headers = {
    "Accept-Encoding": "deflate",
    "Host": "10.10.9.9:8080",
    "Connection": "keep-alive",
    "User-Agent": r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Origin": "http://10.10.9.9:8080",
}


def link_to_net():
    sess = requests.Session()
    res1 = sess.get(r"http://123.123.123.123/")
    next_url = re.findall(href_patten, res1.text)
    assert next_url, "next_url is empty"
    print("next_url :: ", next_url[0])
    data = {
        "userId": username,
        "password": password,
        "service": "shu",
        "operatorPwd": "",
        "operatorUserId": "",
        "validcode": "",
        "passwordEncrypt": "false",
        "queryString": parse.quote_plus(next_url[0].split("?")[-1])
    }
    res2 = sess.get(next_url[0], headers=headers)
    cookies = res2.cookies
    cookie = dict_from_cookiejar(cookies)
    res3 = sess.post("http://10.10.9.9:8080/eportal/InterFace.do?method=login",
                     data=parse.urlencode(data),
                     headers=headers,
                     cookies=cookies)
    res3.encoding = "utf-8"
    res_data = res3.json()
    print(res_data)
    if res_data.get("result") == "success":
        print("联网成功！")
    else:
        print("联网失败！")
    # res = requests.get(next_url[0], headers=headers)
    # html = res.text
    # publicKeyExponent = re.findall(publicKeyExponent_patten, html)
    # publicKeyModulus = re.findall(publicKeyModulus_patten, html)
    # res.encoding = "GBK"
    # print(res.text)


if __name__ == '__main__':
    while True:
        if "10.10" in requests.get("http://baidu.com").text:
            print(time.time(), "网络连接异常，尝试连接校园网")
            link_to_net()
        else:
            print(time.time(), "网络连接正常")
        time.sleep(1)
