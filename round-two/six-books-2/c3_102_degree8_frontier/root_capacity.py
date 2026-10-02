"""Exact marked root/degree-capacity reduction for P1, before X/K search."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import json, resource, time
from cases import CASES

START = time.monotonic()
parser = ArgumentParser()
parser.add_argument('--work', type=Path, required=True)
OUT = parser.parse_args().work
OUT.mkdir(parents=True, exist_ok=True)
FREE = (8,9,9,9,10,10,10)
placements = sorted({tuple(FREE[i] for i in slots) for slots in combinations(range(7),3)})
records = []
residual = []
for A in placements:
    B = list(FREE)
    for d in A:
        B.remove(d)
    B = tuple(B)
    DA = 3*sum(A)
    root_deficit = 171-2*DA
    record = dict(A=A, B=B, DA=DA, root_deficit=root_deficit, cuts=[])
    if root_deficit < 0:
        record['verdict'] = 'negative_fixed_root_deficit'
        records.append(record)
        continue
    for h in range(0,13,3):
        k = 102-DA+h
        if k < 30:
            record['cuts'].append(dict(h=h, k=k, verdict='K_minimum_degree_five'))
            continue
        t_vectors = [t for t in product(range(4), repeat=3) if 3*sum(t)==2*h]
        if not t_vectors:
            raise ValueError('Empty ordinary H-degree upper domain')
        capacities = [(t,17*h-540+8*DA-3*sum(x*d for x,d in zip(t,A))-3*sum(x*(x-1)//2 for x in t)) for t in t_vectors]
        upper = max(c for _,c in capacities)
        beta_vectors = [beta for beta in product(*(range(5,d+1) for d in B)) if 3*sum(beta)==2*k]
        alpha_vectors = sorted({tuple(d-b for d,b in zip(B,beta)) for beta in beta_vectors})
        canonical = []
        for alpha in alpha_vectors:
            if any(B[i]==B[j] and alpha[i]>alpha[j] for i in range(4) for j in range(i+1,4)):
                continue
            overlap = 3*sum(a*(a-1)//2 for a in alpha)
            survives = overlap <= upper
            canonical.append(dict(alpha=alpha, beta=[d-a for d,a in zip(B,alpha)], overlap=overlap, survives=survives))
            if survives:
                match = [name for name,c in CASES.items() if tuple(c['A'])==A and tuple(c['B'])==B and tuple(c['alpha'])==alpha]
                if len(match)!=1 or h!=12:
                    raise ValueError('Unexpected necessary marked root case: extend coverage before a claim')
                residual.append(dict(case=match[0], A=A, B=B, h=h, k=k, alpha=alpha, overlap=overlap, capacity_upper=upper))
        record['cuts'].append(dict(h=h,k=k,capacity_upper=upper,degree_vectors=capacities,ordered_beta_vectors=beta_vectors,
                                   canonical_columns=canonical,minimum_column_overlap=min((v['overlap'] for v in canonical),default=None),
                                   verdict='residual_marked_case' if any(v['survives'] for v in canonical) else 'column_overlap_exceeds_capacity'))
    record['verdict']='some_marked_cases_survive' if any(r['A']==A for r in residual) else 'capacity_exclusion'
    records.append(record)
    if time.monotonic()-START>25:
        raise RuntimeError('INCOMPLETE root reduction; no exclusion')
if {r['case'] for r in residual}!=set(CASES) or len(residual)!=len(CASES):
    raise ValueError('Complete residual case coverage differs')
result=dict(status='COMPLETE_EXACT_P1_ROOT_CAPACITY_REDUCTION',agent='six-books-2',role='researcher',
            scope='Valid ordinary22 caps3/6, degree8^3,9^10,10^9, C3 cycle3^7 1. Necessary root cases only.',
            free_degree_orbits=FREE,placements=records,residual=residual,
            seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1,
            trust='Exact finite integer upper domains; written ordinary/completeness bridges unformalized, same-author checks only.')
(OUT/'root-capacity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='placements'},indent=2))
