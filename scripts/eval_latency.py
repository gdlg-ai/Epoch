#!/usr/bin/env python3
"""
Lightweight local latency benchmark for Project Epoch.
Measures P50/P95 for embedding+query via the public API.

Usage:
  python scripts/eval_latency.py --host http://localhost:8000 --queries 100
"""
import argparse
import json
import random
import statistics
import string
import time
import requests


def random_text(n_words=12):
    words = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3,10))) for _ in range(n_words)]
    return ' '.join(words)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='http://localhost:8000')
    ap.add_argument('--queries', type=int, default=50)
    ap.add_argument('--top_k', type=int, default=5)
    args = ap.parse_args()

    # Warmup ingest a few notes
    for _ in range(20):
        text = random_text(20)
        requests.post(f"{args.host}/ingest", json={"text": text, "tags": ["bench"]}, timeout=10)

    lat = []
    for _ in range(args.queries):
        q = random_text(10)
        t0 = time.time()
        r = requests.post(f"{args.host}/query", json={"query": q, "top_k": args.top_k}, timeout=30)
        r.raise_for_status()
        _ = r.json()
        lat.append((time.time() - t0) * 1000)

    p50 = statistics.median(lat)
    p95 = statistics.quantiles(lat, n=100)[94]
    out = {
        "queries": args.queries,
        "top_k": args.top_k,
        "p50_ms": round(p50, 2),
        "p95_ms": round(p95, 2),
    }
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()

