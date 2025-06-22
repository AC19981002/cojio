import glob_config
from core.code_embedding.base_encoder import BaseCodeEncoder


class TestCodeEncoder(BaseCodeEncoder):
    def encode(self, code):
        """实现抽象方法 encode，调用 get_embeddings 方法生成单段代码的嵌入向量"""
        return self.get_embeddings([code])[0]

def test_code_embedding():
    # 初始化编码器
    encoder = TestCodeEncoder()

    # 示例代码列表
    sample_codes = [
        "def add(a, b):\n    return a + b",
        "def multiply(x, y):\n    return x * y"
    ]

    # 生成嵌入向量
    embeddings = encoder.get_embeddings(sample_codes)

    # 测试单段代码嵌入
    single_code_embedding = encoder.encode(sample_codes[0])

    # 输出多段代码及其对应的嵌入向量
    for i, (code, embedding) in enumerate(zip(sample_codes, embeddings)):
        print(f"代码 {i + 1}:")
        print(code)
        print(f"代码 {i + 1} 对应的嵌入向量:")
        print(embedding)
        print("----------------------")

    # 输出单段代码及其对应的嵌入向量
    print("单段代码:")
    print(sample_codes[0])
    print("单段代码对应的嵌入向量:")
    print(single_code_embedding)


if __name__ == "__main__":
    test_code_embedding()