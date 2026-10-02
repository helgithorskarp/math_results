"""Independent necessary-projection check: literal pairs, load DP, pair joins."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, product, permutations
from collections import Counter, defaultdict
import json,time,resource,hashlib

parser=ArgumentParser()
parser.add_argument('--work',type=Path,required=True)
parser.add_argument('--mode',choices=['A9910','A999'],required=True)
args=parser.parse_args();OUT=args.work;mode=args.mode
DG={'A9910':(9,9,10),'A999':(9,9,9)}[mode]
GLOBAL_DEGREES=[d for d in DG for _ in range(3)]
H_EDGES=12
ALLOWED=[p for p in permutations(range(3)) if all(DG[i]==DG[p[i]] for i in range(3))]
OUT.mkdir(parents=True,exist_ok=True)
START=time.monotonic()
PAIRS=list(combinations(range(9),2))

def local(word):
    rows=[]
    for u in range(9):
        row=set();i,t=divmod(u,3)
        for v in range(9):
            if u==v:continue
            j,s=divmod(v,3)
            if i==j:bit=i
            else:
                first,second=min(i,j),max(i,j)
                base={(0,1):3,(0,2):6,(1,2):9}[first,second]
                shift=(s-t)%3 if i<j else (t-s)%3
                bit=base+shift
            if word>>bit&1:row.add(v)
        rows.append(row)
    return rows

# Independent finite DP: twelve labeled column loads, each between0 and|T|.
dp_by_size={}
for size in range(3,10):
    dp={0:0}
    for _ in range(12):
        new={}
        for total,cost in dp.items():
            for load in range(size+1):
                key=total+load;value=cost+load*(load-1)//2
                new[key]=min(new.get(key,10**9),value)
        dp=new
    dp_by_size[size]=dp
SUBSETS=[]
for size in range(3,10):
    for subset in combinations(range(9),size):
        pair_indices=[k for k,(u,v) in enumerate(PAIRS) if u in subset and v in subset]
        SUBSETS.append((subset,pair_indices))

survivors=[];counts=Counter()
for word in range(4096):
    rows=local(word)
    if sum(map(len,rows))!=2*H_EDGES:continue
    counts['edge_count_words']+=1
    if max(map(len,rows))>3:continue
    counts['degree_words']+=1
    margins=[GLOBAL_DEGREES[u]-1-len(r) for u,r in enumerate(rows)];bounds=[]
    good=True
    for u,v in PAIRS:
        if v in rows[u]:bound=3-1-len(rows[u]&rows[v])
        else:
            blue_A=sum(w not in rows[u] and w not in rows[v] for w in range(9) if w not in [u,v])
            bound=6-blue_A-(12-margins[u]-margins[v])
        bounds.append(bound)
        if bound<max(0,margins[u]+margins[v]-12):good=False
    if not good:continue
    counts['pair_words']+=1
    if any(sum(bounds[k] for k in indices)<dp_by_size[len(subset)][sum(margins[u] for u in subset)] for subset,indices in SUBSETS):continue
    counts['subset_words']+=1;survivors.append(word)
    if time.monotonic()-START>25:raise RuntimeError('Incomplete audit, no exclusion')

source=json.loads((OUT/'projection.json').read_text())
expected_words=sorted(r['word'] for r in source['records'])
if survivors!=expected_words:raise ValueError('ENTIRE independent A word set differs')

# Expand each proposed representative's valid relabeling orbit, rather than
# canonizing each input word as in the primary generator.
groups={}
for representative in sorted(map(int,source['canonical_groups'])):
    original=local(representative);images=set()
    for order in ALLOWED:
        for phases in product(range(3),repeat=3):
            for multiplier in [1,2]:
                mapping={u:3*order[u//3]+(multiplier*(u%3)+phases[u//3])%3 for u in range(9)}
                moved=[set() for _ in range(9)]
                for u in range(9):moved[mapping[u]]={mapping[v] for v in original[u]}
                value=0
                for i in range(3):
                    if 3*i+1 in moved[3*i]:value|=1<<i
                for i,j,base in [(0,1,3),(0,2,6),(1,2,9)]:
                    for shift in range(3):
                        if 3*j+shift in moved[3*i]:value|=1<<(base+shift)
                if local(value)!=moved:raise ValueError('Literal relabeling/C3 decoding differs')
                images.add(value)
    groups[representative]=images
if sorted(set().union(*groups.values()))!=survivors or sum(map(len,groups.values()))!=len(survivors):
    raise ValueError('Full A transport coverage/partition differs')
for rep,images in groups.items():
    if images!=set(source['canonical_groups'][str(rep)]):raise ValueError('Entire representative group differs')

# Bind all semantic local projection fields to this set-defined audit.
for record in source['records']:
    word=record['word'];H=local(word)
    margins=[GLOBAL_DEGREES[u]-1-len(H[u]) for u in range(9)]
    bounds=[]
    for u,v in PAIRS:
        if v in H[u]:bounds.append(2-len(H[u]&H[v]))
        else:
            blue_A=sum(w not in H[u] and w not in H[v] for w in range(9) if w not in [u,v])
            bounds.append(6-blue_A-(12-margins[u]-margins[v]))
    canonical=min(rep for rep,images in groups.items() if word in images)
    expected=dict(word=word,canonical=canonical,degrees=list(map(len,H)),row_sums=margins,pair_bounds=bounds)
    if json.dumps(record,sort_keys=True,separators=(',',':'))!=json.dumps(expected,sort_keys=True,separators=(',',':')):
        raise ValueError('Entire projection record fields differ')
counts['subset_words']+=0
summary=dict(status='COMPLETE_DISTINCT_MARKED_A_PROJECTION_AUDIT',agent='six-books-2',role='researcher',
             mode=mode,counts=dict(counts),groups={str(k):len(v) for k,v in groups.items()},
             whole_survivor_set_equal=True,whole_transport_groups_equal=True,whole_semantic_fields_equal=True,
             seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             trust='Same-author set predicates, load DP and inverse orbit expansion; ordinary bridges unformalized; no peer review.')
(OUT/'projection-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
