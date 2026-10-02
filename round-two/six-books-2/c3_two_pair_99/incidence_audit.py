"""Different marked incidence checker: literal subsets and exact keyed two-block joins."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations
from collections import Counter,defaultdict
import hashlib,json,resource,time

parser=ArgumentParser();parser.add_argument('--work',type=Path,required=True)
OUT=parser.parse_args().work;START=time.monotonic()
PAIRS=list(combinations(range(9),2))

def local(word):
    rows=[]
    for u in range(9):
        row=set();i,t=divmod(u,3)
        for v in range(9):
            if v==u:continue
            j,s=divmod(v,3)
            if i==j:bit=i
            else:
                base={(0,1):3,(0,2):6,(1,2):9}[min(i,j),max(i,j)]
                bit=base+((s-t)%3 if i<j else (t-s)%3)
            if word>>bit&1:row.add(v)
        rows.append(row)
    return rows

def rotate(subset,shift):
    return {3*(u//3)+(u%3+shift)%3 for u in subset}

types={}
for size in [3,4,5]:
    entries=[]
    for mask in range(512):
        if mask.bit_count()!=size:continue
        subset={u for u in range(9) if mask>>u&1}
        sets=[rotate(subset,t) for t in range(3)]
        columns=[sum(1<<u for u in s) for s in sets]
        if mask!=min(columns):continue
        weights=tuple(sum(u in s for s in sets) for u in [0,3,6])
        overlaps=tuple(sum(u in s and v in s for s in sets) for u,v in PAIRS)
        entries.append(dict(mask=mask,columns=columns,weights=list(weights),overlaps=list(overlaps)))
    types[size]=entries
primary=json.loads((OUT/'incidence-records.json').read_text())
canonical=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)
if canonical({str(s):types[s] for s in types})!=canonical(primary['column_types']):
    raise ValueError('Entire typed column domains differ')

middle=defaultdict(list);weight_counts=Counter()
for i in range(42):
    for j in range(i,42):
        a,b=types[4][i],types[4][j]
        weights=tuple(a['weights'][k]+b['weights'][k] for k in range(3))
        overlaps=tuple(a['overlaps'][k]+b['overlaps'][k] for k in range(36))
        middle[weights+overlaps].append((a,b));weight_counts[weights]+=1
if sum(weight_counts.values())!=903:raise ValueError('Complete mid pair domain')

# Different reconstruction of all twelve unordered A-pair orbits.
unseen=set(PAIRS);pair_orbits=[]
while unseen:
    u,v=min(unseen);orbit=set()
    for shift in range(3):
        a=3*(u//3)+(u%3+shift)%3;b=3*(v//3)+(v%3+shift)%3
        orbit.add(tuple(sorted((a,b))))
    if len(orbit)!=3 or not orbit<=unseen:raise ValueError('Complete free pair orbits')
    pair_orbits.append({PAIRS.index(p) for p in orbit});unseen-=orbit
if len(pair_orbits)!=12:raise ValueError('Twelve slack targets')

projection=json.loads((OUT/'projection.json').read_text())
frames=[];by_word=[]
for word in sorted(map(int,projection['canonical_groups'])):
    H=local(word);DG=[8]*3+[9]*3+[10]*3;target=[DG[u]-1-len(H[u]) for u in [0,3,6]]
    caps=[]
    for u,v in PAIRS:
        if v in H[u]:caps.append(2-len(H[u]&H[v]))
        else:
            blue_A=sum(w not in H[u] and w not in H[v] for w in range(9) if w not in [u,v])
            caps.append(6-blue_A-(12-(DG[u]-1-len(H[u]))-(DG[v]-1-len(H[v]))))
    if sum(caps)!=78:raise ValueError('Actual marked cap total')
    matches=0;records=[];left_count=0
    for low in types[3]:
        for high in types[5]:
            left_count+=1
            w=tuple(target[k]-low['weights'][k]-high['weights'][k] for k in range(3))
            matches+=weight_counts[w]
            overlap=tuple(caps[k]-low['overlaps'][k]-high['overlaps'][k] for k in range(36))
            for omitted_orbit in pair_orbits:
                tight=tuple(overlap[k]-(1 if k in omitted_orbit else 0) for k in range(36))
                for a,b in middle.get(w+tight,[]):
                    chosen=[low,a,b,high];columns=[c for t in chosen for c in t['columns']]
                    X=[sum((column>>u&1)<<v for v,column in enumerate(columns)) for u in range(9)]
                    records.append(dict(word=word,column_seeds=[t['mask'] for t in chosen],columns=columns,X=X))
            if time.monotonic()-START>25:raise RuntimeError('INCOMPLETE marked pair join; no exclusion')
    expected=next(r for r in primary['results'] if r['word']==word)
    records.sort(key=lambda r:tuple(r['column_seeds']))
    observed=sorted(expected['records'],key=lambda r:tuple(r['column_seeds']))
    if canonical(records)!=canonical(observed):raise ValueError('Entire typed marked incidence sets differ')
    if expected['counts']['row_margin_matches']!=matches:raise ValueError('Complete margin count differs')
    if expected['counts']['complete_column_choices']!=left_count*903:raise ValueError('Complete choice count differs')
    frames.extend(records)
    by_word.append(dict(word=word,left_pairs=left_count,row_margin_matches=matches,templates=len(records)))
frames.sort(key=lambda r:(r['word'],tuple(r['column_seeds'])))
text=''.join(' '.join(map(str,[f['word'],*f['X']]))+'\n' for f in frames)
if text!=(OUT/'frames.txt').read_text() or canonical(frames)!=canonical(json.loads((OUT/'frames.json').read_text())):
    raise ValueError('Entire marked native frame inputs differ')
summary=dict(status='COMPLETE_TWELVE_SLACK_TARGET_JOIN_AUDIT',agent='six-books-2',role='researcher',
             by_word=by_word,frames=len(frames),whole_typed_column_domains_equal=True,
             whole_typed_incidence_sets_equal=True,whole_native_input_equal=True,
             frames_sha256=hashlib.sha256(text.encode()).hexdigest(),
             seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             trust='Two same-author algorithms; written Gram/completeness bridge unformalized; independent peer review pending.')
(OUT/'incidence-audit.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
