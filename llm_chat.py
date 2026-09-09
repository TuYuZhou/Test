import os
import requests
from dotenv import load_dotenv

# 加载.env环境变量
load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
API_URL = os.getenv("LLM_API_URL")

def build_prompt(context_list: list[str], question: str) -> list[dict]:
    """
    构造RAG提示词
    :param context_list: 向量库检索得到的相关文本片段列表
    :param question: 用户原始提问
    :return: 消息列表，适配openai风格接口
    """
    context_text = "\n".join([f"【参考片段】{item}" for item in context_list])
    system_prompt = """你是文档问答助手。请严格依据提供的参考片段回答用户问题。
- 如果参考片段没有相关信息，直接说明文档中没有找到答案，不要编造内容。
- 回答简洁，不要输出多余解释。"""
    user_prompt = f"参考文档：\n{context_text}\n用户问题：{question}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return messages


def get_answer(context_list: list[str], question: str) -> str:
    """
    调用LLM接口获取RAG答案
    """
    if not API_KEY or not API_URL:
        return "错误：请在.env配置LLM_API_KEY和LLM_API_URL"

    messages = build_prompt(context_list, question)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
               "messages": messages,
        "temperature": 0.3
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"LLM调用失败：{str(e)}"


if __name__ == "__main__":
    # 本地简易测试入口
    print("LLM问答助手启动")
    test_context = ["铜价近期小幅上涨，受市场供需影响。"]
    test_q = "铜价最近怎么样？"
    ans = get_answer(test_context, test_q)
    print("回答：", ans)
    print("LLM问答助手测试完成")