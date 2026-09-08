#!/usr/bin/env python3
"""Reproduce the source and independent h3911 review checks."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_haugland_galois_folding"
MANIFEST_SHA256 = "17d1c67fa46c6b3b29a46a3b7faef7fa134c17320ac908506a95881950f0806f"
INPUT_SHA256 = "201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def run(program, *arguments, optimized=False):
    argv = [sys.executable]
    if optimized:
        argv.append("-O")
    argv += ["-B", str(program), *map(str, arguments)]
    result = subprocess.run(argv, capture_output=True, text=True, check=True)
    need(not result.stderr, ("unexpected stderr", argv, result.stderr))
    return json.loads(result.stdout)


def main():
    need(hashlib.sha256((SOURCE / "SHA256SUMS").read_bytes()).hexdigest() ==
         MANIFEST_SHA256, "reviewed source manifest differs")
    graph = SOURCE.parent / "hadwiger_nelson_haugland2131_exact_reproduction" / "graph.json"
    need(hashlib.sha256(graph.read_bytes()).hexdigest() == INPUT_SHA256,
         "reviewed graph input differs")

    expected_source = json.loads((SOURCE / "expected.json").read_text())
    source_normal = run(SOURCE / "verify.py", "--check-expected")
    source_optimized = run(SOURCE / "verify.py", "--check-expected", optimized=True)
    need(source_normal == source_optimized == expected_source,
         "source verifier output differs")
    source_controlled = run(
        SOURCE / "verify.py", "--check-expected", "--controls", optimized=True
    )
    controls = source_controlled.pop("controls")
    need(source_controlled == expected_source, "controlled verifier output differs")
    need(controls == {
        "malformed_certificates_rejected": 7,
        "small_domain_systems_exhausted": 19208,
    }, "source controls differ")

    expected_exact = json.loads((SOURCE / "expected_exact.json").read_text())
    exact_normal = run(SOURCE / "audit_exact.py")
    exact_optimized = run(SOURCE / "audit_exact.py", optimized=True)
    need(exact_normal == exact_optimized == expected_exact,
         "characteristic-zero audit differs")

    independent_normal = run(HERE / "independent_ac3.py", SOURCE)
    independent_optimized = run(HERE / "independent_ac3.py", SOURCE, optimized=True)
    need(independent_normal == independent_optimized,
         "independent normal/optimized outputs differ")

    receipt = {
        "status": "REPRODUCED_INDEPENDENT_REVIEW_H3911",
        "reviewed_manifest_sha256": MANIFEST_SHA256,
        "source_input_sha256": INPUT_SHA256,
        "source_verifier_expected_match": True,
        "source_verifier_normal_optimized_equal": True,
        "source_controls": controls,
        "characteristic_zero_audit_expected_match": True,
        "characteristic_zero_audit_normal_optimized_equal": True,
        "source_complex_shadow_sha256": exact_normal["source_complex_shadow_sha256"],
        "independent_ac3_normal_optimized_equal": True,
        "independent_ac3": independent_normal,
    }
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(receipt == expected, "review receipt differs from EXPECTED.json")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
