"""配置管理模块"""

import os
import json
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(override=True)

class Settings:
    """配置类"""
    def __init__(self):
        # API配置
        self.api_base_url = os.getenv('OPENAI_API_BASE_URL')
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # 模型配置
        self.simple_image_model = os.getenv('SIMPLE_IMAGE_MODEL')
        self.simple_solver_model = os.getenv('SIMPLE_SOLVER_MODEL')
        self.complex_image_model = os.getenv('COMPLEX_IMAGE_MODEL')
        self.complex_solver_model = os.getenv('COMPLEX_SOLVER_MODEL')
        
        # 验证配置完整性
        self._validate_settings()
        
        # Gradio认证配置
        self.auth_enabled = bool(os.getenv('GRADIO_AUTH'))
        self.auth_data = self._load_auth_data()

    def _validate_settings(self):
        """验证所有必需的配置项"""
        required_vars = [
            ('OPENAI_API_BASE_URL', self.api_base_url),
            ('OPENAI_API_KEY', self.api_key),
            ('SIMPLE_IMAGE_MODEL', self.simple_image_model),
            ('SIMPLE_SOLVER_MODEL', self.simple_solver_model),
            ('COMPLEX_IMAGE_MODEL', self.complex_image_model),
            ('COMPLEX_SOLVER_MODEL', self.complex_solver_model),
        ]
        
        missing_vars = [name for name, value in required_vars if not value]
        
        if missing_vars:
            raise ValueError(
                f"缺少必要的环境变量：{', '.join(missing_vars)}。"
                "请检查.env文件配置。"
            )

    def _load_auth_data(self):
        """加载认证数据"""
        auth_data = os.getenv('GRADIO_AUTH')
        if not auth_data:
            return None
            
        try:
            return json.loads(auth_data)
        except json.JSONDecodeError:
            logging.error("GRADIO_AUTH 环境变量格式错误")
            return None

    def verify_auth(self, username: str, password: str) -> bool:
        """验证用户名和密码"""
        if not self.auth_enabled or not self.auth_data:
            return False
            
        return any(
            cred.get('username') == username and 
            cred.get('password') == password
            for cred in self.auth_data
        )

    def get_model_info(self, is_complex_mode: bool) -> tuple:
        """根据模式获取对应的模型配置"""
        if is_complex_mode:
            return self.complex_image_model, self.complex_solver_model
        return self.simple_image_model, self.simple_solver_model

# 创建全局配置实例
settings = Settings()