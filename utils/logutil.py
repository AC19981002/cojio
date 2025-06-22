from loguru import logger
import os
from glob_config import config
from pathlib import Path

from utils.single_base import Singleton


class LogUtil(metaclass=Singleton):
    def __init__(self):
        utils_dir = Path(__file__).parent
        cojio_dir = utils_dir.parent
        log_dir = str(cojio_dir / config.log_dir)
        log_file = config.log_file
        rotation = config.log_rotation
        retention = config.log_retention
        log_level = config.log_level
        # 确保日志目录存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_path = os.path.join(log_dir, log_file)

        # 添加文件输出处理器
        file_handler_id = logger.add(
            sink=log_path,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="INFO",
            rotation=rotation,
            retention=retention,
            encoding="utf-8"
        )
        print(f"文件日志处理器添加成功，ID: {file_handler_id}")

    def debug(self, message):
        """记录调试级别的日志"""
        logger.debug(message)

    def info(self, message):
        """记录信息级别的日志"""
        logger.info(message)

    def warning(self, message):
        """记录警告级别的日志"""
        logger.warning(message)

    def error(self, message):
        """记录错误级别的日志"""
        logger.error(message)

    def critical(self, message):
        """记录严重错误级别的日志"""
        logger.critical(message)


# 创建单例实例
logutil = LogUtil()

if __name__ == "__main__":
    logutil.info("这是一条测试信息")
    logutil.debug("这是一条测试调试信息")
    logutil.warning("这是一条测试警告信息")