from fastapi import FastAPI,UploadFile, File
from pydantic import BaseModel
from fastapi.responses import StreamingResponse,JSONResponse,FileResponse
#JSONResponse用来给前端返回一个标准 JSON 格式的 HTTP 响应对象
#FileResponse用来给前端返回一个文件响应对象
#StreamingResponse是FastAPI 的流式响应对象，配合 `yield` 生成器，一块一块往外发数据，不用等全部内容生成完再一次性返回
from fastapi.openapi.docs import get_swagger_ui_html
#get_swagger_ui_html它是 FastAPI 里用来生成 Swagger 接口文档页面的 HTML 的函数**FastAPI
from app.retrieve import retrieve
from app.prompt import fromat_docs,rag_prompt
from app.generate import call_llm
from app.rerank import rerank
from app.data_storage import add_doc
import logging
logger = logging.getLogger(__name__)
import json#处理json数据
app = FastAPI(title="RAG知识库接口服务",docs_url=None)
@app.get("/chat")
def home():
    return FileResponse("index.html")
#请求体
class Ask(BaseModel):
    query:str
    k:int =10
    top_k: int = 3
@app.post("/ask")
async def ask_aswer(req:Ask):
    logger.info(f"收到请求:{req.query}")
    try:
        answer = retrieve(query=req.query,k=req.k)
        if not answer:
            def stream():
                yield "没有相关文档,抱歉"
            return StreamingResponse(stream(),media_type="text/plain")
        top = rerank(req.query,answer,req.top_k)
        prompt = rag_prompt(fromat_docs(top),req.query)
    except Exception as e:
        logger.error(f"处理问题失败{e}")
        return JSONResponse(status_code=500, content={"message": f"服务出错了:{e}"})
    def stream_generate():
        try:
            yield from call_llm(prompt)
        except Exception as e:
              logger.error(f"生成回答中断:{e}")
              yield f"\n\n[生成中断] {e}"
              return
        sources = []#加上内容的来源
        for d in top:
            if d["source"] not in sources:
                sources.append(d["source"])
        yield "\n\n<<sources>>" + json.dumps(sources, ensure_ascii=False)#json.dumps将字典转换成json字符串
    return StreamingResponse(stream_generate(),media_type="text/plain")
@app.post("/upload")#上传文件接口
async def upload(f: UploadFile = File(...)):
    if not f.filename.lower().endswith(".txt"):
        return JSONResponse(status_code=400,content={"message":"只支持txt文件"})
    file_content = await f.read()
    try:
        content_str = file_content.decode("utf-8")
    except UnicodeDecodeError:
        return JSONResponse(status_code=400,content={"message":"文件编码错误,请上传UTF-8编码文件"})
    if not content_str.strip():
        return JSONResponse(status_code=400,content={"message":"文件内容为空"})
    try:
        add_doc(content_str,f.filename)
    except Exception as e:
        logger.error(f"上传入库失败:{e}")
        return JSONResponse(status_code=500, content={"message": f"入库失败:{e}"})
    logger.info(f"上传成功:{f.filename}")
    return {"message":"文件上传成功","filename":f.filename}
# 当需要测试时/上传文档时/crul测试时需要打开下面部分
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
    #curl -X POST http://127.0.0.1:8000/upload -F "f=@C:/Users/13694/Desktop/奶茶.txt"例如桌面上有一个奶茶文件