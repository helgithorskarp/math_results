"""Byte-for-byte normal and assertion-disabled replay, plus source manifest."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def encoded(data):
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()


def run():
    manifest = (ROOT / "SHA256SUMS").read_text().splitlines()
    tracked = set()
    for line in manifest:
        digest, name = line.split("  ")
        need(name not in tracked and "/" not in name, "invalid manifest path")
        tracked.add(name)
        need(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, "manifest mismatch: " + name)
    need(tracked == {p.name for p in ROOT.iterdir() if p.is_file() and p.name != "SHA256SUMS"}, "manifest coverage")
    modes = []
    for flags in (["-B"], ["-O", "-B"]):
        def invoke(*args):
            return subprocess.run([sys.executable, *flags, *args], cwd=ROOT, check=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        need(invoke("model.py") == (ROOT / "expected_model.json").read_bytes(), "model replay mismatch")
        bundle = json.loads(invoke("audit.py", "--bundle"))
        for key, filename in (("audit", "expected_audit.json"), ("fixture", "fixture.json"),
                              ("certificate", "fixture_certificate.json")):
            need(encoded(bundle[key]) == (ROOT / filename).read_bytes(), "audit replay mismatch: " + key)
        need(invoke("extract.py", "fixture.json") == (ROOT / "fixture_certificate.json").read_bytes(), "extract replay mismatch")
        need(invoke("verify.py", "fixture.json", "fixture_certificate.json") == b"VERIFIED_PHYSICAL_EXCLUSION\n", "verify replay mismatch")
        modes.append("optimized" if "-O" in flags else "normal")
    return {"status": "REPRODUCED_CUT_RANK_OBSTRUCTION", "modes": modes,
            "manifest_files": len(tracked),
            "model_sha256": hashlib.sha256((ROOT / "expected_model.json").read_bytes()).hexdigest(),
            "audit_sha256": hashlib.sha256((ROOT / "expected_audit.json").read_bytes()).hexdigest(),
            "complete_selected_global_family_excluded": True,
            "ramsey_graph_found": False, "ramsey_bound_improved": False}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
