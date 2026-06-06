"""
Regression tests for the password-protection feature (issue #5).

Covers the security-critical logic in src/utils.py (PBKDF2 hashing, salt
randomness, constant-time verification, and the set/verify/remove config flow
against a temporary config file) plus structural assertions that src/gui.py
actually gates both unblock paths behind the password and exposes the
Set/Change/Remove menu commands.

Standard library only -- no new dependencies. The real user config at
~/.website_blocker is never written: CONFIG_FILE is redirected to a temp file.

Run from the repo root:  python -m tests.test_password
"""
import sys
import json
import tempfile
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import src.utils as utils  # noqa: E402

passed = 0
def ok(name):
    global passed
    print("  PASS:", name)
    passed += 1

# ---- pure hashing ----
rec = utils.hash_password("hunter2")
assert rec["algo"] == "pbkdf2_sha256"
assert rec["iterations"] >= 100_000
assert "hunter2" not in json.dumps(rec)            # never stored in plain text
ok("hash_password: pbkdf2 record, no plaintext, sane iteration count")

rec2 = utils.hash_password("hunter2")
assert rec2["salt"] != rec["salt"]                 # fresh random salt each time
assert rec2["hash"] != rec["hash"]                 # same password -> different stored hash
ok("hash_password: random salt makes stored hashes differ")

assert utils.verify_password_hash(rec, "hunter2") is True
assert utils.verify_password_hash(rec, "wrong") is False
assert utils.verify_password_hash(None, "hunter2") is False
assert utils.verify_password_hash({"salt": "zz", "hash": "zz"}, "x") is False
ok("verify_password_hash: correct True; wrong / None / malformed False")

tampered = dict(rec); tampered["hash"] = "0" * len(rec["hash"])
assert utils.verify_password_hash(tampered, "hunter2") is False
ok("verify_password_hash: tampered stored hash rejected")

# ---- config flow against a temp file ----
tmpdir = tempfile.mkdtemp()
utils.CONFIG_FILE = pathlib.Path(tmpdir) / "config.json"

assert utils.is_password_set() is False
assert utils.verify_password("anything") is True   # no password -> no protection (open)
ok("no password set: is_password_set False, verify open")

assert utils.set_password("s3cret!") is True
assert utils.is_password_set() is True
assert "s3cret!" not in utils.CONFIG_FILE.read_text()   # stored hashed, not plain
on_disk = json.loads(utils.CONFIG_FILE.read_text())
assert on_disk["password"]["hash"] and on_disk["password"]["salt"]
ok("set_password: persisted hashed to disk, never in plain text")

assert utils.verify_password("s3cret!") is True
assert utils.verify_password("nope") is False
ok("verify_password: correct True, wrong False once set")

# does not clobber other config keys
cfg = utils.load_config(); cfg["blocked_sites"] = ["x.com"]
utils.CONFIG_FILE.write_text(json.dumps(cfg))
utils.set_password("new-one")
assert utils.load_config()["blocked_sites"] == ["x.com"]
ok("set_password: preserves blocked_sites / other config")

assert utils.remove_password() is True
assert utils.is_password_set() is False
assert utils.verify_password("new-one") is True         # reopened after removal
assert utils.load_config()["blocked_sites"] == ["x.com"]
ok("remove_password: clears hash, keeps other config, reopens")

# ---- structural: GUI gates + menu ----
gui_src = (REPO_ROOT / "src" / "gui.py").read_text()
assert "def _require_password(self)" in gui_src
sel = gui_src[gui_src.index("def _unblock_selected"):gui_src.index("def _unblock_all")]
allf = gui_src[gui_src.index("def _unblock_all"):gui_src.index("def _export_blocklist")]
assert "self._require_password()" in sel, "_unblock_selected is not gated"
assert "self._require_password()" in allf, "_unblock_all is not gated"
ok("gui: both _unblock_selected and _unblock_all gated by _require_password")

for label in ("Set Password", "Change Password", "Remove Password"):
    assert label in gui_src, f"missing menu command: {label}"
assert "simpledialog" in gui_src and 'show="*"' in gui_src
ok("gui: Security menu has Set/Change/Remove; password entry is masked")

# ---- structural: secure primitives ----
utils_src = (REPO_ROOT / "src" / "utils.py").read_text()
assert "pbkdf2_hmac" in utils_src, "must use PBKDF2"
assert "hmac.compare_digest" in utils_src, "must compare in constant time"
assert "os.urandom" in utils_src, "must use a random salt"
ok("utils: PBKDF2 + constant-time compare + random salt")

print(f"\nALL {passed} CHECKS PASSED")
