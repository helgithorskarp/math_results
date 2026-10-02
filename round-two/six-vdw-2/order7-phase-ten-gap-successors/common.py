"""Pinned existing helpers; no new mathematical generator or checker here."""
import hashlib
import importlib.util
import json
from pathlib import Path
HERE = Path(__file__).absolute().parent
BASE = HERE.parent/'order7-geometric-cut'

def require(ok,message):
    if not ok:raise ValueError(message)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pins():
    data = json.loads((HERE/'SOURCE_PINS.json').read_text())
    for name,digest in data['relative_files'].items():
        require(sha(HERE.parent/name)==digest,'changed pinned source: '+name)
    return data

def module(name,path):
    pins()  # Check every required source before executing mathematical helpers.
    spec = importlib.util.spec_from_file_location(name,path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

def load_encoder():
    return module('cluster_log_encoder',BASE/'encode.py')

def endpoint_generator():
    return module('old_endpoint_generator',HERE.parent/'order7-phase-endpoints/generate.py')

def endpoint_auditor():
    return module('old_endpoint_literal_auditor',HERE.parent/'order7-phase-endpoints/audit.py')
