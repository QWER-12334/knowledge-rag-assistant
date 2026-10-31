from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.openapi.docs import get_swagger_ui_html
from app.retrieve import retrieve
from app.prompt import fromat_docs,rag_prompt
from app.generate import call_llm
from app.rerank import rerank
app = FastAPI(title="RAG知识库接口服务",docs_url=None)
#请求体
class Ask(BaseModel):
    query:str
    k:int =5
    top_k: int = 3
@app.post("/ask")
async def ask_aswer(req:Ask):
    answer = retrieve(query=req.query,k=req.k)
    if not answer:
        def stream():
            yield "没有相关文档,抱歉"
        return StreamingResponse(stream(),media_type="text/plain")
    top = rerank(req.query,answer,req.top_k)
    prompt = rag_prompt(fromat_docs(top),req.query)
    def stream_generate():
        yield from call_llm(prompt)
    return StreamingResponse(stream_generate(),media_type="text/plain")
@app.get("/docs", include_in_schema=False)
def custom_docs():
      return get_swagger_ui_html(
          openapi_url=app.openapi_url,
          title="RAG知识库接口服务 - 文档",
          swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.29.1/swagger-ui-bundle.min.js",
          swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.29.1/swagger-ui.min.css",
      )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_fast_api:app", host="0.0.0.0", port=8000, reload=True)
    #curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d "{\"query\":\"你好\"}"终端调试
