"""Exhaustive small physical controls for the singleton replacement lemma.

All two-row pattern multiplicities0..2 and capacities0..2; all three-row
pattern multiplicities0..1 and capacities0..2. Literal item subsets supply
the oracle, and residual-hole item subsets supply a separate normal form.
"""
import itertools
import json


def pack_max(items, capacities):
    best = 0
    for chosen in range(1<<len(items)):
        number = chosen.bit_count()
        if number <= best:
            continue
        used = [0]*len(capacities)
        for i, pattern in enumerate(items):
            if (chosen >> i)&1:
                for j in range(len(capacities)):
                    used[j] += (pattern >> j)&1
        if all(u <= c for u,c in zip(used,capacities)):
            best = number
    return best


fixtures = 0
for rows, values in ((2,range(3)),(3,range(2))):
    patterns = list(range(1,1<<rows))
    for numbers in itertools.product(values,repeat=len(patterns)):
        items = [p for p,n in zip(patterns,numbers) for i in range(n)]
        for capacities in itertools.product(range(3),repeat=rows):
            singles = [min(capacities[i],numbers[(1<<i)-1]) for i in range(rows)]
            holes = tuple(capacities[i]-singles[i] for i in range(rows))
            residual = [p for p in items if p.bit_count()>1]
            normal_form = sum(singles)+pack_max(residual,holes)
            literal = pack_max(items,capacities)
            if normal_form != literal:
                raise ValueError((rows,numbers,capacities,literal,normal_form))
            fixtures += 1
print(json.dumps({'agent':'six-vdw-3','role':'researcher','small_exhaustive_capacity_fixtures':fixtures,
                  'status':'COMPLETE_SINGLETON_REPLACEMENT_CONTROLS_PASSED'}))
