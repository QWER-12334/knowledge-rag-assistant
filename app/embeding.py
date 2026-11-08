import requests
from dotenv import load_dotenv#用于读取.env的工具
import os
from langchain_core.embeddings import Embeddings
import logging
load_dotenv()
logger=logging.getLogger(__name__)
API_KEY = os.getenv("SILICONFLOW_API_KEY")
model_name = "BAAI/bge-m3"
class SiliconFlowEmbeddings(Embeddings):
    def get_vec(self,text):
        """每家模型的请求格式不一样"""
        try:
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
            response.raise_for_status()#检查请求是否成功
        except requests.Timeout:
            logger.error("向量化超时:等了10s还没有反应")
            raise RuntimeError("向量化超时,请检查网络后重试")
        except requests.ConnectionError:
            logger.error("向量化错误:连接不上服务器")
            raise RuntimeError("连接不上服务器,请检查网络及api是否有余额")
        except requests.HTTPError:
            logger.error("向量化错误:服务器返回错误")
            raise RuntimeError(f"SiliconFlow 拒绝了请求(HTTP {response.status_code})，检查密钥或额度")
        data = response.json()
        vector =  [item["embedding"] for item in data["data"]]
        logger.info(f"向量化成功:一共{len(vector)}条文档,每条{len(vector[0])}维")
        return vector
    def embed_documents(self, texts):# 入库时批量调用
        return self.get_vec(texts)
    def embed_query(self, text):# 查询时单条调用，注意返回的是单个向量而不是列表
        return self.get_vec([text])[0]

if __name__ == "__main__":
    emb = SiliconFlowEmbeddings()
    vec = emb.get_vec("RAG检索增强生成")
    print("向量长度",len(vec[0]))