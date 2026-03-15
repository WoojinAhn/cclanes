import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
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


def test_collect_git_data_valid_repo(tmp_path):
    """Collects git data from a real git repo."""
    repo = tmp_path / "testrepo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, capture_output=True)
    (repo / "file.txt").write_text("hello")
    subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init commit"], cwd=repo, capture_output=True)

    data = lately.collect_git_data(repo)
    assert data["branch"] is not None
    assert data["last_commit_msg"] == "init commit"
    assert data["last_commit_date"] is not None
    assert data["dirty_count"] == 0
    assert data["has_remote"] is False


def test_collect_git_data_dirty(tmp_path):
    """Dirty count reflects uncommitted changes."""
    repo = tmp_path / "testrepo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, capture_output=True)
    (repo / "file.txt").write_text("hello")
    subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, capture_output=True)
    (repo / "file.txt").write_text("changed")
    (repo / "new.txt").write_text("new")

    data = lately.collect_git_data(repo)
    assert data["dirty_count"] == 2


def test_collect_git_data_not_a_repo(tmp_path):
    """Non-git directory returns None."""
    data = lately.collect_git_data(tmp_path)
    assert data is None
