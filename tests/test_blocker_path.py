import os
from pathlib import Path

import pytest

from src.blocker import WebsiteBlocker


def test_get_hosts_path_uses_environment_override(tmp_path: Path, monkeypatch):
    custom_hosts = tmp_path / "hosts"
    custom_hosts.write_text("127.0.0.1 localhost\n")
    monkeypatch.setenv("GW_BLOCKER_HOSTS_PATH", str(custom_hosts))

    blocker = WebsiteBlocker()
    assert blocker.hosts_path == str(custom_hosts)


def test_get_hosts_path_raises_for_missing_env_path(monkeypatch):
    monkeypatch.setenv("GW_BLOCKER_HOSTS_PATH", "/nonexistent/hosts")

    with pytest.raises(FileNotFoundError):
        WebsiteBlocker()
