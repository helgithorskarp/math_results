"""Literal finite-period checks; Python>=3.10, standard library only.

Actual author six-covering-1, researcher. No solver or private search input.
"""
import hashlib
import json
import math
from pathlib import Path

N, B, P = 10080, 1440, 7
MODULI = [m for m in range(8,N+1) if N%m==0]
BASE = [m for m in MODULI if m%P]
TAILS = [m for m in MODULI if m%P==0]
ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode_fixed(rows):
    require(isinstance(rows,list) and rows, 'Missing prescribed classes')
    result = {}
    previous = -1
    for row in rows:
        require(isinstance(row,list) and len(row)==2, 'Malformed class')
        m,a = row
        require(type(m) is int and type(a) is int and m in BASE and previous<m
                and 0<=a<m, 'Non-distinct, noncanonical or ineligible class')
        result[m] = a
        previous = m
    require(8 in result, 'Exact minimum8 anchor is required')
    return result


def decode_weight(nonzero):
    require(isinstance(nonzero,list) and nonzero, 'Missing weight')
    f = [0]*B
    previous = -1
    for row in nonzero:
        require(isinstance(row,list) and len(row)==2, 'Malformed weight row')
        z,w = row
        require(type(z) is int and type(w) is int and previous<z<B and w>0,
                'Nonpositive, repeated or noncanonical weight')
        f[z] = w
        previous = z
    return [f[x%B] for x in range(N)]


def buckets(w,m):
    return [sum(w[x] for x in range(a,N,m)) for a in range(m)]


def check_certificate(cert):
    require(cert['period']==N and cert['base_period']==B, 'Wrong period')
    require(len(cert['families'])==2, 'Missing family')
    result = []
    events = hashlib.sha256()
    for rec in cert['families']:
        fixed = decode_fixed(rec['fixed_classes'])
        free = [m for m in BASE if m not in fixed]
        require(rec['free_base_moduli']==free, 'Missing free base resource')
        w = decode_weight(rec['weight'])
        require(all(w[x]==0 for m,a in fixed.items() for x in range(a,N,m)),
                'Weight intersects prescribed classes')
        unused = [m for m in MODULI if m not in fixed]
        demand, capacity = sum(w), 0
        physical_capacities = {}
        for m in unused:
            v = buckets(w,m)
            physical_capacities[str(m)] = max(v)
            capacity += max(v)
            for a,c in enumerate(v):
                events.update(f'F{len(fixed)}:{m}:{a}:{c}\n'.encode())
        gap = demand-capacity
        require(gap>0 and gap==rec['claimed_gap'], 'No claimed strict gap')
        require(max(w)>0, 'Zero weight')
        result.append(dict(label=rec['label'],prescribed_count=len(fixed),minimum_exactly=8,
                           fixed_lcm=math.lcm(*fixed),free_base_moduli=free,
                           free_base_phase_tuples=math.prod(free),unused_count=len(unused),
                           demand=demand,capacity=capacity,gap=gap,max_weight=max(w),
                           minimum_physical_holes=(gap+max(w)-1)//max(w),
                           physical_capacities=physical_capacities))
    rec = cert['pair_example']
    fixed = decode_fixed(rec['fixed_classes'])
    require(list(fixed)==BASE, 'Pair example needs all thirty bases')
    uncovered = [x for x in range(N) if all(x%m!=a for m,a in fixed.items())]
    H = sorted({x%B for x in uncovered})
    require(uncovered==[x for x in range(N) if x%B in set(H)], 'Residual not periodic')
    support = set(uncovered)
    w = [int(x in support) for x in range(N)]
    values = [buckets(w,m) for m in TAILS]
    demand, capacity = len(uncovered),sum(max(v) for v in values)
    require(demand-capacity==rec['claimed_uniform_gap'], 'Wrong uniform gap')
    unit_max = {-1:None,1:None}
    valid_moves = 0
    for z in H:
        for delta in (-1,1):
            changed_capacity = 0
            for m,old in zip(TAILS,values):
                changed = old[:]
                for x in range(z,N,B):
                    changed[x%m] += delta
                require(min(changed)>=0, 'Negative physical bucket')
                changed_capacity += max(changed)
            gap = demand+P*delta-changed_capacity
            require(gap<=0, 'A single-point move already separates')
            unit_max[delta] = gap if unit_max[delta] is None else max(gap,unit_max[delta])
            events.update(f'U:{z}:{delta}:{gap}\n'.encode())
            valid_moves += 1
    points = rec['points']
    require(isinstance(points,list) and len(points)==2 and all(type(z) is int and z in H for z in points)
            and points[0]<points[1], 'Invalid or repeated pair')
    altered = w[:]
    for z in points:
        for x in range(z,N,B):
            altered[x] += 1
    pair_capacity = 0
    for m in TAILS:
        v = buckets(altered,m)
        pair_capacity += max(v)
        for a,c in enumerate(v):
            events.update(f'P:{m}:{a}:{c}\n'.encode())
    pair_demand = sum(altered)
    gap = pair_demand-pair_capacity
    require(gap>0 and gap==rec['claimed_pair_gap'], 'Pair is not a strict weight')
    pair = dict(base_residual_points=len(H),uniform_demand=demand,uniform_capacity=capacity,
                uniform_gap=demand-capacity,valid_single_unit_moves=valid_moves,
                largest_minus_gap=unit_max[-1],largest_plus_gap=unit_max[1],points=points,
                pair_demand=pair_demand,pair_capacity=pair_capacity,pair_gap=gap,
                maximum_weight=max(altered),minimum_physical_holes=(gap+max(altered)-1)//max(altered))
    return dict(author='six-covering-1',role='researcher',period=N,
                status='TWO_CONDITIONAL_PREFIX_EXCLUSIONS_AND_PAIR_ONLY_WEIGHT_CHECKED',
                families=result,pair_example=pair,event_sha256=events.hexdigest(),
                scope='Specified period10080 prefixes only. No new covering, unrestricted exclusion or optimum claim.')


def main():
    cert = json.loads((ROOT/'certificate.json').read_text())
    actual = check_certificate(cert)
    expected = json.loads((ROOT/'expected.json').read_text())
    require(actual==expected, 'Exact result differs from expected file')
    print(json.dumps(actual,indent=2))


if __name__=='__main__':
    main()
