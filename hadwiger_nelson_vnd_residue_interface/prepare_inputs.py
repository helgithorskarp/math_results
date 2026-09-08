"""Fetch pinned upstream coordinates/edges and reproduce their normalized coordinates.

Uses the already published safe parser. No SAT query or full pair census is run.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, urllib.request, zipfile

S = Path(__file__).resolve().parent
PARENT = S.parent / 'hadwiger_nelson_vnd_case10_verified_gate'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    args = ap.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    upstream = json.loads((PARENT / 'UPSTREAM_INPUTS.json').read_text())
    for item in upstream['files']:
        if item['local_file'] not in ('source_graph.dimacs', 'source_graph.zip'):
            continue
        path = work / item['local_file']
        raw = path.read_bytes() if path.exists() else urllib.request.urlopen(item['url'], timeout=60).read()
        if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
            raise ValueError('upstream identity mismatch')
        if not path.exists():
            path.write_bytes(raw)
    with zipfile.ZipFile(work / 'source_graph.zip') as archive:
        raw = archive.read('s2_graph10.vtx')
    cert = json.loads((S / 'CERTIFICATE.json').read_text())
    if hashlib.sha256(raw).hexdigest() != cert['inputs']['source_graph.vtx']['sha256']:
        raise ValueError('vertex archive member mismatch')
    path = work / 'source_graph.vtx'
    if path.exists() and path.read_bytes() != raw:
        raise ValueError('refuse different vertex file')
    path.write_bytes(raw)
    spec = importlib.util.spec_from_file_location('pinned_vnd_parser', PARENT / 'audit_source.py')
    parser = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parser)
    parser.P = work
    rows, denominator = parser.coordinates()
    raw = (json.dumps({'denominator': denominator, 'basis_radicands': parser.R, 'points': rows}, separators=(',', ':')) + '\n').encode()
    if hashlib.sha256(raw).hexdigest() != cert['inputs']['exact_points.json']['sha256']:
        raise ValueError('normalized point identity mismatch')
    path = work / 'exact_points.json'
    if path.exists() and path.read_bytes() != raw:
        raise ValueError('refuse different normalized point file')
    path.write_bytes(raw)
    print('VERIFIED_PINNED_VND_COLOURING_INPUTS; NO_SOLVER_CALL')


if __name__ == '__main__':
    main()
