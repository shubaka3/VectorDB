import requests
from config.settings import AI_KEY, API_BASE_URL,AI_API
from config import settings



def load_system_prompt(types=None):
    try:
        if types is None:
            with open("system_QUERYprompt.txt", "r", encoding="utf-8") as file:
                return file.read().strip()
        elif types == "ask":
            with open("system_ASKprompt.txt", "r", encoding="utf-8") as file:
                return file.read().strip()
        else:
            return "System Prompt: You are an AI specialized in generating SQL queries. The data I send you will be in two types: if it's normal text, you must return it exactly as is without changes; if it's table-related data including columns and descriptions, you must analyze it and return a correct SQL query. When responding, if the input is normal text, just repeat it exactly. If it’s table-related and a query can be made, return the SQL inside a <query></query> tag, and the tag must contain only the SQL statement with nothing else. Keep the response focused, no extra explanations, no unnecessary content."
    except Exception as e:
        print(f"Lỗi khi tải prompt hệ thống: {e}")
        return "System Prompt: You are an AI specialized in generating SQL queries. The data I send you will be in two types: if it's normal text, you must return it exactly as is without changes; if it's table-related data including columns and descriptions, you must analyze it and return a correct SQL query. When responding, if the input is normal text, just repeat it exactly. If it’s table-related and a query can be made, return the SQL inside a <query></query> tag, and the tag must contain only the SQL statement with nothing else. Keep the response focused, no extra explanations, no unnecessary content."


def query_llm(prompt,user_id,history=None,types=None):
    system_prompt = load_system_prompt(types) 
    try:
        
        full_prompt = f"{system_prompt}{prompt}"
        # Tạo payload cho request
        payload = {
            "model": "mistral",
            "user_id":  user_id, # Thay thế với tên mô hình của bạn 
            "prompt": full_prompt,
            "history": history if history is not None else False,
            "stream": False
        }

    
        # Gửi request tới API của bạn
        headers = {
            'Authorization': f'Bearer {AI_KEY}',  # Sử dụng API key nếu cần
        }
        response = requests.post(AI_API, json=payload, verify=False,headers=headers)

        if response.status_code == 200:
            # Xử lý dữ liệu trả về từ mô hình của bạn
            response_data = response.json()
            return response_data.get("response", "Không có phản hồi từ mô hình.")
        else:
            return f"Đã xảy ra lỗi khi gọi API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Đã xảy ra lỗi khi gọi mô hình: {str(e)}"
# done 