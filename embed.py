import os
import json
import csv
from langchain_core.documents import Document
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
load_dotenv()

csv_file="data/chunks/clean_food_nutrition_100g.csv"
file_name="data/chunks/workoutchunks.json"# change according to file 
documents=[]

embeddings=OllamaEmbeddings(
    model="bge-m3",
    base_url="http://localhost:11434"
)
embeddings2 = OllamaEmbeddings(
    model="nomic-embed-text",  
    base_url="http://localhost:11434"
)
# for json files
with open (file_name,"r", encoding="UTF-8") as f:
    chunks =json.load(f) 
    print(f"Loaded {len(chunks)} chunks from {file_name}")

#normalizing chunks for embedd
for chunk in chunks:
    if "text" in chunk:
        text=chunk["text"]
    elif "content" in chunk:
        text=chunk["content"]
    elif "activity" in chunk:
        text = f"Activity: {chunk['activity']}. MET value: {chunk.get('met', 'N/A')}."
    else:
        continue

    metadata={
        "source":chunk.get("source"),
        "type":chunk.get("doc_type","unknown"),
        "page":chunk.get("page"),
        "category":chunk.get("category"),
        "chunk_id":chunk.get("chunk_id")
    }
    #for compendiumchunks
    if "activity" in chunk:
        metadata["type"]="activity"
        metadata["activity_code"]=chunk.get("activity_code")
        metadata["met"]=chunk.get("met")
    # for exercise chunks
    if "content" in chunk and "Exercise Name" in chunk.get("content",""):
        metadata["type"]="exercise"
        if "metadata" in chunk:
            metadata["level"]=chunk["metadata"].get("level")
            metadata["equipment"]=chunk["metadata"].get("equipment")
            muscles = chunk["metadata"].get("primary_muscles")
            if isinstance(muscles, list):
                metadata["primary_muscles"] = ", ".join(muscles)
            else:
                metadata["primary_muscles"] = muscles

    documents.append(Document(page_content=text,metadata=metadata))


# for csv file
csv_documents=[]
with open(csv_file,encoding="UTF-8")as f:
    reader=csv.DictReader(f)
    rows = list(reader)   

    print(f"Total rows: {len(rows)}")

    for row in rows:
        text=(
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
        metadata=(
            {   "type": "nutrition_csv",
                "source":"clean_food_nutrition_100g.csv",
                "food_name":row.get("food_name"),
                "page":1
            }
        )
        csv_documents.append(Document(page_content=text,metadata=metadata))


#now embedd 
# change according to file name 
db = Chroma(
    persist_directory="chroma db/workout",
    collection_name="workout",
    embedding_function=embeddings
)

db.add_documents(documents)

print("COUNT AFTER embedd:", db._collection.count())


# nutrition_db = Chroma(
#     persist_directory="chroma db/nutrition100g",
#     collection_name="nutrition100g",
#     embedding_function=embeddings   # lighter model
# )

# print("CSV DOCUMENTS LENGTH:", len(csv_documents))
# print("Starting nutrition embedding...")

# BATCH_SIZE = 100
# total = len(csv_documents)

# for i in range(0, total, BATCH_SIZE):
#     batch = csv_documents[i:i + BATCH_SIZE]
#     nutrition_db.add_documents(batch)
#     print(f"Nutrition embedded {min(i + BATCH_SIZE, total)} / {total}")

# print("NUTRITION COUNT:", nutrition_db._collection.count())

















