# agents/deal_agent.py

import sys
import os

# Thêm thư mục cha chứa thư viện 'Embedding' vào sys.path
sys.path.append(r"D:\VectorDB")

from llms.llm_handler import query_llm
from Milvus import milvus_utils as mvs
from Embedding.encoder import TextEncoder
from Embedding.config import EmbeddingConfig
from utils.sql_executor import execute_query  # Tạo file này để chạy SQL
import re

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

    if mode == "document":
        # Lấy dữ liệu liên quan theo vector user_input
        results = mvs.search_topk1(collection, vector)
        context = "\n".join([hit["text"] for hit in results])
        prompt = f"Ngữ cảnh:\n{context}\n\nCâu hỏi:\n{user_input}"
        print(f"Dữ liệu từ vector: {results}")
        llm_response = query_llm(prompt, user_id)
        print(f"Phản hồi của AI: '{llm_response}'")
        return llm_response

    elif mode == "query":
        # Lấy dữ liệu liên quan theo user_input (lấy vector user_input)
        results = mvs.search_topk1(collection, vector)
        context = "\n".join([hit["text"] for hit in results])
        prompt = f"Ngữ cảnh:\n{context}\n\nCâu hỏi:\n{user_input}"
        print(f"Dữ liệu từ vector: {results}")
        llm_response = query_llm(prompt, user_id)
        print(f"Phản hồi của AI: '{llm_response}'")

        # Giả sử AI trả về 1 câu hỏi SQL trong response -> trích xuất SQL
        sql_query = extract_sql_from_response(llm_response)
        if not sql_query:
            return "❗ Không tìm thấy câu lệnh SQL trong phản hồi AI."

        try:
            # Thực thi câu SQL AI trả về
            return execute_query(sql_query)
        except Exception as e:
            return f"❌ Lỗi khi thực thi SQL: {e}"

    elif mode == "ask":
        prompt = f"Viết câu lệnh SQL để trả lời: {user_input}"
        llm_response = query_llm(prompt, user_id)
        print(f"Phản hồi gốc của AI '{llm_response}'")
        sql_query = extract_sql_from_response(llm_response)
        if not sql_query:
            return "❗ Không tìm thấy câu lệnh SQL trong phản hồi AI."
        try:
            data = execute_query(sql_query)
            final_prompt = f"Dữ liệu:\n{data}\n\nCâu hỏi:\n{user_input}"
            return query_llm(final_prompt, user_id)
        except Exception as e:
            return f"❌ Lỗi khi thực thi SQL: {e}"

    return "❗ Chế độ không hợp lệ (document/query/ask)."
