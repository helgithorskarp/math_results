"""A residual red-K4 witness; this is a packing violation, not a red K5."""
from itertools import combinations
from pathlib import Path
import argparse,json,re
PAIRS=list(combinations(range(43),2))
def need(ok,why):
    if not ok:raise ValueError(why)
def decode(obj):
    need(type(obj) is dict and obj.get('n')==43,'graph order');word=obj.get('red_hex')
    need(type(word) is str and re.fullmatch('[0-9a-f]{226}',word) is not None,'graph word')
    bits=int(word,16);need(bits<1<<903,'padding');a=[[0]*43 for _ in range(43)]
    for bit,(u,v) in enumerate(PAIRS):a[u][v]=a[v][u]=(bits>>bit)&1
    return a
def encode(a):return dict(n=43,red_hex=f'{sum(a[u][v]<<bit for bit,(u,v) in enumerate(PAIRS)):0226x}')
def verify(a,q,r,w):
    need(type(w) is dict and w.get('colour')==1,'red witness');vertices=w.get('vertices')
    need(type(vertices) is list and len(vertices)==4 and len(set(vertices))==4,'four vertices')
    need(all(type(v) is int and 4*r<=v<43 for v in vertices),'residual vertices')
    outside=[v for v in vertices if v<4*q];core=[v for v in vertices if v>=4*q]
    need(len(outside)==1 and len(core)==3,'one blue block vertex plus three core vertices')
    need(w['block']==outside[0]//4 and all(a[u][v] for u,v in combinations(vertices,2)),'red K4 and block metadata')
    return True
def inspect(obj):
    match=re.fullmatch('bo1-q([7-9]|10)-r([5-9]|10)-c[0-9]{6}',obj['task']);need(match is not None,'task syntax')
    q,r=map(int,match.groups());need(5<=r<=q<=10,'class');a=decode(obj['graph'])
    for b in range(q):need(all(a[u][v]==int(b<r) for u,v in combinations(range(4*b,4*b+4),2)),'fixed block colors')
    for t in combinations(range(4*q,43),3):
        if not all(a[u][v] for u,v in combinations(t,2)):continue
        for v in range(4*r,4*q):
            if all(a[v][u] for u in t):
                w=dict(vertices=[v,*t],colour=1,block=v//4);verify(a,q,r,w)
                return dict(status='RED_MAXIMALITY_WITNESS',task=obj['task'],witness=w)
    return dict(status='NO_DECLARED_RESIDUAL_WITNESS_NOT_TARGET',task=obj['task'],witness=None)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');a=p.parse_args();print(json.dumps(inspect(json.loads(Path(a.input).read_text())),sort_keys=True))
