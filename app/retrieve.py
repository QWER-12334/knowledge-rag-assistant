from app.data_storage import vector_store
import logging
logger = logging.getLogger(__name__)
def retrieve(query:str,k:int = 5):
    try:
        docs = vector_store.similarity_search(query,k = k)
    except Exception as e:
          logger.error(f"检索失败：{e}")
          raise RuntimeError(f"检索失败,请检查向量库和网络：{e}")
    if not docs:
        logger.info("检索内容为空,可能没有相关资料")
        return []
    res_list = []
    for doc in docs:
        res_list.append({
            "content":doc.page_content,
            "source":doc.metadata["source"]
        })
    logger.info(f"检索成功:一共{len(res_list)}条文档")
    return res_list
if __name__ == "__main__":
    coll = vector_store._collection
    count = coll.count()
    print(f"👉 当前向量库里面一共有 {count} 条切片！")
    query = input("请输入问题：")
    results  = retrieve(query)
    print("\n==== 检索结果 Top5 ====")
    for idx, item in enumerate(results, start=1):
        print(f"\n【第{idx}条】来源文件：{item['source']}")
        print(f"内容：{item['content']}")