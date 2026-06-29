from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class LocalEmbeddings:
    def embed_documents(self, texts):
        return model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text):
        return model.encode([text], normalize_embeddings=True)[0].tolist()

embeddings = LocalEmbeddings()

_db_cache = {}

COLLECTIONS = ["exercise", "workout", "nutrition", "guidelines", "compendium", "nutrition100g"]

def get_db(collection):
    if collection not in _db_cache:
        _db_cache[collection] = Chroma(
            collection_name=collection,
            persist_directory=f"chroma db/{collection}",
            embedding_function=embeddings,
        )
    return _db_cache[collection]

db = {name: None for name in COLLECTIONS}

class LazyDB:
    def __getitem__(self, key):
        return get_db(key)

db = LazyDB()