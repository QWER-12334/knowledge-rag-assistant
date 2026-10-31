from app.retrieve import retrieve
from app.prompt import fromat_docs,rag_prompt
from app.generate import call_llm
from app.rerank import rerank
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
       res =  call_llm(prompt)
       for i in res:
            print(i,end="",flush=True)
       #print(f"\n最终提示词为{prompt}")
       #print(f"\n==== 最相关的 {len(top)} 条 ====")
       #for i,j in enumerate(top,start=1):
           #print(f"第{i}条:来源为{j['source']}内容为{j["content"]}")
if __name__ == "__main__":
    chat()