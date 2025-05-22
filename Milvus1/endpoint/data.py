import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    # dẫn đến thư mục cùng cấp với milvus1
from fastapi import APIRouter
from pydantic import BaseModel
import milvus_utils_api_online as mvs
from Embedding.encoder import TextEncoder
from Embedding.config import EmbeddingConfig


encoder = TextEncoder(EmbeddingConfig(
    model_name="all-MiniLM-L6-v2",
    dim=384,
    device="cpu",
    log_level="INFO"
))

router = APIRouter()

class TextInput(BaseModel):
    collection_name: str
    text: str

@router.post("/insert")
def insert_text(data: TextInput):
    col = mvs.get_collection(data.collection_name)
    if not col:
        return {"error": "Collection không tồn tại"}
    vector = encoder.get_vector(data.text)
    mvs.insert_vector(col, vector, data.text)
    return {"message": "Đã thêm văn bản."}

@router.post("/search")
def search_text(data: TextInput):
    col = mvs.get_collection(data.collection_name)
    if not col:
        return {"error": "Collection không tồn tại"}
    vector = encoder.get_vector(data.text)
    results = mvs.search_topk(col, vector)
    return {"results": results}
