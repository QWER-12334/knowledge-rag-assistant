from langchain_chroma import Chroma
from app.chunk import split_text
from app.embeding import SiliconFlowEmbeddings
import logging
logger = logging.getLogger(__name__)
#向量库配置
PERSIST = "./chroma_db"
COLLECTION_NAME = "rag_docs"
vector_store = Chroma(
    persist_directory = PERSIST,
    collection_name = COLLECTION_NAME,
    embedding_function = SiliconFlowEmbeddings(),
)
def add_doc(content:str,source:str):
    chunks = split_text(content,source)
    if not chunks:
        logger.warning(f"{source}文本为空,无法入库")
        return
    texts = [item["content"] for item in chunks]
    metadata = [{"source":item["source"]} for item in chunks]
    ids = [f"{source}#{i}" for i in range(len(chunks))]
    try:
        vector_store.add_texts(
            texts = texts,
            ids =ids,
            metadatas = metadata
    )
    except Exception as e:
        logger.error(f"{source}入库失败:{e}")
        raise RuntimeError(f"{source}入库失败:{e}")
    logger.info(f"{source} 入库完成，一共 {len(chunks)} 块")
if __name__ == "__main__":
    test_txt = "RAG入库模块,metadata存储source用来记录切片所属原始文件,用于溯源、筛选和文档管理。"
    add_doc(test_txt,"测试文本.txt")