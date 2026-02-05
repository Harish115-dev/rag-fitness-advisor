from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

emb_bge=OllamaEmbeddings(
    model="bge-m3",
    base_url="http://localhost:11434"
)
emb_nomic=OllamaEmbeddings(
    model="nomic-embed-text",  
    base_url="http://localhost:11434"
)
db= {
    "exercise": Chroma(
        collection_name="exercise",
        persist_directory="chroma_db/exercise",
        embedding_function=emb_bge
    ),
    "workout": Chroma(
        collection_name="workout",
        persist_directory="chroma_db/workout",
        embedding_function=emb_bge
    ),
    "nutrition": Chroma(
        collection_name="nutrition",
        persist_directory="chroma_db/nutrition",
        embedding_function=emb_bge
    ),
    "guidelines": Chroma(
        collection_name="guidelines",
        persist_directory="chroma_db/guidelines",
        embedding_function=emb_bge
    ),
    "compendium": Chroma(
        collection_name="compendium",
        persist_directory="chroma_db/compendium",
        embedding_function=emb_bge
    ),
    "nutrition100g": Chroma(
        collection_name="nutrition100g",
        persist_directory="chroma_db/nutrition100g",
        embedding_function=emb_nomic
    )
}

