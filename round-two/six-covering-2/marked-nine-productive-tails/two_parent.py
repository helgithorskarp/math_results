"""Exact controls for the three-parent/eight-tail follow-up lemma."""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, lcm, prod
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def build():
    ds = [d for d in range(1,316) if 315 % d == 0]
    unused = ds[1:]
    prefix = ((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
    actual = {r:[x for x in range(r,2520,8) if all(x % m != a for m,a in prefix)]
              for r in (1,2,3,4,5,6,7)}
    phase_rows = []
    maxima = {}
    for r in actual:
        for d in ds:
            physical = [sum(x % d == a for x in actual[r]) for a in range(d)]
            if r in (2,6):
                factors = ([2,3,5,6,8],range(5),[1,2,3,4,5,6])
            else:
                factors = (range(1,9),range(5) if r == 4 else [0,2,3,4],
                           [1,2,3,5,6] if r == 4 else range(7))
            compressed = [prod(sum(y % q == a % q for y in ys)
                               for q,ys in zip((gcd(d,9),gcd(d,5),gcd(d,7)),factors))
                          for a in range(d)]
            require(physical == compressed, 'Every actual2520 odd phase must match CRT')
            phase_rows.append([r,d,physical])
            maxima[r,d] = max(physical)
    C = {d:maxima[2,d] for d in ds}
    require(all(C[d] == maxima[6,d] for d in ds),'Mandatory parent capacities differ')

    rows = []
    for r in (1,3,4,5,7):
        for g,h in combinations(unused,2):
            remaining = [d for d in unused if d not in (g,h)]
            for triple in combinations(remaining,3):
                shadow = maxima[r,lcm(g,h)]
                covered = sum(C[d] for d in triple)
                rows.append([r,g,h,*triple,shadow,covered,shadow+covered])
    coupled_max = {str(r):max(row[-1] for row in rows if row[0] == r)
                   for r in (1,3,4,5,7)}
    require(coupled_max == {'1':166,'3':166,'4':165,'5':166,'7':166},
            'Global five-extraH coupling bound changed')
    require(len(rows) == 23100,'Complete distinct cofactor allocations missing')

    # Three classes in an unmarked parent, with inactive odd footprints.
    controls = []
    for r in (1,3,4,5,7):
        x = min(actual[r]);lifts = [x+2520*k for k in range(4)]
        for types in ('HHH','HHQ','HQQ','QQQ'):
            domains = [(0,5,10) if t == 'H' else (0,1,2,4,8) for t in types]
            for states in product(*domains):
                masks = []
                for i,(kind,state) in enumerate(zip(types,states)):
                    two = 16 if kind == 'H' else 32
                    d = (3,5,7)[i]
                    k = next((k for k in range(4) if state & (1 << k)),0)
                    binary = lifts[k] % two
                    odd = x % d if state else (x+1) % d
                    phase = next(a for a in range(two*d) if a % two == binary and a % d == odd)
                    mask = sum(1 << j for j,y in enumerate(lifts) if y % (two*d) == phase)
                    require(mask == state,'Literal three-class state differs')
                    masks.append(mask)
                union = masks[0] | masks[1] | masks[2]
                covered = union == 15
                if covered:
                    if types == 'HHH':require(5 in masks and 10 in masks,'Missing opposite three-half orientation')
                    elif types == 'HHQ':require((masks[0] | masks[1]) == 15,'Quarter extends a two-half repair')
                    elif types == 'HQQ':require(all(masks),'A mixed three-class odd footprint is inactive')
                    else:raise ValueError('Three quarters cover four lifts')
                controls.append([r,types,list(states),covered])
    require(len(controls) == 1360,'Three-class raw type controls incomplete')
    cases = []
    for r in (1,3,4,5,7):
        pair_max = max(maxima[r,lcm(g,h)] for g,h in combinations(unused,2))
        cases.extend([
            [r,'2+4+2','HHQ',coupled_max[str(r)]],
            [r,'2+4+2','HQQ',120+pair_max],
            [r,'2+4+2','QQQ',90+18+pair_max],
            [r,'3+3+2','HH / HQ',coupled_max[str(r)]],
            [r,'3+3+2','HQ / HQ',120+pair_max],
            [r,'3+3+2','QQ / HQ',30+90+pair_max],
            [r,'2+3+3','HHH',120+2*pair_max],
            [r,'2+3+3','HHQ',120+pair_max],
            [r,'2+3+3','HQQ',120+pair_max]])
    require(max(row[-1] for row in cases) == 176,'Eight-tail three-parent upper bound changed')
    result = {'agent':'six-covering-2','role':'researcher','status':'AUTHOR-CHECKED two-parent reduction; not part of actual9978',
              'full_marked_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
              'essential_originals_explicit':[16,32],'whole_physical_phase_rows':phase_rows,
              'all_global_five_extra_H_coupling_rows':rows,'coupled_maxima':coupled_max,
              'complete_literal_three_class_controls':controls,'all_three_parent_eight_tail_cases':cases,
              'maximum_three_parent_eight_tail_BASE_holes':176,
              'BASE_holes_lower_bound_imported_from_public9934':177,
              'exactly_eight_productive_TAILs_imply_exactly_two_hole_parents':True,
              'remaining_two_parent_counts':[[2,6],[3,5],[4,4],[5,3]],
              'capacity_sharpness_claimed':False,'ordinary_proof_formalized':False,
              'independent_reviewer':False,'global_bound_changed':False}
    return result
