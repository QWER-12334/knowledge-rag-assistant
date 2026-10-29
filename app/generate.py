import os
from dotenv import load_dotenv
from app.rerank import rerank
from app.retrieve import retrieve
from app.prompt import rag_prompt
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
    }
    headers = {
        "Authorization":f"Bearer {api_key}","content":"application/json"
    }
    response = requests.post(url,headers= headers,json = payload)
    response.raise_for_status
    res = response.json()["choices"][0]["message"]["content"]
    return res
def rag_answer(query: str):
    # 1.检索
    raw_docs = retrieve(query)
    # 2.重排
    ranked_docs = rerank(query, raw_docs)
    # 3.提示词(提示词修改请到prompt文件种修改)
    final_prompt = rag_prompt(query, ranked_docs)
    # 4.调用大模型
    answer = call_llm(final_prompt)
    return answer
if __name__ == "__main__":
    query_text = input("请输入问题:")
    answer = rag_answer(query_text)
    print(answer)