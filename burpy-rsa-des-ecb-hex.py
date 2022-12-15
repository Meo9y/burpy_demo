import re
import base64
import binascii
from Crypto.Cipher import DES
import hashlib
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from Crypto.PublicKey import RSA
import time
import random

#from pyDes import des, PAD_PKCS5, ECB

class Burpy:
    '''
    header is dict
    body is string
    '''
    #-------------------rsa解密获取des key---------------------
    def _rsaencryption(self,text):
    # 字符串指定编码（转为bytes）
        text = text.encode('utf-8')
        public_key = b'-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCB2kB43bYg4Vmfe9BZQdh+IfcY+O1gt9MrC368w1+gcLHvqfwX\nLnRyil9cYXF8Yjrnqwq3rDEyjqLvBV8NFnFxPjLrLSddoBWVOnbmGDEwDmL6Iwsh\npKzeO8lGKA4FGF3nathLLC5PJDcLA1ep5pSXleglT0aIOmjpWexEy9uT0QIDAQAB\nAoGAASVp6g4OEqpwQWW5oCwP75g4ObxPUYD6cW7JXPw+Dqje2KCZAqPMuUGqoL3w\ncYg5bmD7E3yZI5HZ8xqBbSrTS7aDDfUahCluUQaSMdLal1HV6kafCbahKZktjsma\nEc8qEG0lMX9bA2I2Wf5xDLho233h0hq7EUdSRL0gR1RyLpUCQQCCeanptgmeAx2e\nIJEoyxPb4ORYpRMCW1X/jlnAXTgFP/uUESr/VPvRVEZF6esLRjeMxkPpAIw+n+ai\naC7kkxj9AkEA/sc5gxY8Hi8H7p4SV2OBJa5OhBFp1gqPVts8sGU+Q6XnATGncqAB\nDTztEnFC/fLjxz5eJQACezgUg1GfY9cYZQJAGvTP6f02F3NFVzobQ3ZRcAgSpU3V\nk5MTPW1HlbqsrEj/zSOO4pnIPQNQUXl2mimzqF3+AdGfKAEZQUyNA6RwcQJBAPlO\n9gZCQb2/g+GJqKT+56d5s7ckWw5p8u2pRu/Ngmor86qFbjeKPr03ezzqvAVIIoAb\nlYBbTBJLRDdkLbZDCskCQFbc0Omrzg1guVRwlIB4/+X/SkUzLcpZVArync2O3pVF\n55t2iaCsQEEWmPPrhW5eu8Z7cpgb285a/rQTWVtBFdM=\n-----END RSA PRIVATE KEY-----'
    # 构建公钥对象
        cipher_public = PKCS1_v1_5.new(RSA.importKey(public_key))
    # 加密（bytes）
        text_encrypted = cipher_public.encrypt(text)
    # base64编码，并转为字符串
        text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
        return text_encrypted_base64
    def _rsadecryption(self,text_encrypted_base64):
    # 字符串指定编码（转为bytes）
        text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
        private_key = b'-----BEGIN RSA PRIVATE KEY-----\n\n-----END RSA PRIVATE KEY-----'
    # base64解码
        text_encrypted = base64.b64decode(text_encrypted_base64)
    # 构建私钥对象
        cipher_private = PKCS1_v1_5.new(RSA.importKey(private_key))
    # 解密（bytes）
        text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
    # 解码为字符串
        text_decrypted = text_decrypted.decode()
        return text_decrypted
    def __init__(self):
        '''
        here goes some code that will be kept since "start server" clicked, for example, webdriver, which usually takes long time to init
        '''
        self.key = ''
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
        if 'Graphqbodykey' in header:
            a = header['Graphqbodykey']
            des_key = self._rsadecryption(a)
            body_new = self._des_encode(body,des_key)
            body = body_new
        header['Timestamp']=int(time.time())
        header['Requestid']= random.randint(0,999)
        if len(header['Authorization'])>0:
            header['Sign']=self._md5('appId={}&authorization={}&body={}&mode=Mobile&operatinId=&pageId={}&requestId={}&subAppId={}&timestamp={}'.format(header['Appid'],header['Authorization'][7:],body,header['Pageid'],header['Requestid'],header['Subappid'],header['Timestamp']))
        else:
            header['Sign']=self._md5('appId={}&authorization=&body={}&mode=Mobile&operatinId=&pageId={}&requestId={}&subAppId={}&timestamp={}'.format(header['Appid'],body,header['Pageid'],header['Requestid'],header['Subappid'],header['Timestamp']))
        return header,body
    def decrypt(self, header, body):
        '''
        Auto Enc/Dec feature require this function

        '''
        if 'Graphqbodykey' in header:
            a = header['Graphqbodykey']
            #print(a)
            des_key = self._rsadecryption(a)
            body_new = self._des_decode(body,des_key)
            body = body_new
        if 'graphqkey' in header:
            b = header['graphqkey']
            des_key = self._rsadecryption(b)
            data = re.findall(r'data":"([ABCDEF1234567890]*?)"',body)
            item1 = re.findall(r'item1":"([ABCDEF1234567890]*?)"',body)
            if len(data)>0:
                print(des_key)
                print(data[0])
                data_new = self._des_decode(data[0],des_key)
                #print(data_new)
                body = body.replace(data[0],data_new)
            if len(item1)>0:
                print(des_key)
                print(item1[0])
                item1_new = self._des_decode(item1[0],des_key)
                body = body.replace(item1[0],item1_new)
        return header,body

    def processor(self, payload):
        '''
        Enable Processor feature require this function
        payload processor function
        '''
        return payload + "123"
'''
if __name__ == '__main__':
    body="""
    [{"item1":"B4B10EB5A9F752983DA54908140F94AAF60EB3F4D2CCE598D7A2252D8E453E2643C08A5BBB5E14F5023176199C39DF2F549FB584555660F98E72C67140901FFAF05FC4AA433D7BAF758DC043485FCB2D0D85C1E47AE4BE0337268BDF3D99846D54D652BB1C1DAA475CDBB988EC11CE8365DC0A6400781F290427BA2AAD3E06E67676B23764D1C7882A469B7868904DC8","item3":"00:00:00.0597006"},{"item1":{"queryDaibanbiaoContentsWithTotal":{"total":3542,"countFields":{"count_all":3542.0},"items":[{"id":"eac5296d-2038-4801-b61c-51a4b5cd5d5c","contentId":"eac5296d-2038-4801-b61c-51a4b5cd5d5c","dataText":"null.","status":"PUBLISHED","created":"2022-11-21T09:27:54.352+00:00","lastModified":"2022-11-21T09:27:54.352+00:00","createdBy":"sub:3309caef-ffd4-4310-a8c0-69f81a69e067","lastModifiedBy":"sub:3309caef-ffd4-4310-a8c0-69f81a69e067","data":{"daibanid":{"iv":"1b596705-ec54-4dc1-bfbc-184f85c6fb29"},"danbanlx":{"iv":[{"label":"故障报修","value":"gzbx"}]},"shixianglx":{"iv":"泥木类"},"daibanmc":{"iv":"403后门教室外面瓷砖脱落，需要维修，明天上午考试不能维修"},"chulizt":{"iv":"待派工"},"chulirenid":{"iv":""},"chulirenxm":{"iv":""},"chulirengh":{"iv":""},"chulirendh":{"iv":""},"beizhu":{"iv":""},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}},{"id":"5bd590aa-120f-45c3-ba06-00f04c9c68d2","contentId":"5bd590aa-120f-45c3-ba06-00f04c9c68d2","dataText":"null.","status":"PUBLISHED","created":"2022-11-21T01:45:43.503+00:00","lastModified":"2022-11-21T01:45:43.503+00:00","createdBy":"sub:7a82ed34-bbf8-4dc1-b278-15f828c4d792","lastModifiedBy":"sub:7a82ed34-bbf8-4dc1-b278-15f828c4d792","data":{"daibanid":{"iv":"8011686a-96ab-473c-b5e3-2ed972cc0d33"},"danbanlx":{"iv":[{"label":"故障报修","value":"gzbx"}]},"shixianglx":{"iv":"水电类"},"daibanmc":{"iv":"锁坏了"},"chulizt":{"iv":"待评价"},"chulirenid":{"iv":""},"chulirenxm":{"iv":"唐旭东"},"chulirengh":{"iv":""},"chulirendh":{"iv":"13755161321"},"beizhu":{"iv":""},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}},{"id":"c069fc29-7052-4ba2-9c41-95d8af785702","contentId":"c069fc29-7052-4ba2-9c41-95d8af785702","dataText":"null.","status":"PUBLISHED","created":"2022-11-20T16:10:21.386+00:00","lastModified":"2022-11-20T16:10:21.386+00:00","createdBy":"sub:0dacd49f-91fe-4152-b056-d8035177baab","lastModifiedBy":"sub:0dacd49f-91fe-4152-b056-d8035177baab","data":{"daibanid":{"iv":"abb10761-45c7-4f0d-ac27-213d857cde23"},"danbanlx":{"iv":[{"label":"调换宿舍","value":"dhss"}]},"shixianglx":{"iv":""},"daibanmc":{"iv":"胡耀丹"},"chulizt":{"iv":"待辅导员审核"},"chulirenid":{"iv":""},"chulirenxm":{"iv":""},"chulirengh":{"iv":""},"chulirendh":{"iv":""},"beizhu":{"iv":"辅导员审核"},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}},{"id":"fdbb8ffc-0344-4697-b285-4e25974bb4ec","contentId":"fdbb8ffc-0344-4697-b285-4e25974bb4ec","dataText":"null.","status":"PUBLISHED","created":"2022-11-20T13:08:32.793+00:00","lastModified":"2022-11-20T13:08:32.793+00:00","createdBy":"sub:dafcec56-80b2-4edd-9a25-e2a139370a72","lastModifiedBy":"sub:dafcec56-80b2-4edd-9a25-e2a139370a72","data":{"daibanid":{"iv":"a8cdf2fb-4fdd-4b5a-9546-a247570d9ea0"},"danbanlx":{"iv":[{"label":"故障报修","value":"gzbx"}]},"shixianglx":{"iv":"泥木类"},"daibanmc":{"iv":"门坏了"},"chulizt":{"iv":"待派工"},"chulirenid":{"iv":""},"chulirenxm":{"iv":""},"chulirengh":{"iv":""},"chulirendh":{"iv":""},"beizhu":{"iv":""},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}},{"id":"ae80381d-2f1f-4609-9bc2-06e14a5e431c","contentId":"ae80381d-2f1f-4609-9bc2-06e14a5e431c","dataText":"null.","status":"PUBLISHED","created":"2022-11-20T11:09:26.465+00:00","lastModified":"2022-11-20T11:09:26.465+00:00","createdBy":"sub:a5cb2e90-8790-4e22-9e1b-756816be5180","lastModifiedBy":"sub:a5cb2e90-8790-4e22-9e1b-756816be5180","data":{"daibanid":{"iv":"6a987b11-81ee-49b6-af24-dd4d19159db6"},"danbanlx":{"iv":[{"label":"故障报修","value":"gzbx"}]},"shixianglx":{"iv":"泥木类"},"daibanmc":{"iv":"宿舍窗户卡住了，打不开"},"chulizt":{"iv":"待派工"},"chulirenid":{"iv":""},"chulirenxm":{"iv":""},"chulirengh":{"iv":""},"chulirendh":{"iv":""},"beizhu":{"iv":""},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}},{"id":"bc3e73c4-b5b0-4302-ba5e-c3d79462a911","contentId":"bc3e73c4-b5b0-4302-ba5e-c3d79462a911","dataText":"null.","status":"PUBLISHED","created":"2022-11-20T11:06:16.254+00:00","lastModified":"2022-11-20T11:06:16.254+00:00","createdBy":"sub:ea7c447c-1eac-4f28-99af-0880c855e762","lastModifiedBy":"sub:ea7c447c-1eac-4f28-99af-0880c855e762","data":{"daibanid":{"iv":"f7c7c09f-a4ba-4057-adb7-d0ef411cfd5d"},"danbanlx":{"iv":[{"label":"故障报修","value":"gzbx"}]},"shixianglx":{"iv":"泥木类"},"daibanmc":{"iv":"厕所门把手坏了"},"chulizt":{"iv":"待派工"},"chulirenid":{"iv":""},"chulirenxm":{"iv":""},"chulirengh":{"iv":""},"chulirendh":{"iv":""},"beizhu":{"iv":""},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}},{"id":"0e4b6383-8ab4-428a-86b4-58623493591d","contentId":"0e4b6383-8ab4-428a-86b4-58623493591d","dataText":"null.","status":"PUBLISHED","created":"2022-11-20T09:20:51.62+00:00","lastModified":"2022-11-20T09:20:51.62+00:00","createdBy":"sub:7b78f1b3-29f6-4556-b7bb-9e51de5973e0","lastModifiedBy":"sub:7b78f1b3-29f6-4556-b7bb-9e51de5973e0","data":{"daibanid":{"iv":"f0b1d6dc-6b87-43ce-8995-dce6b199943d"},"danbanlx":{"iv":[{"label":"故障报修","value":"gzbx"}]},"shixianglx":{"iv":"泥木类"},"daibanmc":{"iv":"室内晒衣架脱落"},"chulizt":{"iv":"待评价"},"chulirenid":{"iv":""},"chulirenxm":{"iv":"覃璇"},"chulirengh":{"iv":""},"chulirendh":{"iv":"17872061326"},"beizhu":{"iv":""},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}},{"id":"4935fb43-4925-423a-8f38-f14db2165be6","contentId":"4935fb43-4925-423a-8f38-f14db2165be6","dataText":"null.","status":"PUBLISHED","created":"2022-11-20T09:18:49.922+00:00","lastModified":"2022-11-20T09:18:49.922+00:00","createdBy":"sub:7b78f1b3-29f6-4556-b7bb-9e51de5973e0","lastModifiedBy":"sub:7b78f1b3-29f6-4556-b7bb-9e51de5973e0","data":{"daibanid":{"iv":"655cb026-d5e8-40ec-9380-55f73daa9720"},"danbanlx":{"iv":[{"label":"故障报修","value":"gzbx"}]},"shixianglx":{"iv":"水电类"},"daibanmc":{"iv":"钥匙拔不出来 请求维修门锁"},"chulizt":{"iv":"待评价"},"chulirenid":{"iv":""},"chulirenxm":{"iv":"赵梓钧"},"chulirengh":{"iv":""},"chulirendh":{"iv":"18774518188"},"beizhu":{"iv":""},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}},{"id":"acc205fe-9757-452b-8672-4f54e740b577","contentId":"acc205fe-9757-452b-8672-4f54e740b577","dataText":"null.","status":"PUBLISHED","created":"2022-11-20T08:28:48.089+00:00","lastModified":"2022-11-20T08:28:48.089+00:00","createdBy":"sub:7a82ed34-bbf8-4dc1-b278-15f828c4d792","lastModifiedBy":"sub:7a82ed34-bbf8-4dc1-b278-15f828c4d792","data":{"daibanid":{"iv":"995b3404-f569-4d97-a7d8-8bc4df9b3062"},"danbanlx":{"iv":[{"label":"故障报修","value":"gzbx"}]},"shixianglx":{"iv":"水电类"},"daibanmc":{"iv":"厕所漏水，关不紧"},"chulizt":{"iv":"待评价"},"chulirenid":{"iv":""},"chulirenxm":{"iv":"王文浩"},"chulirengh":{"iv":""},"chulirendh":{"iv":"18664340594"},"beizhu":{"iv":""},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}},{"id":"09aa36ae-46d5-4d30-9808-324570b09e60","contentId":"09aa36ae-46d5-4d30-9808-324570b09e60","dataText":"null.","status":"PUBLISHED","created":"2022-11-20T06:04:21.604+00:00","lastModified":"2022-11-20T06:04:21.604+00:00","createdBy":"sub:7a82ed34-bbf8-4dc1-b278-15f828c4d792","lastModifiedBy":"sub:7a82ed34-bbf8-4dc1-b278-15f828c4d792","data":{"daibanid":{"iv":"a50cde9b-27d4-4130-901b-e2fa795f5f74"},"danbanlx":{"iv":[{"label":"故障报修","value":"gzbx"}]},"shixianglx":{"iv":"泥木类"},"daibanmc":{"iv":"凳子烂了"},"chulizt":{"iv":"待评价"},"chulirenid":{"iv":""},"chulirenxm":{"iv":"伍国生"},"chulirengh":{"iv":""},"chulirendh":{"iv":"13348624452"},"beizhu":{"iv":""},"dbclzk":{"iv":[{"label":"待处理","value":"dcl"}]}}}]}},"item3":"00:00:01.1487038"},{"item1":{"queryTiwensjContentsWithTotal":{"total":0,"countFields":{"count_all":0.0},"items":[]}},"item3":"00:00:00.0308305"}]
    """
    head={"graphqkey":"FpQT6OfFFMsODfDKu0VSlZgmL4oBw06eBMyhCBShzzG4c+JDThyw5A2US5Gr7w+e4jFcC7l+2hQRjivHn7V8X6zg3ww5iXv094m5Myt8lNEOBgOna3AXbGELT5fMYGGRgep7T1yN6nqMRi43/iRaGIKG3XDc+AbU4yFstCrXd4I=","Current-Env":"123"}
    burp = Burpy()
    a = burp.decrypt(head,body)
    print(a)
'''
