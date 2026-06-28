import os
import json
import csv
from langchain_core.documents import Document
from langchain_chroma import Chroma
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class LocalEmbeddings:
    def embed_documents(self, texts):
        return model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text):
        return model.encode([text], normalize_embeddings=True)[0].tolist()

embeddings = LocalEmbeddings()

JSON_FILES = {
    "workout":    "data/chunks/workoutchunks.json",
    "exercise":   "data/chunks/exercise_chunks.json",
    "nutrition":  "data/chunks/nutritionchunks.json",
    "guidelines": "data/chunks/guidelineschunks.json",
    "compendium": "data/chunks/compendiumchunks.json",
}
csv_file = "data/chunks/clean_food_nutrition_100g.csv"

for collection, file_name in JSON_FILES.items():
    if not os.path.exists(file_name):
        print(f"Skipping {file_name} — file not found")
        continue

    with open(file_name, "r", encoding="UTF-8") as f:
        chunks = json.load(f)
    print(f"\nLoaded {len(chunks)} chunks from {file_name}")

    documents = []
    for chunk in chunks:
        if "text" in chunk:
            text = chunk["text"]
        elif "content" in chunk:
            text = chunk["content"]
        elif "activity" in chunk:
            text = f"Activity: {chunk['activity']}. MET value: {chunk.get('met', 'N/A')}."
        else:
            continue

        metadata = {
            "source":   str(chunk.get("source") or ""),
            "type":     str(chunk.get("doc_type") or "unknown"),
            "page":     str(chunk.get("page") or ""),
            "category": str(chunk.get("category") or ""),
            "chunk_id": str(chunk.get("chunk_id") or ""),
        }

        if "activity" in chunk:
            metadata["type"] = "activity"
            metadata["activity_code"] = str(chunk.get("activity_code") or "")
            metadata["met"] = str(chunk.get("met") or "")

        if "content" in chunk and "Exercise Name" in chunk.get("content", ""):
            metadata["type"] = "exercise"
            if "metadata" in chunk:
                metadata["level"] = str(chunk["metadata"].get("level") or "")
                metadata["equipment"] = str(chunk["metadata"].get("equipment") or "")
                muscles = chunk["metadata"].get("primary_muscles")
                metadata["primary_muscles"] = (
                    ", ".join(muscles) if isinstance(muscles, list) else str(muscles or "")
                )

        documents.append(Document(page_content=text, metadata=metadata))

    
    db = Chroma(
        persist_directory=f"chroma db/{collection}",
        collection_name=collection,
        embedding_function=embeddings,
    )
    BATCH_SIZE = 50
    total = len(documents)
    for i in range(0, total, BATCH_SIZE):
        db.add_documents(documents[i:i + BATCH_SIZE])
        print(f"  [{collection}] embedded {min(i + BATCH_SIZE, total)}/{total}")

    print(f"  [{collection}] total in DB: {db._collection.count()}")



if not os.path.exists(csv_file):
    print(f"\nSkipping {csv_file} — file not found")
else:
    csv_documents = []
    with open(csv_file, encoding="UTF-8") as f:
        rows = list(csv.DictReader(f))
    print(f"\nLoaded {len(rows)} rows from {csv_file}")

    for row in rows:
        text = (
            f"Food Name: {row.get('food_name')}. "
            f"Calories: {row.get('calories')} kcal per 100g. "
            f"Carbohydrates: {row.get('carbs')} g. "
            f"Protein: {row.get('protein')} g. "
            f"Fat: {row.get('fat')} g. "
            f"Fiber: {row.get('fiber')} g. "
            f"Calcium: {row.get('calcium')} mg. "
            f"Iron: {row.get('iron')} mg. "
            f"Potassium: {row.get('potassium')} mg. "
            f"Sodium: {row.get('sodium')} mg. "
            f"Vitamin A: {row.get('vitamin_a')} IU. "
            f"Vitamin C: {row.get('vitamin_c')} mg. "
            f"Vitamin D: {row.get('vitamin_d')} IU."
        )
        csv_documents.append(Document(
            page_content=text,
            metadata={
                "type":      "nutrition_csv",
                "source":    "clean_food_nutrition_100g.csv",
                "food_name": str(row.get("food_name") or ""),
                "page":      "1",
            },
        ))

    nutrition_db = Chroma(
        persist_directory="chroma db/nutrition100g",
        collection_name="nutrition100g",
        embedding_function=embeddings,
    )
    BATCH_SIZE = 100
    total = len(csv_documents)
    for i in range(0, total, BATCH_SIZE):
        nutrition_db.add_documents(csv_documents[i:i + BATCH_SIZE])
        print(f"  [nutrition100g] embedded {min(i + BATCH_SIZE, total)}/{total}")

    print(f"  [nutrition100g] total in DB: {nutrition_db._collection.count()}")

print("\n✓ All done! Your chroma db/ folder is ready.")