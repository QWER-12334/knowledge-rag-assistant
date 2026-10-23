import os   #os 处理路径
from app.chunk import split_text
from app.embeding import get_vec
DATA_PATH = "./data"
all_chunk_list = []
for file_name in os.listdir(DATA_PATH):
    if file_name.endswith(".txt"):
        file_full_path = os.path.join(DATA_PATH,file_name)
        with open (file_full_path,"r",encoding="utf-8")as f:
            file_content = f.read()
        one_file_chunks = split_text(text = file_content,filename = file_name)
        all_chunk_list.extend(one_file_chunks)
        print(f" {file_name} 切完，生成 {len(one_file_chunks)} 个块")
"""切块"""
print("\n==== 全部切块完成，一共", len(all_chunk_list), "块 ====")
for i, chunk in enumerate(all_chunk_list[:]): 
    print(f"第{i}块: 来源：{chunk['source']}")
    print(chunk["content"][:])
"""向量化"""
for i,chunk in enumerate(all_chunk_list):
    print(f"第{i}块正在向量化")
    chunk["embeding"] = get_vec(chunk["content"])
    print(f"向量为{chunk["embeding"]}")
    

