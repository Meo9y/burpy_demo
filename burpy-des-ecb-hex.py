import re
import base64
import binascii
from Crypto.Cipher import DES
import hashlib
#from pyDes import des, PAD_PKCS5, ECB

class Burpy:
    '''
    header is dict
    body is string
    '''

    def __init__(self):
        '''
        here goes some code that will be kept since "start server" clicked, for example, webdriver, which usually takes long time to init
        '''
        self.key = 'SZBank@9'
        #self.iv = '01234567'
        self.mode = DES.MODE_ECB
    def _md5(self,str):
        return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()

    def main(self, header, body):
        return header, body

    def _des_decode(self, data, key):
        try:
            #des = DES.new(str.encode(key),DES.ECB,str.encode(self.iv))
            des = DES.new(str.encode(key),DES.MODE_ECB)
            decrypted_text = des.decrypt(binascii.a2b_hex(bytes(data, encoding='utf8'))).decode("utf8")

            decrypted_text = decrypted_text[0:-ord(decrypted_text[-1])]
        except Exception as e:
            pass
        return decrypted_text

   
    def _des_encode(self, data, key):
        while len(data) % 8 != 0:
            data += (8 - len(data) % 8) * chr(8 - len(data) % 8)
        data = str.encode(data)
        #des = DES.new(str.encode(key), DES.ECB,str.encode(self.iv))
        des = DES.new(str.encode(key), DES.MODE_ECB)
        return str(binascii.b2a_hex(des.encrypt(data)), encoding='utf8').replace('\n', '')
    
    '''
    def _des_encode_bak(self, data, key):
        length=8 - (len(data) % 8)
        if length != 0:
            data = data + chr(length)*length
        data = str.encode(data)
        des = DES.new(str.encode(key), DES.MODE_ECB)
        return str(base64.encodebytes(des.encrypt(data)), encoding='utf8').replace('\n', '')
    '''

    def encrypt(self, header, body):
        '''
        正则处理提取出加密部分
        '''
        if r"\u001d{" in body:
            a = re.findall(r'encryptData":"(.*?\\u001d.*?\\u001d.*?)"', body)
            b = r'\u001d'
            sign = a[0].split(b)[0]
            data = a[0].split(b)[1]
            sign_new = self._md5(data+'SZBank@9')
            data_encrypt = self._des_encode(data, self.key)+'ea330fd588864869'
            body = body.replace(sign, sign_new)
            body = body.replace(data, data_encrypt)
        return header,body
    def decrypt(self, header, body):
        '''
        Auto Enc/Dec feature require this function

        '''
        if r'encryptData' in body:
            a = re.findall(r'encryptData":"(.*?)"', body)
            print(a[0])
            b=r'\u001d'
            if b in a[0]:
                c = a[0].split(b)[1]
                body=body.replace(c, self._des_decode(c, self.key))
            else:
                body=body.replace(a[0], self._des_decode(a[0], self.key))
        return header,body

    def processor(self, payload):
        '''
        Enable Processor feature require this function
        payload processor function
        '''
        return payload + "123"
'''
if __name__ == '__main__':
    body='[{"encryptData":"c828b41bf0e5c4acdfeb47d3ec4dd713\x1d{"bankUserId":"","mobileNo":"17200926874","otpType":80,"channelNo":"05"}\x1dafc5ea68725a1885c210679cbca29d0edd6223738bd123395799fbdae110a23a498016e41830454b2898f0a9cdc7863ef15b53b656ebe8486a6501b090576df8d53e504e807894cd399c814c42effa13b10797e5ba638adf97579e62fdbe6f1a43493ca35b582f05291152fa5bf38d9191938495dd8d9b0ea9e74e671f2fa8c4","channelNo":"05"}]'
    body1='{"bankUserId":"","mobileNo":"15852696874","otpType":80,"channelNo":"05"}'
    head='head'
    burp = Burpy()
    a = burp.encrypt(head,body)
    print(a[1])
'''