"""Weighted K domains and exact cached B-pair filters, then mixed spines."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, product
from collections import Counter
import hashlib, json, resource, time

START=time.monotonic()
parser=ArgumentParser()
parser.add_argument('--work',type=Path,required=True)
from cases import CASES
parser.add_argument('--mode',choices=sorted(CASES),required=True)
args=parser.parse_args()
OUT=args.work
C=CASES[args.mode]
SIZES=C['alpha']
DG=[d for d in C['A'] for _ in range(3)]
DB=C['B']
BETA=[d-s for d,s in zip(DB,SIZES)]
COLUMN_SIZES=[s for s in SIZES for _ in range(3)]
PAIRS=list(combinations(range(12),2))
LINKS=list(combinations(range(4),2))
BY_WEIGHT=[[m for m in range(8) if m.bit_count()==w] for w in range(4)]

def guard():
    if time.monotonic()-START>25:
        raise RuntimeError('INCOMPLETE cached component census; no exclusion')

def local(n,word):
    rows=[0]*(3*n)
    bit=0
    for i in range(n):
        if word>>bit&1:
            for t in range(3):
                u,v=3*i+t,3*i+(t+1)%3
                rows[u]|=1<<v
                rows[v]|=1<<u
        bit+=1
    for i,j in combinations(range(n),2):
        for shift in range(3):
            if word>>bit&1:
                for t in range(3):
                    u,v=3*i+t,3*j+(t+shift)%3
                    rows[u]|=1<<v
                    rows[v]|=1<<u
            bit+=1
    return rows

counts=Counter()
K=[]
for internal in range(16):
    target=[BETA[i]-2*(internal>>i&1) for i in range(4)]
    for weights in product(range(4),repeat=6):
        counts['degree_weight_frames']+=1
        sums=[0]*4
        for (i,j),w in zip(LINKS,weights):
            sums[i]+=w
            sums[j]+=w
        if sums!=target:
            continue
        counts['matching_weight_frames']+=1
        for masks in product(*(BY_WEIGHT[w] for w in weights)):
            word=internal+sum(mask<<(4+3*k) for k,mask in enumerate(masks))
            rows=local(4,word)
            counts['K_degree_words']+=1
            if [row.bit_count() for row in rows]!=[d for d in BETA for _ in range(3)]:
                raise ValueError('Literal K degree marks')
            blue=[4095^row^(1<<i) for i,row in enumerate(rows)]
            if any((rows[u]&rows[v]).bit_count()>3 if rows[u]>>v&1
                   else (blue[u]&blue[v]).bit_count()>5-max(0,9-COLUMN_SIZES[u]-COLUMN_SIZES[v]) for u,v in PAIRS):
                continue
            counts['K_local_cap_words']+=1
            K.append((word,rows,blue))
        guard()
K.sort()
words=''.join(str(word)+'\n' for word,_,_ in K)
(OUT/'cached-K-words.txt').write_text(words)

# Disjoint byte buckets, converted to exact integer bit sets. No approximate filter.
nbytes=(len(K)+7)//8
buckets={(p,color,pages):bytearray(nbytes) for p in range(66) for color in [0,1] for pages in range(6)}
for index,(_,rows,blue) in enumerate(K):
    for p,(u,v) in enumerate(PAIRS):
        color=0 if rows[u]>>v&1 else 1
        pages=((rows[u]&rows[v]) if color==0 else (blue[u]&blue[v])).bit_count()
        if not 0<=pages<=5:
            raise ValueError('K local page bound')
        buckets[p,color,pages][index//8]|=1<<(index%8)
    if index%256==0:
        guard()
cache={}
for p in range(66):
    for color in [0,1]:
        running=0
        for pages in range(6):
            running|=int.from_bytes(buckets[p,color,pages],'little')
            cache[p,color,pages]=running
    if cache[p,0,5]|cache[p,1,5]!=(1<<len(K))-1 or cache[p,0,5]&cache[p,1,5]:
        raise ValueError('Every K word occupies exactly one B-pair color bucket')

def cached(p,color,cap):
    return 0 if cap<0 else cache[p,color,min(cap,5)]

frames=json.loads((OUT/'frames.json').read_text())
records=[]
flags=bytearray(b'0')*(len(frames)*len(K))
valid=[]
for index,frame in enumerate(frames):
    H=local(3,frame['word'])
    X=frame['X']
    columns=frame['columns']
    if [H[u].bit_count()+X[u].bit_count()+1 for u in range(9)]!=DG or sum(map(int.bit_count,H))!=24 or max(map(int.bit_count,H))>3:
        raise ValueError('Literal marked A/root degrees')
    if [c.bit_count() for c in columns]!=COLUMN_SIZES:
        raise ValueError('Literal marked column sizes')
    blueH=[511^row^(1<<a) for a,row in enumerate(H)]
    blueX=[4095^row for row in X]
    bluecols=[511^c for c in columns]
    passing_B=(1<<len(K))-1
    for p,(u,v) in enumerate(PAIRS):
        red_A=(columns[u]&columns[v]).bit_count()
        blue_A=(bluecols[u]&bluecols[v]).bit_count()
        passing_B &= cached(p,0,3-red_A)|cached(p,1,5-blue_A)
    survivors_B=passing_B.bit_count()
    counts['B_pair_survivors']+=survivors_B
    known_red=[[(H[a]&columns[b]).bit_count() for b in range(12)] for a in range(9)]
    known_blue=[[(blueH[a]&bluecols[b]).bit_count() for b in range(12)] for a in range(9)]
    passing=[]
    while passing_B:
        bit=passing_B&-passing_B
        kindex=bit.bit_length()-1
        passing_B-=bit
        word,rows,blue=K[kindex]
        good=True
        for a in range(9):
            for b in range(12):
                if X[a]>>b&1:
                    if known_red[a][b]+(X[a]&rows[b]).bit_count()>3:
                        good=False
                        break
                elif known_blue[a][b]+(blueX[a]&blue[b]).bit_count()>6:
                    good=False
                    break
            if not good:
                break
        if good:
            passing.append(word)
            valid.append(dict(frame=index,K_word=word))
            flags[index*len(K)+kindex]=ord('1')
    records.append(dict(frame=index,B_pair_survivors=survivors_B,valid_K_words=passing))
    counts['completion_choices']+=len(K)
    counts['valid']+=len(passing)
    guard()
(OUT/'cached-outcomes.txt').write_bytes(flags)
for field in ['B_pair_survivors','completion_choices','valid']:
    counts[field]+=0
summary=dict(status='COMPLETE_EXACT_CACHED_E102_COMPONENT_CENSUS',mode=args.mode,agent='six-books-2',role='researcher',
             counts=dict(counts),frames=len(frames),B_degree_orbits=BETA,column_sizes=SIZES,by_frame=records,valid=valid,
             K_word_stream_sha256=hashlib.sha256(words.encode()).hexdigest(),
             entire_outcome_stream_sha256=hashlib.sha256(flags).hexdigest(),
             seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1,
             trust='Exact bit-set page predicates, fresh weighted K generation; whole native graph/domain comparison required; ordinary bridge unformalized.')
(OUT/'cached-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['by_frame','valid']},indent=2))
