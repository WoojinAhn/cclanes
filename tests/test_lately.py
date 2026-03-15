import json
import os
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lately


def test_load_config_empty():
    """No config file → empty exclude list."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "config.json"
        cfg = lately.load_config(path)
        assert cfg == {"exclude": []}


def test_load_config_existing():
    """Existing config is loaded correctly."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "config.json"
        path.write_text(json.dumps({"exclude": ["repo1", "repo2"]}))
        cfg = lately.load_config(path)
        assert cfg["exclude"] == ["repo1", "repo2"]


def test_save_config():
    """Config is saved and can be reloaded."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "config.json"
        cfg = {"exclude": ["a", "b"]}
        lately.save_config(cfg, path)
        loaded = json.loads(path.read_text())
        assert loaded["exclude"] == ["a", "b"]


def test_add_exclude():
    """--exclude adds repos to config."""
    cfg = {"exclude": ["a"]}
    cfg = lately.add_excludes(cfg, ["b", "c"])
    assert sorted(cfg["exclude"]) == ["a", "b", "c"]


def test_add_exclude_no_duplicates():
    """--exclude does not duplicate existing entries."""
    cfg = {"exclude": ["a"]}
    cfg = lately.add_excludes(cfg, ["a", "b"])
    assert sorted(cfg["exclude"]) == ["a", "b"]


def test_remove_exclude():
    """--include removes repos from config."""
    cfg = {"exclude": ["a", "b", "c"]}
    cfg = lately.remove_excludes(cfg, ["b"])
    assert cfg["exclude"] == ["a", "c"]


def test_remove_exclude_missing():
    """--include with non-existing repo is a no-op."""
    cfg = {"exclude": ["a"]}
    cfg = lately.remove_excludes(cfg, ["z"])
    assert cfg["exclude"] == ["a"]
