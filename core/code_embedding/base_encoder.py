from abc import abstractmethod
import torch
from transformers import AutoTokenizer, AutoModel

import glob_config

MODEL_NAME = glob_config.config.embedding_model
MODEL_DIM = glob_config.config.embedding_model_dim
MODEL_DIM_TYPE = glob_config.config.embedding_model_dim_type
MODEL_DEVICE = glob_config.config.embedding_model_device

class BaseCodeEncoder:

    def __init__(self):
        """
        初始化 CodeT5 模型和分词器
        :param model_name: 预训练模型的名称，默认为 Salesforce/codet5-small
        :param device: 运行模型的设备，默认为 cpu
        """
        self.device = torch.device(MODEL_DEVICE)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModel.from_pretrained(MODEL_NAME).to(MODEL_DEVICE)
        self.model.eval()

    def get_embeddings(self, codes):
        """
        生成多段代码的嵌入向量

        :param codes: 输入的代码列表
        :return: 代码的嵌入向量列表，每个元素为 NumPy 数组
        """
        # 编码输入
        inputs = self.tokenizer(codes, return_tensors='pt', truncation=True, padding=True).to(self.device)
        with torch.no_grad():
            # 仅使用编码器获取输出
            encoder_outputs = self.model.encoder(**inputs)
            last_hidden_state = encoder_outputs.last_hidden_state
            embeddings = last_hidden_state.mean(dim=1).cpu().numpy()
        return embeddings

    @abstractmethod
    def encode(self, codes):
        # 这里可以添加代码嵌入的逻辑
        # 这里只是一个示例，实际实现可能会更加复杂
        pass


