"""Exact component page predicates; separate from whole-host reconstruction."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations, product
from collections import Counter
import time,json,resource,hashlib

START=time.monotonic()
parser=ArgumentParser()
parser.add_argument('--work',type=Path,required=True)
parser.add_argument('--mode',choices=['AA','BB'],required=True)
args=parser.parse_args();OUT=args.work;MODE=args.mode
COLUMN_SIZES=[4]*12 if MODE=='AA' else [3]*3+[4]*6+[5]*3
OUT.mkdir(parents=True,exist_ok=True)
PAIRS=list(combinations(range(12),2));LINKS=list(combinations(range(4),2))
BY_WEIGHT=[[m for m in range(8) if m.bit_count()==w] for w in range(4)]

def local(n,word):
    rows=[0]*(3*n);bit=0
    for i in range(n):
        if word>>bit&1:
            for t in range(3):
                u,v=3*i+t,3*i+(t+1)%3;rows[u]|=1<<v;rows[v]|=1<<u
        bit+=1
    for i,j in combinations(range(n),2):
        for shift in range(3):
            if word>>bit&1:
                for t in range(3):
                    u,v=3*i+t,3*j+(t+shift)%3;rows[u]|=1<<v;rows[v]|=1<<u
            bit+=1
    return rows

counts=Counter();K=[]
for internal in range(16):
    target=[5-2*(internal>>i&1) for i in range(4)]
    for weights in product(range(4),repeat=6):
        counts['degree_weight_frames']+=1
        sums=[0]*4
        for (i,j),w in zip(LINKS,weights):sums[i]+=w;sums[j]+=w
        if sums!=target:continue
        counts['matching_weight_frames']+=1
        for masks in product(*(BY_WEIGHT[w] for w in weights)):
            word=internal+sum(mask<<(4+3*k) for k,mask in enumerate(masks))
            rows=local(4,word);counts['K_degree_words']+=1
            if any(row.bit_count()!=5 for row in rows):raise ValueError('K degree')
            blue=[4095^row^(1<<i) for i,row in enumerate(rows)]
            if any((rows[u]&rows[v]).bit_count()>3 if rows[u]>>v&1 else (blue[u]&blue[v]).bit_count()>5-max(0,9-COLUMN_SIZES[u]-COLUMN_SIZES[v]) for u,v in PAIRS):continue
            counts['K_local_cap_words']+=1
            K.append((word,rows,blue))
        if time.monotonic()-START>25:raise RuntimeError('Incomplete block census; no exclusion')
K.sort();words=''.join(str(word)+'\n' for word,_,_ in K)
(OUT/'block-K-words.txt').write_text(words)

records=[];valid=[];flags=bytearray()
frames=json.loads((OUT/'frames.json').read_text())
for index,frame in enumerate(frames):
    H=local(3,frame['word']);X=frame['X'];columns=frame['columns']
    blueH=[511^row^(1<<a) for a,row in enumerate(H)]
    blueX=[4095^row for row in X];bluecols=[511^c for c in columns]
    red_A=[(columns[u]&columns[v]).bit_count() for u,v in PAIRS]
    blue_A=[(bluecols[u]&bluecols[v]).bit_count() for u,v in PAIRS]
    known_red=[[(H[a]&columns[b]).bit_count() for b in range(12)] for a in range(9)]
    known_blue=[[(blueH[a]&bluecols[b]).bit_count() for b in range(12)] for a in range(9)]
    total=0;passing=[]
    for word,rows,blue in K:
        total+=1;good=True
        for p,(u,v) in enumerate(PAIRS):
            if rows[u]>>v&1:
                if red_A[p]+(rows[u]&rows[v]).bit_count()>3:good=False;break
            elif 1+blue_A[p]+(blue[u]&blue[v]).bit_count()>6:good=False;break
        if good:
            for a in range(9):
                for b in range(12):
                    if X[a]>>b&1:
                        if known_red[a][b]+(X[a]&rows[b]).bit_count()>3:good=False;break
                    elif known_blue[a][b]+(blueX[a]&blue[b]).bit_count()>6:good=False;break
                if not good:break
        flags.append(ord('1') if good else ord('0'))
        if good:passing.append(word);valid.append(dict(frame=index,K_word=word))
    records.append(dict(frame=index,word=frame['word'],column_seeds=frame['column_seeds'],completion_choices=total,valid_K_words=passing))
    counts['completion_choices']+=total;counts['valid']+=len(passing)
    if time.monotonic()-START>25:raise RuntimeError('Incomplete block census; no exclusion')
(OUT/'block-outcomes.txt').write_bytes(flags)
summary=dict(status='COMPLETE_EXACT_NEAR_COMPONENT_PAGE_CENSUS',mode=MODE,agent='six-books-2',role='researcher',counts=dict(counts),
             scope='E99 root9 near-regular8^3,9^16,10^3 specified '+MODE+' placement ONLY',frames=len(frames),by_frame=records,valid=valid,
             K_word_stream_sha256=hashlib.sha256(words.encode()).hexdigest(),
             entire_outcome_stream_sha256=hashlib.sha256(flags).hexdigest(),
             seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             trust='Same-author exact component count; independently generated literal whole graph census still required.',threads=1)
(OUT/'block-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['by_frame','valid']},indent=2))
