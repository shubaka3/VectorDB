import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Milvus1 import milvus_utils as mvs
from Embedding.encoder import TextEncoder
from Embedding.config import EmbeddingConfig

encoder = TextEncoder(EmbeddingConfig(
    model_name="all-MiniLM-L6-v2",
    dim=384,
    device="cpu",
    log_level="INFO"
))

def choose_collection():
    collections = mvs.list_collections()
    if not collections:
        print("❗ Hiện chưa có collection nào.")
        return None
    print("📦 Danh sách collection:")
    for i, c in enumerate(collections):
        print(f"{i+1}. {c}")
    choice = input("Chọn collection theo số (hoặc 0 để huỷ): ").strip()
    if choice == "0":
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(collections):
            return mvs.get_collection(collections[idx])
        else:
            print("❗ Lựa chọn không hợp lệ.")
            return None
    except:
        print("❗ Lựa chọn không hợp lệ.")
        return None

def main():
    current_collection = None
    current_collection_name = None

    while True:
        print("\n🧠 MENU Milvus + Embedding")
        print(f"Collection hiện tại: {current_collection_name if current_collection_name else 'Chưa chọn'}")
        print("1. Tạo collection mới")
        print("2. Chọn collection hiện có")
        print("3. Thêm dữ liệu văn bản")
        print("4. Tạo index cho collection hiện tại")
        print("5. Load collection")
        print("6. Tìm văn bản tương tự")
        print("7. Danh sách collection")
        print("8. Xoá collection")
        print("9. Xem dữ liệu trong collection")
        print("0. Thoát")

        choice = input("→ Chọn: ").strip()

        if choice == "1":
            name = input("Nhập tên collection mới: ").strip()
            current_collection = mvs.create_collection(name, dim=384)
            current_collection_name = name
            mvs.create_index(current_collection)
            mvs.load_collection(current_collection)  # Load luôn sau khi tạo
            print(f"✔️ Collection '{name}' đã tạo, tạo index và load thành công.")
        
        elif choice == "2":
            col = choose_collection()
            if col:
                current_collection = col
                current_collection_name = col.name

                # Tạo index nếu chưa có
                if not current_collection.indexes:
                    print("ℹ️ Collection chưa có index, tạo index tự động...")
                    mvs.create_index(current_collection)

                # Load collection để search được
                mvs.load_collection(current_collection)

                print(f"✔️ Đã chọn và load collection '{current_collection_name}'")
            else:
                print("❗ Không thay đổi collection hiện tại.")

        elif choice == "3":
            if current_collection is None:
                print("❗ Hãy tạo hoặc chọn collection trước.")
                continue
            text = input("Nhập văn bản: ").strip()
            vector = encoder.get_vector(text)
            mvs.insert_vector(current_collection, vector, text)

        elif choice == "4":
            if current_collection:
                mvs.create_index(current_collection)
                print("✔️ Đã tạo index cho collection.")
            else:
                print("❗ Không có collection nào để tạo index.")

        elif choice == "5":
            name = input("Nhập tên collection để load: ").strip()
            col = mvs.get_collection(name)
            if col:
                mvs.load_collection(col)
                current_collection = col
                current_collection_name = name
                print(f"✔️ Đã load collection '{name}'")
            else:
                print("❗ Collection không tồn tại.")

        elif choice == "6":
            if current_collection:
                text = input("Nhập văn bản cần tìm: ").strip()
                vector = encoder.get_vector(text)
                mvs.search_topk(current_collection, vector)
            else:
                print("❗ Chưa chọn hoặc load collection.")

        elif choice == "7":
            collections = mvs.list_collections()
            if collections:
                print("📦 Danh sách collection:")
                for c in collections:
                    print(f"- {c}")
            else:
                print("❗ Chưa có collection nào.")

        elif choice == "8":
            name = input("Nhập tên collection cần xoá: ").strip()
            mvs.delete_collection(name)
            if current_collection_name == name:
                current_collection = None
                current_collection_name = None

        elif choice == "0":
            print("👋 Thoát.")
            break
        elif choice == "9":
            if current_collection:
                mvs.show_all_data(current_collection)
            else:
                print("❗ Hãy chọn collection trước.")

        else:
            print("❗ Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
