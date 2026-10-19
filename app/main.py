from fastapi import FastAPI

app = FastAPI(title="RAG知识库助手")

@app.get("/")
def index():
    return {"message": "RAG项目骨架启动成功 ✅"}
