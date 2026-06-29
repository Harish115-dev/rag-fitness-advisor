---
title: FitForge
emoji: ⚡
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# FitForge — AI Fitness & Nutrition Advisor

FitForge is an AI-powered RAG (Retrieval-Augmented Generation) chatbot that answers questions about workouts, nutrition, calorie burn, and diet planning. It retrieves context from a curated knowledge base and generates accurate, structured responses using Groq's LLaMA model.

---

## Demo

> Coming soon — deploying on Render

---

## How It Works

```
User Query
    │
    ▼
Query Router  ──►  selects relevant ChromaDB collection(s)
    │
    ▼
Similarity Search  ──►  retrieves top-k relevant chunks
    │
    ▼
LLaMA 3.1 (via Groq)  ──►  generates answer from context
    │
    ▼
FitForge UI
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, Vanilla JS |
| Backend | Flask |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| LLM | LLaMA 3.1 8B via Groq API |
| Orchestration | LangChain |

---

## Data Sources

| Collection | Source | Description |
|---|---|---|
| `nutrition` | WHO PDFs | Healthy diet, sodium, sugar, fat intake guidelines |
| `nutrition100g` | USDA FoodData Central | Nutritional values per 100g for 33,000+ foods |
| `exercise` | Open-source exercises JSON | 1000+ exercises with muscles, equipment, level |
| `workout` | Curated PDFs | Beginner workout plans, bulking & cutting diet plans |
| `compendium` | Adult Compendium 2024 | MET values for 1100+ physical activities |
| `guidelines` | WHO + Supplement PDFs | Physical activity guidelines, supplement guide, training methodology |

---

## Project Structure

```
fitforge/
│
├── data/
│   ├── raw/                        # original PDFs and CSVs
│   └── chunks/                     # processed JSON and CSV chunks
│
├── notebooks/
│   ├── csv_file_chunker.ipynb      # USDA nutrition data processing
│   ├── exercise_chunker.ipynb      # exercise JSON processing
│   └── pdf_chunker.ipynb           # PDF text extraction & chunking
│
├── chroma db/                      # vector store (6 collections)
│
├── static/
│   ├── css/style.css
│   └── js/app.js
│
├── templates/
│   └── index.html
│
├── app.py                          # Flask app & routes
├── rag.py                          # RAG pipeline & LLM call
├── router.py                       # query → collection router
├── search_db.py                    # similarity search
├── load_database.py                # loads ChromaDB collections
├── embed.py                        # one-time embedding script
│
├── .env                            # secrets (never committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Harish115-dev/fitforge.git
cd fitforge
```

**2. Create a virtual environment with Python 3.11**
```bash
python3.11 -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root:
```
GROQ_API_KEY=your_groq_api_key
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

**5. Run the app**
```bash
flask run
```

Open `http://localhost:5000`

---

## Embedding (one-time setup)

If you want to rebuild the vector store from scratch:

```bash
python embed.py
```

This reads all files from `data/chunks/`, embeds them using `sentence-transformers/all-MiniLM-L6-v2` locally, and stores vectors in `chroma db/`.

---

## Collections & Routing

The `router.py` file scores each query against keyword sets and routes it to the most relevant ChromaDB collection(s):

| Keywords | Collection |
|---|---|
| eat, meal, diet, pre/post workout | `nutrition` |
| calories, protein, carbs, per 100g | `nutrition100g` |
| exercise, how to, push up, squat | `exercise` |
| workout, routine, split, plan | `workout` |
| burn, MET, energy expenditure | `compendium` |
| safe, avoid, injury, recommend | `guidelines` |

---

## What I Learned

- Building a full RAG pipeline from raw data to production
- Chunking and embedding different data formats (PDF, CSV, JSON)
- Replacing local Ollama embeddings with a hostable sentence-transformers solution
- Query routing across multiple vector collections
- Deploying a Flask + ChromaDB app on Render

---

## Author

**Harish Rathwa**  
[GitHub](https://github.com/Harish115-dev)