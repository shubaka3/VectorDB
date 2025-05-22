from sentence_transformers import SentenceTransformer

_model_cache = {}  # Bộ nhớ RAM cache models theo tên

class EmbeddingModel:
    def __init__(self, model_name: str, device: str = "cpu"):
        self.model_name = model_name
        cache_key = f"{model_name}_{device}"

        if cache_key in _model_cache:
            self.model = _model_cache[cache_key]
        else:
            model = SentenceTransformer(model_name, device=device)
            _model_cache[cache_key] = model
            self.model = model

    def encode(self, texts, convert_to_tensor=False, batch_size=32):
        return self.model.encode(
            texts,
            convert_to_tensor=convert_to_tensor,
            batch_size=batch_size,
            show_progress_bar=False
        )
