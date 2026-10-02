"""Exact MARKED incidence decomposition with total slack six or nine."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, combinations_with_replacement
from collections import Counter
import json,time,hashlib,resource

parser=ArgumentParser()
parser.add_argument('--work',type=Path,required=True)
OUT=parser.parse_args().work
DG=[9]*6+[10]*3
OUT.mkdir(parents=True,exist_ok=True)
START=time.monotonic()
PAIRS=list(combinations(range(9),2))
ORBITS=[tuple((3*i+t,3*i+(t+1)%3) for t in range(3)) for i in range(3)]
ORBITS += [tuple((3*i+t,3*j+(t+s)%3) for t in range(3)) for i,j in combinations(range(3),2) for s in range(3)]

def local(word):
    rows=[0]*9
    for k,orbit in enumerate(ORBITS):
        if word>>k&1:
            for u,v in orbit:rows[u]|=1<<v;rows[v]|=1<<u
    return rows

def translate(mask,phase):
    return sum(((mask>>(3*i+t))&1)<<(3*i+(t+phase)%3) for i in range(3) for t in range(3))

types={}
for size in [4,5]:
    records=[]
    for subset in combinations(range(9),size):
        mask=sum(1<<a for a in subset)
        cols=[translate(mask,t) for t in range(3)]
        if mask!=min(cols):continue
        weights=[((mask>>(3*i))&7).bit_count() for i in range(3)]
        overlaps=[sum((c>>u&1)*(c>>v&1) for c in cols) for u,v in PAIRS]
        records.append(dict(mask=mask,columns=cols,weights=weights,overlaps=overlaps))
    types[size]=sorted(records,key=lambda r:r['mask'])
if [len(types[s]) for s in [4,5]]!=[42,42]:raise ValueError('Complete column orbit types')

projection=json.loads((OUT/'projection.json').read_text())
if projection['mode']!='A9910':raise ValueError('A9/9/10 marked projection required')
H_WORDS=sorted(map(int,projection['canonical_groups']))
results=[];totals=Counter();frames=[]
for word in H_WORDS:
    rows=local(word)
    target=[DG[3*i]-1-rows[3*i].bit_count() for i in range(3)]
    caps=[(2 if rows[u]>>v&1 else DG[u]+DG[v]-15)-(rows[u]&rows[v]).bit_count() for u,v in PAIRS]
    if sum(caps) not in [90,93]:raise ValueError('Changed E102 capacity bridge')
    counts=Counter();records=[]
    for a,b,c in combinations_with_replacement(range(42),3):
        mid1,mid2,mid3=types[4][a],types[4][b],types[4][c]
        partial=[mid1['weights'][i]+mid2['weights'][i]+mid3['weights'][i] for i in range(3)]
        for high in types[5]:
            counts['complete_column_choices']+=1
            if any(partial[i]+high['weights'][i]!=target[i] for i in range(3)):continue
            counts['row_margin_matches']+=1
            chosen=[mid1,mid2,mid3,high]
            overlaps=[sum(t['overlaps'][p] for t in chosen) for p in range(36)]
            if any(o>cap for o,cap in zip(overlaps,caps)):continue
            if sum(cap-o for cap,o in zip(caps,overlaps))!=sum(caps)-84:raise ValueError('Exact total slack')
            counts['A_pair_matches']+=1
            columns=[col for t in chosen for col in t['columns']]
            X=[sum((col>>u&1)<<v for v,col in enumerate(columns)) for u in range(9)]
            if [x.bit_count() for x in X]!=[DG[u]-1-h.bit_count() for u,h in enumerate(rows)]:raise ValueError('Literal row ranks')
            for u,v in PAIRS:
                if rows[u]>>v&1:
                    pages=1+(rows[u]&rows[v]).bit_count()+(X[u]&X[v]).bit_count()
                    if pages>3:raise ValueError('Literal red A cap')
                else:
                    pages=sum(not(rows[u]>>w&1) and not(rows[v]>>w&1) for w in range(9) if w not in [u,v])
                    pages+=sum(not(col>>u&1) and not(col>>v&1) for col in columns)
                    if pages>6:raise ValueError('Literal blue A cap')
            record=dict(word=word,column_seeds=[t['mask'] for t in chosen],columns=columns,X=X)
            records.append(record);frames.append(record)
        if time.monotonic()-START>25:raise RuntimeError('INCOMPLETE E102 incidence guard; no exclusion')
    totals.update(counts)
    results.append(dict(word=word,margins=target,counts=dict(counts),records=records))

frames.sort(key=lambda r:(r['word'],tuple(r['column_seeds'])))
frame_text=''.join(' '.join(map(str,[f['word'],*f['X']]))+'\n' for f in frames)
(OUT/'frames.txt').write_text(frame_text)
(OUT/'frames.json').write_text(json.dumps(frames,indent=2)+'\n')
(OUT/'incidence-records.json').write_text(json.dumps(dict(column_types=types,results=results),indent=2)+'\n')
summary=dict(status='COMPLETE_EXACT_MARKED_INCIDENCE_CENSUS',agent='six-books-2',role='researcher',
             scope='E102 C3 type3^7 1 root9 degree9^16,10^6, A9/9/10 and B9/9/9/10 placement. No B or mixed completion census here.',
             local_words=H_WORDS,column_types={s:len(types[s]) for s in types},counts=dict(totals),
             by_word=[{k:v for k,v in r.items() if k!='records'} for r in results],
             frames_sha256=hashlib.sha256(frame_text.encode()).hexdigest(),
             seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1,
             trust='Same-author exact nested column census; ordinary bridge unformalized; separate audit still required.')
(OUT/'incidence-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
