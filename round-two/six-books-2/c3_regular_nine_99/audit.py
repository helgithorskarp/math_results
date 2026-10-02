"""Independent necessary-projection check: literal pairs, load DP, pair joins."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, product, permutations
from collections import Counter, defaultdict
import json,time,resource,hashlib

parser=ArgumentParser()
parser.add_argument('--work',type=Path,required=True)
OUT=parser.parse_args().work
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
    if sum(map(len,rows))!=24:continue
    counts['edge_count_words']+=1
    if sorted(map(len,rows))!=[2]*3+[3]*6:continue
    counts['degree_words']+=1
    margins=[8-len(r) for r in rows];bounds=[]
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
for representative in [78,540,1616]:
    original=local(representative);images=set()
    for order in permutations(range(3)):
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
if sorted(set.union(*groups.values()))!=survivors or sum(map(len,groups.values()))!=len(survivors):
    raise ValueError('Full A transport coverage/partition differs')
for rep,images in groups.items():
    if images!=set(source['canonical_groups'][str(rep)]):raise ValueError('Entire representative group differs')

def translate(mask,shift):
    return sum(1<<(3*i+(t+shift)%3) for i in range(3) for t in range(3) if mask>>(3*i+t)&1)

masks=[mask for mask in range(512) if mask.bit_count()==4 and mask==min(translate(mask,s) for s in range(3))]
if len(masks)!=42:raise ValueError('Independent column types')
cols={mask:[translate(mask,s) for s in range(3)] for mask in masks}
weights={mask:tuple(((mask>>(3*i))&7).bit_count() for i in range(3)) for mask in masks}
overlaps={mask:tuple(sum((c>>u&1)*(c>>v&1) for c in cols[mask]) for u,v in PAIRS) for mask in masks}
half=defaultdict(list)
for left in range(42):
    for right in range(left,42):
        a,b=masks[left],masks[right]
        w=tuple(weights[a][i]+weights[b][i] for i in range(3))
        half[w].append((left,right,tuple(overlaps[a][p]+overlaps[b][p] for p in range(36))))

frames=[];by_word=[]
primary_data=json.loads((OUT/'incidence-records.json').read_text())
primary_incidences=primary_data['results']
# Bind every primary column field to the independent definition, not just seeds.
canonical=lambda value:json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)
observed_types=primary_data['column_types']
if len(observed_types)!=42:raise ValueError('Complete primary column type table')
for entry in observed_types:
    mask=entry['mask']
    if type(mask) is not int or mask not in masks:raise ValueError('Primary column mask domain')
    expected=dict(mask=mask,columns=cols[mask],weights=list(weights[mask]),overlaps=list(overlaps[mask]))
    if canonical(entry)!=canonical(expected):raise ValueError('Entire typed primary column fields differ')
if sorted(entry['mask'] for entry in observed_types)!=masks:raise ValueError('Primary column type coverage')
for word in [78,540,1616]:
    H=local(word);target=tuple(8-len(H[3*i]) for i in range(3))
    bounds=[]
    for u,v in PAIRS:
        if v in H[u]:bounds.append(3-1-len(H[u]&H[v]))
        else:
            known=sum(w not in H[u] and w not in H[v] for w in range(9) if w not in [u,v])
            bounds.append(6-known-(12-(8-len(H[u]))-(8-len(H[v]))))
    quads=[];matches=0
    for weight,pairs in half.items():
        residual=tuple(target[i]-weight[i] for i in range(3))
        for a,b,left_overlap in pairs:
            for c,d,right_overlap in half.get(residual,[]):
                if b>c:continue
                matches+=1
                if any(left_overlap[p]+right_overlap[p]>bounds[p] for p in range(36)):continue
                quad=(masks[a],masks[b],masks[c],masks[d]);quads.append(quad)
    prim=next(r for r in primary_incidences if r['word']==word)
    for record in prim['records']:
        indices=record['column_type_indices']
        if type(indices) is not list or len(indices)!=4 or any(type(k) is not int or not 0<=k<42 for k in indices):
            raise ValueError('Primary column type indices')
        primary_columns=[c for k in indices for c in observed_types[k]['columns']]
        primary_X=[sum((column>>a&1)<<b for b,column in enumerate(primary_columns)) for a in range(9)]
        primary_intersections=[sum((c>>u&1)*(c>>v&1) for c in primary_columns) for u,v in PAIRS]
        entire=dict(local_word=word,column_type_indices=indices,columns=primary_columns,X=primary_X,intersections=primary_intersections)
        if canonical(record)!=canonical(entire):raise ValueError('Entire typed primary incidence fields differ')
    expected_quads=sorted(tuple(sorted(record['columns'][::3])) for record in prim['records'])
    if sorted(quads)!=expected_quads:raise ValueError('ENTIRE independent incidence set differs')
    by_word.append(dict(word=word,row_margin_matches=matches,templates=len(quads)))
    for quad in sorted(quads):
        columns=[c for mask in quad for c in cols[mask]]
        X=[sum((column>>a&1)<<b for b,column in enumerate(columns)) for a in range(9)]
        frames.append(dict(word=word,column_seeds=list(quad),columns=columns,X=X))

frame_text=''.join(' '.join(map(str,[frame['word'],*frame['X']]))+'\n' for frame in frames)
(OUT/'frames.txt').write_text(frame_text)
(OUT/'frames.json').write_text(json.dumps(frames,indent=2)+'\n')
summary=dict(status='COMPLETE_INDEPENDENT_PROJECTION_AND_INCIDENCE_AUDIT',agent='six-books-2',role='researcher',
             counts=dict(counts),representative_groups={str(k):len(v) for k,v in groups.items()},
             column_types=len(masks),by_word=by_word,templates=len(frames),
             entire_local_sets_equal=True,entire_transport_groups_equal=True,entire_incidence_sets_equal=True,
             frames_sha256=hashlib.sha256(frame_text.encode()).hexdigest(),
             seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             trust='Same-author distinct pair-predicate/load-DP/orbit-expansion/pair-join check; written bridges unformalized. No host completion verdict.')
(OUT/'audit-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
