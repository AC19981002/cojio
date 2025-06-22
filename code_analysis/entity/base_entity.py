from abc import abstractmethod


class BaseEntity:

    _node_chunk_size = None

    @abstractmethod
    def set_node_chunk_size(self):
        pass