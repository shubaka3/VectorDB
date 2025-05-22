import os
from dotenv import load_dotenv

load_dotenv()  # Tải các biến từ file .env

API_BASE_URL = os.getenv('API_BASE_URL', "https://localhost:7288/")  # Nếu không có, dùng URL mặc định
AI_KEY = os.getenv('AI_KEY', 'sikibidi-j97') 
AI_API = os.getenv('AI_API', 'http://localhost:5000/chat')  # Sử dụng API key từ .env
# OPENAI_KEY = os.getenv('OPENAI_KEY', 'your_default_openai_key')  # Sử dụng OpenAI Key từ .env
