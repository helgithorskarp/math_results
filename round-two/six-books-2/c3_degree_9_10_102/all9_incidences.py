"""Fresh direct marked incidence domains for the E102 all-nine A placement."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, combinations_with_replacement
from collections import Counter
import hashlib, json, resource, time

parser = ArgumentParser()
parser.add_argument('--projection',type=Path,required=True)
parser.add_argument('--work',type=Path,required=True)
parser.add_argument('--mode',choices=['G7','GM','G6'],required=True)
args=parser.parse_args()
OUT=args.work
OUT.mkdir(parents=True,exist_ok=True)
START=time.monotonic()
SIZES={'G7':(4,4,3,5),'GM':(3,4,4,5),'G6':(4,4,4,4)}[args.mode]
DG=[9]*9
PAIRS=list(combinations(range(9),2))
ORBITS=[tuple((3*i+t,3*i+(t+1)%3) for t in range(3)) for i in range(3)]
ORBITS += [tuple((3*i+t,3*j+(t+s)%3) for t in range(3)) for i,j in combinations(range(3),2) for s in range(3)]

def local(word):
    rows=[0]*9
    for k,orbit in enumerate(ORBITS):
        if word>>k&1:
            for u,v in orbit:
                rows[u]|=1<<v
                rows[v]|=1<<u
    return rows

def translate(mask,phase):
    return sum((mask>>(3*i+t)&1)<<(3*i+(t+phase)%3) for i in range(3) for t in range(3))

types={}
for size in sorted(set(SIZES)):
    records=[]
    for subset in combinations(range(9),size):
        mask=sum(1<<u for u in subset)
        columns=[translate(mask,t) for t in range(3)]
        if mask!=min(columns):
            continue
        records.append(dict(mask=mask,columns=columns,
                            weights=[((mask>>(3*i))&7).bit_count() for i in range(3)],
                            overlaps=[sum((col>>u&1)*(col>>v&1) for col in columns) for u,v in PAIRS]))
    types[size]=sorted(records,key=lambda r:r['mask'])

def choices():
    # Sort only identical (global B degree, column rank) marks.
    if args.mode=='G7':
        for a,b in combinations_with_replacement(range(42),2):
            for c in range(30):
                yield types[4][a],types[4][b],types[3][c],types[5]
    elif args.mode=='GM':
        for a in range(30):
            for b in range(42):
                for c in range(42):
                    yield types[3][a],types[4][b],types[4][c],types[5]
    else:
        for a,b in combinations_with_replacement(range(42),2):
            for c in range(42):
                yield types[4][a],types[4][b],types[4][c],types[4][c:]

projection=json.loads((args.projection/'projection.json').read_text())
if projection['mode']!='A999':
    raise ValueError('Marked all-nine projection')
results=[]
frames=[]
totals=Counter()
for word in sorted(map(int,projection['canonical_groups'])):
    H=local(word)
    target=[8-H[3*i].bit_count() for i in range(3)]
    caps=[(2 if H[u]>>v&1 else 3)-(H[u]&H[v]).bit_count() for u,v in PAIRS]
    if sum(caps)!=75:
        raise ValueError('All-nine H12 capacity')
    counts=Counter()
    records=[]
    for a,b,c,last in choices():
        partial=[a['weights'][i]+b['weights'][i]+c['weights'][i] for i in range(3)]
        for d in last:
            counts['complete_column_choices']+=1
            if any(partial[i]+d['weights'][i]!=target[i] for i in range(3)):
                continue
            counts['row_margin_matches']+=1
            chosen=[a,b,c,d]
            overlaps=[sum(t['overlaps'][p] for t in chosen) for p in range(36)]
            if any(o>cap for o,cap in zip(overlaps,caps)):
                continue
            counts['A_pair_matches']+=1
            columns=[col for record in chosen for col in record['columns']]
            X=[sum((col>>u&1)<<v for v,col in enumerate(columns)) for u in range(9)]
            if [row.bit_count() for row in X]!=[8-row.bit_count() for row in H]:
                raise ValueError('Literal all-nine incidence ranks')
            for u,v in PAIRS:
                if H[u]>>v&1:
                    if 1+(H[u]&H[v]).bit_count()+(X[u]&X[v]).bit_count()>3:
                        raise ValueError('Literal red A pages')
                else:
                    blue_H=sum(not(H[u]>>w&1) and not(H[v]>>w&1) for w in range(9) if w not in [u,v])
                    blue_X=sum(not(col>>u&1) and not(col>>v&1) for col in columns)
                    if blue_H+blue_X>6:
                        raise ValueError('Literal blue A pages')
            record=dict(word=word,column_seeds=[r['mask'] for r in chosen],columns=columns,X=X)
            records.append(record)
            frames.append(record)
        if time.monotonic()-START>25:
            raise RuntimeError('INCOMPLETE all-nine incidence; no exclusion')
    totals.update(counts)
    results.append(dict(word=word,margins=target,counts=dict(counts),records=records))

frames.sort(key=lambda r:(r['word'],tuple(r['column_seeds'])))
text=''.join(' '.join(map(str,[f['word'],*f['X']]))+'\n' for f in frames)
(OUT/'frames.txt').write_text(text)
(OUT/'frames.json').write_text(json.dumps(frames,indent=2)+'\n')
(OUT/'incidence-records.json').write_text(json.dumps(dict(column_types=types,results=results),indent=2)+'\n')
summary=dict(status='COMPLETE_EXACT_E102_ALL_NINE_INCIDENCE',agent='six-books-2',role='researcher',mode=args.mode,
             scope='E102 C3 type3^7 1 degree9^16,10^6 fixed-root9 A9/9/9 and B9/9/10/10 marked '+args.mode+' ONLY; no K completion here.',
             column_sizes=SIZES,column_types={s:len(types[s]) for s in types},counts=dict(totals),
             by_word=[{k:v for k,v in r.items() if k!='records'} for r in results],
             frames_sha256=hashlib.sha256(text.encode()).hexdigest(),
             seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             threads=1,trust='Same-author direct exact incidence; separate target-join audit required; written bridge unformalized.')
(OUT/'incidence-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
