"""Static semantic damages and a CLI; no capacity or CRT arithmetic."""
import argparse
import copy
import json
from pathlib import Path


def damages(cert):
    edits = [
        lambda c: c['first_pool'].insert(0, 1),
        lambda c: c['last_pool'].remove(1),
        lambda c: c['prefixes']['H'][-1].__setitem__(1, 0),
        lambda c: c['prefixes']['P'].pop(1),
        lambda c: c.__setitem__('period', 5040),
        lambda c: c.__setitem__('minimum', 7),
        lambda c: c['kernels'][0]['parents']['3'].__setitem__(0, 315),
        lambda c: c['kernels'][0]['parents']['3'].__setitem__(0, True),
        lambda c: c['kernels'][0]['parents']['3'].__setitem__(0, 3),
        lambda c: c['kernels'][0].__setitem__('at_most_parents', 1),
        lambda c: c['kernels'][0]['parents']['5'].pop(),
        lambda c: c['kernels'][0]['parents'].__setitem__('0', c['kernels'][0]['parents'].pop('3')),
        lambda c: c['kernels'][0]['parents'].__setitem__('1', c['kernels'][0]['parents'].pop('3')),
        lambda c: c['kernels'][2]['parents']['3'].__setitem__(0, 0),
        lambda c: c['last_pool'].__setitem__(0, True),
        lambda c: c['prefixes']['H'][0].__setitem__(1, False),
        lambda c: c.__setitem__('schema', True),
    ]
    for edit in edits:
        damaged = copy.deepcopy(cert)
        edit(damaged)
        yield damaged


def cli(evaluate, engine):
    root = Path(__file__).parent
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, default=root / 'certificate.json')
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    cert = json.loads(args.certificate.read_text())
    result = evaluate(cert)
    if args.expected and result != json.loads(args.expected.read_text()):
        raise ValueError('Exact expected manifest differs')
    count = 0
    if args.controls:
        for damaged in damages(cert):
            try:
                evaluate(damaged)
            except ValueError:
                count += 1
            else:
                raise ValueError('Semantic damage accepted')
    print(json.dumps({'engine': engine, 'manifest': result,
                      'semantic_damages_rejected': count}, sort_keys=True))
