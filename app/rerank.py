import os
import requests
from  dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("SILICONFLOW_API_KEY")
rerank_url = "https://api.siliconflow.cn/v1/rerank"
rerank_model = "Qwen/Qwen3-Reranker-0.6B"
def rerank(query:str,doc_list:list[dict],top_k:int = 5):
    if not doc_list:
        return []
    payload = {
        "model":rerank_model,
        "query":query,
        "documents":[item["content"] for item in doc_list]
    }
    res = requests.post(
        rerank_url,
        headers = {
            "Authorization":f"Bearer {API_KEY}",
            "Content-Type":"application/json",
        },
        json = payload,
        timeout = 30,
    )
    res.raise_for_status()
    ranks = res.json()["results"]
    out = []
    for i in ranks [:top_k]:
        new_doc =  dict(doc_list[i["index"]])#dict复制
        new_doc["rerank_score"] = round(i["relevance_score"], 4)
        out.append(new_doc)
    return out
if __name__ == "__main__":
    test_query = "python怎么读取csv文件"
    test_top5 = [
        {"content":"pandas.read_csv() 可以读取csv文件,参数filepath_or_buffer是文件路径", "source":"pandas.md"},
        {"content":"python列表可以用append添加元素", "source":"list.md"},
        {"content":"csv模块内置在python标准库,使用csv.reader逐行读取", "source":"csv.md"},
        {"content":"matplotlib用来绘制折线图、柱状图", "source":"plot.md"},
        {"content":"open函数可以打开文本文件,指定'r'只读模式", "source":"file.md"},
    ]
    top3 = rerank(test_query, test_top5, top_k=3)
    print("====原生Rerank接口结果Top3====")
    for i,item in enumerate(top3):
        print(item)