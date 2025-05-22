from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoint import collection, data

app = FastAPI(title="Milvus + Embedding API")

# 👇 Thêm CORS middleware ở đây
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc cụ thể: ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn các router
app.include_router(collection.router, prefix="/collection", tags=["Collection"])
app.include_router(data.router, prefix="/data", tags=["Data"])
