from pathlib import Path

from src.blocker import WebsiteBlocker


def test_block_website_does_not_duplicate_entry(tmp_path: Path, monkeypatch):
    hosts_file = tmp_path / "hosts"
    hosts_file.write_text("127.0.0.1 localhost\n")

    blocker = WebsiteBlocker()
    blocker.hosts_path = str(hosts_file)
    monkeypatch.setattr(blocker, "is_admin", lambda: True)

    assert blocker.block_website("example.com")
    assert blocker.block_website("example.com")

    content = hosts_file.read_text()
    assert content.count("127.0.0.1 example.com") == 1


def test_unblock_website_removes_only_matching_host(tmp_path: Path, monkeypatch):
    hosts_file = tmp_path / "hosts"
    hosts_file.write_text("127.0.0.1 example.com\n127.0.0.1 other-example.com\n")

    blocker = WebsiteBlocker()
    blocker.hosts_path = str(hosts_file)
    monkeypatch.setattr(blocker, "is_admin", lambda: True)

    assert blocker.unblock_website("example.com")
    content = hosts_file.read_text()
    assert "example.com" not in content
    assert "other-example.com" in content


def test_unblock_all_preserves_non_block_entries(tmp_path: Path, monkeypatch):
    hosts_file = tmp_path / "hosts"
    hosts_file.write_text("127.0.0.1 localhost\n127.0.0.1 example.com\n")

    blocker = WebsiteBlocker()
    blocker.hosts_path = str(hosts_file)
    monkeypatch.setattr(blocker, "is_admin", lambda: True)

    assert blocker.unblock_all()
    content = hosts_file.read_text()
    assert "localhost" in content
    assert "example.com" not in content
