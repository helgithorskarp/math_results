"""Source guards only; no mathematical encoder or certificate verifier."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).absolute().parent
BASE = HERE.parent / 'order7-geometric-cut'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pins():
    data = json.loads((HERE / 'SOURCE_PINS.json').read_text())
    for name, digest in data['files'].items():
        require(sha(BASE / name) == digest, 'changed helper: ' + name)
    phase = HERE.parent / 'order7-antipodal-geography' / 'PROOF.md'
    require(sha(phase) == data['phase_proof_sha256'], 'changed phase-cut source')
    return data


def load_encoder():
    pins()  # Refuse changed source before executing its code.
    spec = importlib.util.spec_from_file_location('endpoint_log_encoder', BASE / 'encode.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
