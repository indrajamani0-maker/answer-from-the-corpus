import json
from pathlib import Path
from src.config import TEST_FILE, DATA_DIR
from src.retrieval import Retriever
from src.answer import answer_question


def main():
    items = json.loads(Path(TEST_FILE).read_text(encoding="utf-8"))
    retriever = Retriever()
    results = []
    for i, item in enumerate(items, 1):
        retrieved = retriever.search(item["question"])
        allowed, gate_reason = retriever.gate(retrieved)
        if not allowed:
            answer = {"supported": False, "answer": "not in the source material", "citations": [], "reason": gate_reason}
        else:
            answer = answer_question(item["question"], retrieved)
        row = {**item, "top_similarity": retrieved[0]["similarity"] if retrieved else 0.0, "gate": gate_reason, **answer}
        results.append(row)
        print(f"[{i}/20] {item['question']}\n -> {answer['answer']}\n")
    out = DATA_DIR / "results.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved results to {out}")


if __name__ == "__main__":
    main()
