def fromat_docs(doc_list:list[dict]):
    parts = []
    for i,doc in enumerate(doc_list,start =1):
        parts.append(f"【资料：{i}】(来源：{doc["source"]}) \n 内容:{doc["content"]}")
    return "\n\n".join(parts)
def rag_prompt(content_text:str,query_text:str):
    prompt_template = """你是一个问答助手，请严格只根据下面给出的参考资料回答用户问题。
如果参考资料里面没有相关信息，直接回答【不确定，资料中未找到该内容】，禁止编造、猜测、引入外部知识。 
参考资料：{content} ，问题：{query}"""
    return prompt_template.format(content=content_text,query=query_text)
if __name__ == "__main__":
    text = [ {"content": "Python是一门解释型编程语言,由吉多开发。", "source": "测试.txt"},
          {"content": "Java 是编译型语言。", "source": "测试.txt"},]
    text_query = "Python是什么编程语言"
    print(rag_prompt(fromat_docs(text),text_query))