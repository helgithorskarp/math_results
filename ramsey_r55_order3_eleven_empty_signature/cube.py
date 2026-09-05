#!/usr/bin/env python3
"""Full parent plus minority core and the proved empty first signature."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
INPUT = ROOT/'classification.json'
PIN = '163bf5fd836ff5fbd58387182995d9389f85b2d8eade6f6bef4009a313a09f98'
PARENT_PIN = 'c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f'
VARIABLES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 31, 32, 33, 34, 35, 36, 58, 59, 60)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def info(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while data := stream.read(1 << 20):
            h.update(data)
    return dict(bytes=path.stat().st_size, sha256=h.hexdigest())


def cases():
    require(info(INPUT)['sha256'] == PIN, 'residual input hash')
    data = json.loads(INPUT.read_text())
    rows = [r for r in data['rows'] if r['forces_empty']]
    require(data['selected'] == [r['index'] for r in rows] and len(rows) == 11, 'selected class count')
    require([r['index'] for r in rows] == sorted({r['index'] for r in rows}), 'unique ordered cases')
    return rows


def make(parent, output, bits):
    require(len(bits) == 18 and set(bits) <= {'0', '1'}, 'core bits')
    with parent.open('rb') as source, output.open('wb') as dest:
        require(source.readline() == b'p cnf 34280 615920\n', 'r4 parent header')
        dest.write(b'p cnf 34280 615942\n')
        shutil.copyfileobj(source, dest)
        for variable, bit in zip(VARIABLES, bits):
            dest.write(f'{variable if bit == "1" else -variable} 0\n'.encode())
        for variable in (211, 212, 213, 214):
            dest.write(f'{-variable} 0\n'.encode())
    return info(output)
