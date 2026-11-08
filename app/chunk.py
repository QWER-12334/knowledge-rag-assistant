from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
logger = logging.getLogger(__name__)
def split_text(text:str , filename:str, chunk_size=500,chunk_overlap=50):
    if not text or not text.strip():
        logger.warning(f"文本为空，跳过切分")
        return []
    try:
        text_chunk = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            length_function = len,
        )
        chunks = text_chunk.split_text(text)#切分完是列表！！！
    except Exception as e:
        logger.error(f"{filename}切分失败:{e}")
        raise RuntimeError(f"{filename}切分失败:{e}")
    text_list = []
    for i in chunks:
        text_list.append(
            {
                "content":i,
                "source":filename
            }#是一个字典！！！(可以带两份信息)
        )
    logger.info(f"{filename}切分成功:一共{len(text_list)}个切片")
    return text_list
if __name__ == "__main__":
    text_txt = "测试文本"*20
    out = split_text(text_txt,"测试文本.txt" )
    for item in out:
        print(item)