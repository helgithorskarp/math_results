"""Strict tool identity and proof-byte checks, shared by the replay entry points."""
import hashlib
import json
from pathlib import Path
import subprocess

SOURCE = Path(__file__).resolve().parent


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def check_tool(path, name):
    path = Path(path).resolve()
    record = next(x for x in json.loads((SOURCE/'tools.json').read_text()) if x['name'] == name)
    if sha(path) != record['binary_sha256']:
        raise ValueError('unmatched pinned tool: '+name)
    return path


def external(path):
    path = Path(path).resolve()
    root = next((p for p in [SOURCE, *SOURCE.parents] if (p/'.git').exists()), SOURCE)
    if path == root or root in path.parents:
        raise ValueError('generated data must stay outside the source repository')
    return path


def proof_check(checker, cnf, proof, log):
    # Existence and status metadata cannot stand in for proof bytes.
    proof = Path(proof)
    if not proof.is_file() or proof.stat().st_size == 0:
        raise ValueError('missing or empty physical proof')
    with Path(log).open('w') as f:
        result = subprocess.run([str(checker), str(cnf), str(proof)], stdout=f,
                                stderr=subprocess.STDOUT, timeout=620)
    if result.returncode != 0 or 's VERIFIED' not in Path(log).read_text().splitlines():
        raise ValueError('proof checker did not verify: '+str(proof))
    return {'proof_sha256': sha(proof), 'proof_bytes': proof.stat().st_size}
