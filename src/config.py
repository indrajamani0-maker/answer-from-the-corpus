from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CHUNKS_FILE = DATA_DIR / "chunks.jsonl"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.npy"
META_FILE = DATA_DIR / "index_meta.json"
TEST_FILE = DATA_DIR / "test_questions.json"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 180
TOP_K = 6
MIN_SIMILARITY = 0.42
MIN_MARGIN = 0.025
MIN_EVIDENCE_SCORE = 0.34
