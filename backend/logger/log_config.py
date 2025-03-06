"""日志配置模块"""

import os
import json
import logging
from datetime import datetime
from typing import Any, List, Dict, Optional, Union

class LogConfig:
    """日志配置类"""
    def __init__(self, log_file: str = 'solver.log'):
        """
        初始化日志配置
        
        Args:
            log_file: 日志文件名
        """
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 配置日志记录
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)

    def log_api_interaction(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        response: Optional[str] = None,
        error: Optional[str] = None
    ) -> str:
        """
        记录API交互日志
        
        Args:
            model: 使用的模型名称
            messages: 发送的消息列表
            response: API响应内容
            error: 错误信息（如果有）
            
        Returns:
            str: 格式化的日志字符串
        """
        # 清理消息中的图片数据
        clean_messages = self._clean_messages(messages)
        
        # 构建日志数据
        log_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": model,
            "messages": clean_messages,
            "response": response if not error else str(error)
        }
        
        # 转换为格式化的JSON字符串
        log_str = json.dumps(log_data, ensure_ascii=False, indent=2)
        self.logger.info(log_str)
        return log_str

    def _clean_messages(
        self,
        messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        清理消息中的图片数据
        
        Args:
            messages: 原始消息列表
            
        Returns:
            List[Dict[str, Any]]: 清理后的消息列表
        """
        cleaned_messages = []
        
        for msg in messages:
            if isinstance(msg["content"], list):
                # 处理包含图片的消息
                cleaned_content = []
                for item in msg["content"]:
                    if item["type"] == "image_url":
                        cleaned_content.append({
                            "type": "image_url",
                            "image_url": {"url": "[图片数据已省略]"}
                        })
                    else:
                        cleaned_content.append(item)
                cleaned_messages.append({
                    "role": msg["role"],
                    "content": cleaned_content
                })
            else:
                cleaned_messages.append(msg)
                
        return cleaned_messages

    def log_error(self, error_msg: str, model: Optional[str] = None) -> None:
        """
        记录错误日志
        
        Args:
            error_msg: 错误信息
            model: 相关的模型名称（可选）
        """
        if model:
            error_msg = f"模型 {model} 错误: {error_msg}"
        self.logger.error(error_msg)

# 创建全局日志实例
logger = LogConfig()