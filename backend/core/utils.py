"""工具函数模块"""

import os
import base64
import io
from datetime import datetime
from PIL import Image
from typing import Union, Optional

def encode_image(image: Union[str, Image.Image]) -> str:
    """
    将图片编码为base64格式
    
    Args:
        image: 图片文件路径或PIL Image对象
        
    Returns:
        str: base64编码的图片数据
    """
    if isinstance(image, str):  # 如果是文件路径
        with open(image, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    else:  # 如果是PIL.Image对象
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

def convert_formula_format(text: str) -> str:
    """
    转换公式格式，将\\[...\\]转换为$$...$$，将\\(...\\)转换为$...$
    
    Args:
        text: 包含LaTeX公式的文本
        
    Returns:
        str: 转换后的文本
    """
    result = ""
    i = 0
    while i < len(text):
        if text[i:i+2] == "\\[":
            result += "$$"
            i += 2
            while i < len(text) and text[i:i+2] != "\\]":
                result += text[i]
                i += 1
            if i < len(text):
                result += "$$"
                i += 2
        elif text[i:i+2] == "\\(":
            result += "$"
            i += 2
            while i < len(text) and text[i].isspace():
                i += 1
            formula_content = ""
            while i < len(text) and text[i:i+2] != "\\)":
                formula_content += text[i]
                i += 1
            result += formula_content.strip()
            if i < len(text):
                result += "$"
                i += 2
        else:
            result += text[i]
            i += 1
    return result

import zipfile
import tempfile

def save_solution(
    text_input: str,
    image: Union[str, Image.Image, None],
    solution_content: str,
    output_dir: str = "solutions"
) -> tuple[str, str]:
    """
    保存解答结果到文件，并打包成zip
    
    Args:
        text_input: 题目文本
        image: 题目图片（可选）
        solution_content: 解答内容
        output_dir: 输出目录
        
    Returns:
        tuple[str, str]: (zip文件路径, zip文件名)
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存图片（如果有）
    if image is not None:
        image_filename = f"image_{timestamp}.png"
        image_path = os.path.join(output_dir, image_filename)
        if isinstance(image, str):
            Image.open(image).save(image_path)
        else:
            image.save(image_path)
            
        # 处理图片引用
        image_content = f"![题目图片](./{image_filename})\n\n"
    else:
        image_content = ""
    
    # 生成解答文件名
    filename = f"solution_{timestamp}.md"
    file_path = os.path.join(output_dir, filename)
    
    # 生成解答内容
    content = [
        "# 理论力学题目求解\n\n",
        "## 原题\n\n",
        text_input + "\n\n",
        image_content,
        convert_formula_format(solution_content)
    ]
    
    # 写入文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("".join(content))
    
    # 创建临时zip文件
    zip_filename = f"solution_{timestamp}.zip"
    zip_path = os.path.join(output_dir, zip_filename)
    
    # 压缩文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加markdown文件
        zipf.write(file_path, os.path.basename(file_path))
        # 如果有图片，也添加到zip中
        if image is not None:
            zipf.write(image_path, os.path.basename(image_path))
    
    return zip_path, zip_filename