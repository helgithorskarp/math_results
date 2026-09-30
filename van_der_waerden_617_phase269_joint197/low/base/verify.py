"""Definition-level exact checker; imports no generator, solver, or NumPy.

Generation uses square sets and an LP model. Verification uses Euler's
criterion, actual integer AP coordinates and integral capacity sums.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path

P, N, C = 617, 3704, 1852


def need(value, message):
    if not value:
        raise ValueError(message)


need(all(P % d for d in range(2, isqrt(P)+1)), '617 must be prime')
Q = [-1]+[0 if pow(r, 308, P) == 1 else 1 for r in range(1, P)]
need(all(pow(r, 308, P) in (1, P-1) for r in range(1, P)), 'Euler criterion')


def check_case(data):
    need(set(data) == {'format','P','N','terms','seam','s','t','g','denominator','color0_APs'}, 'schema fields')
    need(data['format'] == 'QR617_REFLECTION_WEIGHTS_1', 'format')
    need(all(type(data[k]) is int for k in ['P','N','terms','seam','s','t','g','denominator']), 'integer fields')
    need((data['P'],data['N'],data['terms'],data['seam']) == (P,N,7,C), 'geometry')
    s, t = data['s'], data['t']
    need(0 <= s < P and t == (1-s) % P and data['g'] == 1, 'reference-family key')
    den = data['denominator']
    need(den > 0, 'positive denominator')
    entries = data['color0_APs']
    need(type(entries) is list and entries, 'nonempty weight list')
    loads = [0]*N
    seen = set()
    totals = [0, 0]
    for e in entries:
        need(type(e) is list and len(e) == 3 and all(type(v) is int for v in e), 'AP entry integers')
        a, d, num = e
        need(d > 0 and num > 0, 'positive AP step and weight')
        for expected_color, aa in [(0, a), (1, N-1-a-6*d)]:
            need(0 <= aa < C <= aa+6*d < N, 'actual crossing AP bounds')
            need((aa, d) not in seen, 'duplicate AP')
            seen.add((aa, d))
            for j in range(7):
                x = aa+j*d
                r = (x-C+(s if x < C else t)) % P
                need(r != 0, 'AP contains a free pole')
                color = Q[r] ^ int(x >= C)
                need(color == expected_color, 'AP not monochromatic in required reference color')
                loads[x] += num
            totals[expected_color] += num
    need(max(loads) <= den, 'exact position capacity exceeded')
    need(totals[0] == totals[1] > 0, 'reflected color totals')
    bound = (totals[0]+den-1)//den
    return {'phase': s, 'key': [s,t,1], 'checked_APs': len(seen),
            'checked_incidences': 7*len(seen),
            'per_color_weight': str(Fraction(totals[0],den)),
            'maximum_position_load': str(Fraction(max(loads),den)),
            'required_edits_per_reference_color': bound,
            'required_total_nonpole_edits': 2*bound,
            'pole_colors_free': True, 'candidate_symmetry_assumed': False,
            'solver_trusted': False, 'edit_optimality_claim': False}


def read_case(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    out = check_case(data)
    out['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    return out


def check_directory(directory, require_complete=False):
    paths = sorted(directory.glob('phase-???.json'))
    cases = []
    phases = set()
    for p in paths:
        item = read_case(p)
        phase = item['phase']
        need(p.name == f'phase-{phase:03d}.json', 'phase filename mismatch')
        need(phase not in phases, 'duplicate phase')
        phases.add(phase)
        cases.append(item)
    complete = phases == set(range(P))
    need(cases, 'no checked cases')
    if require_complete:
        need(complete, 'incomplete phase domain; no universal bound')
    digest = hashlib.sha256()
    for item in cases:
        digest.update(f"{item['phase']}:{item['certificate_sha256']}\n".encode())
    return {'status': 'VERIFIED_COMPLETE_REFLECTION_FAMILY' if complete else 'VERIFIED_EXPLICIT_PARTIAL_PHASES',
            'agent': 'six-vdw-3', 'role': 'researcher', 'complete': complete,
            'phase_count': len(cases), 'checked_APs': sum(v['checked_APs'] for v in cases),
            'checked_incidences': sum(v['checked_incidences'] for v in cases),
            'minimum_edits_per_reference_color': min(v['required_edits_per_reference_color'] for v in cases),
            'minimum_total_nonpole_edits': min(v['required_total_nonpole_edits'] for v in cases),
            'phase_manifest_sha256': digest.hexdigest(), 'cases': cases,
            'solver_trusted': False, 'edit_optimality_claim': False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path)
    p.add_argument('--require-complete', action='store_true')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    out = check_directory(a.source,a.require_complete) if a.source.is_dir() else read_case(a.source)
    if a.require_complete and not a.source.is_dir():
        raise ValueError('Complete coverage requires a directory')
    raw = json.dumps(out,sort_keys=True)
    if a.output:
        a.output.write_text(raw+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'cases'}))


if __name__ == '__main__':
    main()
