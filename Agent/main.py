from agents.deal_agent import handle_user_query
from llms.llm_handler import query_llm

def load_system_prompt():
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Lỗi khi tải prompt hệ thống: {e}")
        return "Bạn là một trợ lý AI thực hiện các truy vấn và hỗ trợ người dùng."

def main():
    system_prompt = load_system_prompt()
    llm_response = query_llm(system_prompt, user_id="user_123")
    print(f"AI phản hồi khi khởi động: {llm_response}")

    while True:
        user_input = input("Bạn cần làm gì với các deal? (gõ 'exit' để thoát): ").strip()
        if user_input.lower() == "exit":
            print("Đóng chương trình...")
            break

        mode = input("Nhập chế độ (document/query/ask): ").strip().lower()
        collection = input("Tên collection cần dùng (nếu không biết có thể xem danh sách): ").strip()

        response = handle_user_query(user_input, user_id="user_123", collection_name=collection, mode=mode)
        print(f"AI trả lời: {response}\n")


if __name__ == "__main__":
    main()
