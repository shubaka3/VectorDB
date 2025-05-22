from dataclasses import dataclass

@dataclass
class EmbeddingConfig:
    model_name: str = "all-MiniLM-L6-v2"
    dim: int = 384
    device: str = "cpu"  # hoặc "cuda"
    batch_size: int = 32
    convert_to_tensor: bool = False
    use_cache: bool = True
    log_level: str = "INFO"
