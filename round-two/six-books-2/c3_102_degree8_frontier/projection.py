"""Exact marked necessary A9 projections for the E102 degree8^3,9^10,10^9 C3 cohort."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, permutations, product
from collections import Counter
import json, time, resource

START = time.monotonic()
parser=ArgumentParser()
parser.add_argument('--work',type=Path,required=True)
parser.add_argument('--mode',choices=['P1_81010','P1_999','P1_9910','P1_8910'],required=True)
args=parser.parse_args()
OUT=args.work
mode=args.mode
DG={'P1_81010':(8,10,10),'P1_999':(9,9,9),'P1_9910':(9,9,10),'P1_8910':(8,9,10)}[mode]
GLOBAL_DEGREES=[d for d in DG for _ in range(3)]
H_EDGES=12
PERMUTATIONS=[p for p in permutations(range(3)) if all(DG[i]==DG[p[i]] for i in range(3))]
OUT.mkdir(parents=True,exist_ok=True)

ORBITS = []
for i in range(3):
    ORBITS.append(tuple((3*i+t,3*i+(t+1)%3) for t in range(3)))
for i,j in combinations(range(3),2):
    for shift in range(3):
        ORBITS.append(tuple((3*i+t,3*j+(t+shift)%3) for t in range(3)))
EDGES = [tuple(sorted(e)) for orbit in ORBITS for e in orbit]
if len(ORBITS)!=12 or len(set(EDGES))!=36:
    raise ValueError('Complete A edge-orbit partition')

def graph(word):
    rows=[0]*9
    for index, orbit in enumerate(ORBITS):
        if word>>index&1:
            for u,v in orbit:
                rows[u]|=1<<v;rows[v]|=1<<u
    return rows

def capacities(rows):
    row_sums=[GLOBAL_DEGREES[u]-1-r.bit_count() for u,r in enumerate(rows)]
    bounds=[]
    for u,v in combinations(range(9),2):
        common=(rows[u]&rows[v]).bit_count()
        bound=(2 if rows[u]>>v&1 else GLOBAL_DEGREES[u]+GLOBAL_DEGREES[v]-15)-common
        if bound<max(0,row_sums[u]+row_sums[v]-12):return None
        bounds.append(bound)
    return row_sums,bounds

PAIRS=list(combinations(range(9),2))
SUBSETS=[]
for size in range(3,10):
    for subset in combinations(range(9),size):
        indices=set(subset)
        pair_positions=[k for k,(u,v) in enumerate(PAIRS) if u in indices and v in indices]
        SUBSETS.append((subset,pair_positions))

def subset_screen(row_sums,bounds):
    for subset,pair_positions in SUBSETS:
        total=sum(row_sums[u] for u in subset)
        q,r=divmod(total,12)
        needed=12*q*(q-1)//2+r*q
        if sum(bounds[k] for k in pair_positions)<needed:return False
    return True

def transformed_word(rows,permutation,phases,multiplier):
    image=[3*permutation[i]+(multiplier*t+phases[i])%3 for i in range(3) for t in range(3)]
    moved=[0]*9
    for u,v in PAIRS:
        if rows[u]>>v&1:
            moved[image[u]]|=1<<image[v];moved[image[v]]|=1<<image[u]
    bits=[]
    for orbit in ORBITS:
        values=[moved[u]>>v&1 for u,v in orbit]
        if len(set(values))!=1:raise ValueError('Relabeling must preserve C3 invariance')
        bits.append(values[0])
    return sum(bit<<index for index,bit in enumerate(bits))

def canonical(rows):
    # Only permutations preserving global degree marks plus phase shifts/common inversion.
    return min(transformed_word(rows,perm,phases,multiplier)
               for perm in PERMUTATIONS for phases in product(range(3),repeat=3) for multiplier in [1,2])

counts=Counter();groups={};records=[]
for slots in combinations(range(12),H_EDGES//3):
    if time.monotonic()-START>25:raise RuntimeError('Incomplete projection; preserve files, no exclusion')
    counts['edge_count_templates']+=1
    word=sum(1<<i for i in slots);rows=graph(word)
    degrees=[r.bit_count() for r in rows]
    if max(degrees)>3:continue
    counts['degree_templates']+=1
    cap=capacities(rows)
    if cap is None:continue
    counts['pair_templates']+=1
    if not subset_screen(*cap):continue
    counts['subset_templates']+=1
    c=canonical(rows);groups.setdefault(c,[]).append(word)
    records.append(dict(word=word,canonical=c,degrees=degrees,row_sums=cap[0],pair_bounds=cap[1]))
counts['subset_templates']+=0
result=dict(status='COMPLETE_EXACT_NECESSARY_A9_PROJECTION',agent='six-books-2',role='researcher',
            scope='E102 C3 type3^7 1 fixed-root9 degree8^3,9^10,10^9. Marked necessary A projection ONLY.', mode=mode,H_edges=H_EDGES,allowed_A_orbit_permutations=PERMUTATIONS,
            global_A_degrees=GLOBAL_DEGREES,counts=dict(counts),canonical_groups=groups,records=records,
            seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            threads=1,source='projection.py',
            trust='Exact necessary projection; audit not yet run; written bridges unformalized.')
(OUT/'projection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
