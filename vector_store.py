from sentence_transformers import SentenceTransformer
import chromadb
from load_doc import load_txt_file, split_text_overlap

# 加载本地向量化模型
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def create_chroma_collection(db_path="./chroma_db"):
    """创建/加载本地持久化向量库"""
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name="doc_collection")
    return collection

def add_text_to_vector_db(collection, chunk_list):
    """文本块转为向量，存入Chroma"""
    embeddings = embedding_model.encode(chunk_list).tolist()
    ids = [f"id_{i}" for i in range(len(chunk_list))]
    collection.add(
        embeddings=embeddings,
        documents=chunk_list,
        ids=ids
    )

def search_related_chunk(collection, query: str, top_n=2):
    """问题向量化，检索语义最匹配的片段"""
    query_embedding = embedding_model.encode([query]).tolist()
    result = collection.query(
        query_embeddings=query_embedding,
        n_results=top_n
    )
    return result["documents"][0]


if __name__ == "__main__":
    # 端到端测试：加载文档→分块→入库→检索
    full_text = load_txt_file("docs/test.txt")
    chunks = split_text_overlap(full_text)
    coll = create_chroma_collection()
    add_text_to_vector_db(coll, chunks)
    print("✅文本向量入库完成")

    question = "LME铜价最高达到多少？"
    res = search_related_chunk(coll, question)
    print(f"\n🔍检索问题：{question}")
    for idx, text in enumerate(res):
        print(f"\n片段{idx+1}：\n{text}")
