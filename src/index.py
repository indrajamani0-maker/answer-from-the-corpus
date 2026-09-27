import json
import numpy as np
from sentence_transformers import SentenceTransformer

from .config import CHUNKS_FILE, EMBEDDINGS_FILE, META_FILE, EMBEDDING_MODEL


def load_chunks():
    with CHUNKS_FILE.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def main():
    chunks = load_chunks()
    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    np.save(EMBEDDINGS_FILE, np.asarray(embeddings, dtype="float32"))
    META_FILE.write_text(json.dumps({"model": EMBEDDING_MODEL, "count": len(chunks)}, indent=2), encoding="utf-8")
    print(f"Indexed {len(chunks)} chunks")


if __name__ == "__main__":
    main()
