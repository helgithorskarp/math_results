"""105-edge C3(3^7 1) root census with degree-marked completeness.

Exploration first: full completion and an independent coverage checker are
needed before this root census becomes an exclusion theorem.
"""
import argparse
from itertools import combinations, permutations, product
import json
from pathlib import Path
import resource
import time

PAIRS = tuple(combinations(range(9),2))
CYCLE_PAIRS = ((0,1),(0,2),(1,2))
SUBSETS = tuple(tuple(s) for n in range(3,10) for s in combinations(range(9),n))
CASES = (
    ('A3',(3,0,0,0,0,0,0)),
    ('A2A1',(2,1,0,0,0,0,0)),
    ('A2B1',(2,0,0,1,0,0,0)),
    ('A1B2',(1,0,0,2,0,0,0)),
    ('A1A1A1',(1,1,1,0,0,0,0)),
    ('A1A1B1',(1,1,0,1,0,0,0)),
    ('A1B1B1',(1,0,0,1,1,0,0)),
)


def require(value,message):
    if not value:
        raise RuntimeError(message)


def local_graph(code):
    rows = [set() for _ in range(9)]
    for u,v in PAIRS:
        i,j = u//3,v//3
        bit = i if i==j else 3+3*CYCLE_PAIRS.index((i,j))+(v-u)%3
        if code>>bit&1:
            rows[u].add(v)
            rows[v].add(u)
    return rows


def encode(rows):
    bits = [int(3*i+1 in rows[3*i]) for i in range(3)]
    bits += [int(3*j+t in rows[3*i]) for i,j in CYCLE_PAIRS for t in range(3)]
    return sum(bit<<k for k,bit in enumerate(bits))


def canonical(rows,cycle_degrees):
    best = 4096
    for perm in permutations(range(3)):
        if any(cycle_degrees[i]!=cycle_degrees[perm[i]] for i in range(3)):
            continue
        for shifts in product(range(3),repeat=3):
            for unit in (1,2):
                relabel = {3*i+t:3*perm[i]+(unit*t+shifts[i])%3 for i in range(3) for t in range(3)}
                changed = [set() for _ in range(9)]
                for old,row in enumerate(rows):
                    changed[relabel[old]] = {relabel[v] for v in row}
                best = min(best,encode(changed))
    return best


def enumerate_roots():
    out = []
    for name,deficits in CASES:
        degree_cycles = tuple(10-d for d in deficits)
        full = [degree_cycles[u//3] for u in range(9)]
        lower_X = 15-3*sum(deficits[:3])
        initial,triples,all_subsets = {},{},{}
        for code in range(4096):
            rows = local_graph(code)
            degrees = list(map(len,rows))
            X = sum(degrees)//2
            if max(degrees)>3 or not lower_X<=X<=12:
                continue
            demands = [full[u]-1-degrees[u] for u in range(9)]
            caps = {(u,v):(2 if v in rows[u] else full[u]+full[v]-15)-len(rows[u]&rows[v]) for u,v in PAIRS}
            if any(cap<max(0,demands[u]+demands[v]-12) for (u,v),cap in caps.items()):
                continue
            representative = canonical(rows,degree_cycles[:3])
            initial.setdefault(str(representative),[]).append(code)
            triple_good, subset_good = True, True
            for points in SUBSETS:
                q,r = divmod(sum(demands[u] for u in points),12)
                lower = 12*q*(q-1)//2+r*q
                upper = sum(caps[u,v] for u,v in combinations(points,2))
                if lower>upper:
                    subset_good = False
                    if len(points)==3:
                        triple_good = False
                    break
            if triple_good:
                triples.setdefault(str(representative),[]).append(code)
            if subset_good:
                all_subsets.setdefault(str(representative),[]).append(code)
        record = dict(name=name,deficits=list(deficits),degree_cycles=list(degree_cycles),
                      minimum_local_edges=lower_X,pair_raw=sum(map(len,initial.values())),
                      pair_classes=len(initial),pair_groups=initial,
                      triple_raw=sum(map(len,triples.values())),triple_classes=len(triples),
                      triple_groups=triples,all_subsets_raw=sum(map(len,all_subsets.values())),
                      all_subsets_classes=len(all_subsets),all_subsets_groups=all_subsets)
        out.append(record)
        print(json.dumps({k:v for k,v in record.items() if not k.endswith('_groups')}),flush=True)
    return out


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    start = time.monotonic()
    result = enumerate_roots()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('seconds',time.monotonic()-start,'RSS KiB',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,flush=True)
