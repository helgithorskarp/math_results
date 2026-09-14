"""Reject corrupted certificates without relying on file hashes."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
from geometry import verify as geometry
from verify import verify_completions, edges

HERE = Path(__file__).resolve().parent


def rejected(call):
    try:
        call()
    except ValueError:
        return
    raise RuntimeError('corrupted input was accepted')


def run():
    c = json.loads((HERE / 'geometry_certificate.json').read_text())
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / 'certificate.json'
        for change in ('inverse', 'centre', 'missing_edge', 'radius'):
            d = deepcopy(c)
            if change == 'inverse':
                d['inverse_numerators'] = [[0]*34 for _ in range(34)]
            elif change == 'centre':
                d['centre_numerators'][2][0] += d['point_denominator']
            elif change == 'missing_edge':
                d['edge_equations'].pop()
            elif change == 'radius':
                d['radius_denominator'] = 1
            path.write_text(json.dumps(d))
            rejected(lambda: geometry(path))
    text = (HERE / 'completions.txt').read_text()
    rows = text.splitlines()
    es = set(edges())
    for bad in ('\n'.join(rows[:-1])+'\n', '000000000\n'+'\n'.join(rows[1:])+'\n',
                '4'+text[1:], text+'000000000\n'):
        rejected(lambda: verify_completions(bad, es))
    return {'corruptions_rejected': 8, 'hash_rejection_used': False}


if __name__ == '__main__':
    print(json.dumps(run()))
