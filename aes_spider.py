# coding: utf-8

import json
import re
import pymysql
import requests
from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import pad
import pprint
import urllib3


def encrypt_data():
    # 得到加密表单
    key = 'wxtdefgabcdawn12'.encode("utf-8")
    aes = AES.new(key, AES.MODE_ECB)
    for i in range(30):
        aes_str = '{"typeId":"","source":"0","pageSize":40,"pageIndex":%d}' % i
        res = pad(aes_str.encode('utf-8'), AES.block_size, style='pkcs7')
        encrypt_aes = aes.encrypt(res)
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8').replace('\n', '')
        # 请求数据
        headers = {
            'Cookie': 'JSESSIONID=8b5942cc-1f4f-4b85-9bf8-78a1297276f8; Domain=.aliyizhan.com; Path=/; HttpOnly',
            'Content-Type': 'application/wxt;charset=UTF-8',
            'Content-Length': '88',
            'Host': 'gz.aliyizhan.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0',
        }
        data = "%s" % encrypted_text
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        res = requests.post("https://gz.aliyizhan.com/market/getMarketArchivesMouths.action?marketCode=gz",
                            headers=headers,
                            data=data, verify=False).text
        # pprint.pprint(res)
        yield res


def result_decrypt(res):
    key = 'wxtdefgabcdawn12'.encode("utf-8")
    aes_str = base64.b64decode(res)
    aes = AES.new(key, AES.MODE_ECB)
    res1 = aes.decrypt(aes_str)
    res2 = res1.decode(encoding='utf-8')
    res3 = res2.replace('\r', '').replace('\n', '')
    res4 = '{' + re.search('\{(.*?)success', res3, re.S).group(1) + 'success":true}'
    res5 = json.loads(res4)
    for store_info in res5['data']:
        store_info_dict = {}
        store_info_dict['houseNumber'] = store_info['houseNumber']
        store_info_dict['wxNumber'] = store_info['wxNumber']
        store_info_dict['phone'] = store_info['phone']
        pprint.pprint(store_info_dict)

        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root",
                               database="gong_xiang_hy",
                               charset="utf8mb4")
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO gxhy (houseNumber, wxNumber, phone) VALUE ('%s','%s','%s')"
            base = (store_info_dict['houseNumber'], store_info_dict['wxNumber'], store_info_dict['phone'])
            cursor.execute(sql % base)
            conn.commit()
        except:
            conn.rollback()
        conn.close()


def main():
    res_list = encrypt_data()
    for res in res_list:
        result_decrypt(res)


if __name__ == '__main__':
    main()
