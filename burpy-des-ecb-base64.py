import re
import base64
from Crypto.Cipher import DES
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
        self.key = 'CSIIZRCb'
        #self.iv = '01234567'
        self.mode = DES.MODE_ECB


    def main(self, header, body):
        return header, body

    def _des_decode(self, data, key):
        try:
            #des = DES.new(str.encode(key),DES.ECB,str.encode(self.iv))
            des = DES.new(str.encode(key),DES.MODE_ECB)
            decrypted_text = des.decrypt(base64.decodebytes(bytes(data, encoding='utf8'))).decode("utf8")

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
        return str(base64.encodebytes(des.encrypt(data)), encoding='utf8').replace('\n', '')
    
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
        if r'"data":"' in body:
            a = re.findall(r'\{\"data\"\:\"(.+)\",', body)
            if a:
                b = a[0]
            else:
                pass
            body=body.replace(b,self._des_encode(b,self.key))
        if r'"resultMap":"' in body:
            result = re.findall(r'"resultMap\"\:\"(.+)\"', body)
            if result:
                res=result[0]
            else:
                pass
            body=body.replace(res,self._des_encode(res,self.key))
        return header,body
    def decrypt(self, header, body):
        '''
        Auto Enc/Dec feature require this function

        '''
        if r'"data":"' in body:
            a = re.findall(r'\{\"data\"\:\"(.+)\",', body)
            b="11"
            if a:
                b = a[0]
            else:
                pass
           # if r'sign' in body:
               # sign=re.findall(r',"sign\"\:\"(.+)\"',body)
               # c=sign[0]
            body=body.replace(b, self._des_decode(b, self.key))
        if r'"resultMap":"' in body:
            result = re.findall(r'"resultMap\"\:\"(.+)\"', body)
            if result:
                res=result[0]
           # body=body.replace(c,"")
            body=body.replace(res, self._des_decode(res, self.key))
            print(body)
        return header,body

    def processor(self, payload):
        '''
        Enable Processor feature require this function
        payload processor function
        '''
        return payload + "123"
'''        
if __name__ == '__main__':
    body='{"data":"/jlLsZlfM3oQ/pudIrIFWjLdYWYSoqp7JsdUcGqJm44bh/7VEvr4QgR3/4TxqQomjA1bQyWHyxOtcK205B3yqshnH0DRctZxcVyyo0YA7fQy/fjNtMFB4D15DDhY8FSSGmlK/JZ3ucaw9MTHGNzpyivLSXfUnrJ0k9TCQlb537Q8lunLM17f9lci4OB62AU/sZcClWLcEbQQ/pudIrIFWjLdYWYSoqp7JsdUcGqJm44bh/7VEvr4QlRjSjPCW5YO","sign":"0f3e78b11526ae89f77b781ab88db293"}'
    body1='{"data":"{"OpenId":"oKPs444P9afDTE8HwvXg2cZqpgDA","CHAINEDID":"MINE","ProductCode":"SC030009","ProductPode":"SC030009","_locale":"zh_CN","BankId":"9999","_openid":"oKPs444P9afDTE8HwvXg2cZqpgDA"}","sign":"0f3e78b11526ae89f77b781ab88db293"}'
    head='head'
    burp=Burpy()
    a,b=burp.encrypt(burp.key,body1)
    print('a=')
    print(a)
    print('b=')
    print(b)
'''