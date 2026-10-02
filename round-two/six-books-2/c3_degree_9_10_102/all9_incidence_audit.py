"""Distinct E102 census: set columns and twelve-orbit deficit target joins."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, combinations_with_replacement, product
from collections import Counter, defaultdict
import hashlib, json, resource, time

parser = ArgumentParser()
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--projection', type=Path, required=True)
parser.add_argument('--mode', choices=['G7','GM','G6'], required=True)
args = parser.parse_args()
OUT = args.work
SIZES = {'G7':(4,4,3,5),'GM':(3,4,4,5),'G6':(4,4,4,4)}[args.mode]
START = time.monotonic()
PAIRS = list(combinations(range(9), 2))
DG = [9]*9

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)

def local(word):
    rows = []
    for u in range(9):
        row = set()
        i, t = divmod(u, 3)
        for v in range(9):
            if u == v:
                continue
            j, s = divmod(v, 3)
            if i == j:
                bit = i
            else:
                base = {(0,1):3, (0,2):6, (1,2):9}[min(i,j),max(i,j)]
                bit = base + ((s-t)%3 if i<j else (t-s)%3)
            if word >> bit & 1:
                row.add(v)
        rows.append(row)
    return rows

def rotate(subset, shift):
    return {3*(u//3)+(u%3+shift)%3 for u in subset}

types = {}
for size in sorted(set(SIZES)):
    entries = []
    for mask in range(512):
        if mask.bit_count() != size:
            continue
        subset = {u for u in range(9) if mask>>u&1}
        sets = [rotate(subset, t) for t in range(3)]
        columns = [sum(1<<u for u in s) for s in sets]
        if mask != min(columns):
            continue
        weights = [sum(u in s for s in sets) for u in [0,3,6]]
        overlaps = [sum(u in s and v in s for s in sets) for u,v in PAIRS]
        entries.append(dict(mask=mask, columns=columns, weights=weights, overlaps=overlaps))
    types[size] = entries
primary = json.loads((OUT/'incidence-records.json').read_text())
if canonical({str(k):v for k,v in types.items()}) != canonical(primary['column_types']):
    raise ValueError('Entire literal column domains differ')

# Recover orbit representatives by set transport, independently of generator slots.
unseen = set(PAIRS)
orbits = []
while unseen:
    u,v = min(unseen)
    orbit = {tuple(sorted((3*(u//3)+(u%3+t)%3, 3*(v//3)+(v%3+t)%3))) for t in range(3)}
    if len(orbit)!=3 or not orbit<=unseen:
        raise ValueError('Orbit partition')
    orbits.append(sorted(PAIRS.index(p) for p in orbit))
    unseen -= orbit
if len(orbits)!=12:
    raise ValueError('Orbit count')
positions = [o[0] for o in orbits]
vectors = {}
for size, entries in types.items():
    vectors[size] = []
    for record in entries:
        if any(len({record['overlaps'][p] for p in orbit}) != 1 for orbit in orbits):
            raise ValueError('Nonconstant column overlaps')
        vectors[size].append(tuple(record['weights']+[record['overlaps'][p] for p in positions]))


# These two-column domains differ from the producer's three-prefix loop.
left_choices = list(product(range(42), repeat=2)) if args.mode=='GM' else list(combinations_with_replacement(range(42),2))
right_choices = list(combinations_with_replacement(range(42),2)) if args.mode=='G6' else list(product(range(30),range(42)))
left_join = defaultdict(list)
weight_counts = Counter()
for a,b in left_choices:
    vector = tuple(x+y for x,y in zip(vectors[4][a],vectors[4][b]))
    left_join[vector].append((a,b))
    weight_counts[vector[:3]] += 1
projection = json.loads((args.projection/'projection.json').read_text())
frames = []
by_word = []
for word in sorted(map(int,projection['canonical_groups'])):
    H=local(word)
    target=[8-len(H[u]) for u in [0,3,6]]
    caps=[]
    for u,v in PAIRS:
        if v in H[u]:
            caps.append(2-len(H[u]&H[v]))
        else:
            blue_A=sum(w not in H[u] and w not in H[v] for w in range(9) if w not in [u,v])
            caps.append(6-blue_A-(12-(8-len(H[u]))-(8-len(H[v]))))
    if sum(caps)!=75 or any(len({caps[p] for p in orbit})!=1 for orbit in orbits):
        raise ValueError('Literal all-nine cap domain')
    overlap=3*sum(s*(s-1)//2 for s in SIZES)
    units,remainder=divmod(75-overlap,3)
    if remainder or units not in [0,1]:
        raise ValueError('All-nine exact deficit budget')
    slacks=[]
    for slots in combinations_with_replacement(range(12),units):
        delta=[0]*12
        for p in slots:delta[p]+=1
        slacks.append(tuple(delta))
    base=tuple(target+[caps[p] for p in positions])
    records=[]
    margins=0
    for c,d in right_choices:
        rc=types[4][c] if args.mode=='G6' else types[3][c]
        rd=types[4][d] if args.mode=='G6' else types[5][d]
        vc=vectors[4][c] if args.mode=='G6' else vectors[3][c]
        vd=vectors[4][d] if args.mode=='G6' else vectors[5][d]
        remaining=tuple(x-y-z for x,y,z in zip(base,vc,vd))
        margins+=weight_counts[remaining[:3]]
        for delta in slacks:
            key=remaining[:3]+tuple(remaining[3+i]-delta[i] for i in range(12))
            for a,b in left_join.get(key,[]):
                chosen=[rc,types[4][a],types[4][b],rd] if args.mode=='GM' else [types[4][a],types[4][b],rc,rd]
                columns=[col for record in chosen for col in record['columns']]
                X=[sum((col>>u&1)<<v for v,col in enumerate(columns)) for u in range(9)]
                records.append(dict(word=word,column_seeds=[r['mask'] for r in chosen],columns=columns,X=X))
        if time.monotonic()-START>25:
            raise RuntimeError('INCOMPLETE all-nine join; no exclusion')
    records.sort(key=lambda r:tuple(r['column_seeds']))
    expected=next(r for r in primary['results'] if r['word']==word)
    if canonical(records)!=canonical(sorted(expected['records'],key=lambda r:tuple(r['column_seeds']))):
        raise ValueError('Entire all-nine incidence sets differ')
    if expected['counts']['row_margin_matches']!=margins or expected['counts']['complete_column_choices']!=len(left_choices)*len(right_choices):
        raise ValueError('Complete margin/choice counts differ')
    frames.extend(records)
    by_word.append(dict(word=word,left_pairs=len(left_choices),right_pairs=len(right_choices),slack_targets=len(slacks),row_margin_matches=margins,templates=len(records)))
frames.sort(key=lambda r:(r['word'],tuple(r['column_seeds'])))
text=''.join(' '.join(map(str,[f['word'],*f['X']]))+'\n' for f in frames)
if text!=(OUT/'frames.txt').read_text() or canonical(frames)!=canonical(json.loads((OUT/'frames.json').read_text())):
    raise ValueError('Whole all-nine native input differs')
summary=dict(status='COMPLETE_ALL_NINE_DISTINCT_PAIR_JOIN',agent='six-books-2',role='researcher',mode=args.mode,by_word=by_word,frames=len(frames),whole_column_domains_equal=True,whole_typed_incidence_sets_equal=True,whole_native_input_equal=True,frames_sha256=hashlib.sha256(text.encode()).hexdigest(),seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,trust='Same-author different exact domains/joins; written bridge unformalized; independent peer review pending.')
(OUT/'incidence-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))

