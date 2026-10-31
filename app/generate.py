import os
from dotenv import load_dotenv
from app.rerank import rerank
from app.retrieve import retrieve
from app.prompt import rag_prompt,fromat_docs
import json
import requests
load_dotenv()
api_key = os.getenv("SILICONFLOW_API_KEY")
model_name = "Qwen/Qwen2.5-7B-Instruct"
url = "https://api.siliconflow.cn/v1/chat/completions"
def call_llm(prompt:str):
    payload = {
        "model":model_name,
        "messages" :[{"role":"user","content":prompt}],
        "temperature":0.5,
        "stream":True
    }
    headers = {
        "Authorization":f"Bearer {api_key}","Content-Type":"application/json"
    }
    response = requests.post(url,headers= headers,json = payload, stream=True)
    response.raise_for_status()
    for raw_line in response.iter_lines():
        if not raw_line:
            continue
        line = raw_line.decode("utf-8")
        if not line.startswith("data: "):
            continue
        data = line[6:]
        if data == "[DONE]":
            break
        chunk = json.loads(data)
        content = chunk["choices"][0]["delta"].get("content","")
        if content:
            yield content
def rag_answer(query: str):
    # 1.检索
    raw_docs = retrieve(query)
    # 2.重排
    ranked_docs = rerank(query, raw_docs)
    # 3.提示词(提示词修改请到prompt文件种修改)
    final_prompt = rag_prompt(fromat_docs(ranked_docs), query)
    # 4.调用大模型
    yield from call_llm(final_prompt)
if __name__ == "__main__":
    query_text = input("请输入问题:")
    for i in rag_answer(query_text):
        print(i, end="", flush=True)
        