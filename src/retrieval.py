import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer

from .config import CHUNKS_FILE, EMBEDDINGS_FILE, EMBEDDING_MODEL, TOP_K, MIN_SIMILARITY, MIN_MARGIN


class Retriever:
    def __init__(self):
        with CHUNKS_FILE.open(encoding="utf-8") as f:
            self.chunks = [json.loads(line) for line in f]
        self.embeddings = np.load(EMBEDDINGS_FILE)
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def search(self, question, top_k=TOP_K):
        q = self.model.encode([question], normalize_embeddings=True)[0]
        scores = self.embeddings @ q
        order = np.argsort(-scores)[:top_k]
        results = []
        for idx in order:
            item = dict(self.chunks[int(idx)])
            item["similarity"] = float(scores[int(idx)])
            results.append(item)
        return results

    @staticmethod
    def gate(results):
        if not results:
            return False, "no retrieval results"
        top = results[0]["similarity"]
        second = results[1]["similarity"] if len(results) > 1 else 0.0
        margin = top - second
        if top < MIN_SIMILARITY:
            return False, f"top similarity {top:.3f} < {MIN_SIMILARITY:.3f}"
        if margin < MIN_MARGIN:
            return False, f"top-2 margin {margin:.3f} < {MIN_MARGIN:.3f}"
        return True, f"top={top:.3f}, margin={margin:.3f}"


def keywords(text):
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", text.lower())
    stop = {"what", "does", "the", "about", "which", "that", "this", "with", "from", "into", "how", "why", "what", "is", "are", "and", "for"}
    return set(w for w in words if w not in stop)
