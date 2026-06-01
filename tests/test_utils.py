import json
from pathlib import Path

import pytest

from src import utils


def test_clean_url_strips_scheme_and_path():
    assert utils.clean_url("https://www.example.com/path?query=1") == "example.com"
    assert utils.clean_url("http://example.com") == "example.com"
    assert utils.clean_url("www.example.com") == "example.com"


def test_is_valid_url_accepts_domains():
    assert utils.is_valid_url("example.com")
    assert utils.is_valid_url("sub.domain.co")


def test_is_valid_url_rejects_invalid_formats():
    assert not utils.is_valid_url("http://example.com")
    assert not utils.is_valid_url("example")
    assert not utils.is_valid_url("example!.com")
    assert not utils.is_valid_url("javascript:alert(1)")
    assert not utils.is_valid_url("127.0.0.1")


def test_save_and_load_config_roundtrip(tmp_path: Path, monkeypatch):
    config_file = tmp_path / "config.json"
    monkeypatch.setattr(utils, "CONFIG_FILE", config_file)

    assert utils.save_blocked_sites(["example.com", "test.org"])
    config = utils.load_config()
    assert config["blocked_sites"] == ["example.com", "test.org"]
    assert config["block_until"] is None


def test_save_block_until_updates_config(tmp_path: Path, monkeypatch):
    config_file = tmp_path / "config.json"
    monkeypatch.setattr(utils, "CONFIG_FILE", config_file)

    assert utils.save_block_until("2025-01-01T12:00:00")
    config = json.loads(config_file.read_text())
    assert config["block_until"] == "2025-01-01T12:00:00"
