"""Complete independent order-24 record, ranks and original spectral floors."""
import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path
from fractions import Fraction as Q
from math import comb
sys.path.insert(0, str(Path(__file__).resolve().parent))
from exact import need, matmul, transpose, pivot_rows, psd, cut, subtract, pack
from model import parameters, decode, sector
from literal import literal_control


def calculate(w, floor=Q(1, 100000000), damage=None):
    need(floor > 0, 'positive floor required')
    n = w['n']
    B, empty, loop = decode(n, w['active'], w['names'], w['values'])
    _, populations, N, s = parameters(n)
    h = N-s
    q = sum(comb(n, a) for a in range(2, 7))
    bound = s//(N-2*s)
    subsets = []
    for bits in itertools.product((0, 1), repeat=10):
        absent = [a for a, b in zip(range(2, 12), bits) if b]
        saturated = sum(comb(n, a) for a in absent)
        subsets.append([list(bits), saturated, saturated <= bound])
    permitted_five = [x for x in subsets if sum(x[0]) == 5 and x[2]]
    need(len(permitted_five) == 1 and permitted_five[0][0] == [1]*5+[0]*5, 'unique absent set')
    need(not any(x[2] for x in subsets if sum(x[0]) >= 6), 'four-class obstruction')
    sectors = []
    dimensions = nullity = upper_rank = 0
    for j in range(13):
        if damage == 'omitted-highest' and j == 12:
            continue
        sizes, g, H, V, R, Z = sector(n, B, j)
        if damage == 'physical-cross' and j == 3:
            H[0][1] += 1
        if damage == 'wrong-kernel' and j == 0:
            Z[0][0] += 1
        if damage == 'wrong-mean-metric' and j == 0:
            R[0][0] += 1
            need(V == subtract([[N*v for v in row] for row in R], H), 'complete original metric identity')
        need(H == transpose(H) and V == transpose(V), 'physical symmetry')
        psd(R, positive=True)
        if Z:
            need(all(x == 0 for row in matmul(H, transpose(Z)) for x in row), 'full physical kernel')
        pivots = pivot_rows(Z)
        keep = [i for i in range(len(sizes)) if i not in pivots]
        lower = psd(H)
        upper = psd(V, positive=True)
        need(len(lower) == len(sizes)-len(Z), 'complete lower nullity')
        # A complementary coordinate plane and ORIGINAL metric, not a discarded mean coordinate.
        lower_floor = psd(cut(subtract(H, R, floor), keep), positive=True)
        upper_floor = psd(subtract(V, R, floor), positive=True)
        m = comb(n, j)-(comb(n, j-1) if j else 0)
        if damage == 'wrong-multiplicity' and j == 11:
            m += 1
        dimensions += m*len(sizes)
        nullity += m*len(Z)
        upper_rank += m*len(upper)
        sectors.append({'j':j, 'sizes':sizes, 'norm':g, 'multiplicity':m,
                        'lower':H, 'upper':V, 'original_metric':R,
                        'kernel':Z, 'removed_kernel_pivots':pivots,
                        'lower_pivots':lower, 'upper_pivots':upper,
                        'lower_floor_pivots':lower_floor, 'upper_floor_pivots':upper_floor})
    need(dimensions == N-1 and upper_rank == N-1, 'complete harmonic dimension')
    need(nullity == n+q, 'original independent kernel multiplicity')
    need(loop == Q(2238275691119621, 4468750000), 'independently regenerated original loop')
    delta = floor/(2**93)
    need(min(Q(x) for x in w['values'][:6]) > delta, 'whole-box active deficits')
    summary = {'n':n, 'N':N, 's':s, 'h':h, 'q':q, 'saturated_count_budget':bound,
               'original_lower_rank':N-nullity, 'original_upper_rank':upper_rank,
               'lower_nullity':nullity, 'original_spectral_floor':str(floor),
               'M_two_endpoint_gap':str(floor/h), 'independent_box_radius':str(delta),
               'box_operator_perturbation_bound':str((2**91)*delta),
               'box_two_endpoint_floor':str(3*floor/4),
               'kernel_counts':[len(x['kernel']) for x in sectors],
               'actual_empty_loop':str(loop), 'actual_empty_rows':list(map(str, empty))}
    return pack({'summary':summary, 'completed_table':B,
                 'all_1024_absent_subsets':subsets, 'sectors':sectors})


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--record')
    p.add_argument('--check')
    p.add_argument('--literal', action='store_true')
    p.add_argument('--damage', choices=['missing','duplicate','float','negative-deficit','oversized-floor',
                   'omitted-highest','physical-cross','wrong-kernel','wrong-mean-metric','wrong-multiplicity'])
    a = p.parse_args()
    w = json.loads(Path(__file__).with_name('WITNESS.json').read_text())
    floor = Q(1, 100000000)
    if a.damage == 'missing':
        w['values'].pop()
    elif a.damage == 'duplicate':
        w['names'][-1] = w['names'][0]
    elif a.damage == 'float':
        w['values'][0] = .5
    elif a.damage == 'negative-deficit':
        w['values'][0] = '-1'
    elif a.damage == 'oversized-floor':
        floor = Q(100000000)
    record = literal_control() if a.literal else calculate(w, floor, a.damage)
    b = (json.dumps(record, sort_keys=True, separators=(',',':'))+'\n').encode()
    result = (record if a.literal else record['summary'])|{'record_bytes':len(b),'record_sha256':hashlib.sha256(b).hexdigest()}
    if a.literal:
        result = {k:result[k] for k in ['n','actual_vertices','all_lift_entry_checks',
                     'all_original_point_star_checks','record_bytes','record_sha256']}
    if a.check:
        need(json.loads(Path(a.check).read_text()) == result, 'whole compact result differs')
    if a.record:
        Path(a.record).write_bytes(b)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
