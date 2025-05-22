import logging
import re

def setup_logger(name="embedding", level="INFO"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def ensure_list(val):
    return val if isinstance(val, list) else [val]

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # loại bỏ dấu câu
    text = re.sub(r"\s+", " ", text).strip()  # loại bỏ khoảng trắng thừa
    return text