from search_db import search
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import re
load_dotenv()
client = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)
 

def answer(query):
    q = re.sub(r"[^a-zA-Z\s]", "", query.lower()).strip()

    
    if q in ["what is your name", "who are you", "name", "your name"]:
        return "### 👋 Hello!\nMy name is **ATLAS** — your AI Fitness & Nutrition Advisor."

    if q in ["hi", "hello", "hey", "hyy", "hii"]:
        return "Hello! 👋 How can I help you with fitness or nutrition today?"

    docs=search(query)
    context="\n\n".join([doc.page_content for doc in docs])
    prompt = f"""
                You are a fitness & diet advisor.
                your name is ATLAS.
                Use ONLY the context for factual answers
                If the answer is missing, say: "I don't have enough information."
                Rules for answers:
                - Start with a short heading
                - Then bullet points
                - Avoid filler text
                - Use clear headings
                - Use bullet points
                - Avoid long paragraphs
                - Output clean Markdown


                Context: {context}
                quetion:{query}
                """

    response = client.invoke(prompt)

    return response.content
    