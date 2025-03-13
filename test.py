# conda activate F:\ComfyUI-Caption-Generator\cdvenv
# python test.py

# import transformers
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM

# # 模型路径
# model_id = r"D:\ComfyUI-0.2.7\models\LLM\Meta-Llama-3.1-8B-bnb-4bit"

# # 显式加载 tokenizer 和模型
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForCausalLM.from_pretrained(
#     model_id,
#     torch_dtype=torch.bfloat16,
#     device_map="auto",
# )

# # 创建 pipeline
# pipeline = transformers.pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
# )

# # 定义对话消息
# messages = [
#     {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
#     {"role": "user", "content": "Who are you?"},
# ]

# # 检查并设置聊天模板
# if tokenizer.chat_template is None:
#     # 使用适合 LLaMA 的简单聊天模板
#     chat_template = "{% for message in messages %}{{message['role']}}: {{message['content']}}\n{% endfor %}"
#     tokenizer.chat_template = chat_template

# # 生成输出
# outputs = pipeline(
#     messages,
#     max_new_tokens=256,
# )

# # 打印生成的文本（假设你想要最后一条消息的回复）
# print(outputs[0]["generated_text"][-1]["content"])



# import os

# def get_all_files(directory, extension=None):
#     file_paths = []
    
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             # 如果指定了扩展名，只获取匹配的文件
#             if extension and not file.endswith(extension):
#                 continue
#             abs_path = os.path.abspath(os.path.join(root, file))
#             file_paths.append(abs_path)
    
#     return file_paths

# 使用示例
#directory_path = r"F:\ComfyUI-Caption-Generator\api_server"
#directory_path = r"F:\ComfyUI-Caption-Generator\app"
#directory_path = r"F:\ComfyUI-Caption-Generator\comfy"
# directory_path = r"F:\ComfyUI-Caption-Generator\comfy_execution"
# directory_path = r"F:\ComfyUI-Caption-Generator\comfy_extras"
# directory_path = r"F:\ComfyUI-Caption-Generator\custom_nodes"
# directory_path = r"F:\ComfyUI-Caption-Generator\model_filemanager"
# directory_path = r"F:\ComfyUI-Caption-Generator\script_examples"
# directory_path = r"F:\ComfyUI-Caption-Generator\tests"
# directory_path = r"F:\ComfyUI-Caption-Generator\tests-unit"
# directory_path = r"F:\ComfyUI-Caption-Generator\utils"
# # 获取所有文件
# all_files = get_all_files(directory_path)

# # 只获取特定类型文件（如.py）
# txt_files = get_all_files(directory_path, extension=".py")

# # 打印结果
# # print("所有文件：")
# # for file in all_files:
# #     print(file)

# print("\n只显示.py文件：")
# for file in txt_files:
#     print("\'"+file+"\',")


#调试PyInstaller导入
import sys
import os

print("Python path:", sys.path)
print("Setuptools path:", os.path.exists(r"F:\ComfyUI-Caption-Generator\cdvenv\lib\site-packages\setuptools\_distutils\compilers"))

try:
    import setuptools._distutils.compilers
    print("Import success!")
    print("compilers path:", setuptools._distutils.compilers)
except ImportError as e:
    print("ImportError:", e)

