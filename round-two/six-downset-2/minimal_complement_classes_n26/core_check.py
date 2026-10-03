"""Standard-library exact checking of the two minimal-class certificates.

No solver status, tolerance, numerical eigenvalue, or unpublished external
input is accepted as proof. Credited harmonic/lift bridges remain ordinary
unformalized mathematics. Two exact PSD algorithms check every full sector.
"""
from fractions import Fraction as Q
import importlib.util
from math import comb
from pathlib import Path
import sys
from model import specification, table, sectors, lower_keep, empty_entries, require, check_table

HERE = Path(__file__).resolve().parent
PRIOR = HERE/'credited'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


face_model = sys.modules['model']
old_model = module('credited_three_class_model', PRIOR/'model.py')
sys.modules['model'] = old_model
try:
    old_affine = module('credited_three_class_affine', PRIOR/'affine.py')
    exact = module('credited_three_class_exact', PRIOR/'exact.py')
finally:
    sys.modules['model'] = face_model


def verify(spec, values, floor=Q(1, 100)):
    require(type(floor) is Q and floor >= 0, 'Exact nonnegative floor')
    require(all(type(v) is Q for v in values), 'Exact coefficients, not floats')
    B = table(spec, values)
    count = len(spec['active'])+1
    require(all(0 < d <= 2*(spec['s']-1) for d in values[:count]),
            'This certificate uses strictly positive active deficits')
    where = {a:i for i, a in enumerate([*spec['active'], spec['middle']])}
    budgets = []
    for t, (a, b) in zip(values[count:], spec['proper']):
        u, v = values[where[min(a, spec['n']-a)]], values[where[min(b, spec['n']-b)]]
        slack = 4*u*v-t*t
        require(slack >= 0, 'Necessary original complement-pair coupling budget')
        budgets.append(slack)
    rec, core_rank, upper_rank = [], 0, 0
    blocks = sectors(spec, B)
    credited = old_model.blocks(spec['n'], B)
    require(len(blocks) == spec['n']//2+1, 'All lower and upper degrees retained')
    for b, (j, aa, g, K, U) in zip(blocks, credited):
        require((b['j'], b['layers'], b['gram'], b['K'], b['U']) == (j, aa, g, K, U),
                'Whole credited harmonic coefficient agreement')
        keep, kernels = lower_keep(spec, b)
        rank = exact.both(b['lower'], len(aa)-len(kernels))
        urank = exact.both(b['upper'], len(aa))
        reduced = [[b['lower'][i][k]-floor*g[i]*int(i == k) for k in keep] for i in keep]
        exact.both(reduced, len(keep))
        cap_floor = [[b['upper'][i][k]-floor*g[i]*int(i == k)
                      for k in range(len(aa))] for i in range(len(aa))]
        exact.both(cap_floor, len(aa))
        core_rank += rank*b['multiplicity']
        upper_rank += urank*b['multiplicity']
        rec.append(dict(j=j, layers=aa, gram=g, multiplicity=b['multiplicity'],
                        lower_rank=rank, lower_kernel_count=len(kernels),
                        lower_retained_layers=[aa[i] for i in keep],
                        upper_rank=urank, both_floor_tests=True))
    require(core_rank == spec['N']-1-spec['n']-spec['saturated_pairs'],
            'Complete original lower rank, including saturated-pair nullity')
    require(upper_rank == spec['N']-1, 'Complete original cap rank')
    e = empty_entries(spec, B)
    require(0 <= e['loop'] <= spec['N'], 'Actual original empty loop lies in cap interval')
    for a in range(1, spec['r']+1):
        row = e['row'][a-1]+spec['s']+sum(B[a][b]*comb(spec['n']-a, b)
                                                      for b in range(1, spec['r']+1))
        require(row == spec['N'], 'Every actual original nonempty row')
        for i_in_A in (True, False):
            # Complete original star sum for any point in / outside A.
            total = spec['s'] if i_in_A else sum(B[a][b]*comb(spec['n']-a-1, b-1)
                                                        for b in range(1, spec['r']+1))
            require(total == spec['s'], 'Definition-level original point-star sum')
    empty_star = sum(comb(spec['n']-1, b-1)*e['row'][b-1]
                     for b in range(1, spec['r']+1))
    require(empty_star == spec['s'], 'Actual empty-row star equation')
    return dict(specification=spec, values=values, table=B,
                lower_rank=1+core_rank, upper_rank=upper_rank, sectors=rec,
                floor=floor, original_upper_gap_at_least=floor/spec['h'],
                actual_empty=e, coupling_slacks=budgets,
                saturated_pairs=spec['saturated_pairs'],
                saturated_budget=spec['s']//spec['gap'],
                noncentral_attenuated_classes=len(spec['active']))


def affine_audit(spec):
    zero = [Q(0)]*len(spec['names'])
    probes = [zero]
    for k in range(len(zero)):
        unit = zero[:]
        unit[k] = Q(1)
        probes.append(unit)
    probes += [[Q((-1)**k*(k+1), k+2) for k in range(len(zero))]]
    free_pairs, recover = old_affine.rref(spec['n'])
    total_entries = 0
    for values in probes:
        B = table(spec, values)
        free = [B[a][b] for a, b in free_pairs]
        require(B == recover(free) == old_affine.direct(spec['n'], free),
                'Entire affine basis against independent full star RREF')
        for b in sectors(spec, B):
            lower_keep(spec, b)
        total_entries += len(B)**2
    return dict(order=spec['n'], probes=len(probes),
                complete_table_entries=total_entries, all_stars=True,
                independent_rref=True, all_constant_lower_kernels=True)


def credited_control():
    spec = specification(8, (2, 3))
    values = [Q(6), Q(179, 100), Q(449, 200)]+[Q(0)]*len(spec['proper'])
    values[len(spec['active'])+1+spec['proper'].index((2, 2))] = Q(37, 25)
    # Its known margin is much smaller than our new 1/100 floor, so use zero.
    result = verify(spec, values, Q(0))
    old = module('credited_literal_pair_expanded', PRIOR/'matrices.py')
    members, L = old.construct(8, {2:Q(6), 3:Q(179, 100), 4:Q(449, 200)}, Q(37, 25))
    B, e = result['table'], result['actual_empty']
    entry_count = 0
    for i, A in enumerate(members):
        for k, T in enumerate(members):
            if not A and not T:
                value = e['loop']
            elif not A or not T:
                value = e['row'][(A or T).bit_count()-1]
            elif A == T:
                value = Q(spec['s'])
            elif A & T:
                value = Q(0)
            else:
                value = B[A.bit_count()][T.bit_count()]
            require(value == L[i][k], 'Every credited n8 original entry')
            entry_count += 1
        require(sum(L[i]) == spec['N'], 'Every credited original row')
        for point in range(8):
            require(sum(L[i][k] for k,T in enumerate(members) if T & (1 << point)) == spec['s'],
                    'Every credited original star')
    return dict(credited_claim='8319/0', source_commit='6dffbb940c10f415b71e275a45010a7141d1ee4e',
                order=8, vertices=len(members), entry_alignment=entry_count,
                original_star_rows=8*len(members), lower_rank=result['lower_rank'],
                upper_rank=result['upper_rank'], status='validation only, not new')


def reject(f, label):
    try:
        f()
    except (ValueError, TypeError, IndexError):
        return label
    raise ValueError('Damaged control accepted: '+label)
