#conda activate F:\ComfyUI-Caption-Generator\cdvenv
#pip install --upgrade pip
#pip install pycryptodome
#python app_activation.py

import uuid
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
import os
import signal
import platform
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import json
from datetime import datetime, timedelta
import secrets

class AppActivation(object):

    # 定义密码和盐值（需要安全保存）
    # 密码
    password = b'iLu\xaa\xefiD\xbc\xd8\xe0\xd9\x95\xee\xbf\xecfG\xaf\x14TDf\xbe$S\x93\x00\xf3\xf80\x91\x17'
    # 盐值
    salt =b'\x0c\xa2\x91\x8d)\x0b\xa8\x8f\xdf\x00\xd2\xcb\xd8\x10n8\xc2\x1a%\\\xf7\xb79Rm"\xe6}\x01e\xca\xc3'

    # 第一步生成 password 和 salt
    # random_bytes = secrets.token_bytes(32)# 生成32字节的随机字节串（长度与你提供的相同）
    # print("random_bytes:", random_bytes)
    # salt = get_random_bytes(16)  # 随机生成16字节的盐值
    # password = scrypt(random_bytes, salt, 32, N=2**14, r=8, p=1)# 使用Scrypt进行密钥推导
    # print("password:", password)   # 将生成的密钥和盐值打印出来（实际项目中不应该打印出来，而是安全保存）
    # print("salt:", salt)

    def __init__(self):
        pass

    def encrypt_message(self,message):
        kdf_salt = self.salt
        key = scrypt(self.password, kdf_salt, 32, N=2**14, r=8, p=1)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

    def decrypt_message(self,encrypted_message):
        kdf_salt = self.salt
        key = scrypt(self.password, kdf_salt, 32, N=2**14, r=8, p=1)
        data = base64.b64decode(encrypted_message)
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')

    def getEncryptActivation(self):
        # 示例日期和有效期
        current_date = datetime.now()
        #expiry_date = current_date + timedelta(days=1)  # 假设有效期为1天   
        #expiry_date = current_date + timedelta(days=90)  # 假设有效期为90天     
        #expiry_date = current_date + timedelta(days=180)  # 假设有效期为180天     
        expiry_date = current_date + timedelta(days=720)  # 假设有效期为720天  
        print(current_date)
        print(expiry_date)
        # 生成一个随机的UUID
        new_uuid = uuid.uuid4()
        print(new_uuid)
        # 生成一个基于名称和命名空间的UUID（例如基于URL或OID）
        name_based_uuid = uuid.uuid5(uuid.NAMESPACE_URL, '@老王的AI实验室')
        print(name_based_uuid)
        # 构建包含日期和有效期的字典
        data = {
            "current_date": current_date.isoformat(),  # 将日期转换为ISO 8601格式
            "expiry_date": expiry_date.isoformat(),
            "uuid":str(new_uuid),
            "inactivated": 1 #未激活=1
        }       
        print(data)#{'current_date': '2024-06-27T17:18:10.294877', 'expiry_date': '2024-09-25T17:18:10.294877', 'uuid': '8fbd423d-a12f-4a17-8e1c-834660bfb3dd', 'inactivated': 1}
        # 将字典转换为JSON字符串
        json_string = json.dumps(data, indent=4)
        print(json_string)
        # {
        #     "current_date": "2024-06-27T17:18:10.294877",
        #     "expiry_date": "2024-09-25T17:18:10.294877",          使用     
        #     "uuid": "8fbd423d-a12f-4a17-8e1c-834660bfb3dd",
        #     "inactivated": 1
        # }
        # 加密激活日期并写入文件
        encrypted_activation_code = self.encrypt_message(json_string)
        print("activation_code:",encrypted_activation_code)
        #1 
        #90 
        #720 Xf2vkxVFrfnT0l43D+ksVO6JrzKrHMGvcnsQ4orRfuUMC+IR5NKMgqLjbUna7WLNLwPFLbY3ORDIgi1lIbDrvaSdoyUlwQDezbbSo7vtvIkEcxupe21Vg1NK+OSi3zdo3mrsVRvKiVXO+HIpbSbCPNjFYPGdkJAIGa94obM2IFTz7qDOdSB+AU1khXFl/QVdqr+hHNXfboQsqNL+PRSyXVptHkG9vGWBDA37s7/J6vgwMX8nkcbxWR7CHFVNId/BggJsuQtpv7TfGemi6gfQ

    def get_activation_date(self):
        json_activation=None
        # 尝试从文件中读取加密的激活日期
        try:
            with open('activation_date.txt', 'rb') as file:
                encrypted_activation_date = file.read().strip()
                activation_code_str = self.decrypt_message(encrypted_activation_date)
                #print(activation_code_str)
                # 将JSON字符串换转为字典
                json_activation=json.loads(activation_code_str)
                json_activation["status"]=200
                # print(json_activation)
                # print(json_activation["current_date"])
                # print(json_activation["expiry_date"])
                # print(json_activation["uuid"])
                # print(json_activation["inactivated"])
                # 将字符串转换为日期对象
                current_date = datetime.strptime(str(json_activation["current_date"]), "%Y-%m-%dT%H:%M:%S.%f")
                expiry_date = datetime.strptime(str(json_activation["expiry_date"]), "%Y-%m-%dT%H:%M:%S.%f")     
                # 输出转换后的日期对象
                #print(f"Current Date: {current_date}")
                #print(f"Expiry Date: {expiry_date}")
                # 格式化日期对象
                json_activation["current_date_str"] = current_date.strftime("%Y-%m-%d")
                json_activation["expiry_date_str"] = expiry_date.strftime("%Y-%m-%d")
        except Exception as ex:   
            #print(str(ex))    
            # 创建一个空字典
            json_activation = {}
            json_activation["status"]=300
            json_activation["error"]= str(ex)
        return json_activation

    def check_validity(self,json_activation):
        # 将日期字符串转换为日期时间对象
        current_date_str= datetime.now().strftime("%Y-%m-%d")#今天日期
        #expiry_date_str=json_activation["current_date_str"]#开发测试
        expiry_date_str=json_activation["expiry_date_str"]
        current_date = datetime.strptime(current_date_str, '%Y-%m-%d')
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
        # 计算日期之间的差值
        validity_period = (expiry_date - current_date).days  # 计算天数
        # 获取当前日期
        today_date = datetime.today()
        # 通过将有效期天数添加到今天的日期来计算到期日期
        expiry_date_calculated = today_date + timedelta(days=validity_period)
        # 打印有效期（天）
        print(f"Validity period: {validity_period} days")
        #print(f"Current date: {today_date} days")
        #print(f"Expiry date: {expiry_date_calculated} days")
        # 比较当前日期和有效期
        if validity_period == 0:
            print(f"Program is within the valid period until {expiry_date_str}. This program has expired.")
            return False
        else:
            print(f"Program is within the valid period until {expiry_date_str}. Proceeding...")
            return True


if __name__=="__main__":
    app=AppActivation()
    #生成激活日期的激活码字符串
    app.getEncryptActivation()
    # 获取激活日期
    json_activation = app.get_activation_date()
    #print(json_activation)#{'current_date': '2024-06-27T15:48:34.165310', 'expiry_date': '2024-09-25T15:48:34.165310', 'uuid': '8bae5540-e790-4347-b8c5-b586a34fb5fd', 'status': 200, 'current_date_str': '2024-06-27', 'expiry_date_str': '2024-09-25'}
    if(json_activation["status"]==200):
        # 检查程序有效期
        app.check_validity(json_activation)
    else:
        print(json_activation["status"])
        print(json_activation["error"])
