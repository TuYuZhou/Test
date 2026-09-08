def load_txt_file(file_path: str) -> str:
    """读取txt文本，返回完整字符串"""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def split_text_overlap(text: str, chunk_size=300, chunk_overlap=50):
    """
    实现带重叠窗口的文本分割
    :param chunk_size:每块最大字符数
    :param chunk_overlap:相邻块重叠字符数量
    :return:分块后的文本列表
    """
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        # 滑动窗口：下一块起点 = 当前起点 + 块大小 - 重叠长度
        start = start + chunk_size - chunk_overlap
    return chunks


if __name__ == "__main__":
    # 测试代码
    full_text = load_txt_file("docs/test.txt")
    chunk_list = split_text_overlap(full_text, chunk_size=300, chunk_overlap=50)
    print(f"一共分割成 {len(chunk_list)} 块")
    for idx, content in enumerate(chunk_list):
        print(f"\n====块{idx+1}====")
        print(content)
