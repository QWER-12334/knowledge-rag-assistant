import os   #os 处理路径
from app.chunk import split_text
from app.embeding import SiliconFlowEmbeddings
from app.store import add_doc,vector_store
from app.retrieve import retrieve
end = SiliconFlowEmbeddings()
DATA_PATH = "./data"
all_chunk_list = []
for file_name in os.listdir(DATA_PATH):
    if file_name.endswith(".txt"):
        file_full_path = os.path.join(DATA_PATH,file_name)
        with open (file_full_path,"r",encoding="utf-8")as f:
            file_content = f.read()
        one_file_chunks = split_text(text = file_content,filename = file_name)
        all_chunk_list.extend(one_file_chunks)
        add_doc (file_content,file_name)
        print(f"{file_name}入库完成,生成{len(one_file_chunks)}块")
"""输出切块"""
print("\n==== 全部切块完成，一共", len(all_chunk_list), "块 ====")
for i, chunk in enumerate(all_chunk_list[:]): 
    print(f"第{i}块: 来源：{chunk['source']}")
    print(chunk["content"][:])
"""向量化输出"""
for i,chunk in enumerate(all_chunk_list):
    print(f"第{i}块正在向量化")
    chunk["embeding"] = end.get_vec(chunk["content"])
    print(f"向量为{chunk["embeding"]}")
docs = vector_store.similarity_search("跨境电商发展情况", k=3)
for d in docs:
    print(d.metadata["source"], "|", d.page_content[:40], "...")
"""问答"""
def chat():
   print("进入问答模式,输入问题即可进行问答")
   while True:
       qure = input("请输入问题(退出问答输q):")
       if qure == "q":
           print("退出问答")
           break
       reswer = retrieve(qure,k=3)
       print("\n检索结果--3条(最多)")
       if not reswer:
           print("没有相关文档,抱歉")
           continue
       for i,j in enumerate(reswer,start=1):
           print(f"第{i}条:来源为{j['source']}内容为{j["content"]}")
if __name__ == "__main__":
    chat()