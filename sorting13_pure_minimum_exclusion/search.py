"""Depth-free L109 completion with145 independently audited ternary cuts.

Author/executing agent: six-sorting-2, researcher. Structural augmentation
and native solver runner are explicitly reused from7474/source4ac1823.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'sorting13_maximum_preparation'
spec = importlib.util.spec_from_file_location('published_preparation', PRIOR / 'search.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def fixture():
    base = json.loads((PRIOR / 'fixture.json').read_text())
    extra = json.loads((HERE / 'additional_witnesses.json').read_text())
    existing = {(r['x'], r['y']) for r in base['critical_single_bounds'] +
                base['selected_mixed_bounds'] + base['designated_bounds']}
    assert len(existing) == 53 and len(extra) == 92
    assert not existing & {(r['x'], r['y']) for r in extra}
    assert len({(r['x'], r['y']) for r in extra}) == 92
    assert all(r['cap'] <= 8 for r in extra)
    result = dict(base)
    result['selected_mixed_bounds'] = base['selected_mixed_bounds'] + extra
    return result


def generate(path, gates=16, freeze_control=False):
    f = fixture()
    freeze = f['control18'] if freeze_control else None
    if freeze:
        gates = 18

    def augmentation(w, choices, pairs, bits):
        result = prior.augment(w, choices, pairs, bits, f, gates, freeze,
                               gates == 16, gates == 16, None)
        result.update(witness_count=145, additional_witnesses=92,
                      additional_witnesses_sha256=hashlib.sha256((HERE / 'additional_witnesses.json').read_bytes()).hexdigest(),
                      pruning_fixture_sha256=hashlib.sha256((PRIOR / 'fixture.json').read_bytes()).hexdigest(),
                      scope='All root positions, all36 pairs per slot, arbitrary depth; no selected timing class')
        return result

    return prior.generate(9, f['states'], gates, path, commute=False,
                          encode_sorted=True, augment=augmentation)


def main():
    if not __debug__:
        raise RuntimeError('Run without Python optimization')
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['generate', 'solve'])
    p.add_argument('--path', type=Path, required=True)
    p.add_argument('--gates', type=int, default=16)
    p.add_argument('--freeze-control', action='store_true')
    p.add_argument('--conflicts', type=int, default=30000)
    p.add_argument('--seconds', type=float, default=40)
    a = p.parse_args()
    if a.command == 'generate':
        m = generate(a.path, a.gates, a.freeze_control)
        print(json.dumps({k: v for k, v in m.items() if k not in ('states', 'pairs', 'choices')}))
    else:
        prior.solve(a.path, a.conflicts, a.seconds)


if __name__ == '__main__':
    main()
