"""Independent physical row and binary-half star enumeration.

Only the displayed type counts are shared mathematical input. Neither the
producer's census nor its subset routine is imported or read.
"""
import collections
import itertools
import math
from functools import lru_cache

COUNTS = (0,0,3,1,2,3,0,2,2,1,1,1,1,1,0)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def configuration():
    types=tuple(m for m in range(1,16) for _ in range(COUNTS[m-1]))
    red=[tuple(x for x,t in enumerate(types) if t & (1<<i)) for i in range(4)]
    require(len(types)==18 and all(len(r)==9 for r in red), 'Physical degree margins')
    budget=[72-sum(10-sum(bool(types[x] & (1<<j)) for j in range(4)) for x in row) for row in red]
    require(budget==[2,2,1,1], 'Physical mixed budgets')
    return list(COUNTS),types,red,budget

def physical_templates(types,red,budget):
    options=[]
    for i,d in enumerate(budget):
        blue=tuple(x for x in range(18) if x not in red[i]);row_options=[]
        for alpha in range(1,d+1,2):
            for rpoints in itertools.combinations_with_replacement(red[i],alpha):
                for bpoints in itertools.combinations_with_replacement(blue,d-alpha):
                    row=[0]*18
                    for x in rpoints+bpoints:row[x]+=1
                    transport=tuple(sum(row[x] for x in red[j]) for j in range(4))
                    row_options.append((tuple(row),transport))
        require(len({row for row,_ in row_options})==len(row_options),'duplicate physical row')
        options.append(row_options)
    census=0;surviving=0;found=collections.Counter()
    for chosen in itertools.product(*options):
        census+=1
        walk=[rec[1] for rec in chosen]
        if any(walk[i][j]!=walk[j][i] for i in range(4) for j in range(i)):continue
        surviving+=1
        rows=[rec[0] for rec in chosen]
        column=[sum(rows[i][x]*(4**i) for i in range(4)) for x in range(18)]
        cell=collections.defaultdict(list)
        for x,t in enumerate(types):cell[t].append(column[x])
        template=tuple(v for t in sorted(cell) for v in sorted(cell[t]))
        found[template]+=1
    require(census==math.prod(len(r) for r in options),'incomplete physical matrix census')
    return sorted(found),{'physical_row_options':[len(r) for r in options],'physical_matrices':census,
                          'symmetric_physical_matrices':surviving,'orbit_sizes':[found[r] for r in sorted(found)]}

def half(vertices,types):
    result=[]
    for word in range(1<<len(vertices)):
        points=[v for k,v in enumerate(vertices) if word&(1<<k)]
        result.append((sum(1<<v for v in points),len(points),
                       tuple(sum(bool(types[v]&(1<<i)) for v in points) for i in range(4))))
    return result

def physical_domains(types,budget):
    rows=collections.defaultdict(list);examined=0
    for x,t in enumerate(types):
        right=collections.defaultdict(list)
        for rec in half([v for v in range(9,18) if v!=x],types):right[rec[1]].append(rec)
        size=10-sum(bool(t&(1<<i)) for i in range(4))
        for lm,ln,lc in half([v for v in range(9) if v!=x],types):
            for rm,rn,rc in right[size-ln]:
                examined+=1
                deficits=[(3 if t&(1<<i) else 5)-(lc[i]+rc[i]) for i in range(4)]
                valid=True
                for i,d in enumerate(deficits):
                    red=bool(t&(1<<i))
                    # A positive odd red row sum is1, or3 only at budget3.
                    largest=(3 if budget[i]==3 else 1) if red else budget[i]-1
                    if d<0 or d>largest:valid=False;break
                if not valid:continue
                code=sum(d*(4**i) for i,d in enumerate(deficits))
                rows[(x,code)].append(lm|rm)
    require(all(len(row)==len(set(row)) for row in rows.values()),'duplicate physical neighbor subset')
    return {k:sorted(v) for k,v in rows.items()},examined


@lru_cache(maxsize=1)
def build():
    counts,types,low_rows,row_budgets=configuration()
    matrices,census=physical_templates(types,low_rows,row_budgets)
    domains,raw_stars=physical_domains(types,row_budgets)
    require(len(matrices)==40 and raw_stars==422994
            and sum(len(v) for v in domains.values())==14085, 'Physical census mismatch')
    return counts,types,low_rows,row_budgets,matrices,census,domains,raw_stars
