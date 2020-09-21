# coding: utf-8

import requests
from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import pad
import pprint
import urllib3


def result_decrypt():
    key = 'wxtdefgabcdawn12'.encode("utf-8")
    aes = AES.new(key, AES.MODE_ECB)
    aes_str = '{"typeId":"","source":"0","pageIndex":29,"pageSize":40}'
    res = pad(aes_str.encode('utf-8'), AES.block_size, style='pkcs7')
    encrypt_aes = aes.encrypt(res)
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8').replace('\n', '')
    # 请求数据
    headers = {
        'Cookie': 'JSESSIONID=9f4cd5b4-a19c-4edc-b30d-fd43c3f915c9; Domain=.aliyizhan.com; Path=/; HttpOnly',
        'Content-Type': 'application/wxt;charset=UTF-8',
        'Content-Length': '88',
        'Host': 'gz.aliyizhan.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.11.0',
    }
    print(encrypted_text)
    data = "%s" % encrypted_text
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    res = requests.post("https://gz.aliyizhan.com/market/getMarketArchivesMouths.action?marketCode=gz", headers=headers,
                        data=data, verify=False).text
    aes_str = base64.b64decode(res)
    aes = AES.new(key, AES.MODE_ECB)
    res1 = aes.decrypt(aes_str)
    res2 = res1.decode(encoding='utf-8')
    res3 = res2.replace('\r', '').replace('\n', '')
    pprint.pprint(res3)


result_decrypt()
