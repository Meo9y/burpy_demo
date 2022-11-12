import base64
import re
from urllib.parse import unquote

from Crypto.Cipher import AES

BLOCK_SIZE = AES.block_size
# 不足BLOCK_SIZE的补位(s可能是含中文，而中文字符utf-8编码占3个位置,gbk是2，所以需要以len(s.encode())，而不是len(s)计算补码)
pad = lambda s: s + (BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE)
# 去除补位
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class Burpy:
    '''
    header is dict
    body is string
    '''

    def __init__(self):
        self.key = 'GbhJQUqFIZRmmGZc'  # 密钥
        self.iv = "AAAAAAAAAAAAAAAA"  # 偏移量
        self.BLOCK_SIZE = AES.block_size
        # 不足BLOCK_SIZE的补位(s可能是含中文，而中文字符utf-8编码占3个位置,gbk是2，所以需要以len(s.encode())，而不是len(s)计算补码)
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s.encode()) % self.BLOCK_SIZE) * chr(
            self.BLOCK_SIZE - len(s.encode()) % self.BLOCK_SIZE)
        # 去除补位
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def _aes_decode(self, data):
        encrypted_text = base64.b64decode(data)
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_CBC, IV=self.iv.encode())
        decrypted_text = cipher.decrypt(encrypted_text)
        #return unpad(decrypted_text).decode('utf-8')
        return decrypted_text.decode('utf-8').rstrip('\x00')
    def _aes_encode(self, data):
        # text = pad(text) 包pycrypto的写法，加密函数可以接受str也可以接受bytess
        text = pad(data).encode()  # 包pycryptodome 的加密函数不接受str
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_CBC, IV=self.iv.encode())
        encrypted_text = cipher.encrypt(text)
        # 进行64位的编码,返回得到加密后的bytes，decode成字符串
        return base64.b64encode(encrypted_text).decode('utf-8')

    def encrypt(self, header, body):
        '''
        正则处理提取出加密部分
        '''
        if 'P' in body:
            data = re.findall(r'"P":"(.*)"', body)[0]
            #print(data)
            data2 = self._aes_encode(data)
            print(data2)
            body = body.replace(data, data2)
            '''
        if 'account' in body:
            data3 = re.findall(r'account":"(.*?)"', body)[0]
            #print(data)
            data4 = self._aes_encode(data3)
            print(data2)
            body = body.replace(data3, data4)
            '''
        return header, body

    def decrypt(self, header, body):
        if '{' in body:
            data = re.findall(r'"P":"(.*?)"', body)[0]
            #print(data)
            data = unquote(data)
            #print(data)
            data2 = str(self._aes_decode(data))
            #print('123' + data2)
            body = body.replace(data, data2)
        if '{' not in body:
            data = re.findall(r'"(.*?)"', body)[0]
            #print(data)
            data = unquote(data)
            #print(data)
            data2 = str(self._aes_decode(data))
            #print('123' + data2)
            body=data2
            #body = body.replace(data, data2)
        # print(body)
        return header, body

'''
if __name__ == '__main__':
    #body = 'oNo0a9QRLE1jw0lLlcF3jA=='
    body='{"P":"m7C484esMPAyzCYVfCmgeurTVWGU6BbVU/xMG3vvURI="}'
    header = '123'
    burp = Burpy()
    a = burp.decrypt(header,body)
    print(a)
'''