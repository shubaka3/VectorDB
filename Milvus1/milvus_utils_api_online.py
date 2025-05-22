from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility
import config

# Kết nối Milvus
# connections.connect(alias="default", host=config.MILVUS_HOST, port=config.MILVUS_PORT)
ZILLIZ_URI = "https://in03-599d745cd2af08d.serverless.gcp-us-west1.cloud.zilliz.com"
ZILLIZ_TOKEN = "db_599d745cd2af08d:Tp7*sTxq!c<]KqWU"  # User và Password nối bằng dấu ":"

try:
    connections.connect(
        alias="default",
        uri=ZILLIZ_URI,
        token=ZILLIZ_TOKEN
    )
except Exception as e:
    print(f"❌ Kết nối Milvus thất bại: {e}")


def connect_milvus():
    if not connections.has_connection("default"):
        connections.connect("default", host=config.MILVUS_HOST, port=config.MILVUS_PORT)


def create_collection(name, dim):
    if utility.has_collection(name):
        return Collection(name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=1024)
    ]
    schema = CollectionSchema(fields)
    collection = Collection(name=name, schema=schema)
    return collection


def insert_vector(collection, vector, raw_text):
    if hasattr(vector, 'tolist'):
        vector = vector.tolist()

    if not isinstance(vector, list) or not all(isinstance(x, float) for x in vector):
        raise ValueError("Vector phải là list[float] đúng định dạng.")

    insert_data = [
        [vector],
        [raw_text]
    ]

    collection.insert(insert_data)
    return {"message": "Đã thêm vector thành công."}


def create_index(collection):
    index_params = {
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    return {"message": f"Đã tạo index cho collection '{collection.name}'."}


def load_collection(collection):
    collection.load()
    return {"message": f"Đã load collection '{collection.name}'.", "schema": str(collection.schema)}


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

    hits_data = []
    for hits in results:
        for hit in hits:
            hits_data.append({
                "id": hit.id,
                "distance": float(hit.distance),
                "text": hit.entity.get("text")
            })

    return hits_data


def list_collections():
    return utility.list_collections()


def get_collection(name):
    if utility.has_collection(name):
        return Collection(name)
    return None


def delete_collection(name):
    if utility.has_collection(name):
        utility.drop_collection(name)
        return {"message": f"Đã xoá collection '{name}'"}
    return {"error": "Collection không tồn tại."}


def show_all_data(collection, limit=10):
    expr = ""  # không lọc gì cả
    try:
        results = collection.query(
            expr=expr,
            output_fields=["id", "text"],
            limit=limit
        )
        return results
    except Exception as e:
        return {"error": str(e)}
