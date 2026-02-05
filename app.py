from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag import answer
import os

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/api/v1/query")
def query_atlas(query: Query):
    return {"answer": answer(query.question)}

if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
