"""Exact standalone reconstruction and positive-witness checker; Python 3.11+."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib,json,argparse
D=(1,3,11,33)
def need(v,msg):
    if not v:raise ValueError(msg)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def mul(x,y):
    z=[0]*4
    for i,a in enumerate(x):
        for j,b in enumerate(y):z[i^j]+=a*b*D[i&j]
    return tuple(z)
def scalar(x):return (F(x),0,0,0)
def ca(z,w):return add(z[0],w[0]),add(z[1],w[1])
def cm(z,w):return add(mul(z[0],w[0]),neg(mul(z[1],w[1]))),add(mul(z[0],w[1]),mul(z[1],w[0]))
def row(z):
    v=tuple(12*x for xy in z for x in xy)
    need(all(x.denominator==1 if isinstance(x,F) else isinstance(x,int) for x in v),'nonintegral row')
    return tuple(map(int,v))
def normdiff(z,w):
    x=add(z[:4],neg(w[:4]));y=add(z[4:],neg(w[4:]));return add(mul(x,x),mul(y,y))
def build(root):
    source=[tuple(map(int,s.split())) for s in (root/'source214.tsv').read_text().splitlines() if s and not s.startswith('#')]
    need(len(source)==214 and all(len(z)==4 for z in source),'source shape')
    B=[(a,0,0,b,0,c+6,d,0) for a,b,c,d in source]
    zero=scalar(0);one=scalar(1)
    rho=(scalar(F(1,2)),(0,F(1,2),0,0));t=(scalar(F(5,6)),(0,0,F(1,6),0))
    m=[(zero,zero),(one,zero),rho,ca((one,zero),rho),t,cm(t,rho),cm(t,ca((one,zero),rho))]
    M=list(map(row,m));N=[neg(z[:4])+z[4:] for z in M];C=(0,0,0,0,0,6,0,0)
    pts=[];index={};maps=[]
    for block in [B,M,N,[C]]:
        mp=[]
        for z in block:
            if z not in index:index[z]=len(pts);pts.append(z)
            mp.append(index[z])
        maps.append(mp)
    need(len(set(B))==214,'source collisions')
    edges=[];norms=[]
    for i,j in combinations(range(len(pts)),2):
        n=normdiff(pts[i],pts[j]);norms.append([i,j,*n])
        if n==(144,0,0,0):edges.append([i,j])
    return pts,edges,maps,norms

def proper(word,edges,n,k):
    need(len(word)==n and all(x in '01234'[:k] for x in word),'word shape')
    need(all(word[a]!=word[b] for a,b in edges),'improper word')

def verify(root,cert=None):
    if cert is None:cert=json.loads((root/'certificate.json').read_text())
    need(hashlib.sha256((root/'source214.tsv').read_bytes()).hexdigest()==cert['source214_sha256'],'source hash')
    pts,edges,maps,norms=build(root);B,M,N,center=map(set,maps);C=maps[3][0];O=maps[1][0];P=maps[1][3];Q=maps[2][3];H=M|N
    need(len(pts)==217 and len(edges)==985,'whole inventory')
    need(C==216 and O==89 and P==186 and Q==187,'roles')
    need(normdiff(pts[O],pts[C])==(108,0,0,0),'centre squared distance')
    need(normdiff(pts[P],pts[Q])==(1296,0,0,0),'tip distance')
    need(not any(C in e for e in edges),'declared terminal is not isolated')
    be=[e for e in edges if set(e)<=B];he=[e for e in edges if set(e)<=H]
    need(len(be)==977 and len(H)==13 and len(he)==23 and len(B&H)==11,'component census')
    extra=[e for e in edges if not(set(e)<=B or set(e)<=H)]
    need(extra==[[58,214],[61,215]],'private contact census')
    proper(cert['B214_word'],be,214,4)
    for name in ['proper4_equal_centres','proper4_different_centres']:
        word=cert[name];proper(word,edges,217,4);need(word[:214]==cert['B214_word'],'source word changed')
    need(cert['proper4_equal_centres'][O]==cert['proper4_equal_centres'][C],'equal-centre witness')
    need(cert['proper4_different_centres'][O]!=cert['proper4_different_centres'][C],'unequal-centre witness')
    proper(cert['proper5'],edges,217,5);need(set(cert['proper5'])==set('01234'),'five-word palette')
    ids=sorted(H);need(ids==cert['relay_vertices'],'relay map');hc=dict(zip(ids,cert['relay_equal_tips_word']))
    need(len(hc)==13 and all(hc[a]!=hc[b] for a,b in he) and hc[P]==hc[Q],'input equal-tip word')
    me=[(i,j) for i,j in combinations(range(7),2) if [min(maps[1][i],maps[1][j]),max(maps[1][i],maps[1][j])] in edges]
    need(len(me)==11,'Moser edge set')
    need(not any(all(v[i]!=v[j] for i,j in me) for v in product(range(3),repeat=7)),'Moser three-colouring')
    adj=[set() for _ in pts]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    seen=set();sizes=[]
    for v in range(217):
        if v in seen:continue
        stack=[v];seen.add(v);size=0
        while stack:
            a=stack.pop();size+=1
            for b in adj[a]-seen:seen.add(b);stack.append(b)
        sizes.append(size)
    need(sorted(sizes)==[1,216],'component sizes')
    def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
    return {'status':'VERIFIED_FIXED_RELAY_STOP','unaugmented_points':216,'physical_points_with_declared_terminal':217,'complete_unit_edges':985,'all_unordered_pairs':23436,'chromatic_number':4,'component_sizes':sorted(sizes),'isolated_declared_terminal':C,'selected_centres':[O,C],'centre_squared_distance':'3/4','opposed_Moser_order':13,'opposed_Moser_edges':23,'B214_overlap':11,'new_nonisolated_points':2,'private_contacts_beyond_inherited_graphs':extra,'frozen_complete_B214_word_extends':True,'selected_centres_equality_feasible':True,'selected_centres_inequality_feasible':True,'all_complete_B214_colourings_tested':False,'unconstructed_two_copy_graph_classified':False,'point_hash':digest(pts),'edge_hash':digest(edges),'norm_stream_hash':digest(norms)}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check-expected',action='store_true');args=ap.parse_args();root=Path(__file__).resolve().parent;out=verify(root)
    if args.check_expected:need(out==json.loads((root/'EXPECTED.json').read_text()),'expected output mismatch')
    print(json.dumps(out,indent=2,sort_keys=True))
