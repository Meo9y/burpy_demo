import re
from urllib.parse import unquote, quote
import base64
import binascii
from Crypto.Cipher import AES
#body='data=7F6E461B590B0F5AB6869330B0FE6F60341E01585D3E2A122CC02BE0938DF43EC3F25F08A84554D91F5F7745D208D61AD81F3E9E694F6B392B43F2F69504A6EB4FEAC3311A313DF97DD1CEA9602472673CAF19A63E8C0E62B21BED358CD35A3835C37B8082B367FFA5CD22A757B9430AE66619B7448BD04F5875109D2AA75D71383E88C7750126C561B447FA8E64EB16BBB7A74A6EA1ECC3AD46E074C628F93D753A2EB33107C816EC367D3CCF36A444247BD59F9B0CDFD33CE012CABF17A179DB729771690B95012A03D1581DDDA7488F40859BCB0F510B65FE70136EE009E06ECF3501113FCE9676BD5498B7E815E6E88712AC626BEF658F6DE1A957CE1814&rpd=n5YsUHvPA8IurhXd6hkOI4hZ2cq1vglwf8sr60nLqkczFGVIvc2gLQAcwfh5BAnftbIJG6V8xMX1DAXCslDm3fMofSAs9Wc5P28m2evekJirNui63RGS7FkbobvvmfhSIpMv0HZuXNER8cHoLn93GYhZFDNxcIzKGMuCA8JwcyssQxh2vxiqflTM03w6ipY9Vsql2r9lCtAjIx0Lkwyl9KW8zftYwIyNxIDrTZ7oVx0ZIB8inxtTy9hfY8G2pn7rH%2B2QyZltN6il%2BTmOjFlU4Ftn81wKsJh3xW8WHSwk7UWFNZaBng1k%2B99Zq7%2BS8K6GwaJIwtSE9MgN%2Fks7ecrh4A%3D%3D&riskInfo=158AAAD5E2B2CCC49789E4BCA05BDB14312063CE7B32F87F8E55CFC797D845DEDBCBF9896739745150DF1618FBE073E8D681440670942E78A12B08456538376D3DC15B14068930223C0C4F4621F0433D33EE0BE097D44D36F9AFC52AE2430C71'
#header='1'
class Burpy:
    '''
    header is dict
    body is string
    '''

    def __init__(self):
        '''
        here goes some code that will be kept since "start server" clicked, for example, webdriver, which usually takes long time to init
        '''
        self.key = '20a1d32f6fbf5fc0'

    def main(self, header, body):
        
        return header, body
    def _add_to_16(self,text):
        while len(text) % 16 != 0:
            text += '\0'
        return text
    def _aes_decode(self, data, key):
        if isinstance(key,str):
            key = key.encode('utf-8')
        cipher = AES.new(key,AES.MODE_ECB)
        plain_text = cipher.decrypt(binascii.a2b_hex(data))
        return plain_text.decode('utf-8').rstrip('\x0f')

    def _aes_encode(self, data, key):
        if isinstance(key,str):
            key = key.encode('utf-8')
        bs = AES.block_size
        pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        cipher = AES.new(key, AES.MODE_ECB)
        data = cipher.encrypt(pad(data).encode('utf8'))
        encrypt_data = binascii.b2a_hex(data)  # 输出hex
        return encrypt_data.decode('utf8')
    def encrypt(self, header, body):
        '''
        正则处理提取出加密部分
        '''
        if 'messageCaptcha' in header['first_line']: 
            phone = re.findall(r'messageCaptcha/(.*?) ', header['first_line'])[0]
            phone2 = self._aes_encode(phone, self.key)
            header['first_line'] = header['first_line'].replace(phone, phone2)
            print(header['first_line'])
        return header, body

    def decrypt(self, header, body):
        '''
        Auto Enc/Dec feature require this function

        '''
        if 'responseContent' in body:
            data = re.findall(r'"responseContent":"(.*?)"',body)[0]
            data2 = self._aes_decode(data,self.key)
            body = body.replace(data,data2)
        if 'data' in body:
            data = re.findall(r'data=(.*?)&', body)[0]
            data2 = self._aes_decode(data,self.key)
            body = body.replace(data,data2)
        else:
            body=body
        return header, body

    def processor(self, payload):
        '''
        Enable Processor feature require this function
        payload processor function
        '''
        return payload + "123"