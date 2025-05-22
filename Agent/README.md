Đây là AI kết hợp cả 3:  AI, Milvus, Embedding 
Hướng dẫn sử dụng 
- tạo máy ảo nếu vừa clone về : python -m venv venv
- Active máy ảo: venv\Scripts\activate
- tải thư viện : pip install -r requirements.txt
- Chạy milvus Docker 
- Chạy: uvicorn main_api:app --reload --port 8000
- http://127.0.0.1:8000/docs
Luồng xử lý -> Gửi request -> request đi qua miluvs -> embedding thành vector -> hàm search_topk của milvus -> so sánh vector với các vector đang có, lấy vector gần đúng nhất (Id,vector,metadata) -> metadata vào lln 
- if(model = document) -> AI xử lý metadata ròi đưa ra luôn 
- if(model = query) -> AI xử lý metadata -> đưa result được chuẩn hóa trong <query>sql sysntax </query> về sql_executor, thực thi sql và trả về kết quả -> kết quả nhận được là result từ câu hỏi ( có thể là table hay obj)
    + vd: lấy deal có status canceled => datatable
- if(model = ask) -> AI xử lý metadata -> đưa result được chuẩn hóa trong <query>sql sysntax </query> về sql_executor, thực thi sql và trả về kết quả -> đưa kêt quả cho lln -> lln phân tích -> kết quả cuối 
    + vd: có bao nhiêu deal bị canceled -> datatable -> lln đọc datatable -> có 3 status bị canceled
