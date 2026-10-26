from app.store import vector_store
def retrieve(query:str,k:int = 5):
    docs = vector_store.similarity_search(query,k = k)
    res_list = []
    for doc in docs:
        res_list.append({
            "content":doc.page_content,
            "source":doc.metadata["source"]
        })
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