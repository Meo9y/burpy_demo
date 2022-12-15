import re
from urllib.parse import unquote, quote
import base64
from Crypto.Cipher import AES


class Burpy:
	'''
	header is dict
	body is string
	'''

	def __init__(self):
		self.key = "xxxxx"
		self.length = AES.block_size  # 初始化数据块大小
		self.aes = AES.new(self.key.encode("utf8"), AES.MODE_ECB)  # 初始化AES,ECB模式的实例
		# 截断函数，去除填充的字符
		self.unpad = lambda date: date[0:-ord(date[-1])]

	def main(self, header, body):
		return header, body

	def _pad(self, text):
		count = len(text.encode('utf-8'))
		add = self.length - (count % self.length)
		entext = text + (chr(add) * add)
		return entext

	def _aes_decode(self, data):
		print(data)
		res = base64.decodebytes(data.encode("utf8"))
		msg = self.aes.decrypt(res).decode("utf8")
		return self.unpad(msg)

	def _aes_encode(self, data):
		res = self.aes.encrypt(self._pad(data).encode("utf8"))
		msg = str(base64.b64encode(res), encoding="utf8")
		return msg

	def encrypt(self, header, body):
		'''
		正则处理提取出加密部分
		'''
		if 'userpwd' in body:
			data = re.findall(r'userpwd=(.*)&', body)[0]
			data2 = self._aes_encode(data)
			body = body.replace(data, data2)
		return header, body

	def decrypt(self, header, body):
		'''
		Auto Enc/Dec feature require this function

		'''
		if 'securityParam' in body:
			data = re.findall(r'securityParam":"(.*)"', body)[0]
			data = unquote(data)
			data2 = self._aes_decode(data)
			body = body.replace(data, data2)
			print(body)
		if 'securityRes' in body:
			data = re.findall(r'securityRes":"(.*)"', body)[0]
			data2 = self._aes_decode(data)
			body = body.replace(data, data2)
		return header, body

	def processor(self, payload):
		'''
		Enable Processor feature require this function
		payload processor function
		'''
		#payload='{"userName":"'+payload+'"}'
		#payload=self._aes_encode(payload)
		return payload+'123'


if __name__ == '__main__':
	payload = 'admin'
	a='123'
	burp = Burpy()
	a= burp._aes_encode(payload)
	print(a)
