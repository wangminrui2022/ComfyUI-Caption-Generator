#conda activate D:\ChatTTS_colab\cdvenv
#python app_start.py

import traceback
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
import os
import signal
import platform
import requests
import json

from app_activation import AppActivation
from app_ip_address import AppIPAddress

class AppStart(object):

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        print("---Global exception capture---")
        print("Exception type:", exc_type.__name__)
        print("Exception message:", exc_value)
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    sys.excepthook = handle_exception

    def __init__(self):
        print("---AppStart---")
        print("Python version=",sys.version)
        try:
            #CUDA or ROCm
            gpu="Unknown"
            gpu=self.get_gpu_vendor() 
            print("gpu:"+gpu) 
        except Exception as e:
            # 捕获异常并打印异常信息
            print(f"Caught an exception: {e}")           
        print("\n---Contact us: @老王的AI实验室 Old Wang's AI Lab v2025.1.0---\n")

        #获取地区区域信息
        ip_checker = AppIPAddress()
        result = ip_checker.compare_ips()
        if(result==None):
            self.show_dialog(f"Network request failed, please check the network connection!")#网络请求失败， 请检查网络连接！
        else:
            ips=json.dumps(result, indent=2, ensure_ascii=False)
            #print(ips)
            # 测试代码
            restricted = ip_checker.is_restricted_country(result)
            if(restricted==True):
                self.show_dialog(f"Warning: Restricted Country Detected.\n {ips}") #警告：检测到受限制国家 
            try:
                self.show_startup_dialog()
                #raise Exception("no display name and no $DISPLAY environment variable")
            except Exception as e:
                # 捕获异常并打印异常信息
                print(f"Caught an exception: {e}")

    def get_gpu_vendor(self):
        if platform.system() == "Windows":
            try:
                output = subprocess.check_output(["nvidia-smi"]).decode(errors="ignore")
                if "NVIDIA" in output:
                    return "NVIDIA"
            except subprocess.CalledProcessError as e:
                print(str(e))
            try:
                output = subprocess.check_output(["amdgpu-pro-px"])
                if "AMD" in output.decode():
                    return "AMD"
            except subprocess.CalledProcessError as e:
                print(str(e))
            return "Unknown"
        elif platform.system() == "Linux":
            try:
                output = subprocess.check_output(["lspci", "-v"]).decode(errors="ignore")
                if "NVIDIA" in output:
                    return "NVIDIA"
                elif "AMD" in output:
                    return "AMD"
            except subprocess.CalledProcessError as e:
                print(str(e))
            return "Unknown"
        else:
            return "Unsupported"

    #agreement_window=None

    def show_startup_dialog(self):
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口

        appActivation=AppActivation()
        # 获取激活日期
        json_activation = appActivation.get_activation_date()
        #print(json_activation)
        if(json_activation["status"]==200):
            # 检查程序有效期
            if(appActivation.check_validity(json_activation)==True):
                agreement_window = tk.Toplevel(root)
                agreement_window.title("User Agreement")
                #agreement_window.protocol("WM_DELETE_WINDOW", lambda: None)#禁用窗口关闭按钮
                agreement_window.protocol("WM_DELETE_WINDOW", self.on_close)#监听关闭按钮的事件，并调用 self.on_close 方法

                text = ScrolledText(agreement_window, wrap=tk.WORD, width=80, height=20)
                text.insert(tk.END, self.getDisclaimer())
                text.config(state=tk.DISABLED)
                text.pack(expand=True, fill=tk.BOTH)

                button_frame = tk.Frame(agreement_window)
                button_frame.pack(fill=tk.X, pady=10)

                agree_button = tk.Button(button_frame, text="Agree", command=lambda: self.on_agree(agreement_window,root))
                agree_button.pack(side=tk.LEFT, padx=10)

                decline_button = tk.Button(button_frame, text="Decline", command=lambda: self.on_decline(agreement_window))
                decline_button.pack(side=tk.RIGHT, padx=10)
                #阻塞主线程，直到所有窗口都被销毁
                root.mainloop()   
            else:
                expiry_date_str=json_activation["expiry_date_str"]
                self.show_dialog(f"Program is within the valid period until {expiry_date_str}. This program has expired.")  
                #阻塞主线程，直到所有窗口都被销毁
                root.mainloop()         
                            
        else:
            print(json_activation["status"])
            print(json_activation["error"])     
            self.show_dialog(str(json_activation["status"])+","+str(json_activation["error"]))  
            #阻塞主线程，直到所有窗口都被销毁
            root.mainloop()                 
        
    # 创建一个按钮来显示对话框
    def show_dialog(self,msg):
        messagebox.showinfo("Message", msg)
        self.on_close()

    def on_agree(self,agreement_window,root):
        #messagebox.showinfo("Agreement Accepted", "You have agreed to the terms.")
        agreement_window.destroy()
        #退出主事件循环而不销毁主窗口，然后在主程序中继续执行代码
        root.quit()

    def on_decline(self,agreement_window):
        #messagebox.showwarning("Agreement Declined", "You have declined to agree.")
        self.on_close()

    def close_batch_file(self):
        if platform.system() == "Windows":
            # 关闭当前启动的批处理文件 (Windows)
            subprocess.run("taskkill /f /im cmd.exe", shell=True)
        else:
            # 关闭当前终端会话 (Unix)
            pid = os.getppid()  # 获取父进程ID
            os.kill(pid, signal.SIGTERM)

    def on_close(self):
        self.close_batch_file() #杀死进程
        self.close_current_process()#关闭当前进程
        sys.exit()  # 终止程序

    def close_current_process(self):
        # 获取当前进程ID
        pid = os.getpid()
        if platform.system() == "Windows":
            # 关闭当前进程（Windows）
            os.system(f"taskkill /f /pid {pid}")
        else:
            # 关闭当前进程（Unix）
            os.kill(pid, signal.SIGTERM)

    # 免责申明内容(英文前排和空格)
    def getDisclaimer(self):
        #三重引号（"""或'''）来定义多行字符串
        text = """
DISCLAIMER

Last updated: March 9, 2025

1. NO WARRANTY
The software is provided "as is" without any express or implied warranties, including but not limited to merchantability, fitness for a particular purpose, or noninfringement. The author does not guarantee that the software will meet your requirements or operate without errors or interruptions. You assume all risks associated with its use.

2. LIMITATION OF LIABILITY
To the maximum extent permitted by applicable law, the author shall not be liable for any direct, indirect, incidental, special, or consequential damages (including loss of data, profits, or business interruption) arising from the use of this software, even if advised of such possibilities.

3. THIRD-PARTY CONTENT
The software may link to third-party content or services not controlled by the author. The author is not responsible for their accuracy, legality, or reliability. Use of such content is at your own risk.

4. APPLICABLE LAW
This disclaimer is governed by the laws of the People's Republic of China. All other warranties, express or implied, are excluded to the fullest extent permitted by law.

5. CHANGES AND TERMINATION
The author reserves the right to modify or terminate the software at any time without notice and shall not be liable for any resulting loss or inconvenience. No user data will be retained after termination.

6. LICENSE TERMS
This software includes the ComfyUI open source model, licensed under the GNU General Public License v3.0 by https://github.com/comfyanonymous/ComfyUI. See https://github.com/comfyanonymous/ComfyUI/blob/master/LICENSE for details.

By using this software, you agree to this disclaimer. For questions, contact: oldwangsailab@gmail.com
        """
        return text


if __name__=="__main__":
    app=AppStart()
