import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Embedding.encoder import TextEncoder
from Embedding.config import EmbeddingConfig

config = EmbeddingConfig(
    model_name="all-MiniLM-L6-v2",
    dim=384,
    device="cpu",
    log_level="INFO"
)

encoder = TextEncoder(config)

print("Nhập câu để tạo embedding, gõ 'exit' để thoát.")

while True:
    text = input("Nhập câu: ").strip()
    if text.lower() == "exit":
        print("Thoát chương trình.")
        break
    if not text:
        print("Vui lòng nhập câu hợp lệ.")
        continue

    vector = encoder.get_vector(text)
    print(f"Vector có {len(vector)} chiều, 5 giá trị đầu: {vector[:5]}")
    # Lưu text vào memory store và kiểm tra decode
    idx = len(encoder.memory_store.all()) - 1
    print(f"Decode lại index {idx}: {encoder.decode(idx)}\n")
