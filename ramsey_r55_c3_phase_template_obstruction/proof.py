"""Dense physical-pair checker for the phase-template obstruction and trade.
No imports from template producer, search objective, or physical.py.
"""
import argparse,json
from collections import Counter
from itertools import combinations
from pathlib import Path
from hashlib import sha256

def need(ok,msg):
    if not ok:raise ValueError(msg)

def read(path):
    lines=Path(path).read_text().splitlines();need(lines and lines[0]=='43','order')
    edges=[tuple(map(int,l.split())) for l in lines[1:]]
    need(all(len(e)==2 and 0<=e[0]<e[1]<43 for e in edges),'edge range')
    need(edges==sorted(set(edges)),'edge order')
    a=[[0]*43 for _ in range(43)]
    for u,v in edges:a[u][v]=a[v][u]=1
    return a

def template(a):
    counts={};fixed=[[None]*43 for _ in range(43)]
    for i,j in combinations(range(14),2):
        c=sum(a[3*i][3*j+t] for t in range(3));counts[i,j]=c
        for s in range(3):
            for t in range(3):
                need(a[3*i+s][3*j+t]==a[3*i][3*j+(t-s)%3],'phase action')
    for u,v in combinations(range(43),2):
        if v==42:
            need(a[u][v]==a[3*(u//3)][v],'root action');color=a[u][v]
        elif u//3==v//3:
            need(a[u][v]==int(u<21),'internal color');color=a[u][v]
        else:
            c=counts[u//3,v//3];color=0 if c==0 else 1 if c==3 else None
        fixed[u][v]=fixed[v][u]=color
    return counts,fixed

def certify(fixed,q,color):
    need(len(q)==5 and len(set(q))==5 and all(type(v) is int and 0<=v<43 for v in q),'five-set')
    need(all(fixed[u][v]==color for u,v in combinations(q,2)),'frozen color witness')

def frozen_fives(fixed):
    out=[[],[]]
    for q in combinations(range(43),5):
        c=fixed[q[0]][q[1]]
        if c is not None and all(fixed[u][v]==c for u,v in combinations(q,2)):out[c].append(list(q))
    return out

def verify_trade(a,b):
    ca,fa=template(a);cb,fb=template(b)
    need([sum(r) for r in a]==[sum(r) for r in b],'labeled degrees')
    delta={q:cb[q]-ca[q] for q in ca if ca[q]!=cb[q]}
    need(delta=={(2,10):1,(0,5):1,(0,2):-1,(5,10):-1},'exact count trade')
    need(all(a[u][42]==b[u][42] for u in range(42)),'root frozen')
    return ca,fa,cb,fb

def main():
    ap=argparse.ArgumentParser();ap.add_argument('parent');ap.add_argument('traded');args=ap.parse_args()
    a=read(args.parent);b=read(args.traded);ca,fa,cb,fb=verify_trade(a,b)
    witnesses=[[u,30,31,32,42] for u in (6,7,8)]
    for q in witnesses:certify(fa,q,0)
    pa=frozen_fives(fa);pb=frozen_fives(fb)
    need(pa==[witnesses,[]],'complete parent fixed-five list');need(pb==[[],[]],'traded fixed fives')
    rejected=[]
    for name,q,c in [('wrong_color',witnesses[0],1),('repeated_vertex',[6,30,31,31,42],0),('wrong_triangle',[3,30,31,32,42],0)]:
        try:certify(fa,q,c)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted bad witness')
    broken=[r.copy() for r in b];broken[0][42]^=1;broken[42][0]^=1
    try:verify_trade(a,broken)
    except ValueError:rejected.append('broken_trade')
    else:raise ValueError('accepted broken trade')
    ma=sum(c in (1,2) for c in ca.values());mb=sum(c in (1,2) for c in cb.values())
    need((ma,mb)==(73,76),'mixed pair count')
    print(json.dumps({'status':'VERIFIED_FIXED_PHASE_OBSTRUCTION_AND_DEGREE_TRADE',
        'parent_sha256':sha256(Path(args.parent).read_bytes()).hexdigest(),
        'traded_sha256':sha256(Path(args.traded).read_bytes()).hexdigest(),
        'degree_histogram':dict(sorted(Counter(map(sum,a)).items())),
        'parent_phase_variables':ma,'parent_labeled_family_size':3**ma,
        'parent_persistent_blue_K5':witnesses,'parent_score_lower_bound':3,
        'traded_phase_variables':mb,'traded_labeled_family_size':3**mb,
        'traded_fixed_K5':pb,'traded_family_excluded':False,
        'negative_controls_rejected':rejected},indent=2,sort_keys=True))
if __name__=='__main__':main()
