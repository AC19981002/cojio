import os

import glob_config
from utils.single_base import Singleton


class FileFilter(metaclass=Singleton):
    def get_java_files(self, path):
        """
        检查指定路径是否存在，若存在则返回该路径下以 .java 结尾的文件列表。

        :param path: 要检查的文件或目录路径
        :return: 包含 .java 结尾文件的列表，若路径不存在则返回空列表
        """
        java_files = []
        if os.path.exists(path):
            if os.path.isfile(path) and path.endswith('.java'):
                java_files.append(path)
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.java'):
                            java_files.append(os.path.join(root, file))
        return java_files

    def get_kotlin_files(self, path):
        """
        检查指定路径是否存在，若存在则返回该路径下以 .kt 结尾的文件列表。

        :param path: 要检查的文件或目录路径
        :return: 包含 .kt 结尾文件的列表，若路径不存在则返回空列表
        """
        kotlin_files = []
        if os.path.exists(path):
            if os.path.isfile(path) and path.endswith('.kt'):
                kotlin_files.append(path)
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.kt'):
                            kotlin_files.append(os.path.join(root, file))
        return kotlin_files

    def get_xml_files(self, path):
        """
        检查指定路径是否存在，若存在则返回该路径下以 .xml 结尾的文件列表。

        :param path: 要检查的文件或目录路径
        :return: 包含 .xml 结尾文件的列表，若路径不存在则返回空列表
        """
        xml_files = []
        if os.path.exists(path):
            if os.path.isfile(path) and path.endswith('.xml'):
                xml_files.append(path)
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.xml'):
                            xml_files.append(os.path.join(root, file))
        return xml_files


file_filter = FileFilter()

if __name__ == "__main__":
    # 打印 source_code_dirs 配置
    print(glob_config.config)
    print({"source_code_dirs": glob_config.config.source_code_dirs})
    java_files = file_filter.get_java_files(glob_config.config.source_code_dirs)
    print(java_files)