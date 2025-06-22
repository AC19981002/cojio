from core.code_embedding.base_encoder import BaseCodeEncoder
from utils.single_base import Singleton


class JavaEncoder(BaseCodeEncoder, metaclass=Singleton):
    def __init__(self):
        super().__init__()
    def encode(self, code):
        return self.get_embeddings(code)

java_encoder = JavaEncoder()