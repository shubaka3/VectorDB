from .models import EmbeddingModel
from .config import EmbeddingConfig
from .utils import setup_logger, ensure_list, preprocess_text  # import thêm preprocess_text
from .store import MemoryStore

class TextEncoder:
    def __init__(self, config: EmbeddingConfig = EmbeddingConfig()):
        self.config = config
        self.logger = setup_logger(level=config.log_level)
        self.model = EmbeddingModel(config.model_name, config.device)
        self.memory_store = MemoryStore()

    def get_vector(self, text: str):
        # dùng get_vectors rồi lấy phần tử đầu tiên
        return self.get_vectors([text])[0]

    def get_vectors(self, texts: list[str]):
        try:
            texts = ensure_list(texts)
            # Tiền xử lý từng câu trước khi embedding
            texts = [preprocess_text(t) for t in texts]

            self.memory_store.add(texts)
            vectors = self.model.encode(
                texts,
                convert_to_tensor=self.config.convert_to_tensor,
                batch_size=self.config.batch_size
            )
            if hasattr(vectors, "tolist"):
                return vectors.tolist()
            return vectors
        except Exception as e:
            self.logger.error(f"Failed to encode texts: {e}")
            raise RuntimeError("Encoding failed.")

    def decode(self, idx: int):
        return self.memory_store.get(idx)
