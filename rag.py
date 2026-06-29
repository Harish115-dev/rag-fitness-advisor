from search_db import search
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import re
import difflib

load_dotenv()

client = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

GREETINGS = ["hi", "hello", "hey", "yo", "sup", "hii", "hyy", "hy"]

def is_greeting(q: str) -> bool:
    if not q or len(q.split()) > 3:
        return False
    return any(difflib.SequenceMatcher(None, q, g).ratio() > 0.75 for g in GREETINGS)


def answer(query):
    q = re.sub(r"[^a-zA-Z\s]", "", query.lower()).strip()

    if q in ["what is your name", "who are you", "name", "your name"]:
        return "### 👋 Hello!\nMy name is **FitForge** — your AI Fitness & Nutrition Advisor."

    if is_greeting(q):
        return "Hello! 👋 How can I help you with fitness or nutrition today?"

    docs = search(query)

    if not docs:
        prompt = f"""
You are a friendly fitness & diet advisor named FitForge.
The user said: "{query}"

This doesn't match a specific topic in your knowledge base yet.

Rules:
- NEVER ask a clarifying question. Do not ask the user anything.
- Always give a short, concrete, generically useful starting point
  related to fitness/nutrition, even if the message is vague.
- If the message is just small talk or unclear, gently steer toward
  fitness/nutrition with ONE example suggestion (e.g. "if you're not
  sure where to start, a simple 3-day full body beginner routine is
  a great default").
- Keep it conversational, 2-4 sentences max.
- Do NOT invent specific numbers/facts, do NOT use headings or bullets.
"""
        response = client.invoke(prompt)
        return response.content

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a fitness & diet advisor.
Your name is FitForge.
Use ONLY the context for factual answers.
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
Question: {query}
"""
    response = client.invoke(prompt)
    return response.content