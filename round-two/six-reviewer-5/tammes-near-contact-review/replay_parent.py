"""Replay a pinned published dependency and export its validated witnesses.

This bridge explicitly trusts the original cover/graph checker. It is not
the independent new-margin audit, which runs in a separate process and
imports no prerequisite Python code.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repository-root', type=Path, required=True)
    p.add_argument('--strip', choices=['lower', 'upper'], required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    root = a.repository_root.resolve()
    cfg = json.loads((root / 'round-two/six-tammes-2/robust-eight-core/certificate.json').read_text())
    entry = cfg['prerequisites'][a.strip]
    base = root / entry['directory']
    for filename, digest in entry['files_sha256'].items():
        if Path(filename).name != filename or hashlib.sha256((base / filename).read_bytes()).hexdigest() != digest:
            raise ValueError('Changed pinned prerequisite: ' + filename)
    sys.path.insert(0, str(base))
    spec = importlib.util.spec_from_file_location('published_dependency', base / 'check.py')
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    data = json.loads((base / 'certificate.json').read_text())
    parts = parent.verify(data, details=True)
    if parts[0] != json.loads((base / 'EXPECTED.json').read_text()):
        raise ValueError('Full dependency receipt mismatch')
    result = {'strip': a.strip, 'receipt': parts[0], 'discarded': parts[3],
              'interval': data['interval'],
              'single_cells': data.get('single_cells', []),
              'conditioned_pairs': data.get('conditioned_pairs', [])}
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'strip': a.strip, 'status': 'PINNED_PARENT_REPLAYED',
                      'cover_cells': parts[0]['cover_cells'],
                      'clique_search_states': parts[0]['clique_search_states']}))


if __name__ == '__main__':
    main()
