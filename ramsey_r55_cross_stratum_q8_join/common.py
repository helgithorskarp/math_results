"""Pinned interfaces, literal graphs and the complete physical core partition."""
from pathlib import Path
from itertools import combinations
import hashlib,json,re
HERE=Path(__file__).resolve().parent
REPO=HERE.parent
Q8=REPO/'ramsey_r55_q8_assumption_queue'
ROOT=REPO/'ramsey_r55_q8_root_unit'
LOCAL=REPO/'ramsey_r55_mixed_q7_elimination'
COUNTS={7:640,8:546356,9:362,10:4}

def need(ok,message):
    if not ok:raise ValueError(message)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def dependencies():
    pins=json.loads((HERE/'DEPENDENCIES.json').read_text())
    for row in pins['files']:
        need(sha(REPO/row['path'])==row['sha256'],'changed dependency: '+row['path'])
    return len(pins['files'])

def parameters(task):
    m=re.fullmatch(r'bo1-q(7|8|9|10)-r(5|6|7|8|9|10)-c([0-9]{6})',task)
    need(m is not None,'canonical original task ID');q,r,c=map(int,m.groups())
    need(5<=r<=q and c<COUNTS[q],'original task range')
    return q,r,c

def route_class(q,r):
    return 'Q8_PHYSICAL' if (q>=8 and r<=8) or (q==7 and r in (5,6)) else 'ORIGINAL_PARENT'

def matrix(g):
    need(g.get('n')==43 and isinstance(g.get('red_hex'),str) and re.fullmatch('[0-9a-f]{226}',g['red_hex']),'graph framing')
    w=int(g['red_hex'],16);need(w<1<<903,'graph padding');a=[[0]*43 for _ in range(43)]
    for k,(u,v) in enumerate(combinations(range(43),2)):a[u][v]=a[v][u]=w>>k&1
    return a

def word(a,p=None):
    if p is None:p=list(range(43))
    return {'n':43,'red_hex':format(sum(a[p[u]][p[v]]<<k for k,(u,v) in enumerate(combinations(range(43),2))),'0226x')}

def mono(a,vertices,k,color):
    return next((list(S) for S in combinations(sorted(vertices),k) if all(a[u][v]==color for u,v in combinations(S,2))),None)

def source_geometry(source):
    q,r,c=parameters(source['task']);a=matrix(source)
    p=source['carrier_to_input'];need(isinstance(p,list) and all(type(x) is int for x in p) and sorted(p)==list(range(43)),'source carrier permutation')
    blocks=[p[4*b:4*b+4] for b in range(q)];C=p[4*q:]
    for b,B in enumerate(blocks):need(mono(a,B,4,int(b<r)) is not None,'source block color')
    need(mono(a,sum(blocks[r:],[])+C,4,1) is None,'source red maximality')
    need(mono(a,C,4,0) is None,'source blue maximality')
    return a,q,r,c,blocks,C

def source_catalog(source,data):
    a,q,r,c,blocks,C=source_geometry(source)
    pins=json.loads((REPO/'ramsey_r55_global_maximal_packing/INPUTS.json').read_text())
    pin=next(x for x in pins if x['n']==len(C));path=Path(data)/pin['name'];need(sha(path)==pin['sha256'],'source catalog identity')
    line=path.read_bytes().splitlines()[c];need(line[0]-63==len(C),'source graph6 order')
    bits=[(x-63)>>b&1 for x in line[1:] for b in range(5,-1,-1)]
    pairs=[(i,j) for j in range(1,len(C)) for i in range(j)]
    need(all(a[C[i]][C[j]]==bit for (i,j),bit in zip(pairs,bits)),'exact original source core')
    return a,q,r,c,blocks,C

def core_guards(directory):
    path=Path(directory)/'cohorts.json';expected=json.loads((Q8/'EXPECTED.json').read_text())['cohorts']['cohort_sha256']
    need(sha(path)==expected,'pinned physical guard tree');tree=json.loads(path.read_text());nodes=tree['nodes']
    seen=set();leaves={}
    def walk(i,mask,value):
        need(type(i) is int and 0<=i<len(nodes) and i not in seen,'tree cycle or reused node');seen.add(i);node=nodes[i]
        need(node['id']==i and int(node['mask'],16)==mask and int(node['value'],16)==value,'physical cylinder identity')
        if 'leaf' in node:
            j=node['leaf'];need(type(j) is int and j not in leaves,'leaf identity');leaves[j]=(mask,value);return
        b=node['bit'];need(type(b) is int and 0<=b<55 and not(mask>>b&1),'fresh split coordinate')
        walk(node['zero'],mask|1<<b,value);walk(node['one'],mask|1<<b,value|1<<b)
    need(tree['root']==0,'root');walk(0,0,0)
    need(seen==set(range(len(nodes))) and sorted(leaves)==list(range(239)),'complete 239-leaf partition')
    need(sum(1<<(55-m.bit_count()) for m,v in leaves.values())==1<<55,'full Boolean volume')
    return [leaves[i] for i in range(239)]

def assumptions(guard):
    mask,value=guard
    return [(802+i)*(1 if value>>i&1 else -1) for i in range(55) if mask>>i&1]
