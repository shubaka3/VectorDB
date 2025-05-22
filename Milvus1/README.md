- Milvus là 1 vectorDb lưu trữ dữ liệu dạng vector ( có thể thay bằng csdl khác nhưng k tối ưu bằng milvus, có chrome gì đó quên rồi nó là dàng cho nhỏ hơn ( để test hoặc csdl nhỏ))
- config có host,port tùy chỉnh
- Có milvus_untils.py các chức năng hiện tại
    + Tạo collection mới
    + Chọn collection hiện có
    + Thêm dữ liệu văn bản
    + Tạo index cho collection hiện tại
    + Load collection
    + Tìm văn bản tương tự
    + Danh sách collection
    + Xoá collection
    + Xem dữ liệu trong collection
=====
Cách sử dụng: 
- tạo máy ảo nếu vừa clone về : python -m venv venv
- Active máy ảo: venv\Scripts\activate
- tải thư viện : pip install -r requirements.txt
- Chạy milvus Docker 
- Chạy: python main.py

- Add main_api.py
    + cd /d E:\VectorDB\Milvus1
    + chạy bằng uvicorn main_api:app --reload 
    + uvicorn main_api:app --host 0.0.0.0 --port 8001 --reload
