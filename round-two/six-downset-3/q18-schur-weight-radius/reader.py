"""Self-contained q18 combined author reader; source checked before math.

POSIX, CPython >=3.11, standard library only, isolated interpreter (-I).
The ordinary proofs, not this finite executable, pay all real/completeness
bridges. SOURCE.json needs the externally verified Git commit as anchor.
"""
import sys
if not sys.flags.isolated:
    raise SystemExit('Use python3 -I reader.py (or python3 -I -O reader.py).')

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal


ROOT = Path(__file__).resolve().parent
FILES = {
    '.gitignore', 'CANDIDATE.json', 'COMPARISON.json', 'QUARTER-REFERENCE.json',
    'aggregate.py', 'optimize.py', 'individual_dual.py', 'radius.py',
    'coupled_radius.py', 'reader.py', 'reproduce.py', 'adverse.py',
    'PROOF.md', 'BASIC-RADIUS-PROOF.md', 'COUPLED-PROOF.md', 'README.md',
    'DEPENDENCIES.json', 'PROVENANCE.json', 'CLAIM.json', 'EXPECTED.json',
    'VALIDATION.json',
}
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')
MAX_FILE = 256*1024
MAX_BUNDLE = 1024*1024


def require(ok, message):
    if not ok:
        raise ValueError(message)


def source_gate():
    require(sys.version_info >= (3, 11), 'Python version must be >=3.11')
    sp = ROOT/'SOURCE.json'
    require(sp.is_file() and not sp.is_symlink(), 'source seal missing')
    raw = sp.read_bytes()
    require(len(raw) <= MAX_FILE, 'source descriptor byte guard')
    seal = json.loads(raw)
    require(seal.get('schema') == 1 and set(seal.get('files', {})) == FILES,
            'source file coverage mismatch')
    require(set(p.name for p in ROOT.iterdir() if p.is_file()) == FILES|{'SOURCE.json'},
            'unexpected source file')
    require(all(p.name == '__pycache__' for p in ROOT.iterdir() if p.is_dir()),
            'unexpected source directory')
    total = 0
    for name in sorted(FILES):
        p = ROOT/name
        require(p.is_file() and not p.is_symlink(), 'source file missing: '+name)
        raw = p.read_bytes(); total += len(raw)
        item = seal['files'][name]
        require(len(raw) <= MAX_FILE and len(raw) == item['bytes'] and
                hashlib.sha256(raw).hexdigest() == item['SHA256'],
                'source bytes mismatch: '+name)
    require(total <= MAX_BUNDLE, 'source bundle byte guard')
    return seal


def coefficient_preflight():
    for name, dkey, nkey, expected_denominator in [
            ('CANDIDATE.json', 'denominator', 'free_numerators', 2**32),
            ('COMPARISON.json', 'comparison_free_denominator',
             'comparison_free_numerators', 16384)]:
        d = json.loads((ROOT/name).read_bytes())
        values = d.get(nkey)
        require(type(d.get(dkey)) is int and d[dkey] == expected_denominator,
                'coefficient denominator guard: '+name)
        require(isinstance(values, list) and len(values) == 143 and
                all(type(x) is int and abs(x) < 10**15 for x in values),
                'coefficient count/integer/size guard: '+name)
    d = json.loads((ROOT/'QUARTER-REFERENCE.json').read_bytes())
    require(d.get('v_S_complete58_denominator') == 4*2**32 and
            len(d.get('v_S_complete58_numerators', [])) == 58 and
            all(type(x) is int and abs(x) < 10**15
                for x in d['v_S_complete58_numerators']),
            'quarter-reference original vector guard')


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/(name+'.py'))
    require(spec is not None and spec.loader is not None, 'producer loader')
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


def compute():
    # Every code/document/data/EXPECTED byte was pinned first. EXPECTED is
    # used as semantic DATA only AFTER every fresh mathematical derivation.
    coefficient_preflight()
    aggregate = module('aggregate'); optimize = module('optimize')
    individual = module('individual_dual'); radius = module('radius')
    coupled = module('coupled_radius')
    data = aggregate.aggregate(include_individual_data=True)
    opt = optimize.check(data)
    dual = individual.check(data)  # Removes transient literal individual arrays.
    decoded = radius.decode()
    row = radius.check(decoded); col = coupled.check(decoded)
    from fractions import Fraction as F
    require(data['original_star_masks'] == row['original_star_masks'] and
            [sum(v[s] for v in data['candidate_three_whole58_vector_numerators'])
             for s in range(58)] == row['complete_original58_vector_numerators'],
            'ALL58 combined original-coordinate bindings')
    cap = sum(F(x) for line in data['old_BB_cap'] for x in line)
    require(str(cap) == row['old_all_one_BB_cap'] == col['old_BB_cap'] ==
            opt['comparison_cap_all_one'], 'whole combined original-cap binding')
    require(dual['full_individual_weight_maximum'] == opt['full_three_type_maximum'] and
            F(dual['sum_all_ordered_edge_prices']) == 2*F(dual['full_individual_weight_maximum']),
            'combined full81 dual/three-type exact optimum binding')
    require(row['positive_star_positions'] == col['positive_original_star_positions'] and
            row['negative_star_positions'] == col['negative_original_star_positions'] and
            row['positive_coordinate_sum'] == col['positive_original_aggregate_sum'],
            'combined ENTIRE original signed partition binding')
    require(all(rec['full_real_tau_interval'] == ['0', '1/256']
                for rec in (opt, row, col)), 'published witness real interval licence')
    require(all(rec['independent_review_claimed'] is False
                for rec in (data, opt, dual, row, col)), 'author evidence scope')
    license = {
        'actual_agent': 'six-downset-3', 'role': 'researcher',
        'carrier_N_s_B': row['original_carrier_N_s_B'],
        'full_real_tau_interval': col['full_real_tau_interval'],
        'individual_nonnegative_weight_domain':
            'ALL81 individual-real weights, alpha>0; alpha=0 has no positive gap',
        'all81_unique_positive_maximizers': 'u=c1_B,c>0',
        'fixed_fiber_clean_strict_gap_lower': opt['clean_strict_lower'],
        'original_optimizer_NS_movement_clean_strict_lower':
            col['original_optimizer_NS_entry_movement_clean_strict_lower'],
        'basic_aggregate_threshold_strict_cage': row['threshold_strict_rational_isolation'],
        'coupled_aggregate_threshold_strict_cage': col['threshold_strict_rational_isolation'],
        'both_relaxations_full_real_radius_coverage':
            'feasible iff e>=their stated threshold, ALL real e>=0',
        'original_NS_matrix_at_threshold_or_best_original_distance_claimed': False,
        'general_signed_H_I_solution_or_counterexample_claimed': False,
        'ordinary_bridges_unformalized': True,
        'independent_review_claimed': False,
    }
    require(json.loads((ROOT/'CLAIM.json').read_bytes()) == license, 'CLAIM licence/scope mismatch')
    result = {
        'actual_agent': 'six-downset-3', 'role': 'researcher',
        'licensed_scope': license,
        'math_records': {
            'three_weight_aggregate': data, 'three_weight_optimum': opt,
            'individual81_dual': dual, 'original58_box_radius': row,
            'original58_coupled_radius': col,
        },
    }
    raw = (json.dumps(result, indent=2)+'\n').encode()
    expected_raw = (ROOT/'EXPECTED.json').read_bytes()
    require(json.loads(expected_raw) == result, 'whole EXPECTED semantic record mismatch')
    require(expected_raw == raw, 'whole EXPECTED canonical-byte mismatch')
    require(len(raw) <= MAX_FILE, 'complete output byte guard')
    return raw


def alarm(signum, frame):
    raise TimeoutError('fixed45-second process guard: incomplete, not nonexistence')


def main():
    for name in THREADS:
        os.environ[name] = '1'
    signal.signal(signal.SIGALRM, alarm); signal.alarm(45)
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path)
    ap.add_argument('--source-only', action='store_true')
    args = ap.parse_args()
    source_gate()
    if args.source_only:
        raw = (json.dumps({'source_verified': True, 'files': len(FILES),
                           'mathematical_producer_imported': False})+'\n').encode()
    else:
        raw = compute()
    if args.out is None:
        sys.stdout.buffer.write(raw)
    else:
        require(not args.out.exists() and not args.out.is_symlink(), 'output path must be fresh')
        require(not args.out.resolve().is_relative_to(ROOT), 'generated output outside source directory')
        with args.out.open('xb') as out:
            out.write(raw)
    signal.alarm(0)


if __name__ == '__main__':
    try:
        main()
    except ValueError as exc:
        print(json.dumps({'accepted': False, 'gate': str(exc)}), file=sys.stderr)
        raise SystemExit(2)
