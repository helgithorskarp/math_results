"""Verify both rational certificates using only this directory and the standard library."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import comb
import os
from pathlib import Path
import platform
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import require, specification, table, check_table, sectors
from core_check import verify, affine_audit, credited_control, reject, exact

THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')


def rational(v):
    require(type(v) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', v),
            'Exact rational string, never a decimal or float')
    return Q(v)


def decode(seed):
    require(type(seed['n']) is int and seed['n'] in (12, 16), 'Only the two claimed orders')
    active = (3, 4, 5) if seed['n'] == 12 else (4, 5, 6, 7)
    require(seed['active'] == list(active), 'Exact active classes')
    spec = specification(seed['n'], active)
    require(seed['names'] == spec['names'], 'Complete ordered affine coordinates')
    values = [rational(v) for v in seed['values']]
    floor = rational(seed['floor'])
    require(floor > 0, 'Positive stated core upper floor')
    result = verify(spec, values, floor)
    require(result['lower_rank'] == seed['expected_lower_rank'] and
            result['upper_rank'] == seed['expected_upper_rank'], 'Claimed complete original ranks')
    require(result['actual_empty']['loop'] == rational(seed['actual_empty_loop']) and
            result['actual_empty']['row'] == [rational(v) for v in seed['actual_empty_rows']],
            'Every actual empty-row entry and loop')
    return spec, values, result


def literal_populations(spec):
    n, full = spec['n'], (1 << spec['n'])-1
    populations = {a:0 for a in range(2, n//2+1)}
    vertices = 0
    for A in range(1 << n):
        a = A.bit_count()
        if a <= n-2:
            vertices += 1
        Ac = full ^ A
        if 2 <= a <= n-2 and A < Ac:
            populations[min(a, n-a)] += 1
    require(vertices == spec['N'], 'Original downset population')
    require(all(v == comb(n, a)//(2 if a == n//2 else 1)
                for a,v in populations.items()), 'Every literal whole-ground complement class')
    require(sum(populations.values()) == spec['s']-1, 'All original complement pairs')
    actual = sum(populations[a] for a in spec['saturated'])
    require(actual == spec['saturated_pairs'], 'Literal saturated population')
    ell = len(spec['active'])-1
    unavoidable = sum(populations[a] for a in range(2, n//2-ell))
    budget = spec['s']//spec['gap']
    require(unavoidable > budget, 'Exact published population lower bound is strict')
    # For exactly the claimed minimum class count, every absent class is
    # saturated. Their smallest possible population gives a universal rank
    # bound, since stars and all actual saturated pair differences are killed.
    absent_count = (n//2-2)-len(spec['active'])
    minimum_sat = sum(sorted(v for a,v in populations.items() if a < n//2)[:absent_count])
    require(minimum_sat == actual, 'The witness has the least possible saturated population at the class minimum')
    return dict(order=n, vertices=vertices, complementary_populations=populations,
                saturated_pairs=actual, count_budget=budget,
                excluded_class_count=ell, unavoidable_saturated_pairs=unavoidable,
                minimum_noncentral_classes=len(spec['active']),
                unavoidable_saturated_pairs_at_class_minimum=minimum_sat,
                greatest_lower_rank_at_class_minimum=spec['N']-n-minimum_sat)


def damages(seed, spec, values):
    bad = json.loads(json.dumps(seed))
    bad['values'].pop()
    out = [reject(lambda:decode(bad), 'Missing exact free coordinate')]
    bad_float = json.loads(json.dumps(seed))
    bad_float['values'][0] = float(Q(seed['values'][0]))
    out.append(reject(lambda:decode(bad_float), 'Floating coefficient input'))
    bad_empty = json.loads(json.dumps(seed))
    bad_empty['actual_empty_loop'] = str(Q(seed['actual_empty_loop'])+1)
    out.append(reject(lambda:decode(bad_empty), 'Wrong actual original empty loop'))
    wrong_floor = json.loads(json.dumps(seed))
    wrong_floor['floor'] = '-1'
    out.append(reject(lambda:decode(wrong_floor), 'Negative claimed spectral floor'))
    negative, zero = values[:], values[:]
    negative[0], zero[0] = Q(-1), Q(0)
    out.append(reject(lambda:verify(spec, negative), 'Negative complement deficit'))
    out.append(reject(lambda:verify(spec, zero), 'Zero deficit with surviving proper coupling'))
    B = table(spec, values)
    B[1][1] += 1
    out.append(reject(lambda:check_table(spec, B), 'Damaged original star equation'))
    ordinary = sectors(spec, table(spec, [Q(0)]*len(values)))
    out.append(reject(lambda:exact.both(ordinary[0]['upper']), 'Omitting full mean cap would accept ordinary baseline'))
    middle = spec['middle']
    high = table(spec, values)
    high[middle][middle] = Q((-1)**middle*(-spec['s']-1))
    high_block = sectors(spec, high)[middle]['lower']
    out.append(reject(lambda:exact.both(high_block), 'Highest middle parity cone'))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--certificate', default=str(HERE/'CERTIFICATE.json'))
    p.add_argument('--output', help='optional whole regenerated record')
    p.add_argument('--mode', help='optional actual runtime metadata')
    p.add_argument('--check', help='compare the complete expected summary and whole-record hash')
    a = p.parse_args()
    require(all(os.environ.get(k) == '1' for k in THREADS), 'All six native threads fixed at one')
    raw = Path(a.certificate).read_bytes()
    cert = json.loads(raw)
    require(cert['agent'] == 'six-downset-2' and cert['role'] == 'researcher' and
            cert['original_ground_complements'] is True, 'Actual author and original complement domain')
    require([s['n'] for s in cert['cases']] == [12, 16], 'Both claimed cases, once each')
    results, audits, populations, damaged = [], [], [], []
    for seed in cert['cases']:
        spec, values, result = decode(seed)
        results.append(result)
        audits.append(affine_audit(spec))
        population = literal_populations(spec)
        require(result['lower_rank'] == population['greatest_lower_rank_at_class_minimum'],
                'The universal lower rank bound at the class minimum is attained')
        populations.append(population)
        damaged.append(dict(order=spec['n'], rejected=damages(seed, spec, values)))
    audits.append(affine_audit(specification(8, (2, 3))))
    baseline = credited_control()
    out = dict(agent='six-downset-2', role='researcher',
               status='exact rational caps attaining the minimum noncentral class counts and greatest ranks at n12/n16',
               source_status='ordinary author proof; independent review pending; real bridges unformalized',
               rational_certificate_sha256=hashlib.sha256(raw).hexdigest(),
               certificate_results=results, original_populations=populations,
               affine_audits=audits, credited_control=baseline, damages=damaged,
               solver_input=False, solver_status_premise=False,
               mathematical_nonexistence_from_operational_status=False)
    output = json.dumps(out, indent=2, default=lambda v:str(v) if type(v) is Q else None)+'\n'
    if a.output:
        Path(a.output).write_text(output)
    summary = dict(agent='six-downset-2', role='researcher',
                   record_bytes=len(output.encode()),
                   record_sha256=hashlib.sha256(output.encode()).hexdigest(),
                   case_orders=[r['specification']['n'] for r in results],
                   class_counts=[r['noncentral_attenuated_classes'] for r in results],
                   lower_ranks=[r['lower_rank'] for r in results],
                   upper_ranks=[r['upper_rank'] for r in results],
                   upper_gaps=[str(r['original_upper_gap_at_least']) for r in results],
                   original_populations=populations, affine_audits=audits,
                   credited_control=baseline,
                   rejected_damages=[len(r['rejected']) for r in damaged],
                   solver_input=False, independently_reviewed=False,
                   real_bridges_formalized=False)
    summary = json.loads(json.dumps(summary))
    if a.check:
        require(summary == json.loads(Path(a.check).read_text()),
                'Every expected field and the entire regenerated record must match')
    mode = dict(agent='six-downset-2', role='researcher', python=platform.python_version(),
                optimize=sys.flags.optimize, isolated=sys.flags.isolated,
                native_threads={k:os.environ[k] for k in THREADS},
                record_bytes=len(output.encode()), record_sha256=hashlib.sha256(output.encode()).hexdigest(),
                source_sha256={f:hashlib.sha256((HERE/f).read_bytes()).hexdigest()
                               for f in ('model.py', 'core_check.py', 'verify.py', 'CERTIFICATE.json',
                                         'credited/affine.py', 'credited/model.py',
                                         'credited/exact.py', 'credited/matrices.py')})
    if a.mode:
        Path(a.mode).write_text(json.dumps(mode, indent=2)+'\n')
    print(json.dumps(dict(ok=True, expected_checked=bool(a.check), summary=summary,
                         optimize=mode['optimize'], isolated=mode['isolated'])))


if __name__ == '__main__':
    main()
