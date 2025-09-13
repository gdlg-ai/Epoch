#!/usr/bin/env python3
"""
Lightweight retrieval quality evaluation (toy).
Define a tiny local dataset of (query -> relevant doc ids) and measure Recall@K.
Extend later to load public subsets.

Usage:
  python scripts/eval_retrieval.py --host http://localhost:8000 --top_k 5
"""
import argparse
import json
import time
import requests


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='http://localhost:8000')
    ap.add_argument('--top_k', type=int, default=5)
    args = ap.parse_args()

    # Small corpus and labels (toy). Replace with real subsets later.
    docs = [
        ("d1", "Apple unveils new M3 chip for MacBook Pro."),
        ("d2", "Open-source vector databases like Chroma support local-first apps."),
        ("d3", "Whisper small model improves Chinese punctuation accuracy."),
        ("d4", "Maximal Marginal Relevance increases result diversity in IR."),
        ("d5", "Raspberry Pi 5 performance for local AI workloads."),
    ]
    queries = [
        ("q1", "What is MMR in information retrieval?", {"d4"}),
        ("q2", "Which vector DB works well for local use?", {"d2"}),
        ("q3", "Apple M3 chip news", {"d1"}),
    ]

    # Ingest
    for _, text in docs:
        requests.post(f"{args.host}/ingest", json={"text": text, "tags": ["eval"]}, timeout=10)

    # Evaluate Recall@K
    hits = 0
    for qid, qtext, rel in queries:
        r = requests.post(f"{args.host}/query", json={"query": qtext, "top_k": args.top_k}, timeout=20)
        r.raise_for_status()
        res = r.json().get('results', [])
        got = False
        for item in res:
            if any(doc_text == item.get('text') for _, doc_text in docs if _ in rel):
                got = True
                break
        hits += 1 if got else 0
    recall = hits / len(queries)
    out = {
        "queries": len(queries),
        "top_k": args.top_k,
        "recall@k": round(recall, 3),
    }
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()

