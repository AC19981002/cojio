from dataclasses import dataclass

import glob_config
from utils.file_filters import file_filter
from utils.single_base import Singleton

class GlobalContext(metaclass=Singleton):
    __source_code_dirs = glob_config.config.source_code_dirs
    __java_files = []
    __kotlin_files = []
    __xml_files = []

    def __init__(self):
        self.__java_files = file_filter.get_java_files(self.__source_code_dirs)
        self.__kotlin_files = file_filter.get_kotlin_files(self.__source_code_dirs)
        self.__xml_files = file_filter.get_xml_files(self.__source_code_dirs)

    def get_java_files(self):
        """获取 Java 文件列表"""
        return self.__java_files

    def get_kotlin_files(self):
        """获取 Kotlin 文件列表"""
        return self.__kotlin_files

    def get_xml_files(self):
        """获取 XML 文件列表"""
        return self.__xml_files

global_context = GlobalContext()