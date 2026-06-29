"""
Day 4: run the tagger over every article in data/ and write results to output/.
This is the 'it works at scale, not just one example' piece.
"""
import os
import json
from src.tagger import tag_article

DATA_DIR = "data"
OUTPUT_FILE = "output/results.json"


def run_batch():
    results = {}
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".txt")]

    if not files:
        print(f"No .txt files in {DATA_DIR}/ — drop some articles there first.")
        return

    for filename in files:
        path = os.path.join(DATA_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"Processing {filename} ...")
        result = tag_article(text)
        results[filename] = result
        print(f"  -> {result['status']} | category: {result.get('category', 'N/A')}")

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    ok = sum(1 for r in results.values() if r["status"] == "ok")
    review = len(results) - ok
    print(f"\nDone. {ok} auto-tagged, {review} routed for human review.")
    print(f"Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_batch()
