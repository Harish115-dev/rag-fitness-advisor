from load_database import db
from router import query_router

def search(query,k=5):
    source=query_router(query)
    docs=[]
    for s in source:
        results=db[s].similarity_search(query,k=k)
        docs.extend(results)
    return docs

