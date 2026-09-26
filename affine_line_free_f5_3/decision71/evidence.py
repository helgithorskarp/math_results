"""Shared serialization and strict, restartable certificate-record checks."""
import hashlib
import json
import os
from pathlib import Path

from point_model import generate

COUNT = 109676
DOMAIN_SHA256 = "02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2"
VERIFIED = "UNSAT_DRAT_VERIFIED"
PRODUCTION_RANGES = ((0, 27419), (27419, 54838), (54838, 82257), (82257, COUNT))


def blocks(start, stop):
    """Stable digest blocks, also valid when the audit is run in four ranges."""
    cuts = {start, stop}
    for a, b in PRODUCTION_RANGES:
        cuts.update(x for x in range(a, b, 1000) if start < x < stop)
        if start < b < stop:
            cuts.add(b)
    ordered = sorted(cuts)
    return list(zip(ordered, ordered[1:]))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def load_domain(path):
    path = Path(path)
    if digest(path) != DOMAIN_SHA256:
        raise ValueError("domain differs from the completely verified enumeration")
    domain = json.loads(path.read_text())
    if len(domain) != COUNT:
        raise ValueError("incomplete representative domain")
    return domain


def cnf_bytes(formula):
    """The exact DIMACS bytes written by the pinned Python-SAT version."""
    return (f"p cnf {formula.nv} {len(formula.clauses)}\n"
            + "".join(" ".join(map(str, clause)) + " 0\n"
                      for clause in formula.clauses)).encode("ascii")


def case_files(out, index):
    prefix = Path(out) / f"{index // 1000:03d}" / f"case_{index:06d}"
    return tuple(prefix.with_suffix(suffix)
                 for suffix in (".cnf", ".drat", ".check.log", ".json"))


def audit_record(out, index, representative):
    """Check source/input agreement and stored evidence; do not recheck DRAT."""
    cnf, proof, log, path = case_files(out, index)
    record = json.loads(path.read_text())
    formula, gauge = generate(representative["weights"])
    generated_hash = hashlib.sha256(cnf_bytes(formula)).hexdigest()
    expected = {
        "index": index, "type": representative["type"],
        "weights": representative["weights"], "gauge": list(gauge),
        "variables": 125, "clauses": len(formula.clauses),
        "input_catalogue_sha256": DOMAIN_SHA256,
        "status": VERIFIED, "cnf_sha256": generated_hash,
    }
    if formula.nv != 125 or sum(map(int, representative["weights"])) != 71:
        raise ValueError(f"incorrect formula semantics at {index}")
    for key, value in expected.items():
        if record.get(key) != value:
            raise ValueError(f"record field {key} disagrees at {index}")
    if digest(cnf) != generated_hash:
        raise ValueError(f"stored CNF disagrees with regenerated source at {index}")
    if digest(proof) != record["proof_sha256"] or proof.stat().st_size != record["proof_bytes"]:
        raise ValueError(f"proof bytes changed at {index}")
    if "s VERIFIED" not in log.read_text():
        raise ValueError(f"missing checker acceptance at {index}")
    if len(bytes.fromhex(record["checker_sha256"])) != 32:
        raise ValueError(f"invalid checker identity at {index}")
    return record
