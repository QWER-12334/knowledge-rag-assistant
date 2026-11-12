import logging
logger = logging.getLogger(__name__)
def fromat_docs(doc_list:list[dict]):
    parts = []
    for i,doc in enumerate(doc_list,start =1):
        parts.append(f"【资料：{i}】(来源：{doc["source"]}) \n 内容:{doc["content"]}")
    return "\n\n".join(parts)
def rag_prompt(content_text:str,query_text:str):
    prompt_template = """你是一个问答助手，请根据下面给出的参考资料回答用户问题。规则按优先级从高到低：
1. 参考资料里有的内容，按原文回答，不要改口。原文写"突破""超过"就照用，不要换成"增长较快""持续提升"之类的软话；原文自带"预计"的，照抄原文的"预计"。
2. 参考资料里没有的内容，可以用常识补充，但不许编造具体数字、时间、机构名称，不许猜测。
3. 实在拿不准时，只回答【这个我还不确定，请您自行去官网查询呢】，不要解释原因。
4. 除了照抄原文，回答中不许出现"资料中没有""报告没有提到"之类的说法，也不许自己加"预计""大约""可能""有望"等推测词。
参考资料：{content} ，问题：{query}"""
    prompt = prompt_template.format(content=content_text,query=query_text)
    logger.debug(f"完整提示词为{prompt}")
    return prompt
if __name__ == "__main__":
    text = [ {"content": "Python是一门解释型编程语言,由吉多开发。", "source": "测试.txt"},
          {"content": "Java 是编译型语言。", "source": "测试.txt"},]
    text_query = "Python是什么编程语言"
    print(rag_prompt(fromat_docs(text),text_query))