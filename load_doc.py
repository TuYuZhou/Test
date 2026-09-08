"""
文档加载与文本分割模块
功能：读取 docs/ 目录下的 txt / pdf 文档，并切分为文本块
"""
import os
from pathlib import Path

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 文档目录
DOCS_DIR = Path(__file__).parent / "docs"

# 文本分割器（按字符递归切分，保证块大小适中、有重叠）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # 每块最大字符数
    chunk_overlap=50,     # 块之间重叠字符数，保留上下文
    separators=["\n\n", "\n", "。", "！", "？", ".", " ", ""],
)


def load_single_file(file_path: Path):
    """加载单个文档，返回 langchain Document 列表"""
    suffix = file_path.suffix.lower()
    if suffix == ".txt":
        loader = TextLoader(str(file_path), encoding="utf-8")
    elif suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
    else:
        print(f"[load_doc] 跳过不支持的文件类型: {file_path.name}")
        return []
    return loader.load()


def load_all_docs(docs_dir: Path = DOCS_DIR):
    """加载目录下所有支持的文档并切分"""
    if not docs_dir.exists():
        print(f"[load_doc] 文档目录不存在: {docs_dir}")
        return []

    all_docs = []
    for file in docs_dir.iterdir():
        if file.is_file() and file.suffix.lower() in (".txt", ".pdf"):
            print(f"[load_doc] 正在加载: {file.name}")
            all_docs.extend(load_single_file(file))

    # 切分
    chunks = text_splitter.split_documents(all_docs)
    print(f"[load_doc] 共加载 {len(all_docs)} 篇文档，切分为 {len(chunks)} 个文本块")
    return chunks


if __name__ == "__main__":
    chunks = load_all_docs()
    if chunks:
        print("首个文本块预览：")
        print(chunks[0].page_content[:200])
