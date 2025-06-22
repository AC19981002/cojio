import os
import faiss
import numpy as np
import glob_config
from utils.logutil import logutil
from utils.single_base import Singleton

FAISS_INDEX_PATH = os.path.join(glob_config.config.local_cache_dir, 'faiss_index.index')
VECTOR_DIM = glob_config.config.embedding_model_dim  # 向量维度，可根据实际情况修改

class FaissOperator(metaclass=Singleton):
    def __init__(self):
        self.index_path = FAISS_INDEX_PATH
        self.index = self._load_or_create_index()

    def _load_or_create_index(self):
        """加载已有的索引，若不存在则创建新索引"""
        if os.path.exists(self.index_path):
            try:
                return faiss.read_index(self.index_path)
            except Exception as e:
                logutil.error(f"加载 Faiss 索引时出错: {e}")
        # 创建一个基于 L2 距离的索引，并使用 IndexIDMap 包装
        # TODO: 这里可以根据实际情况选择不同的索引类型，后续优化算法场景·
        index = faiss.IndexIVFFlat(VECTOR_DIM)
        return faiss.IndexIDMap(index)

    def save_index(self):
        """保存索引到文件"""
        try:
            faiss.write_index(self.index, self.index_path)
            logutil.info("Faiss 索引已保存")
        except Exception as e:
            logutil.error(f"保存 Faiss 索引时出错: {e}")

    def add_vectors(self, vectors, ids):
        """
        向 Faiss 索引中添加向量，并指定对应的 id

        :param vectors: 二维 numpy 数组，形状为 (n, d)，n 是向量数量，d 是向量维度
        :param ids: 一维 numpy 数组，形状为 (n,)，包含每个向量对应的 int 类型 id
        :return: 添加的向量数量
        """
        if not isinstance(vectors, np.ndarray):
            vectors = np.array(vectors).astype('float32')
        if not isinstance(ids, np.ndarray):
            ids = np.array(ids).astype('int64')
        try:
            self.index.add_with_ids(vectors, ids)
            self.save_index()
            return len(vectors)
        except Exception as e:
            logutil.error(f"添加向量到 Faiss 索引时出错: {e}")
            return 0

    def query_vector(self, query_vector, k=5):
        """
        单个查询与查询向量最相似的 k 个向量

        :param query_vector: 一维 numpy 数组，形状为 (d,)，d 是向量维度
        :param k: 要返回的最相似向量数量
        :return: 包含 (距离, id) 元组的列表
        """
        if not isinstance(query_vector, np.ndarray):
            query_vector = np.array(query_vector).astype('float32')
        # 将一维向量转换为二维数组
        query_vector = query_vector.reshape(1, -1)
        try:
            distances, indices = self.index.search(query_vector, k)
            # 将结果转换为 (距离, id) 元组的列表
            results = list(zip(distances[0], indices[0]))
            return results
        except Exception as e:
            logutil.error(f"查询 Faiss 索引时出错: {e}")
            return []

    def close(self):
        """关闭 Faiss 操作，保存索引"""
        self.save_index()

if __name__ == "__main__":
    faiss_operator = FaissOperator()
    # 生成一些示例向量
    sample_vectors = np.random.rand(10, VECTOR_DIM).astype('float32')
    # 生成对应的 id
    sample_ids = np.arange(10).astype('int64')
    print(f"添加的向量数量: {faiss_operator.add_vectors(sample_vectors, sample_ids)}")
    # 生成一个查询向量
    query_vector = np.random.rand(VECTOR_DIM).astype('float32')
    results = faiss_operator.query_vector(query_vector, k=3)
    print("查询结果 (距离, id):", results)
    faiss_operator.close()