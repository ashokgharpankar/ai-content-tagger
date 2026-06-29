"""
Quick single-article test. Run this during Days 1-3 to check your work:
    python main.py
"""
from src.tagger import tag_article
import json

SAMPLE = """
The new electric vehicle startup announced record deliveries this quarter,
beating analyst expectations. The company credited improved battery supply
chains and a new factory in Texas. Shares rose 12% in after-hours trading.
"""

if __name__ == "__main__":
    result = tag_article(SAMPLE)
    print(json.dumps(result, indent=2))
