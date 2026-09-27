# Answer From the Corpus — API-Free RAG

A measured retrieval QA system built for the **Answer From the Corpus** exercise.

## What it does

- Ingests 30+ public Python PEP documents.
- Cleans and chunks the documents.
- Builds local sentence-transformer embeddings.
- Retrieves the most relevant passages with cosine similarity.
- Uses an explicit evidence gate for abstention.
- Produces an extractive answer from the retrieved evidence — **no Gemini/OpenAI/LLM API**.
- Shows document and chunk citations for every supported answer.
- Returns exactly `not in the source material` when evidence is insufficient.
- Includes a Streamlit interface with an attractive landing page, Ask Corpus page, and evaluation dashboard.

## Run

### 1. Create environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install

```powershell
pip install -r requirements.txt
```

### 3. Build corpus

```powershell
python -m src.ingest
python -m src.index
```

The first run downloads the public PEP pages and the local embedding model. No AI API key is required.

### 4. Launch the app

```powershell
streamlit run app.py
```

### 5. Run evaluation

```powershell
python evaluate.py
```

## API requirement

**None.** There is no Gemini, OpenAI, Claude, or other hosted LLM call in this project.

The only network access during setup is downloading the public corpus pages and the open-source embedding model. After those assets are present locally, retrieval and answer extraction run locally.

## Architecture

```text
PEP documents
    ↓
HTML cleaning + paragraph-aware chunking
    ↓
Sentence-transformer embeddings
    ↓
Cosine similarity retrieval
    ↓
Evidence gate
    ├── weak → not in the source material
    └── strong
          ↓
    sentence-level evidence scoring
          ↓
    extractive answer + citations
```

## Design note

This version deliberately avoids an LLM answer-generation step. That makes abstention behavior deterministic and keeps the evaluation focused on retrieval quality, evidence coverage, citations, and failure modes.
