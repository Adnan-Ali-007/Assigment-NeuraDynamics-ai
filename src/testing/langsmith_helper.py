import os
import json
from datetime import datetime
from typing import Optional


def log_evaluation(example_id: str, prediction: str, reference: str, meta: Optional[dict] = None):
    """Write a simple evaluation record to tests/langsmith_logs.jsonl.

    This helper intentionally avoids external SDKs and network calls.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "example_id": example_id,
        "prediction": prediction,
        "reference": reference,
        "meta": meta or {}
    }

    try:
        root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logs_dir = os.path.join(root, "tests")
        os.makedirs(logs_dir, exist_ok=True)
        logs_file = os.path.join(logs_dir, "langsmith_logs.jsonl")
        with open(logs_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        # If writing fails, return the entry so callers can inspect it
        return entry

    return entry
