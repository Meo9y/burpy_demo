import re
from urllib.parse import unquote, quote
import base64
import binascii
from Crypto.Cipher import AES
import hashlib
class Burpy:
    def __init__(self):
        self.key = 'BjSRk7WJw4ErxyQh'
    def _md5(self,str):
        return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()
    def encrypt(self, header, body):
        print(body)
        a = re.findall('name="myyz"\r\n(.*?)\r\n------WebKitFormBoundary0rOsspCdbIl6fzHy',body)
        print(a)
        b = re.findall(r'timestamp=(.*?)&',body)
        c = re.findall(r'sign=(.*)',body)
        md5 = '1qaz2wsx'+str(a[0])+str(b[0])
        cc = self._md5(md5)
        body = body.replace(c[0], cc)
        return header, body

    def decrypt(self, header, body):
        return header, body