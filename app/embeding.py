import requests
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("SILICONFLOW_API_KEY")
model_name = "BAAI/bge-m3"
def get_vec(text):
    response = requests.post(
        "https://api.siliconflow.cn/v1/embeddings",
        headers = {
            "Authorization":f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json = {
            "input":text,
            "model":model_name
        },
        timeout = 10#最多等10s
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]
if __name__ == "__main__":
    vec = get_vec("RAG检索增强生成")
    print("向量长度",len(vec))