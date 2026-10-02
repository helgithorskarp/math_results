"""Exact marked AA near-regular A9--B12 incidence projection only."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, combinations_with_replacement
from collections import Counter
import json,time,resource,hashlib

parser=ArgumentParser()
parser.add_argument('--work',type=Path,required=True)
OUT=parser.parse_args().work
OUT.mkdir(parents=True,exist_ok=True)
GLOBAL_DEGREES=[8]*3+[9]*3+[10]*3
START=time.monotonic()
PAIRS=list(combinations(range(9),2))
ORBITS=[]
for i in range(3):ORBITS.append(tuple((3*i+t,3*i+(t+1)%3) for t in range(3)))
for i,j in combinations(range(3),2):
    for shift in range(3):ORBITS.append(tuple((3*i+t,3*j+(t+shift)%3) for t in range(3)))

def local(word):
    rows=[0]*9
    for k,orbit in enumerate(ORBITS):
        if word>>k&1:
            for u,v in orbit:rows[u]|=1<<v;rows[v]|=1<<u
    return rows

def translate(mask,phase):
    return sum(((mask>>(3*i+t))&1)<<(3*i+(t+phase)%3) for i in range(3) for t in range(3))

types=[]
for subset in combinations(range(9),4):
    mask=sum(1<<a for a in subset)
    cols=[translate(mask,t) for t in range(3)]
    if mask!=min(cols):continue
    weights=[((mask>>(3*i))&7).bit_count() for i in range(3)]
    overlaps=[sum((c>>u&1)*(c>>v&1) for c in cols) for u,v in PAIRS]
    types.append(dict(mask=mask,columns=cols,weights=weights,overlaps=overlaps))
if len(types)!=42:raise ValueError('Complete126/3 column orbit types')

projection=json.loads((OUT/'projection.json').read_text())
H_WORDS=sorted(map(int,projection['canonical_groups']))
results=[];total=Counter()
for word in H_WORDS:
    rows=local(word);margins=[GLOBAL_DEGREES[3*i]-1-rows[3*i].bit_count() for i in range(3)]
    caps=[(2 if rows[u]>>v&1 else GLOBAL_DEGREES[u]+GLOBAL_DEGREES[v]-15)-(rows[u]&rows[v]).bit_count() for u,v in PAIRS]
    records=[];counts=Counter()
    for choices in combinations_with_replacement(range(42),4):
        counts['complete_column_multisets']+=1
        if time.monotonic()-START>25:raise RuntimeError('Incomplete incidence projection; no exclusion')
        if any(sum(types[k]['weights'][i] for k in choices)!=margins[i] for i in range(3)):continue
        counts['row_margin_matches']+=1
        intersections=[sum(types[k]['overlaps'][p] for k in choices) for p in range(36)]
        if any(n>bound for n,bound in zip(intersections,caps)):continue
        columns=[c for k in choices for c in types[k]['columns']]
        X=[sum((c>>a&1)<<b for b,c in enumerate(columns)) for a in range(9)]
        if [r.bit_count() for r in X]!=[GLOBAL_DEGREES[a]-1-r.bit_count() for a,r in enumerate(rows)]:raise ValueError('Literal margin disagreement')
        for u,v in PAIRS:
            red=1+(rows[u]&rows[v]).bit_count()+(X[u]&X[v]).bit_count()
            if rows[u]>>v&1:
                if red>3:raise ValueError('Literal red A cap disagreement')
            else:
                blue=sum(not(rows[u]>>a&1) and not(rows[v]>>a&1) for a in range(9) if a not in [u,v])
                blue+=sum(not(c>>u&1) and not(c>>v&1) for c in columns)
                if blue>6:raise ValueError('Literal blue A cap disagreement')
        counts['all_A_pair_pass']+=1
        records.append(dict(local_word=word,column_type_indices=list(choices),columns=columns,X=X,intersections=intersections))
    total.update(counts)
    results.append(dict(word=word,margins=margins,counts=dict(counts),records=records))
summary=dict(status='COMPLETE_EXACT_A_INCIDENCE_PROJECTION',agent='six-books-2',role='researcher',
             scope='Near-regular C3 type3^7 1 E99 root9 AA placement, marked A degrees8/9/10, all B9. Necessary incidence projection only.',
             column_types=len(types),local_words=H_WORDS,counts=dict(total),by_word=[{k:v for k,v in r.items() if k!='records'} for r in results],
             seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1)
(OUT/'incidence-records.json').write_text(json.dumps(dict(column_types=types,results=results),indent=2)+'\n')
(OUT/'incidence-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
