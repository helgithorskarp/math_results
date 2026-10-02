"""Emit the312 original-phase terms; generated clause belongs in scratch."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from check import verify, hitting_clause

ap = argparse.ArgumentParser()
ap.add_argument("--out", type=Path, required=True)
args = ap.parse_args()
here = Path(__file__).resolve().parent
fixture = json.loads((here / "fixture.json").read_text())
expected = json.loads((here / "expected.json").read_text())
verify(fixture, expected)
terms = hitting_clause(fixture["kernel_cofactor_fibers"])
data = json.dumps(terms, separators=(",", ":")).encode()
if sha256(data).hexdigest() != expected["hitting_clause_sha256"]:
    raise ValueError("emitted original terms differ")
args.out.write_bytes(data+b"\n")
print(json.dumps({"terms": len(terms), "canonical_sha256": sha256(data).hexdigest()}, sort_keys=True))
