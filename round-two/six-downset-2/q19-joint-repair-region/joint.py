"""Self-contained joint-flow source, openly reusing the exact 10332 model.

The published all-count completeness proof is the mathematical bridge;
this pilot does not borrow any old endpoint factor or floor.
"""
from binding import check_current
check_current()
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib
import json
import resource
import sys
import time

PARENT = Path(__file__).resolve().parent
model = importlib.import_module('model')
diagnose = importlib.import_module('diagnose')
physical = importlib.import_module('physical')


def table_at(raw, tau, pxx, px, d):
    """Affine four-coordinate recipe; domain/feasibility are separate."""
    model.require(all(type(v) is F for v in (tau, pxx, px, d)),
                  'all four coordinates are exact rational values')
    changed, record = model.q19_candidate(raw, tau)
    P = F(record['P'])
    def add(t, u, value):
        key = tuple(sorted((t, u)))
        model.require(key in changed, 'actual independent joint-flow coordinate')
        changed[key] += value
    add((0, 2, 0), (0, 2, 0), (pxx-P/4)/378)
    add((0, 1, 0), (0, 1, 0), (px-P/2)/36)
    add((0, 0, 1), (0, 0, 1), ((P-pxx-px)-P/4)/45)
    add((7, 0, 0), (0, 0, 2), tau-d)
    return changed, dict(tau=str(tau), pXX=str(pxx), pX=str(px),
                         pY=str(P-pxx-px), star_release=str(d), P=str(P))


def run(tau, shares, release_share, mode):
    start = time.monotonic()
    raw = model.coefficient_input(PARENT / 'COEFFICIENTS.json')
    old_table = model.comparison(raw, 9, 10)
    b = model.type_budgets(old_table, 9, 10)
    P = b['P0']+38*tau
    table, recipe = table_at(raw, tau, shares[0]*P, shares[1]*P,
                             release_share*tau)
    model.require(all(F(recipe[key]) >= 0 for key in ('pXX','pX','pY','star_release')),
                  'nonnegative component masses and star release')
    if mode == 'physical':
        point = physical.original(table, 9, 10)
        basis, gram = physical.complete_basis(point)
        actions = physical.literal_actions(point, table, basis)
        data = dict(gram=gram, actions=actions,
                    original_L_rational_sha256=model.digest([
                        [str(F(a,point['den'])) for a in row] for row in point['L']]),
                    original_T_rational_sha256=model.digest([
                        [str(F(a,point['den'])) for a in row] for row in point['T']]))
    else:
        old = model.literal_point(old_table, 9, 10)
        point = model.literal_point(table, 9, 10)
        data = dict(entries=diagnose.entry_audit(point, old, b, tau))
    tests = diagnose.certificates(table, 9, 10)
    return dict(agent='six-downset-2', role='researcher',
                status='exact first-trial evidence; ordinary physical bridge credited to actual10332',
                mode=mode, recipe=recipe, data=data, fresh_blocks=tests,
                all_twelve_shifted_forms_positive=all(
                    v['exact_block_test']['positive_definite'] for v in tests.values()),
                defining_input_sha256=hashlib.sha256((PARENT/'COEFFICIENTS.json').read_bytes()).hexdigest(),
                source_imports={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (PARENT/'model.py', PARENT/'diagnose.py', PARENT/'physical.py')},
                observed_seconds=time.monotonic()-start,
                peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                no_global_optimizer_domain_or_H_nonexistence_claim=True)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv)>1 else 'entries'
    record = run(F(1,12), (F(5,16), F(7,16)), F(3,4), mode)
    print(json.dumps(record,sort_keys=True,indent=2))
