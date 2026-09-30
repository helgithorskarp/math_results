"""Byte-pinned premises and exact triangular-cell primitives."""
import hashlib
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError('mathematical assertions require an unoptimized interpreter')

BASE = Path(__file__).resolve().parent
PARENT = BASE.parent / 'heesch_polyiamond_fixed_fourth_extension'
PINS = {
    'common.py': 'b678ee87051432382752e0b290c47e5c086d64a39a2b8327551c6851695ccd93',
    'build.py': '0016f049979e53c88be6dc894dc48e88a59998790bb06d4af1fd2d42b87cc03c',
    'patterns.py': '92f06995edbf5b683361a47afaaaf71ca693539f54eed917e5a21b35ca5dbe10',
    'patterns.json': '4bb58e3394b97eca19d6ec76d9955b752144c7ae86820c7a65abf0e0b8e56124',
}
for name, digest in PINS.items():
    assert hashlib.sha256((PARENT / name).read_bytes()).hexdigest() == digest, name
sys.path.insert(0, str(PARENT))
from common import g, PRIOR, compact, masks, star, vertices, footprint, adjacent, write, cnf_text
import build as parent_build
import patterns as parent_patterns
