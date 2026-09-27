# Answer From the Corpus — Write-up

## 1. System overview

Describe the corpus, chunking, local embedding model, retrieval, evidence gate, extractive answerer, and citation display.

## 2. 20-question evaluation

Run `python evaluate.py` and paste the results table here. Separate results into direct, spread, adjacent-but-absent, and plainly outside.

## 3. Abstention threshold

Current starting gate:
- top cosine similarity >= 0.42
- top-1 minus top-2 margin >= 0.025
- sentence evidence score >= 0.34

Do not claim these are final until measured. Compare threshold settings on the 20-question test set and record false accepts vs false abstentions.

## 4. Chunking experiment

Compare at least two chunk sizes/overlaps. Report retrieval quality and observed failure modes.

## 5. Confidently wrong case

Choose one case where retrieval looked strong but the evidence did not actually establish the requested fact. Explain why the system failed and what guard could reduce it.

## 6. Next week

Possible improvements: stronger reranking, hybrid lexical + semantic retrieval, better sentence-level evidence verification, larger held-out evaluation set, document metadata filters, and a local LLM answerer if hardware permits.

## 7. Client questions

Ask about corpus update frequency, expected query volume, acceptable latency, citation granularity, and what should happen when multiple documents disagree.
