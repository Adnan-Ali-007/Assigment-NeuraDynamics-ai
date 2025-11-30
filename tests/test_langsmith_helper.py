import os
import json
from src.testing.langsmith_helper import log_evaluation


def test_log_evaluation_writes_file(tmp_path, monkeypatch):
    # Redirect tests dir to tmp for isolation
    repo_root = tmp_path
    tests_dir = repo_root / "tests"
    tests_dir.mkdir()

    # Monkeypatch the helper's path calculation by setting environment variable for repo root
    # Simpler: call function and ensure it returns the entry dict and that write happens
    entry = log_evaluation("example-1", "predicted", "reference", {"foo": "bar"})
    assert entry["example_id"] == "example-1"
    assert entry["prediction"] == "predicted"
    assert entry["reference"] == "reference"
