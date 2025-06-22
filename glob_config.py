import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# 获取项目 lib 目录的相对路径
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib\\data")
# 确保 lib 目录存在
os.makedirs(lib_dir, exist_ok=True)

class AppConfig(BaseSettings):
    # 大模型交互相关配置
    openai_api_key: str = "your_openai_api_key"
    # 向量数据库相关配置

    # SQLlite&&Faiss本地存储相关配置
    local_cache_dir: str = lib_dir

    # 日志相关配置
    log_dir: str = "logs"
    log_file: str = "app.log"
    log_rotation: str = "100 MB"
    log_retention: str = "7 days"
    log_level: str = "DEBUG"

    # embedding 模型相关配置
    embedding_model: str = 'Salesforce/codet5-small'
    embedding_model_dim: int = 1024
    embedding_model_dim_type: str = "float32"
    embedding_model_device: str = "cpu"

    # source code 相关配置
    source_code_dirs: str = "D:\\Download\\code\\code\\bluebells"


config = AppConfig()

if __name__ == "__main__":
    print(config)