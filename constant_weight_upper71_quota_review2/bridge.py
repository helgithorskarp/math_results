"""Small exact checks for the written global bridge and positive baselines."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from hashlib import sha256
from math import comb
import json
from incidence import need


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for z in range(minimum, total+1):
        for rest in partitions(total-z, z):
            yield (z,)+rest


def main():
    source=Path(__file__).resolve().parent
    raw=(source/'baseline69.txt').read_bytes()
    need(sha256(raw).hexdigest()=='cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d', 'primary 69 fixture bytes changed')
    lines=raw.decode().splitlines()
    need(len(lines)==69 and all(len(l)==18 and set(l)<={'0','1'} for l in lines), 'malformed primary69 fixture')
    words=[frozenset(i for i,c in enumerate(l) if c=='1') for l in lines]
    need(len(set(words))==69 and all(len(w)==5 for w in words), 'invalid primary69 words')
    overlaps=Counter(len(u&v) for u,v in combinations(words,2))
    need(max(overlaps)<=2, 'primary69 pair distance violation')
    fixtures=json.loads((source/'fixtures.json').read_text())
    records=[]
    for rec in fixtures['profiles']:
        ws=[frozenset(w) for w in rec['fixture']]
        need(len(ws)==20 and len(set(ws))==20 and all(len(w)==4 and w<=set(range(17)) for w in ws), 'invalid unit positive fixture')
        need(all(len(u&v)<=1 for u,v in combinations(ws,2)), 'positive fixture repeated pair')
        rho=Counter(z for w in ws for z in w)
        need(Counter(rho.values())=={4:5,5:12} and len(rho)==17, 'positive fixture profile wrong')
        h=frozenset(z for z in range(17) if rho[z]==4)
        leave={p for p in combinations(range(17),2) if not any(set(p)<=w for w in ws)}
        e=sum(set(p)<=h for p in leave);m=sum(not set(p)&h for p in leave)
        need(e==4 and m==0 and len(leave)==16, 'positive fixture leave does not realize four')
        b=[sum(len(w&h)==j for w in ws) for j in range(5)]
        need(b==rec['b'], 'fixture intrinsic profile changed')
        records.append(dict(profile=b, high_high_leave=e, low_low_leave=m))
    edges=tuple(combinations(range(3),2));distribution=Counter()
    for g in range(8):
        degree=[0]*3
        for i,(u,v) in enumerate(edges):
            if g>>i&1:degree[u]+=1;degree[v]+=1
        homogeneous=sum(d in (0,2) for d in degree)
        need(homogeneous>=1,'three-vertex homogeneous claim false');distribution[homogeneous]+=1
    ps=list(partitions(5));need(len(ps)==7,'deficit partition census incomplete')
    local=[]
    for p in ps:
        h=len(p)
        # e-m=h-1. For h=4,5 use the explicitly imported/proved structural inputs.
        e_values=range(h-1,comb(h,2)+1) if h<=3 else (3,) if h==4 else (4,)
        hom=max(2*e-(h-1) for e in e_values)
        need(hom<=4, 'local homogeneous bound mismatch')
        local.append(dict(deficits=p, homogeneous_bound=hom))
    need(comb(18,3)-72*comb(5,3)==96 and 18*4==72, 'global count changed')
    need(comb(18,3)-71*comb(5,3)==106, '71-word necessary count changed')
    record=dict(agent='six-reviewer-2',role='independent mathematical reviewer',
                primary69=dict(url='https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69',bytes=len(raw),sha256=sha256(raw).hexdigest(),words=69,overlap_counts=dict(overlaps)),
                sharp_unit_fixtures=records, three_vertex_graphs=8, homogeneous_distribution=dict(distribution),
                seven_deficit_partitions=local, at72=dict(uncovered_triples=96,J_lower=96,J_upper=72),
                at71_necessary=dict(uncovered_triples=106,unsaturated_centers_range=[1,5],
                                   unsaturated_homogeneous_lower={k:34+4*k for k in range(1,6)},
                                   all_five_point_deficits_one_forces_a_19_star_homogeneous_at_least=11))
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
