"""Fresh exact arithmetic and physical checks, never a saved-verdict consumer."""
from pathlib import Path
import hashlib
import json
import time
from audit import run
from model import physical
from verify import verify


def reproduce():
    root = Path(__file__).resolve().parent
    entries = []
    for line in (root/"SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        if "/" in name or name in entries or len(digest) != 64:
            raise ValueError("invalid manifest")
        entries.append(name)
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != digest:
            raise ValueError("source hash mismatch: "+name)
    actual = {p.name for p in root.iterdir() if p.is_file() and p.name != "SHA256SUMS"}
    if set(entries) != actual:
        raise ValueError("manifest does not cover every package file")
    start = time.monotonic()
    result = run()
    evidence = json.dumps(result, indent=2, sort_keys=True)+"\n"
    expected = (root/"expected_audit.json").read_text(encoding="utf-8")
    if evidence != expected:
        raise ArithmeticError("fresh evidence differs from expected result")
    fixture = result["physical"]["fixture"]
    for key, name in [("parameters", "fixture_parameters.json"), ("graph", "fixture_graph.json"), ("certificate", "fixture_certificate.json")]:
        if json.loads((root/name).read_text(encoding="utf-8")) != fixture[key]:
            raise ArithmeticError("fixture changed")
    if physical(fixture["parameters"]) != fixture["graph"]:
        raise ArithmeticError("fixture physical map changed")
    verify(fixture["graph"], fixture["certificate"])
    print(json.dumps({"status": result["status"], "audit_sha256": hashlib.sha256(evidence.encode()).hexdigest(),
                      "removed": result["arithmetic"]["counts"]["removed"],
                      "remaining": result["arithmetic"]["counts"]["remaining"],
                      "elapsed_seconds": time.monotonic()-start}, sort_keys=True))


if __name__ == "__main__":
    reproduce()
