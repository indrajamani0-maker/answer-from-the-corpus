import re
from .config import MIN_EVIDENCE_SCORE
from .retrieval import keywords


def split_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 25]


def sentence_score(question, sentence, chunk_similarity):
    q = keywords(question)
    s = keywords(sentence)
    overlap = len(q & s) / max(1, len(q))
    return 0.65 * overlap + 0.35 * max(0.0, min(1.0, chunk_similarity))


def answer_question(question, passages):
    if not passages:
        return {"supported": False, "answer": "not in the source material", "citations": [], "reason": "No retrieved evidence."}

    candidates = []
    for p in passages:
        for sentence in split_sentences(p["text"]):
            score = sentence_score(question, sentence, p["similarity"])
            candidates.append((score, sentence, p))

    candidates.sort(key=lambda x: x[0], reverse=True)
    if not candidates or candidates[0][0] < MIN_EVIDENCE_SCORE:
        return {
            "supported": False,
            "answer": "not in the source material",
            "citations": [],
            "reason": f"Best evidence score {candidates[0][0]:.3f} is below {MIN_EVIDENCE_SCORE:.3f}." if candidates else "No sentence evidence.",
        }

    best_score, best_sentence, best_passage = candidates[0]
    selected = [best_sentence]
    citations = [best_passage["chunk_id"]]

    # Add one complementary sentence when it materially shares question terms.
    for score, sentence, passage in candidates[1:]:
        if score >= max(MIN_EVIDENCE_SCORE, best_score - 0.08) and passage["chunk_id"] not in citations:
            selected.append(sentence)
            citations.append(passage["chunk_id"])
            break

    return {
        "supported": True,
        "answer": " ".join(selected),
        "citations": citations,
        "reason": f"Extracted from retrieved evidence; evidence score {best_score:.3f}.",
    }
