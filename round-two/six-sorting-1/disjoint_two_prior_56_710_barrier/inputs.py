"""Local generated-input byte transport only; no producer/checker mathematics.

All work inputs are regenerated and independently checked in this directory.
Static compact source inputs are pinned separately from generated arrays.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def checked_finite(value):
    need(digest(value['finite']) == value['finite_sha256'], 'Whole finite input binding differs')
    return value


def bound_path(name):
    mapping = json.loads((WORK / 'transport-inputs.json').read_text())['inputs']
    row = mapping[name]
    path = ROOT / row['path']
    need(path.resolve().is_relative_to(ROOT), 'Generated input outside standalone directory')
    raw = path.read_bytes()
    need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
         'Local regenerated input changed: ' + name)
    return path


def load(name):
    return json.loads(bound_path(name).read_text())


def static_sources():
    pins = json.loads((ROOT / 'SOURCE-PINS.json').read_text())
    for row in pins['files']:
        path = ROOT / row['path']
        raw = path.read_bytes()
        need(path.resolve().is_relative_to(ROOT) and len(raw) == row['bytes'] and
             hashlib.sha256(raw).hexdigest() == row['sha256'], 'Standalone static source changed')
    return pins
