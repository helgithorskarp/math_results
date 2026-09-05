#!/usr/bin/env python3
"""Regenerate the one plain four-colouring instance used for discovery."""
import argparse
from hashlib import sha256
import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def build():
    path = REPO / 'hadwiger_nelson_parts509_partner_compatibility/data.py'
    spec = importlib.util.spec_from_file_location('partner_geometry', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = module.build()
    vertices, edges = data['vertices'], data['edges']
    pos = {v: i for i, v in enumerate(vertices)}
    col = lambda v, c: 4 * pos[v] + c + 1
    clauses = [[col(v, c) for c in range(4)] for v in vertices]
    clauses += [[-col(u, c), -col(v, c)] for u, v in edges for c in range(4)]
    clauses += [[col(0, 0)]]
    return module.dimacs(4 * len(vertices), clauses)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    raw = build()
    args.out.write_bytes(raw)
    print(sha256(raw).hexdigest())


if __name__ == '__main__':
    main()
