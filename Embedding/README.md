Đây là thư viện dùng để chuyển đổi data thành vector tự viết 
- tùy chỉnh config, trong đây sẽ k có hàm để chạy gọi nó ở thư viện khác 
- Import TextEncoder & Config
- Cấu hình config, truyền config vào TextEncoder
- Trong encoder có các hàm để lấy vector, có decode nhưng k thật sự hoạt động vì nó chỉ lưu sate hiện tại dưới cache
- Nhiệm vụ của nó chỉ là chuyển đổi dữ liệu thành vector theo đúng dim được set