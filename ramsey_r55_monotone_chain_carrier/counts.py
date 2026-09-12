"""Two exact chain counts and complete old/new physical carrier counts."""
from collections import Counter
from math import comb
import json
from pathlib import Path
from chains import distribution, ways


def laurent(m):
    p = {0: 1}
    for _ in range(m):
        out = Counter()
        for a, c in p.items():
            for b, d in ((0, 5), (-2, 3), (2, 3), (-1, 1), (1, 1), (-3, 1), (3, 1)):
                out[a+b] += c*d
        p = out
    return p.get(0, 0)+p.get(1, 0)


def fixed_factor(q, r):
    a, b = r-1, q-r
    return (comb(1998+a-1, a)*comb(1931+b-1, b)*
            37823**(comb(a, 2)+comb(b, 2))*35714**(a*b))


def calculate():
    levels, rows = [], []
    for q, cores in ((7, 640), (8, 546356), (9, 362), (10, 4)):
        m = q*(43-4*q)
        d = distribution(m)
        a = sum(d.values())
        if a != laurent(m) or a != ways(m) or sum(k*v for k, v in d.items()) != 15**m:
            raise ValueError('independent chain-count disagreement')
        levels.append(dict(q=q, stars=m, chains=a, states=15**m,
                           ratio_display=15**m/a, strict_integer_gain=(15**m-1)//a,
                           maximum_chain_length=max(d)))
        for r in range(5, q+1):
            factor = fixed_factor(q, r)
            rows.append(dict(q=q, r=r, cores=cores, fixed_factor=factor,
                             old_per_task=factor*15**m, new_per_task=factor*a))
    old = sum(x['cores']*x['old_per_task'] for x in rows)
    new = sum(x['cores']*x['new_per_task'] for x in rows)
    parent = json.loads((Path(__file__).resolve().parent.parent/
                         'ramsey_r55_maximal_block_order/COUNTS.json').read_text())
    if old != parent['P']:
        raise ValueError('complete reviewed carrier identity mismatch')
    remaining = [x for x in rows if not (x['q'] == 7 and x['r'] < 7)]
    physical = []
    for r in range(5, 9):
        for g, multiplicity in ((7, 17), (8, 222)):
            base = fixed_factor(8, r)*2**(55-g)
            physical.append(dict(q=8, r=r, guard_size=g, cohort_count=multiplicity,
                                 old_per_cohort=base*15**88,
                                 new_per_cohort=base*laurent(88)))
    if 17*2**48+222*2**47 != 2**55:
        raise ValueError('guard cylinder volume mismatch')
    return dict(levels=levels, original_tasks=sum(x['cores'] for x in rows),
                original_macros=rows, original_codes=old, chain_obligations=new,
                ratio_display=old/new,
                after_mixed_q7_redirect=dict(tasks=sum(x['cores'] for x in remaining),
                    original_codes=sum(x['cores']*x['old_per_task'] for x in remaining),
                    chain_obligations=sum(x['cores']*x['new_per_task'] for x in remaining)),
                physical_q8_cohorts=sum(x['cohort_count'] for x in physical),
                physical_q8_rows=physical,
                active_M8_positive_edge119=dict(root_matrices_below_4096=213,
                    excluded_fixed_frames=comb(219, 7)*37823**21,
                    retained_fixed_frames=fixed_factor(8, 8)-comb(219, 7)*37823**21,
                    states_per_frame=15**88, chains_per_frame=laurent(88),
                    imported_root_unit=True),
                retired_original_tasks=0, closed_physical_cohorts=0,
                runtime_improvement_claimed=False)


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2, sort_keys=True))
