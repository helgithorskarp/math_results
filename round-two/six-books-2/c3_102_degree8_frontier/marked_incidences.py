"""Nested marked column census; all canonical choices, then row/pair predicates."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib, json, resource, time
from cases import CASES

START=time.monotonic()
parser=ArgumentParser()
parser.add_argument('--work',type=Path,required=True)
parser.add_argument('--case',choices=sorted(CASES),required=True)
args=parser.parse_args();OUT=args.work;C=CASES[args.case]
OUT.mkdir(parents=True,exist_ok=True)
DG=[d for d in C['A'] for _ in range(3)]
PAIRS=list(combinations(range(9),2))
ORBITS=[tuple((3*i+t,3*i+(t+1)%3) for t in range(3)) for i in range(3)]
ORBITS += [tuple((3*i+t,3*j+(t+s)%3) for t in range(3)) for i,j in combinations(range(3),2) for s in range(3)]

def guard():
    if time.monotonic()-START>25:
        raise RuntimeError('INCOMPLETE marked incidence guard; no exclusion')

def local(word):
    rows=[0]*9
    for k,orbit in enumerate(ORBITS):
        if word>>k&1:
            for u,v in orbit:
                rows[u]|=1<<v;rows[v]|=1<<u
    return rows

def translate(mask,phase):
    return sum(((mask>>(3*i+t))&1)<<(3*i+(t+phase)%3) for i in range(3) for t in range(3))

types={}
for size in sorted(set(C['alpha'])):
    entries=[]
    for subset in combinations(range(9),size):
        mask=sum(1<<a for a in subset);cols=[translate(mask,t) for t in range(3)]
        if mask!=min(cols):
            continue
        entries.append(dict(mask=mask,columns=cols,weights=[((mask>>(3*i))&7).bit_count() for i in range(3)],
                            overlaps=[sum((col>>u&1)*(col>>v&1) for col in cols) for u,v in PAIRS]))
    types[size]=sorted(entries,key=lambda r:r['mask'])
    if len(types[size])!={3:30,4:42,5:42}[size]:
        raise ValueError('Complete marked column domain')
marks=list(zip(C['B'],C['alpha']))

def choices(indices=()):
    slot=len(indices)
    if slot==3:
        yield indices
        return
    lower=max((indices[i] for i in range(slot) if marks[i]==marks[slot]),default=0)
    for index in range(lower,len(types[C['alpha'][slot]])):
        yield from choices(indices+(index,))

projection=json.loads((OUT/'projection.json').read_text())
if projection['mode']!=C['projection'] or projection['global_A_degrees']!=DG or projection['H_edges']!=12:
    raise ValueError('Entire marked projection prerequisite')
results=[];frames=[];totals=Counter()
for word in sorted(map(int,projection['canonical_groups'])):
    rows=local(word)
    margins=[DG[3*i]-1-rows[3*i].bit_count() for i in range(3)]
    caps=[(2 if rows[u]>>v&1 else DG[u]+DG[v]-15)-(rows[u]&rows[v]).bit_count() for u,v in PAIRS]
    overlap_required=3*sum(a*(a-1)//2 for a in C['alpha'])
    counts=Counter();records=[]
    domain_size=1
    for mark in set(marks):
        slots=[i for i,m in enumerate(marks) if m==mark]
        domain_size*=comb(len(types[C['alpha'][slots[0]]])+len(slots)-1,len(slots))
    counts['complete_column_choices']=domain_size
    # Exact dispatch of the fourth column by its three row weights. Every
    # omitted last-column choice violates an actual degree margin. This is
    # different from the auditor's full overlap/slack-target pair join.
    last_by_weight={}
    for index,t in enumerate(types[C['alpha'][3]]):
        last_by_weight.setdefault(tuple(t['weights']),[]).append(index)
    def dispatched_choices():
        for prefix in choices():
            partial=[types[C['alpha'][i]][index] for i,index in enumerate(prefix)]
            remaining=tuple(margins[i]-sum(t['weights'][i] for t in partial) for i in range(3))
            lower=max((prefix[i] for i in range(3) if marks[i]==marks[3]),default=0)
            for last in last_by_weight.get(remaining,[]):
                if last>=lower:
                    yield prefix+(last,)
            guard()
    for indices in dispatched_choices():
        chosen=[types[size][index] for size,index in zip(C['alpha'],indices)]
        if any(sum(t['weights'][i] for t in chosen)!=margins[i] for i in range(3)):
            raise ValueError('Last-column weight dispatch missed a literal margin')
        counts['row_margin_matches']+=1
        overlaps=[sum(t['overlaps'][p] for t in chosen) for p in range(36)]
        if sum(overlaps)!=overlap_required:
            raise ValueError('Literal total marked column overlap')
        if any(o>cap for o,cap in zip(overlaps,caps)):
            continue
        counts['A_pair_matches']+=1
        columns=[col for t in chosen for col in t['columns']]
        X=[sum((col>>u&1)<<v for v,col in enumerate(columns)) for u in range(9)]
        if [x.bit_count() for x in X]!=[DG[u]-1-h.bit_count() for u,h in enumerate(rows)]:
            raise ValueError('Literal A global degree margins')
        for u,v in PAIRS:
            if rows[u]>>v&1:
                if 1+(rows[u]&rows[v]).bit_count()+(X[u]&X[v]).bit_count()>3:
                    raise ValueError('Literal red A pages')
            else:
                blue_A=sum(not(rows[u]>>w&1) and not(rows[v]>>w&1) for w in range(9) if w not in [u,v])
                blue_B=sum(not(col>>u&1) and not(col>>v&1) for col in columns)
                if blue_A+blue_B>6:
                    raise ValueError('Literal blue A pages')
        record=dict(word=word,column_seeds=[t['mask'] for t in chosen],columns=columns,X=X)
        records.append(record);frames.append(record)
        guard()
    for key in ['complete_column_choices','row_margin_matches','A_pair_matches']:
        counts[key]+=0
    totals.update(counts)
    results.append(dict(word=word,margins=margins,capacity=sum(caps),marked_overlap=overlap_required,counts=dict(counts),records=records))
frames.sort(key=lambda r:(r['word'],tuple(r['column_seeds'])))
text=''.join(' '.join(map(str,[f['word'],*f['X']]))+'\n' for f in frames)
(OUT/'frames.txt').write_text(text)
(OUT/'frames.json').write_text(json.dumps(frames,indent=2)+'\n')
(OUT/'incidence-records.json').write_text(json.dumps(dict(case=args.case,column_types=types,results=results),indent=2)+'\n')
summary=dict(status='COMPLETE_EXACT_P1_MARKED_INCIDENCE_CENSUS',agent='six-books-2',role='researcher',case=args.case,
             scope='Specified P1 degree8^3,9^10,10^9 root/K marks; A spines only, no B/mixed completion conclusion.',
             A=C['A'],B=C['B'],alpha=C['alpha'],marks=marks,local_words=sorted(map(int,projection['canonical_groups'])),
             column_types={s:len(v) for s,v in types.items()},counts=dict(totals),
             by_word=[{k:v for k,v in r.items() if k!='records'} for r in results],frames=len(frames),
             frames_sha256=hashlib.sha256(text.encode()).hexdigest(),seconds=time.monotonic()-START,
             peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1,
             canonical_domain_size_counted_combinatorially=True,last_column_weight_dispatch=True,
             trust='Complete exact recursive prefixes/last-column weight dispatch; separate overlap/slack-target check required; ordinary/completeness bridges unformalized.')
(OUT/'incidence-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
