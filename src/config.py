"""
项目配置文件
"""

import os
from typing import Optional


class Config:
    """项目配置类"""

    # API 配置
    QWEN_API_KEY: str = os.getenv('QWEN_API_KEY', 'sk-36af5e3baa1e46239a130cc453dd8a77')
    QWEN_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    QWEN_TIMEOUT: int = 30

    # 模型配置
    MODEL_NAME: str = "qwen-vl-plus"
    MAX_TOKENS: int = 1500
    TEMPERATURE: float = 0.1

    # 路径配置
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    RESULTS_DIR: str = os.path.join(BASE_DIR, "results")
    TEST_IMAGES_DIR: str = os.path.join(BASE_DIR, "tests")

    # 服务器配置
    HOST: str = "127.0.0.1"
    PORT: int = 5000
    DEBUG: bool = True

    # 允许的图片格式
    ALLOWED_EXTENSIONS: set = {'.jpg', '.jpeg', '.png', '.gif'}

    # 最大文件大小 (16MB)
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024

    @classmethod
    def init_directories(cls):
        """初始化必要的目录"""
        dirs = [cls.UPLOAD_DIR, cls.RESULTS_DIR, cls.TEST_IMAGES_DIR]
        for dir_path in dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    @classmethod
    def allowed_file(cls, filename: str) -> bool:
        """
        检查文件扩展名是否允许

        Args:
            filename: 文件名

        Returns:
            bool: 是否允许
        """
        return '.' in filename and \
               os.path.splitext(filename)[1].lower() in cls.ALLOWED_EXTENSIONS