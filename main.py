import os   #os 处理路径
from app.chunk import split_text
from app.embeding import SiliconFlowEmbeddings
from app.store import add_doc
from app.retrieve import retrieve
from app.prompt import fromat_docs,rag_prompt
from app.generate import call_llm
end = SiliconFlowEmbeddings()
from app.rerank import rerank
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
"""  #输出切块
print("\n==== 全部切块完成，一共", len(all_chunk_list), "块 ====")
for i, chunk in enumerate(all_chunk_list[:]): 
    print(f"第{i}块: 来源：{chunk['source']}")
    print(chunk["content"][:])
  #向量化输出
for i,chunk in enumerate(all_chunk_list):
    print(f"第{i}块正在向量化")
    chunk["embeding"] = end.get_vec(chunk["content"])
    print(f"向量为{chunk["embeding"]}")"""
"""问答"""
def chat():
   print("进入问答模式,输入问题即可进行问答")
   while True:
       qure = input("请输入问题(退出问答输q):")
       if qure == "q":
           print("退出问答")
           break
       reswer = retrieve(qure,k=5)
       #print("\n检索结果--5条(最多)")
       if not reswer:
           print("没有相关文档,抱歉")
           continue
       top = rerank(qure,reswer,top_k=3)
       prompt = rag_prompt(fromat_docs(top),qure)
       res = call_llm(prompt)
       print(f"\nAI回答为:{res}")
       #print(f"\n最终提示词为{prompt}")
       #print(f"\n==== 最相关的 {len(top)} 条 ====")
       #for i,j in enumerate(top,start=1):
           #print(f"第{i}条:来源为{j['source']}内容为{j["content"]}")
if __name__ == "__main__":
    chat()