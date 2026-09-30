"""Regenerate and independently check the doubled first-corona family cases.

Batches refer to positions in the 434-member previously grid-zero subset.
One temporary CNF/proof arena is reused; compact entry data is resumable.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import sys
import time

from decide import decision
from halfgrid import load_dependencies


GROWTH_SHA256 = 'c53990fa6f6e433aa171f8ddec9e82aa76cfded14751d47da4608cf6a593ed7c'
FAMILY_SHA256 = '935192a6bead7d979d7ed60f3907e52278962940d9b3c008d18af94a85fc36ef'
MANIFEST_SHA256 = '8f96c536c15f739130b6ca7e5a67fcba1ff1e51fa4bbc18b16d652182c24ff85'
SEED_SHA256 = '24ceb5aefe2e0843d16d7ab7ced16f17356789426a12607b00cf956df02dbe51'


def family_inputs(prior, motion_directory):
    prior = Path(prior).resolve()
    _, motion = load_dependencies(prior, motion_directory)
    for file, digest in [('growth.py', GROWTH_SHA256), ('kaplan17.json', SEED_SHA256),
                         ('growth20_manifest.json', MANIFEST_SHA256)]:
        if hashlib.sha256((prior/file).read_bytes()).hexdigest() != digest:
            raise ValueError(file+' provenance mismatch')
    from growth import generate_family, serialization
    if Path(sys.modules['growth'].__file__).resolve() != prior/'growth.py':
        raise ValueError('growth module loaded from an unexpected path')
    manifest = json.loads((prior/'growth20_manifest.json').read_text())
    seed = json.loads((prior/'kaplan17.json').read_text())['cells']
    family, sizes = generate_family(seed, 3)
    assert hashlib.sha256(serialization(family).encode()).hexdigest() == FAMILY_SHA256
    assert len(family) == 1233 and sizes == [17, 166, 1237]
    assert [r['i'] for r in manifest['cases']] == list(range(len(family)))
    selected = [r['i'] for r in manifest['cases'] if r.get('radius') == 1]
    assert len(selected) == 434
    return family, selected, motion


def compact_record(index, position, tile, statistics, work, motion):
    record = {'i': index, 'zero_list_position': position,
              'cnf_sha256': statistics['cnf_sha256'], 'candidates': statistics['candidates'],
              'variables': statistics['variables'], 'clauses': statistics['clauses']}
    if statistics['result'].startswith('UNSAT VERIFIED'):
        record.update({'decision': 'zero', 'proof_sha256': statistics['proof_sha256'],
                       'proof_bytes': statistics['proof_bytes']})
    elif statistics['result'].startswith('SAT;'):
        cert = json.loads((work/'witness.json').read_text())
        shapes = sorted(motion.variants(tile))
        poses = motion.load_poses(tile, cert['placements'])
        compact = [[shapes.index(p.shape), int(2*p.tx), int(2*p.ty)] for p in poses if p.level]
        record.update({'decision': 'positive', 'poses': compact,
                       'copies': statistics['copies'], 'fractional_copies': statistics['fractional_copies'],
                       'final_disc': statistics['prefixes'][-1]['disc']})
    else:
        record.update({'decision': 'unknown', 'native_result': statistics['result']})
    return record


def main():
    a = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent.parent
    a.add_argument('--prior-dir', type=Path, default=root/'heesch_polyomino_euler_cnf')
    a.add_argument('--motion-dir', type=Path, default=root/'heesch_polyomino_motion_bridge')
    a.add_argument('--start', type=int, default=0)
    a.add_argument('--stop', type=int, default=434)
    a.add_argument('--work-dir', type=Path, required=True)
    a.add_argument('--checker', type=Path, required=True)
    a.add_argument('--expected', type=Path, default=Path(__file__).parent/'family_expected.json')
    a.add_argument('--record', action='store_true', help='discovery mode; not a completed classification')
    a.add_argument('--records', type=Path, help='private resumable compact data for discovery mode')
    args = a.parse_args()
    if args.record and args.records is None:
        a.error('--record needs an explicit --records path')
    family, selected, motion = family_inputs(args.prior_dir, args.motion_dir)
    if not 0 <= args.start <= args.stop <= len(selected):
        raise ValueError('invalid bounded batch')
    work = args.work_dir.resolve()
    if args.record:
        records = json.loads(args.records.read_text()) if args.records.exists() else {}
        expected = None
    else:
        data = json.loads(args.expected.read_text())
        assert data['family_sha256'] == FAMILY_SHA256
        expected = {str(r['i']): r for r in data['cases']}
        assert len(expected) == len(selected) and set(expected) == {str(i) for i in selected}
        records = None
    started = time.monotonic()
    counts = collections.Counter()
    for position in range(args.start, args.stop):
        index = selected[position]
        stats = decision(family[index], args.prior_dir, args.motion_dir, work, args.checker)
        record = compact_record(index, position, family[index], stats, work, motion)
        key = str(index)
        if expected is not None:
            # A solver may emit a different valid native proof on another platform.
            # The mathematical replay checks the exact formula, decision and verifier.
            actual = {k: v for k, v in record.items() if k not in ('proof_sha256', 'proof_bytes')}
            wanted = {k: v for k, v in expected[key].items() if k not in ('proof_sha256', 'proof_bytes')}
            assert actual == wanted, 'entry mismatch at '+key
        else:
            if key in records and records[key] != record:
                raise ValueError('deterministic local discovery replay mismatch at '+key)
            records[key] = record
            temp = args.records.with_suffix('.tmp')
            temp.write_text(json.dumps(records, sort_keys=True, indent=2)+'\n')
            temp.replace(args.records)
        counts[record['decision']] += 1
        print(json.dumps({'position': position, 'i': index, 'decision': record['decision'],
                          'seconds': round(time.monotonic()-started, 3),
                          'rss_kib': stats['peak_self_rss_kib']}), flush=True)
        if record['decision'] == 'unknown':
            break
    complete = sum(counts.values()) == args.stop-args.start and 'unknown' not in counts
    print(json.dumps({'range': [args.start, args.stop], 'complete': complete,
                      'counts': dict(counts), 'seconds': round(time.monotonic()-started, 3)}), flush=True)
    if not complete:
        raise RuntimeError('incomplete batch; no full-family exclusion')


if __name__ == '__main__':
    main()
