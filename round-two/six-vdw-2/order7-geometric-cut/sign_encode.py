"""44-variable generator for three antipodal phase profiles."""
import argparse
import hashlib
import json
from pathlib import Path

from encode import field_edges, require

CASES = ('anti', 'one-opposed-pair', 'one-agreed-pair')


def phase_for(case):
    require(case in CASES, "unknown signed case")
    if case == 'anti':
        return [1]*44
    baseline = int(case == 'one-agreed-pair')
    phase = [baseline]*44
    phase[0] = 1-baseline
    return phase


def write_cnf(path, case):
    phase = phase_for(case)
    clauses = set()
    skipped = 0
    for edge in field_edges():
        signed = {i+1 if i < 44 else (-1 if phase[i-44] else 1)*(i-44+1) for i in edge}
        if any(-v in signed for v in signed):
            skipped += 1  # necessarily has both colors under this phase
            continue
        clauses.add(tuple(sorted(signed)))
        clauses.add(tuple(sorted(-v for v in signed)))
    ordered = sorted(clauses, key=lambda c: (len(c), c)) + [(-1,)]
    # Color exchange preserves the phase and fixes c(1)=0.
    text = f'p cnf 44 {len(ordered)}\n'
    text += ''.join(' '.join(map(str, c))+' 0\n' for c in ordered)
    path.write_text(text)
    return {'case': case, 'phase': phase, 'variables': 44, 'clauses': len(ordered),
            'skipped_tautological_supports': skipped,
            'cnf_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output', type=Path)
    ap.add_argument('--case', choices=CASES, required=True)
    args = ap.parse_args()
    print(json.dumps(write_cnf(args.output, args.case), sort_keys=True))


if __name__ == '__main__':
    main()
