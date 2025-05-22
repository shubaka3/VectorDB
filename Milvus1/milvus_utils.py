from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility
# from Milvus1 import config
import config
from config import MILVUS_URI

ZILLIZ_URI = "https://in03-599d745cd2af08d.serverless.gcp-us-west1.cloud.zilliz.com"
ZILLIZ_TOKEN = "db_599d745cd2af08d:Tp7*sTxq!c<]KqWU"
# Kết nối Milvus
connections.connect(alias="default", host=config.MILVUS_HOST, port=config.MILVUS_PORT)

def connect_milvus():
    if not connections.has_connection("default"):
        connections.connect("default", host=config.MILVUS_HOST, port=config.MILVUS_PORT)

def create_collection(name, dim):
    if utility.has_collection(name):
        print(f"Collection '{name}' đã tồn tại.")
        return Collection(name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=1024)
    ]
    schema = CollectionSchema(fields)
    collection = Collection(name=name, schema=schema)
    print(f"✅ Đã tạo collection '{name}'")
    return collection

def insert_vector(collection, vector, raw_text):
    # Ép kiểu về list[float] nếu là numpy hoặc tensor
    if hasattr(vector, 'tolist'):
        vector = vector.tolist()

    # Đảm bảo vector là list of float
    if not isinstance(vector, list) or not all(isinstance(x, float) for x in vector):
        raise ValueError("Vector phải là list[float] đúng định dạng.")

    print("📎 Inserting vector:", vector[:384])
    print("📎 Text:", raw_text)

    insert_data = [
        [vector],      # embedding: list chứa 1 vector
        [raw_text]     # text: list chứa 1 chuỗi
    ]

    collection.insert(insert_data)
    print("✅ Đã thêm vector.")



def create_index(collection):
    index_params = {
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    print("✅ Đã tạo index.")

def load_collection(collection):
    collection.load()
    print("✅ Đã load collection.")
    print("📋 Schema Collection:")
    print(collection.schema)

def search_topk(collection, vector, top_k=3):
    if hasattr(vector, 'tolist'):
        vector = vector.tolist()

    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    results = collection.search(
        data=[vector],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["text"]
    )
    print("🔍 Kết quả gần nhất:")
    for hits in results:
        for hit in hits:
            print(f" - ID={hit.id}, distance={hit.distance:.4f}, text='{hit.entity.get('text')}'")

def list_collections():
    return utility.list_collections()

def get_collection(name):
    if utility.has_collection(name):
        return Collection(name)
    return None

def delete_collection(name):
    if utility.has_collection(name):
        utility.drop_collection(name)
        print(f"🗑️ Đã xoá collection '{name}'")

def show_all_data(collection, limit=10):
    expr = ""  # không lọc gì cả
    results = collection.query(
        expr=expr,
        output_fields=["id", "text"],
        limit=limit
    )
    print(f"📋 {len(results)} bản ghi đầu trong collection '{collection.name}':")
    for i, res in enumerate(results):
        print(f"{i+1}. ID={res['id']}, text='{res['text']}'")

def search_topk1(collection, vector, top_k=3):
    if hasattr(vector, 'tolist'):
        vector = vector.tolist()

    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    results = collection.search(
        data=[vector],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["text"]
    )
    hits_data = []
    for hits in results:
        for hit in hits:
            hits_data.append({
                "id": hit.id,
                "distance": hit.distance,
                "text": hit.entity.get("text")
            })
    return hits_data
