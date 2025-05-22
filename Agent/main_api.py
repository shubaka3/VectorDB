# main_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.deal_agentAPI import handle_user_query, handle_followup_ask

app = FastAPI(title="AI Deal Assistant API")

class QueryRequest(BaseModel):
    question: str
    user_id: str = "user"
    collection: str = "default"
    mode: str  # document, query, ask

class FollowUpRequest(BaseModel):
    question: str
    data: str
    user_id: str = "user"

@app.post("/query")
def query_handler(req: QueryRequest):
    try:
        result = handle_user_query(req.question, req.user_id, req.collection, req.mode)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask/followup")
def ask_followup(req: FollowUpRequest):
    try:
        result = handle_followup_ask(req.data, req.question, req.user_id)
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def load_system_prompt():
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Lỗi khi tải prompt hệ thống: {e}")
        return "Bạn là một trợ lý AI thực hiện các truy vấn và hỗ trợ người dùng."