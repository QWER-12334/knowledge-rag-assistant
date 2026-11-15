import os
from dotenv import load_dotenv
from app.rerank import rerank
from app.retrieve import retrieve
from app.prompt import rag_prompt,fromat_docs
import json
import logging
import requests
logger = logging.getLogger(__name__)
load_dotenv()
api_key = os.getenv("SILICONFLOW_API_KEY")
model_name = "Qwen/Qwen2.5-7B-Instruct"
url = "https://api.siliconflow.cn/v1/chat/completions"
def call_llm(prompt:str):
    payload = {
        "model":model_name,
        "messages" :[{"role":"user","content":prompt}],
        "temperature":0.2,
        "stream":True#流式返回
    }
    headers = {
        "Authorization":f"Bearer {api_key}","Content-Type":"application/json"
    }
    try:
        response = requests.post(url,headers= headers,json = payload, stream=True,timeout = 30)#stream=True表示流式返回
        response.raise_for_status()
    except requests.Timeout:
        logger.error("生成超时:等了30s还没有反应")
        raise RuntimeError("生成超时:请检查网络后重试")
    except requests.ConnectionError:
        logger.error("调用大模型失败,连不上服务器")
        raise RuntimeError("连不上 SiliconFlow,请检查网络")
    except requests.HTTPError:
        logger.error(f"生成失败:HTTP {response.status_code}")
        raise RuntimeError(f"生成请求被拒绝(HTTP {response.status_code})")
    char = 0
    for raw_line in response.iter_lines():
        if not raw_line:
            continue
        line = raw_line.decode("utf-8")
        if not line.startswith("data: "):#过滤掉非数据(即没有data:)的行
            continue
        data = line[6:]#去掉data:前缀
        if data == "[DONE]":#流式返回结束
            break
        chunk = json.loads(data)#将json字符串转化成字典
        content = chunk["choices"][0]["delta"].get("content","")#get方法可以避免key不存在时报错
        if content:
            char += len(content)
            yield content
    logger.info(f"生成成功:一共{char}字符")
def rag_answer(query: str):#RAG回答整套流程
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
        