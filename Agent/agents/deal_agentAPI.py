# agents/deal_agent.py

import sys
import re

sys.path.append(r"D:\VectorDB")  # nếu cần thêm thư viện ngoài

from llms.llm_handler import query_llm
from Milvus import milvus_utils as mvs
from Embedding.encoder import TextEncoder
from Embedding.config import EmbeddingConfig
from utils.sql_executor import execute_query

encoder = TextEncoder(EmbeddingConfig(
    model_name="all-MiniLM-L6-v2",
    dim=384,
    device="cpu",
    log_level="INFO"
))

def extract_sql_from_response(response):
    match = re.search(r"<query>(.*?)</query>", response, re.DOTALL)
    return match.group(1).strip() if match else None

def handle_user_query(user_input, user_id="user", collection_name="default", mode="document"):
    vector = encoder.get_vector(user_input)
    collection = mvs.get_collection(collection_name)
    if collection is None:
        return f"❗ Collection '{collection_name}' không tồn tại."

    # --- Mode: DOCUMENT ---
    if mode == "document":
        results = mvs.search_topk1(collection, vector)
        context = "\n".join([hit["text"] for hit in results])
        prompt = f"Prompt:\n{context}\n\nQuestion:\n{user_input}"
        llm_response = query_llm(prompt, user_id)
        return llm_response

    # --- Mode: QUERY ---
    elif mode == "query":
        results = mvs.search_topk1(collection, vector)
        context = "\n".join([hit["text"] for hit in results])
        prompt = f"Prompt:\n{context}\n\nnQuestion:\n{user_input}"
        llm_response = query_llm(prompt, user_id)

        sql_query = extract_sql_from_response(llm_response)
        if not sql_query:
            return "❗ Không tìm thấy câu lệnh SQL trong phản hồi AI."

        try:
            result = execute_query(sql_query)
            return result  # Trả về dữ liệu thô (cho client hiển thị)
        except Exception as e:
            return f"❌ Lỗi khi thực thi SQL: {e}"

    # --- Mode: ASK ---
    elif mode == "ask":
        # Giai đoạn 1: chỉ tạo SQL từ câu hỏi
        prompt = f"Viết câu lệnh SQL để trả lời: {user_input}"
        llm_response = query_llm(prompt, user_id)
        sql_query = extract_sql_from_response(llm_response)

        if not sql_query:
            return "❗ Không tìm thấy câu lệnh SQL trong phản hồi AI."

        # Gửi câu query này sang .NET backend để thực thi SQL (phía client xử lý tiếp)
        return {
            "sql_query": sql_query,
            "message": "Gửi query cho backend để thực thi, sau đó gọi lại API /ask/followup để có kết quả cuối."
        }

    return "❗ Chế độ không hợp lệ (document/query/ask)."

def handle_followup_ask(data: str, user_input: str, user_id="user"):
    # Giai đoạn 2: AI trả lời dựa trên dữ liệu SQL backend trả về
    prompt = f"Prompt:\n{data}\n\nnQuestion:\n{user_input}"
    types = "ask"
    return query_llm(prompt, user_id,types)
