import json
from pathlib import Path
import streamlit as st

from src.config import CHUNKS_FILE, EMBEDDINGS_FILE, TEST_FILE, MIN_SIMILARITY, MIN_MARGIN
from src.retrieval import Retriever
from src.answer import answer_question

st.set_page_config(page_title="Answer From the Corpus", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1180px;}
.hero {padding: 3rem 2.5rem; border: 1px solid rgba(124,58,237,.35); border-radius: 28px; background: radial-gradient(circle at 85% 15%, rgba(124,58,237,.28), transparent 35%), linear-gradient(135deg,#111113,#18121f); box-shadow: 0 18px 70px rgba(0,0,0,.28);}
.badge {display:inline-block; padding:.4rem .8rem; border-radius:999px; background:rgba(124,58,237,.18); color:#c4b5fd; font-weight:700; font-size:.82rem; letter-spacing:.04em;}
.hero h1 {font-size:3.2rem; margin:.8rem 0 .5rem; letter-spacing:-.04em;}
.hero p {font-size:1.08rem; color:#d4d4d8; max-width:760px; line-height:1.7;}
.card {padding:1.25rem; border:1px solid #27272a; border-radius:18px; background:#111113; height:100%;}
.card h3 {margin-top:0;}
.metric {padding:1rem; border-radius:16px; background:#18181b; border:1px solid #27272a;}
.citation {padding:.85rem 1rem; border-left:3px solid #8b5cf6; background:#18181b; margin:.5rem 0; border-radius:0 10px 10px 0;}
.answer {padding:1.25rem; border-radius:18px; background:#141416; border:1px solid #3f3f46; line-height:1.7;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_retriever():
    if not CHUNKS_FILE.exists() or not EMBEDDINGS_FILE.exists():
        return None
    return Retriever()

retriever = get_retriever()

with st.sidebar:
    st.markdown("## ◈ Corpus RAG")
    page = st.radio("Navigate", ["Home", "Ask the Corpus", "Evaluation", "About"], label_visibility="collapsed")
    st.divider()
    st.caption("API-free retrieval QA")
    st.caption(f"Similarity gate: ≥ {MIN_SIMILARITY:.2f}")
    st.caption(f"Margin gate: ≥ {MIN_MARGIN:.3f}")

if page == "Home":
    st.markdown('''<div class="hero"><span class="badge">API-FREE • EVIDENCE-FIRST • ABSTENTION</span><h1>Answer From the Corpus</h1><p>A measured retrieval QA system that answers only from its source material — and knows when to say <b>not in the source material</b>.</p></div>''', unsafe_allow_html=True)
    st.write("")
    cols = st.columns(3)
    for col, title, body in zip(cols, ["Retrieve", "Verify", "Cite"], ["Find the strongest passages with local semantic search.", "Use an explicit evidence gate before answering.", "Show the exact document and chunk supporting the answer."]):
        with col:
            st.markdown(f'<div class="card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
    st.write("")
    st.info("No Gemini, OpenAI, Claude, or other hosted LLM API is used. Embeddings and answer extraction run locally.")
    if retriever:
        st.success(f"Corpus ready: {len(retriever.chunks):,} indexed passages from 30+ public Python PEP documents.")
    else:
        st.warning("Corpus is not indexed yet. Run `python -m src.ingest` and `python -m src.index`." )

elif page == "Ask the Corpus":
    st.title("Ask the Corpus")
    st.caption("Answers are extracted from retrieved evidence. If the evidence is insufficient, the system abstains.")
    if not retriever:
        st.error("Index not found. Run the ingestion and indexing commands first.")
        st.stop()
    question = st.text_area("Your question", placeholder="e.g. What does PEP 8 say about spaces around binary operators?", height=100)
    if st.button("Search corpus", type="primary", use_container_width=True) and question.strip():
        retrieved = retriever.search(question)
        allowed, gate_reason = retriever.gate(retrieved)
        if allowed:
            result = answer_question(question, retrieved)
        else:
            result = {"supported": False, "answer": "not in the source material", "citations": [], "reason": gate_reason}
        if result["supported"]:
            st.markdown("### Answer")
            st.markdown(f'<div class="answer">{result["answer"]}</div>', unsafe_allow_html=True)
            st.markdown("### Sources")
            for p in retrieved:
                if p["chunk_id"] in result["citations"]:
                    st.markdown(f'<div class="citation"><b>PEP {p["pep"]}: {p["title"]}</b><br><small>{p["chunk_id"]} • similarity {p["similarity"]:.3f}</small><br>{p["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown("### Answer")
            st.markdown('<div class="answer"><b>not in the source material</b></div>', unsafe_allow_html=True)
        with st.expander("Retrieval diagnostics"):
            st.write(result["reason"])
            st.write(gate_reason)
            for p in retrieved:
                st.write(f"{p['similarity']:.3f} — PEP {p['pep']} — {p['chunk_id']}")

elif page == "Evaluation":
    st.title("20-Question Evaluation")
    results_path = Path("data/results.json")
    if not results_path.exists():
        st.info("Run `python evaluate.py` to generate the evaluation results.")
    else:
        results = json.loads(results_path.read_text(encoding="utf-8"))
        supported = sum(r["supported"] for r in results)
        abstained = len(results) - supported
        a,b,c = st.columns(3)
        a.metric("Questions", len(results))
        b.metric("Supported answers", supported)
        c.metric("Abstentions", abstained)
        st.dataframe([{k:r[k] for k in ["id","group","question","answer","top_similarity"]} for r in results], use_container_width=True, hide_index=True)

elif page == "About":
    st.title("About the system")
    st.markdown("""
### Why no API?
The assignment does not mandate a hosted LLM. This implementation keeps the answer step local so the system can be evaluated without API availability or model-service outages.

### Evidence policy
A supported answer must come from retrieved corpus text. If retrieval is weak, the system abstains with the exact required phrase:

> `not in the source material`

### Current design
- 30+ Python PEP documents
- paragraph-aware chunking
- local `all-MiniLM-L6-v2` embeddings
- cosine similarity retrieval
- top-score + top-2 margin gate
- sentence-level extractive answering
- chunk-level citations
- 20-question evaluation
""")
