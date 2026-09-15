#!/usr/bin/env python3
"""Independent exact sparse-radical checker of one fixed root150 transfer."""
from pathlib import Path
from itertools import combinations,product
from math import gcd
import json,hashlib,argparse
BASE=Path(__file__).resolve().parent
RAD=(1,3,5,15,11,33,55,165)
H=[i for i in range(374) if i!=310]
B=[0,150,169,243,244,245,287,296,344,345,346,357,358,359,360,361,362,363,364,365,366,367,368]
SOURCE_SHA='f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50'
def require(p,m):
    if not p:raise ValueError(m)
def digest(obj):return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def square_sparse(axis):
    terms=[(d,a) for d,a in zip(RAD,axis) if a];result={}
    for i,(d,a) in enumerate(terms):
        result[1]=result.get(1,0)+d*a*a
        for e,b in terms[i+1:]:
            g=gcd(d,e);r=d*e//(g*g)
            result[r]=result.get(r,0)+2*g*a*b
    return result

def norm(delta):
    x=square_sparse(delta[:8]);y=square_sparse(delta[8:])
    for r,c in y.items():x[r]=x.get(r,0)+c
    return {r:c for r,c in x.items() if c}

def reconstruct():
    raw=(BASE/'points.tsv').read_bytes();require(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'source hash')
    P=[tuple(map(int,l.split())) for l in raw.decode().splitlines() if l and not l.startswith('#')]
    require(len(P)==509 and all(len(p)==16 for p in P),'source dimensions')
    shift=P[150]
    require(shift==(48,0,0,0,0,0,0,0,0,48,0,0,0,0,0,0),'fixed receiving frame')
    # The source centre is already host vertex150. Append exactly its135 noncentral points.
    moved=[tuple(x+t for x,t in zip(P[v],shift)) for v in range(374,509)]
    points=[P[v] for v in H]+moved
    require(len(points)==len(set(points))==508,'exact distinct merged cap')
    require(set(points)&set(P)=={P[v] for v in H},'all135 added points new to parent')
    require(tuple(x+t for x,t in zip(P[0],shift))==P[150],'shared source centre')
    edges=[];distances=hashlib.sha256();extra=[]
    for a,b in combinations(range(508),2):
        n=norm(tuple(x-y for x,y in zip(points[a],points[b])))
        require(n,'no hidden collision')
        distances.update((json.dumps(n,sort_keys=True,separators=(',',':'))+'\n').encode())
        if n=={1:96**2}:
            edges.append([a,b])
            if a<373<=b and a!=150:extra.append([a,b])
    require(not extra,'no private-to-host incidental contacts')
    hs=[e for e in edges if e[1]<373]
    source_map=[150]+list(range(373,508));sm=set(source_map)
    ss=[e for e in edges if set(e)<=sm]
    require(len(hs)==1856 and len(ss)==564 and len(edges)==2420,'complete inherited edge partition')
    require({tuple(e) for e in edges}=={tuple(e) for e in hs+ss},'literal one-vertex sum')
    require(len([e for e in edges if e[0]==150 and e[1]>=373])==12,'shared-centre incident source edges')
    result={'points':508,'new_points':135,'unit_edges':2420,'all_pairs':128778,'host_edges':1856,'small_gadget_edges':564,'shared_vertices':1,'shared_original_host_label':150,'actual_host_boundary':[150],'extra_contacts':0,'point_sha256':digest(points),'edge_sha256':digest(edges),'distance_sha256':distances.hexdigest()}
    return result,edges,hs,ss,source_map

def proper(word,edges,k=4):
    require(set(word)<=set('0123456789'[:k]),'colour domain')
    require(all(word[a]!=word[b] for a,b in edges),'proper all-edge colouring')

def verify(cert):
    result,edges,he,se,sm=reconstruct();word=cert['colour4']
    require(len(word)==508,'full word length');proper(word,edges)
    require(word[:373]==cert['host_word'],'frozen full host word')
    require(''.join(word[H.index(v)] for v in B)==cert['boundary_word'],'frozen boundary word')
    sw=''.join(word[v] for v in sm);local=[[sm.index(a),sm.index(b)] for a,b in se]
    proper(sw,local);require(sw[0]==word[150],'shared colour')
    # For any new host colour at150, swapping it with the old root colour gives an extension.
    for c in '0123':
        root=sw[0];perm={str(i):str(i) for i in range(4)};perm[root]=c;perm[c]=root
        w=''.join(perm[x] for x in sw);require(w[0]==c,'root alignment');proper(w,local)
    five='4'+word[1:];proper(five,edges,5)
    ids=[H.index(v) for v in [0,149,152,312,151,154,314]]
    me=[[ids.index(a),ids.index(b)] for a,b in he if a in ids and b in ids]
    require(len(me)==11,'Moser induced edge count')
    require(not any(all(c[a]!=c[b] for a,b in me) for c in product(range(3),repeat=7)),'Moser three-colour lower bound')
    result.update({'chromatic_number':4,'proper_four_checked':True,'proper_five_checked':True,'all_host_four_colourings_extend':True,'all_host_projected_relations_unchanged':True,'boundary_word':cert['boundary_word'],'source_word':sw,'colour4_sha256':hashlib.sha256(word.encode()).hexdigest(),'record_candidate':False,'solver_needed':False})
    if 'expected' in cert:require(result==cert['expected'],'expected exact result')
    return result

def controls():
    # Sparse square oracle checks all eight pure basis squares and every two-term product.
    for i,j in combinations(range(8),2):
        a=[0]*8;a[i]=a[j]=1;n=square_sparse(a)
        g=gcd(RAD[i],RAD[j]);r=RAD[i]*RAD[j]//(g*g)
        expected={1:RAD[i]+RAD[j],r:2*g};require(n==expected,'two-term square identity')
    for i in range(8):
        a=[0]*16;a[i]=1;require(norm(a)=={1:RAD[i]},'basis norm identity')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'certificate.json');ap.add_argument('--output',type=Path);args=ap.parse_args();controls()
    r=verify(json.loads(args.certificate.read_text()));s=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(s)
    print(s,end='')
if __name__=='__main__':main()
