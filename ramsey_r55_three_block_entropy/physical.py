"""Literal 43-vertex witness interface for the declared three-block filter."""
from itertools import combinations
from pathlib import Path
import argparse,json,re
PAIRS=list(combinations(range(43),2));INDEX={p:k for k,p in enumerate(PAIRS)}

def require(ok,why):
    if not ok:raise ValueError(why)
def matrix(g):
    require(type(g) is dict and type(g.get('n')) is int and g['n']==43,'graph order')
    h=g.get('red_hex');require(type(h) is str and re.fullmatch('[0-9a-f]{226}',h) is not None,'physical word')
    w=int(h,16);require(w<1<<903,'physical padding');a=[[0]*43 for _ in range(43)]
    for k,(u,v) in enumerate(PAIRS):a[u][v]=a[v][u]=(w>>k)&1
    return a

def graph(a):return dict(n=43,red_hex=format(sum(a[u][v]<<k for k,(u,v) in enumerate(PAIRS)),'0226x'))
def column_types(mask):
    require(type(mask) is int and 0<=mask<16,'neighbour mask')
    return [i for i in range(4) if mask&(15^(1<<i))==(15^(1<<i))]
def witness(a,q,r):
    require(type(q) is int and 7<=q<=10 and type(r) is int and 5<=r<=q,'family class')
    for block in range(q):
        for u,v in combinations(range(4*block,4*block+4),2):require(a[u][v]==int(block<r),'fixed block colour')
    for centre in range(1,q):
        colour=int(centre<r);groups=[[] for _ in range(4)]
        for other in range(1,q):
            if other==centre:continue
            for v in range(4*other,4*other+4):
                mask=sum(int(a[4*centre+u][v]==colour)<<u for u in range(4))
                if mask.bit_count()<3:continue
                for omitted in column_types(mask):groups[omitted].append((other,v))
        for omitted,entries in enumerate(groups):
            for (left,v),(right,w) in combinations(entries,2):
                if left!=right and a[v][w]==colour:
                    vertices=sorted([4*centre+u for u in range(4) if u!=omitted]+[v,w])
                    return dict(vertices=vertices,colour=colour,centre_block=centre,other_blocks=[left,right])
    return None

def verify_witness(a,q,w):
    require(type(w) is dict and w.get('colour') in (0,1),'witness format');s=w.get('vertices')
    require(type(s) is list and len(s)==5 and len(set(s))==5 and all(type(v) is int and 4<=v<4*q for v in s),'non-root vertices')
    blocks=[v//4 for v in s];sizes=sorted(blocks.count(b) for b in set(blocks))
    require(sizes==[1,1,3],'three-block split');require(all(a[u][v]==w['colour'] for u,v in combinations(s,2)),'witness colours')
    centre=next(b for b in set(blocks) if blocks.count(b)==3)
    require(w['centre_block']==centre and sorted(w['other_blocks'])==sorted(set(blocks)-{centre}),'witness block metadata')
    return True

def inspect(obj):
    match=re.fullmatch('bo1-q([7-9]|10)-r([5-9]|10)-c[0-9]{6}',obj['task']);require(match is not None,'task syntax')
    q,r=map(int,match.groups());a=matrix(obj['graph']);w=witness(a,q,r)
    if w is not None:verify_witness(a,q,w)
    return dict(status='THREE_BLOCK_RAMSEY_REJECT' if w else 'NO_THREE_BLOCK_WITNESS_NOT_TARGET',task=obj['task'],witness=w)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');a=p.parse_args();print(json.dumps(inspect(json.loads(Path(a.input).read_text())),sort_keys=True))
