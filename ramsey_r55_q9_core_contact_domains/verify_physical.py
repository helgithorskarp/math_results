"""Standalone physical checker; no encoder, row-counter, or parent imports."""
from itertools import combinations
from pathlib import Path
import hashlib,json,re
PIN='6a3da7f0687c392420f190db0643b5c5b7ecb1a3c5ed098c7d96200185a5f010'

def require(ok,why):
    if not ok:raise ValueError(why)
def cores(cache):
    raw=(Path(cache)/'r44_7.g6').read_bytes();require(hashlib.sha256(raw).hexdigest()==PIN,'physical core pin')
    result=[]
    for line in raw.splitlines():
        require(len(line)==5 and line[0]==70,'graph6 shape')
        bits=[int(b) for char in line[1:] for b in format(char-63,'06b')];a=[[0]*7 for _ in range(7)];k=0
        for v in range(1,7):
            for u in range(v):a[u][v]=a[v][u]=bits[k];k+=1
        result.append(a)
    require(len(result)==362,'catalogue size');return result

def physical(obj):
    require(type(obj) is dict and type(obj.get('n')) is int and obj['n']==43,'physical n')
    h=obj.get('red_hex');require(type(h) is str and re.fullmatch('[0-9a-f]{226}',h) is not None,'physical word')
    x=int(h,16);require(x<1<<903,'physical padding');a=[[0]*43 for _ in range(43)];k=0
    for u in range(43):
        for v in range(u+1,43):a[u][v]=a[v][u]=(x>>k)&1;k+=1
    return a

def mono(a,vertices):
    for s in combinations(vertices,5):
        color=a[s[0]][s[1]]
        if all(a[u][v]==color for u,v in combinations(s,2)):return dict(vertices=list(s),color=color)
    return None

def witness(a):
    for color in (0,1):
        neighbors=[sum(1<<v for v in range(43) if v!=u and a[u][v]==color) for u in range(43)]
        def visit(chosen,allowed):
            if len(chosen)==5:return chosen
            while allowed.bit_count()>=5-len(chosen):
                bit=allowed&-allowed;allowed-=bit;v=bit.bit_length()-1
                found=visit(chosen+[v],allowed&neighbors[v])
                if found is not None:return found
            return None
        s=visit([], (1<<43)-1)
        if s is not None:return dict(vertices=s,color=color)
    return None

def validate(obj,core_list):
    match=re.fullmatch('bo1-q9-r([5-9])-c([0-9]{6})',obj['task']);require(match is not None,'physical task')
    r,c=map(int,match.groups());require(c<362,'core index');a=physical(obj['graph']);core=core_list[c]
    for u,v in combinations(range(7),2):require(a[36+u][36+v]==core[u][v],'fixed core')
    for i in range(9):
        for u,v in combinations(range(4*i,4*i+4),2):require(a[u][v]==int(i<r),'fixed block')
    root=[]
    for j in range(1,9):
        signatures=[sum(a[u][4*j+v]<<u for u in range(4)) for v in range(4)]
        require(signatures==sorted(signatures,reverse=True),'root columns')
        root.append(sum(a[u][4*j+v]<<(4*u+v) for u in range(4) for v in range(4)))
    require(root[:r-1]==sorted(root[:r-1],reverse=True) and root[r-1:]==sorted(root[r-1:],reverse=True),'root block order')
    for i,j in combinations(range(9),2):require(mono(a,list(range(4*i,4*i+4))+list(range(4*j,4*j+4))) is None,'block pair K5')
    selected=[];used=set()
    for u,v in combinations(range(7),2):
        if core[u][v] and u not in used and v not in used:selected.append((u+36,v+36));used.update((u,v))
    require(len(selected)>=2,'selected edges');e,f=selected[:2]
    for i in range(9):
        block=list(range(4*i,4*i+4))
        require(mono(a,block+list(range(36,43))) is None,'joint contact K5')
        if i<r:
            for s in combinations(block,2):
                t=[u for u in block if u not in s]
                require(not(all(a[u][v] for u in s for v in e) and all(a[u][v] for u in t for v in f)),'packing augmentation')
    bad=witness(a)
    require(bad is not None,'unexpected possible target: preserve and invoke target verifier')
    require(all(a[u][v]==bad['color'] for u,v in combinations(bad['vertices'],2)),'bad-five certificate')
    return dict(status='VERIFIED_Q9_CONTACT_CARRIER_FIXTURE_NOT_TARGET',task=obj['task'],bad_five=bad,
                tested_local_five_sets=36*56+9*462)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('fixture');args=p.parse_args()
    print(json.dumps(validate(json.loads(Path(args.fixture).read_text()),cores(args.cache)),sort_keys=True))
