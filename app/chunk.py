from langchain_text_splitters import RecursiveCharacterTextSplitter
def split_text(text:str , filename:str, chunk_size=500,chunk_overlap=50):
    text_chunk = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
    )
    chunks = text_chunk.split_text(text)#切分完是列表！！！
    text_list = []
    for i in chunks:
        text_list.append(
            {
                "content":i,
                "source":filename
            }#是一个字典！！！(可以带两份信息)
        )
    return text_list
if __name__ == "__main__":
    text_txt = "测试文本"*20
    out = split_text(text_txt,"测试文本.txt" )
    for item in out:
        print(item)