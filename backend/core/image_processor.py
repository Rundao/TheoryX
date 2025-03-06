#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TheoryX Solver - AI-powered Theoretical Mechanics Problem Solver
Copyright (C) 2024 Rundao

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Generator, Tuple, Any, Optional
from openai import OpenAI

from backend.config.settings import settings
from backend.logger.log_config import logger
from backend.core.utils import encode_image
from prompts.image_prompts import IMAGE_SYSTEM_PROMPT, get_image_prompt

class ImageProcessor:
    """图片处理类"""
    def __init__(self):
        """初始化OpenAI客户端"""
        self.client = OpenAI(
            base_url=settings.api_base_url,
            api_key=settings.api_key,
        )

    def get_image_description(
        self,
        text_input: str,
        image: Any,
        is_complex_mode: bool = False
    ) -> Generator[str | Tuple[str, str], None, None]:
        """
        获取图片描述（流式输出）
        
        Args:
            text_input: 题目文本
            image: 题目图片
            is_complex_mode: 是否使用复杂模式
            
        Yields:
            str | Tuple[str, str]: 描述内容或(描述内容, 日志)
        """
        # 编码图片
        base64_image = encode_image(image)
        
        # 获取对应模式的模型
        image_model, _ = settings.get_model_info(is_complex_mode)
        
        # 构建消息
        messages = [
            {
                "role": "system",
                "content": IMAGE_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": get_image_prompt(text_input)
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        try:
            # 创建流式请求
            stream = self.client.chat.completions.create(
                model=image_model,
                messages=messages,
                stream=True,
                temperature=0.01
            )
            
            # 处理流式响应
            description = []
            collected_chunks = []
            
            for chunk in stream:
                if (hasattr(chunk, 'choices') and
                    chunk.choices and
                    hasattr(chunk.choices[0], 'delta') and
                    hasattr(chunk.choices[0].delta, 'content') and
                    chunk.choices[0].delta.content is not None):
                    
                    content = chunk.choices[0].delta.content
                    collected_chunks.append(content)
                    description.append(content)
                    yield "".join(description)
            
            if not collected_chunks:
                raise Exception("未收到模型响应")
                
            # 生成最终描述和日志
            final_description = "".join(description)
            log_str = logger.log_api_interaction(image_model, messages, final_description)
            yield final_description, log_str
            
        except Exception as e:
            error_msg = f"图片处理出错：{str(e)}"
            log_str = logger.log_api_interaction(image_model, messages, None, error_msg)
            logger.log_error(str(e), image_model)
            yield error_msg, log_str

# 创建全局图片处理器实例
image_processor = ImageProcessor()