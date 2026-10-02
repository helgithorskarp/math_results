"""Distinct E102 census: set columns and twelve-orbit deficit target joins."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, combinations_with_replacement
from collections import Counter, defaultdict
import hashlib, json, resource, time

parser = ArgumentParser()
parser.add_argument('--work', type=Path, required=True)
OUT = parser.parse_args().work
START = time.monotonic()
PAIRS = list(combinations(range(9), 2))
DG = [9]*6 + [10]*3

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
for size in [4,5]:
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

pair_join = defaultdict(list)
weight_prefixes = []
weights = Counter()
for b in range(42):
    for a in range(b+1):
        vector = tuple(x+y for x,y in zip(vectors[4][a],vectors[4][b]))
        pair_join[vector].append((a,b))
        weights[vector[:3]] += 1
    weight_prefixes.append(dict(weights))
if sum(len(v) for v in pair_join.values()) != 903:
    raise ValueError('Whole sorted column-pair domain')

projection = json.loads((OUT/'projection.json').read_text())
frames = []
by_word = []
for word in sorted(map(int, projection['canonical_groups'])):
    H = local(word)
    target_rows = [DG[u]-1-len(H[u]) for u in [0,3,6]]
    caps = []
    for u,v in PAIRS:
        if v in H[u]:
            caps.append(2-len(H[u]&H[v]))
        else:
            blue_A = sum(w not in H[u] and w not in H[v] for w in range(9) if w not in [u,v])
            caps.append(6-blue_A-(12-(DG[u]-1-len(H[u]))-(DG[v]-1-len(H[v]))))
    if any(len({caps[p] for p in orbit}) != 1 for orbit in orbits):
        raise ValueError('Cap transport')
    units, remainder = divmod(sum(caps)-84,3)
    if remainder or units not in [2,3]:
        raise ValueError('Exact E102 slack budget')
    slack_vectors = []
    for slots in combinations_with_replacement(range(12), units):
        slack = [0]*12
        for p in slots:
            slack[p] += 1
        slack_vectors.append(tuple(slack))
    base = tuple(target_rows+[caps[p] for p in positions])
    targets = [base[:3]+tuple(base[3+i]-slack[i] for i in range(12)) for slack in slack_vectors]
    matches = 0
    records = []
    for c, vc in enumerate(vectors[4]):
        for h, vh in enumerate(vectors[5]):
            remaining = tuple(x-y-z for x,y,z in zip(base,vc,vh))
            matches += weight_prefixes[c].get(remaining[:3],0)
            for goal in targets:
                key = tuple(x-y-z for x,y,z in zip(goal,vc,vh))
                for a,b in pair_join.get(key,[]):
                    if b>c:
                        continue
                    chosen = [types[4][a],types[4][b],types[4][c],types[5][h]]
                    columns = [col for record in chosen for col in record['columns']]
                    X = [sum((col>>u&1)<<v for v,col in enumerate(columns)) for u in range(9)]
                    records.append(dict(word=word,column_seeds=[r['mask'] for r in chosen],columns=columns,X=X))
            if time.monotonic()-START>25:
                raise RuntimeError('INCOMPLETE E102 slack-target join; no exclusion')
    records.sort(key=lambda r:tuple(r['column_seeds']))
    expected = next(r for r in primary['results'] if r['word']==word)
    if canonical(records)!=canonical(sorted(expected['records'],key=lambda r:tuple(r['column_seeds']))):
        raise ValueError('Entire typed E102 incidence sets differ')
    if expected['counts']['row_margin_matches']!=matches or expected['counts']['complete_column_choices']!=556248:
        raise ValueError('Whole E102 margin/choice counts differ')
    frames.extend(records)
    by_word.append(dict(word=word,slack_units=units,slack_targets=len(targets),right_pairs=1764,
                        row_margin_matches=matches,templates=len(records)))

frames.sort(key=lambda r:(r['word'],tuple(r['column_seeds'])))
text = ''.join(' '.join(map(str,[f['word'],*f['X']]))+'\n' for f in frames)
if text!=(OUT/'frames.txt').read_text() or canonical(frames)!=canonical(json.loads((OUT/'frames.json').read_text())):
    raise ValueError('Entire native E102 input differs')
summary = dict(status='COMPLETE_E102_DISTINCT_SLACK_TARGET_JOIN',agent='six-books-2',role='researcher',
               by_word=by_word,frames=len(frames),whole_column_domains_equal=True,whole_typed_incidence_sets_equal=True,
               whole_native_input_equal=True,frames_sha256=hashlib.sha256(text.encode()).hexdigest(),
               seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               trust='Same-author different exact algorithms; ordinary bridge unformalized; independent review pending.')
(OUT/'incidence-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
