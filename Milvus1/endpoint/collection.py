from fastapi import APIRouter
import milvus_utils_api_online as mvs

router = APIRouter()

@router.post("/create")
def create_collection(name: str, dim: int = 384):
    col = mvs.create_collection(name, dim=dim)
    mvs.create_index(col)
    mvs.load_collection(col)
    return {"message": f"Collection '{name}' đã được tạo và load."}

@router.get("/list")
def list_collections():
    return {"collections": mvs.list_collections()}

@router.get("/load")
def load_collection(name: str):
    col = mvs.get_collection(name)
    if col:
        mvs.load_collection(col)
        return {"message": f"Đã load collection '{name}'"}
    return {"error": "Collection không tồn tại"}

@router.delete("/delete")
def delete_collection(name: str):
    mvs.delete_collection(name)
    return {"message": f"Đã xoá collection '{name}'"}

@router.get("/data")
def get_all_data(name: str):
    col = mvs.get_collection(name)
    if col:
        return mvs.show_all_data(col)
    return {"error": "Collection không tồn tại"}
