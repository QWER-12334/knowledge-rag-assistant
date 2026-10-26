import requests
from dotenv import load_dotenv
import os
from langchain_core.embeddings import Embeddings
load_dotenv()
API_KEY = os.getenv("SILICONFLOW_API_KEY")
model_name = "BAAI/bge-m3"
class SiliconFlowEmbeddings(Embeddings):
    def get_vec(self,text):
        """每家模型的请求格式不一样"""
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
        data = response.json()
        return [item["embedding"] for item in data["data"]]
    def embed_documents(self, texts):# 入库时批量调用
        return self.get_vec(texts)
    def embed_query(self, text):# 查询时单条调用，注意返回的是单个向量而不是列表
        return self.get_vec([text])[0]

if __name__ == "__main__":
    emb = SiliconFlowEmbeddings()
    vec = emb.get_vec("RAG检索增强生成")
    print("向量长度",len(vec[0]))