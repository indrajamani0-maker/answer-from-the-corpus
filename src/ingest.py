import json
import re
import time
from bs4 import BeautifulSoup
import requests

from .config import CHUNK_SIZE, CHUNK_OVERLAP, CHUNKS_FILE, RAW_DIR
from .corpus import PEP_NUMBERS, pep_title, pep_url


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    main = soup.find("main") or soup.body or soup
    text = main.get_text("\n", strip=True)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def chunk_text(text: str):
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks, current = [], ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= CHUNK_SIZE:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
            overlap = current[-CHUNK_OVERLAP:] if current else ""
            current = (overlap + "\n\n" + para).strip()
    if current:
        chunks.append(current)
    return chunks


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "AnswerFromCorpus/1.0 educational retrieval exercise"}
    rows = []
    for i, number in enumerate(PEP_NUMBERS, 1):
        path = RAW_DIR / f"pep-{number:04d}.html"
        if path.exists():
            html = path.read_text(encoding="utf-8")
        else:
            print(f"[{i}/{len(PEP_NUMBERS)}] Downloading PEP {number}...")
            r = requests.get(pep_url(number), headers=headers, timeout=30)
            r.raise_for_status()
            html = r.text
            path.write_text(html, encoding="utf-8")
            time.sleep(0.1)
        text = clean_html(html)
        for idx, chunk in enumerate(chunk_text(text)):
            rows.append({
                "chunk_id": f"pep-{number:04d}-chunk-{idx:03d}",
                "pep": number,
                "title": pep_title(number),
                "url": pep_url(number),
                "text": chunk,
            })
    with CHUNKS_FILE.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows)} chunks from {len(PEP_NUMBERS)} PEP documents to {CHUNKS_FILE}")


if __name__ == "__main__":
    main()
