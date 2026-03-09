from sentence_transformers import SentenceTransformer
import chromadb

model=SentenceTransformer("BAAI/bge-small-en")

client = chromadb.Client()

collection = client.create_collection("meeting")

def store_context(text):
    chunks = text.split("/n")
    for i,chunk in enumerate(chunks):
        emb=model.encode(chunk).tolist()
        collection.add(ids=[str(i)],embeddings=[emb],documents=[chunk])

def retrieve(query):
    emb=model.encode(query).tolist()
    res=collection.query(query_embeddings=[emb],n_results=5)
    return "\n".join(res["documents"][0])       