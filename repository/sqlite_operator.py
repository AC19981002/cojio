import os
import sqlite3

import glob_config
from utils.logutil import logutil
from utils.single_base import Singleton

DB_PATH = os.path.join(glob_config.config.local_cache_dir, 'code_db.db')
DB_TABLE_NAME = "code_table"

class DbOperator(metaclass=Singleton):
    def __init__(self):
        self.db_path = DB_PATH
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()


    def _create_table(self):
        self.cursor.execute(f'''
         CREATE TABLE IF NOT EXISTS {DB_TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')

    def save_code_to_db(self, code,type):
        """将代码保存到 SQLite 数据库"""
        if self.conn is None:
            logutil.error("无法保存代码到数据库，sqlite3 连接未建立。")
            return None
        cursor = self.conn.cursor()
        try:
            # 修改插入语句，同时插入 code 和 type 字段
            cursor.execute(f"""
                INSERT INTO {DB_TABLE_NAME} (code, "type") VALUES (?, ?)
                """, (code, type))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            # 插入失败时回滚事务
            self.conn.rollback()
            logutil.error(f"保存代码到数据库时出错: {e}")
            return None

    def batch_save_codes_to_db(self, code_list):
        """
        批量将代码保存到 SQLite 数据库

        :param code_list: 包含 (code, type) 元组的列表
        :return: 插入的行的 ID 列表，顺序与 code_list 一致
        """
        if self.conn is None:
            logutil.error("无法批量保存代码到数据库，sqlite3 连接未建立。")
            return []
        cursor = self.conn.cursor()
        try:
            # 使用 RETURNING 子句返回插入行的 id
            cursor.execute(f"""
                INSERT INTO {DB_TABLE_NAME} (code, "type") 
                VALUES {','.join('(?, ?)' for _ in code_list)}
                RETURNING id
            """, [item for sublist in code_list for item in sublist])
            self.conn.commit()
            # 获取插入行的 ID 列表
            last_row_ids = [row[0] for row in cursor.fetchall()]
            return last_row_ids
        except Exception as e:
            self.conn.rollback()
            logutil.error(f"批量插入代码到数据库时出错: {e}")
            return []

    def batch_query_codes_by_ids(self, id_list):
        """
        根据 id 列表批量查询代码记录

        :param id_list: 包含 id 的列表
        :return: 包含查询结果的列表，每个结果为 (id, code, type) 元组
        """
        if not id_list:
            return []
        if self.conn is None:
            logutil.error("无法批量查询代码，sqlite3 连接未建立。")
            return []
        cursor = self.conn.cursor()
        try:
            # 构建 IN 子句的占位符
            placeholders = ', '.join(['?'] * len(id_list))
            query = f"SELECT id, code, \"type\" FROM {DB_TABLE_NAME} WHERE id IN ({placeholders})"
            cursor.execute(query, id_list)
            results = cursor.fetchall()
            return results
        except Exception as e:
            logutil.error(f"批量查询代码时出错: {e}")
            return []

    def query_all_codes(self):
        """
        查询数据库中所有的代码记录

        :return: 包含查询结果的列表，每个结果为 (id, code, type) 元组
        """
        if self.conn is None:
            logutil.error("无法查询所有代码，sqlite3 连接未建立。")
            return []
        cursor = self.conn.cursor()
        try:
            query = f"SELECT id, code, \"type\" FROM {DB_TABLE_NAME}"
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            logutil.error(f"查询所有代码时出错: {e}")
            return []

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logutil.info("数据库连接已关闭。")

if __name__ == "__main__":
    db_operator = DbOperator()
    print(db_operator.save_code_to_db("print('hello world')", "java"))
    print(db_operator.query_all_codes())
    db_operator.close()