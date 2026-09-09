#!/usr/bin/env python3
"""Deterministic positive and negative controls for the compact checker."""
from itertools import combinations
from pathlib import Path
import json
import tempfile

import check_certificate as checker

HERE = Path(__file__).resolve().parent
SOURCE = (HERE.parent / "ramsey_r55_cyclic43_q13_boundary_certificate" /
          "objective-twelve-component-fast.json")


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rejects(call, label):
    try:
        call()
    except (ValueError, KeyError, IndexError):
        return
    raise ValueError(f"negative control was accepted: {label}")


def local_coherent(red):
    """Criterion used by the generator, specialized to five vertices."""
    color = red[1, 2] ^ red[0, 1] ^ red[0, 2]
    spin = {0: 0, **{v: red[0, v] ^ color for v in range(1, 5)}}
    if all(red[u, v] ^ spin[u] ^ spin[v] == color
           for u, v in combinations(range(5), 2)):
        return {(color, tuple(spin[v] ^ flip for v in range(5)))
                for flip in (0, 1)}
    return set()


def exhaustive_local_lemma():
    edges = list(combinations(range(5), 2))
    cases = 0
    monochromatic_events = 0
    coherent_graphs = 0
    for word in range(1 << len(edges)):
        red = {edge: (word >> index) & 1 for index, edge in enumerate(edges)}
        expected = set()
        for spin_word in range(1 << 5):
            spin = tuple((spin_word >> v) & 1 for v in range(5))
            colors = {red[u, v] ^ spin[u] ^ spin[v] for u, v in edges}
            if len(colors) == 1:
                expected.add((colors.pop(), spin))
                monochromatic_events += 1
            cases += 1
        actual = local_coherent(red)
        need(actual == expected, f"local coherence mismatch at graph word {word}")
        coherent_graphs += bool(actual)
    return {"base_graphs": 1 << len(edges), "switch_truth_cases": cases,
            "coherent_base_graphs": coherent_graphs,
            "monochromatic_events": monochromatic_events}


def main():
    sources = checker.pinned_sources(SOURCE)
    cores = checker.parse_sections(HERE / "cores.dimacs", core=True)
    proofs = checker.parse_sections(HERE / "proofs.drat", core=False)
    core, _, _ = checker.physical_core(cores[0], sources[0])
    proof_stats = checker.verify_proof(core, proofs[0])
    need(proof_stats["rup_additions"] > 0, "positive RUP control")

    bad_core = list(cores[0])
    first = checker.parse_clause(bad_core[0])
    first[0] = -first[0]
    bad_core[0] = " ".join(map(str, first)) + " 0"
    rejects(lambda: checker.physical_core(bad_core, sources[0]),
            "nonphysical core clause")
    rejects(lambda: checker.physical_core(cores[0] + [cores[0][0]], sources[0]),
            "duplicate core clause")
    rejects(lambda: checker.verify_proof(core, proofs[0][:-1]),
            "proof without empty clause")
    rejects(lambda: checker.verify_proof(core, ["43 0"]),
            "proof variable outside switch range")
    rejects(lambda: checker.parse_clause("1 -1 0"), "tautological clause")
    rejects(lambda: checker.parse_clause("1 1 0"), "repeated literal")
    rejects(lambda: checker.parse_clause("1"), "missing terminator")

    with tempfile.TemporaryDirectory(prefix="r55-seidel-controls-") as folder:
        folder = Path(folder)
        malformed = folder / "sections.txt"
        malformed.write_text("c source 1\np cnf 42 0\n")
        rejects(lambda: checker.parse_sections(malformed, core=True),
                "out-of-order source marker")
        corrupted_source = folder / "source.json"
        text = SOURCE.read_text()
        corrupted_source.write_text(text.replace('"order": 43', '"order": 42', 1))
        rejects(lambda: checker.pinned_sources(corrupted_source),
                "changed pinned source")

    report = {
        "status": "VERIFIED_CERTIFICATE_CONTROLS",
        "local_encoding": exhaustive_local_lemma(),
        "positive_certificate_sources": 1,
        "negative_controls": 9,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
