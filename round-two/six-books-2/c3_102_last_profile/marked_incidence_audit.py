"""Set column domains and marked two-pair/slack-target joins, no producer import."""
from argparse import ArgumentParser
from collections import defaultdict
from itertools import combinations, combinations_with_replacement
from math import comb
from pathlib import Path
import hashlib,json,resource,time
from cases import CASES

START=time.monotonic()
parser=ArgumentParser();parser.add_argument('--work',type=Path,required=True)
parser.add_argument('--case',choices=sorted(CASES),required=True)
args=parser.parse_args();OUT=args.work;C=CASES[args.case]
DG=[d for d in C['A'] for _ in range(3)];PAIRS=list(combinations(range(9),2))
marks=list(zip(C['B'],C['alpha']))

def guard():
    if time.monotonic()-START>25:
        raise RuntimeError('INCOMPLETE marked slack-target join; no exclusion')

def encode(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)

def local(word):
    rows=[]
    for u in range(9):
        i,t=divmod(u,3);row=set()
        for v in range(9):
            if v==u:
                continue
            j,s=divmod(v,3)
            bit=i if i==j else {(0,1):3,(0,2):6,(1,2):9}[min(i,j),max(i,j)]+((s-t)%3 if i<j else (t-s)%3)
            if word>>bit&1:
                row.add(v)
        rows.append(row)
    return rows

def rotated(subset,t):
    return {3*(u//3)+(u%3+t)%3 for u in subset}

types={}
for rank in sorted(set(C['alpha'])):
    entries=[]
    for mask in range(512):
        if mask.bit_count()!=rank:
            continue
        subset={u for u in range(9) if mask>>u&1}
        sets=[rotated(subset,t) for t in range(3)]
        cols=[sum(1<<u for u in s) for s in sets]
        if mask!=min(cols):
            continue
        entries.append(dict(mask=mask,columns=cols,weights=[sum(u in s for s in sets) for u in [0,3,6]],
                            overlaps=[sum(u in s and v in s for s in sets) for u,v in PAIRS]))
    types[rank]=entries
primary=json.loads((OUT/'incidence-records.json').read_text())
if primary['case']!=args.case or encode({str(k):v for k,v in types.items()})!=encode(primary['column_types']):
    raise ValueError('Entire independent marked column domain differs')
unseen=set(PAIRS);orbits=[]
while unseen:
    u,v=min(unseen)
    pairs={tuple(sorted((3*(u//3)+(u%3+t)%3,3*(v//3)+(v%3+t)%3))) for t in range(3)}
    if len(pairs)!=3 or not pairs<=unseen:
        raise ValueError('Literal A-pair orbit partition')
    orbits.append(sorted(PAIRS.index(p) for p in pairs));unseen-=pairs
positions=[orbit[0] for orbit in orbits]
if len(positions)!=12:
    raise ValueError('Pair orbit completeness')
vectors={}
for rank,entries in types.items():
    vectors[rank]=[]
    for entry in entries:
        if any(len({entry['overlaps'][p] for p in orbit})!=1 for orbit in orbits):
            raise ValueError('Nonconstant literal column pair orbit')
        vectors[rank].append(tuple(entry['weights']+[entry['overlaps'][p] for p in positions]))
domain_sizes=[len(types[rank]) for rank in C['alpha']]

def canonical_indices(indices):
    return not any(marks[i]==marks[j] and indices[i]>indices[j] for i in range(4) for j in range(i+1,4))

left=defaultdict(list);weight_left=defaultdict(list)
for a in range(domain_sizes[0]):
    for b in range(domain_sizes[1]):
        if marks[0]==marks[1] and a>b:
            continue
        value=tuple(x+y for x,y in zip(vectors[C['alpha'][0]][a],vectors[C['alpha'][1]][b]))
        left[value].append((a,b));weight_left[value[:3]].append((a,b))
choice_count=1
for mark in set(marks):
    slots=[i for i,m in enumerate(marks) if m==mark]
    choice_count*=comb(domain_sizes[slots[0]]+len(slots)-1,len(slots))
projection=json.loads((OUT/'projection.json').read_text())
if projection['mode']!=C['projection'] or projection['global_A_degrees']!=DG:
    raise ValueError('Marked projection prerequisite differs')
words=sorted(map(int,projection['canonical_groups']))
if [r['word'] for r in primary['results']]!=words:
    raise ValueError('Complete incidence word coverage differs')
frames=[];by_word=[]
for word in words:
    H=local(word);margins=[DG[u]-1-len(H[u]) for u in [0,3,6]]
    caps=[]
    for u,v in PAIRS:
        if v in H[u]:
            cap=2-len(H[u]&H[v])
        else:
            blue_A=sum(w not in H[u] and w not in H[v] for w in range(9) if w not in [u,v])
            cap=6-blue_A-(12-(DG[u]-1-len(H[u]))-(DG[v]-1-len(H[v])))
        caps.append(cap)
    overlap=3*sum(rank*(rank-1)//2 for rank in C['alpha'])
    units,remainder=divmod(sum(caps)-overlap,3)
    if remainder or units>3:
        raise ValueError('Changed marked pair-deficit domain')
    targets=[]
    if units>=0:
        for slots in combinations_with_replacement(range(12),units):
            slack=[0]*12
            for i in slots:
                slack[i]+=1
            targets.append(tuple(margins+[caps[p]-slack[i] for i,p in enumerate(positions)]))
    records=[];margin_matches=0
    for c in range(domain_sizes[2]):
        vc=vectors[C['alpha'][2]][c]
        for d in range(domain_sizes[3]):
            if marks[2]==marks[3] and c>d:
                continue
            vd=vectors[C['alpha'][3]][d]
            weight_key=tuple(x-y-z for x,y,z in zip(margins,vc[:3],vd[:3]))
            margin_matches+=sum(canonical_indices((a,b,c,d)) for a,b in weight_left.get(weight_key,[]))
            for goal in targets:
                key=tuple(x-y-z for x,y,z in zip(goal,vc,vd))
                for a,b in left.get(key,[]):
                    if not canonical_indices((a,b,c,d)):
                        continue
                    chosen=[types[rank][index] for rank,index in zip(C['alpha'],(a,b,c,d))]
                    cols=[col for entry in chosen for col in entry['columns']]
                    X=[sum((col>>u&1)<<v for v,col in enumerate(cols)) for u in range(9)]
                    records.append(dict(word=word,column_seeds=[e['mask'] for e in chosen],columns=cols,X=X))
            guard()
    records.sort(key=lambda r:tuple(r['column_seeds']))
    expected=next(r for r in primary['results'] if r['word']==word)
    if encode(records)!=encode(sorted(expected['records'],key=lambda r:tuple(r['column_seeds']))):
        raise ValueError('Entire typed marked incidence sets differ')
    expected_counts=dict(complete_column_choices=choice_count,row_margin_matches=margin_matches,A_pair_matches=len(records))
    if encode(expected['counts'])!=encode(expected_counts) or expected['margins']!=margins or expected['capacity']!=sum(caps) or expected['marked_overlap']!=overlap:
        raise ValueError('Whole marked incidence count/margin/capacity fields differ')
    frames.extend(records)
    by_word.append(dict(word=word,slack_units=units,slack_targets=len(targets),canonical_column_choices=choice_count,
                        row_margin_matches=margin_matches,frames=len(records)))
frames.sort(key=lambda r:(r['word'],tuple(r['column_seeds'])))
text=''.join(' '.join(map(str,[f['word'],*f['X']]))+'\n' for f in frames)
if text!=(OUT/'frames.txt').read_text() or encode(frames)!=encode(json.loads((OUT/'frames.json').read_text())):
    raise ValueError('Entire marked native input differs')
result=dict(status='COMPLETE_DISTINCT_P2_MARKED_SLACK_TARGET_JOIN',agent='six-books-2',role='researcher',case=args.case,
            by_word=by_word,frames=len(frames),whole_column_domains_equal=True,whole_typed_incidence_sets_equal=True,
            whole_native_input_equal=True,frames_sha256=hashlib.sha256(text.encode()).hexdigest(),
            seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            trust='Same-author distinct exact set/target algorithm; written completeness bridges unformalized, independent review pending.')
(OUT/'incidence-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
