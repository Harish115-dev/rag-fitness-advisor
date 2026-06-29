from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
class LocalEmbeddings:
    def embed_documents(self, texts):
        return model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text):
        return model.encode([text], normalize_embeddings=True)[0].tolist()

embeddings = LocalEmbeddings()
db= {
    "exercise": Chroma(
        collection_name="exercise",
        persist_directory="chroma db/exercise",
        embedding_function=embeddings
    ),
    "workout": Chroma(
        collection_name="workout",
        persist_directory="chroma db/workout",
        embedding_function=embeddings
    ),
    "nutrition": Chroma(
        collection_name="nutrition",
        persist_directory="chroma db/nutrition",
        embedding_function=embeddings
    ),
    "guidelines": Chroma(
        collection_name="guidelines",
        persist_directory="chroma db/guidelines",
        embedding_function=embeddings
    ),
    "compendium": Chroma(
        collection_name="compendium",
        persist_directory="chroma db/compendium",
        embedding_function=embeddings
    ),
    "nutrition100g": Chroma(
        collection_name="nutrition100g",
        persist_directory="chroma db/nutrition100g",
        embedding_function=embeddings
    )
}

