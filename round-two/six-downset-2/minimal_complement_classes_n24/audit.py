"""Exact validation of the complete ORIGINAL degree-zero coordinates.

No SDP status, stored expected mathematical record or numerical eigenvalue
is a premise. Literal8319 is a validation control, not a new result.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import comb
import os
from pathlib import Path
import sys

from model import specification, table, sectors, require
from original_forms import original_form, coordinate_scales

HERE = Path(__file__).resolve().parent
PRIOR = HERE
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dense_congruence(matrix, populations):
    """Independent generic matrix multiplication, not the row-sum recipe."""
    r = len(populations)
    P = [[Q(int(i == k)+populations[k]) for k in range(r)] for i in range(r)]
    HP = [[sum(matrix[i][c]*P[c][k] for c in range(r)) for k in range(r)]
          for i in range(r)]
    return [[sum(P[c][i]*HP[c][k] for c in range(r)) for k in range(r)]
            for i in range(r)]


def audit_basis():
    spec = specification(24, (7, 8, 9, 10, 11))
    scales, gammas = coordinate_scales(spec)
    require(len(spec['names']) == 36 and len(spec['proper']) == 30,
            'Complete unique n24 five-class face')
    zero = [Q(0)]*len(scales)
    probes = [zero]
    for k, scale in enumerate(scales):
        v = zero[:]
        v[k] = scale
        probes.append(v)
    probes.append([scales[k]*Q((-1)**k*(k+1), k+2) for k in range(len(scales))])
    original_signature = None
    total_entries = 0
    for values in probes:
        b = sectors(spec, table(spec, values))
        original = [original_form(spec, block) for block in b]
        signature = [(d['j'], d['lower_keep'], d['kernels'], d['gram']) for d in original]
        if original_signature is None:
            original_signature = signature
        require(signature == original_signature, 'Every scaled affine direction has constant metric and kernels')
        # Exact independent generic P multiplication at the actual target order.
        for side in ('lower', 'upper'):
            require(original[0][side] == dense_congruence(b[0][side], b[0]['gram']),
                    'Full quadratic mean assembly equals generic original congruence')
        total_entries += sum(2*len(d['layers'])**2 for d in original)
    final = original
    q = sum(comb(24, a) for a in range(2, 7))
    next_q = sum(comb(24, a) for a in range(2, 6))+comb(24, 7)
    require(q <= spec['s']//spec['gap'] < next_q, 'Unique five-absent assignment')
    weighted_kernels = sum(len(d['kernels'])*d['multiplicity'] for d in final)
    require(weighted_kernels == 24+q, 'Complete forced-star/saturated weighted nullity')
    return dict(order=24, active=spec['active'], saturated=spec['saturated'],
                coordinates=len(scales), scaled_affine_probes=len(probes),
                complete_original_form_entries=total_entries,
                full_mean_dense_products=2*len(probes),
                all_transformed_kernels=True, all_mean_directions_retained=True,
                necessary_pair_budget=spec['s']//spec['gap'],
                least_five_saturated_population=q, second_least_population=next_q,
                feasibility='not tested by this affine audit', weighted_known_lower_nullity=weighted_kernels,
                degrees=[dict(j=d['j'], full_dimension=len(d['layers']),
                              lower_retained_dimension=len(d['lower_keep']),
                              lower_kernel_count=len(d['kernels']),
                              full_upper_dimension=len(d['layers'])) for d in final],
                scales=[str(s) for s in scales], gamma_pairs=gammas)


def literal_control():
    credited = import_file('credited_literal8319', PRIOR/'credited/matrices.py')
    spec = specification(8, (2, 3))
    values = [Q(6), Q(179, 100), Q(449, 200)]+[Q(0)]*len(spec['proper'])
    values[3+spec['proper'].index((2, 2))] = Q(37, 25)
    blocks = sectors(spec, table(spec, values))
    original = original_form(spec, blocks[0])
    members, L = credited.construct(8, {2:Q(6), 3:Q(179, 100), 4:Q(449, 200)}, Q(37, 25))
    require(len(members) == spec['N'] and members[0] == 0, 'Literal actual original empty index')
    r = spec['r']
    populations = [sum(A.bit_count() == a for A in members) for a in range(1, r+1)]
    require(populations == blocks[0]['gram'], 'Literal population Gram alignment')
    totals = [[Q(0)]*r for _ in range(r)]
    empty_rows = [Q(0)]*r
    entries = 0
    for i, A in enumerate(members):
        for k, B in enumerate(members):
            aa, bb = A.bit_count(), B.bit_count()
            if not aa and bb:
                empty_rows[bb-1] += L[i][k]
            elif aa and bb:
                totals[aa-1][bb-1] += L[i][k]
            entries += 1
    physical = [[populations[i]*populations[k]*L[0][0]
                 -populations[i]*empty_rows[k]-populations[k]*empty_rows[i]
                 +totals[i][k] for k in range(r)] for i in range(r)]
    upper = [[spec['N']*original['gram'][i][k]-physical[i][k]
              for k in range(r)] for i in range(r)]
    require(physical == original['lower'] and upper == original['upper'],
            'Literal original L/NI-L energies, every full mean entry')
    require(original['lower'] == dense_congruence(blocks[0]['lower'], populations),
            'Independent dense congruence on literal control')
    return dict(credited_claim='8319/0', source_commit='6dffbb940c10f415b71e275a45010a7141d1ee4e',
                order=8, vertices=len(members), literal_entries=entries,
                lower_mean_entries=r*r, upper_mean_entries=r*r,
                complete_actual_empty_frame=True, status='new-coordinate validation only')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    a = p.parse_args()
    require(all(os.environ.get(k) == '1' for k in THREADS), 'All native threads one')
    result = dict(agent='six-downset-2', role='researcher',
                  status='exact coordinate validation; certificate tested separately',
                  affine_basis=audit_basis(), literal_control=literal_control(),
                  flags=dict(isolated=sys.flags.isolated, optimized=sys.flags.optimize),
                  native_threads={k:os.environ[k] for k in THREADS},
                  source_sha256={str(f.relative_to(HERE)):hashlib.sha256(f.read_bytes()).hexdigest()
                      for f in [HERE/'model.py', HERE/'original_forms.py', Path(__file__),
                                PRIOR/'credited/matrices.py']})
    Path(a.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(order=24, affine_probes=result['affine_basis']['scaled_affine_probes'],
                         literal_entries=result['literal_control']['literal_entries'],
                         feasibility='not tested by this affine audit')))


if __name__ == '__main__':
    main()
