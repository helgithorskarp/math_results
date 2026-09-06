"""Separate exact geometry and list audit; imports no submitted/inherited code."""
import argparse,hashlib,json,time
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,product
from collections import Counter
HERE=Path(__file__).resolve().parent

def need(x,msg):
    if not x:raise ValueError(msg)

def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def sub(x,y):return plus(x,neg(y))
def times(x,y):
    out=[R(0)]*4
    for i in range(4):
        for j in range(4):
            common=i&j;factor=(3 if common&1 else 1)*(11 if common&2 else 1)
            out[i^j]+=x[i]*y[j]*factor
    return tuple(out)
def scale(x,t):return tuple(v*t for v in x)
def pp(x,y):return plus(x[0],y[0]),plus(x[1],y[1])
def cm(x,y):return sub(times(x[0],y[0]),times(x[1],y[1])),plus(times(x[0],y[1]),times(x[1],y[0]))
def norm2(x,y):
    a,b=sub(x[0],y[0]),sub(x[1],y[1]);return plus(times(a,a),times(b,b))
def rational(q):return (R(q),R(0),R(0),R(0))
def decode(p):
    need(len(p)==2 and all(len(c)==4 and all(type(a) is int for a in c) for c in p),'bad coordinate')
    return tuple(tuple(R(a,12) for a in c) for c in p)

def components(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    todo=set(range(n));out=[]
    while todo:
        seen={min(todo)};q=list(seen)
        for a in q:
            for b in adj[a]-seen:seen.add(b);q.append(b)
        todo-=seen;out.append((len(seen),sum(len(adj[v]) for v in seen)//2,sorted(len(adj[v]) for v in seen)))
    return adj,sorted(out)

def audit(c):
    need(c['scale']==12 and c['basis']==['1','sqrt3','sqrt11','sqrt33'],'wrong field')
    z=rational(0);u=(rational(1),z);v=(rational(R(1,2)),(R(0),R(1,2),R(0),R(0)))
    rho=(rational(R(5,6)),(R(0),R(0),R(1,6),R(0)))
    M=[(z,z),u,v,pp(u,v),cm(rho,u),cm(rho,v),cm(rho,pp(u,v))]
    need(M==[decode(p) for p in c['M']] and len(set(M))==7,'spindle transcription')
    C=[decode(p) for p in c['C']];need(len(C)==len(set(C))==25 and set(M)<=set(C),'point domain')
    dist={e:norm2(C[e[0]],C[e[1]]) for e in combinations(range(25),2)}
    def d(a,b):return rational(0) if a==b else dist[tuple(sorted((a,b)))]
    mi=[C.index(m) for m in M]
    need([p[:2] for p in c['circle_pairs']]==[list(e) for e in combinations(range(7),2)],'circle domain incomplete')
    used=set()
    for i,j,a,b in c['circle_pairs']:
        need(type(a) is int and type(b) is int and 0<=a<25 and 0<=b<25 and a!=b,'circle witness indices')
        for q in (a,b):
            need(d(q,mi[i])==d(q,mi[j])==rational(1),'circle witness is not a double unit neighbour')
            used.add(q)
    need(used==set(range(25)),'unwitnessed point')
    # Two distinct intersections are the maximum for distinct equal-radius
    # circles. These positive witnesses prove completeness without reproducing
    # any reflection or root construction from the producer.
    di=sorted(set(range(25))-set(mi));need(di==c['D_indices'] and len(di)==18,'external point domain')
    neighbours=[[i for i in range(7) if d(a,mi[i])==rational(1)] for a in di]
    need(neighbours==c['D_neighbours'] and all(len(ns)==2 for ns in neighbours),'wrong M neighbours')
    edges=[list(e) for e in combinations(range(18),2) if d(di[e[0]],di[e[1]])==rational(1)]
    long=[list(e) for e in combinations(range(18),2) if d(di[e[0]],di[e[1]])==rational(7)]
    three=[list(e) for e in combinations(range(18),2) if d(di[e[0]],di[e[1]])==rational(9)]
    need(edges==c['D_unit_edges'] and long==c['D_sqrt7_pairs'] and three==c['D_distance3_pairs'],'pair classification mismatch')
    need(len(edges)==6 and len(long)==4 and not three,'unexpected pair counts')
    need(len({i for e in long for i in e})==8,'sqrt7 pairs not a matching')
    adj,comps=components(18,edges)
    need(Counter((n,m) for n,m,ds in comps)==Counter({(1,0):10,(2,1):2,(4,4):1}),'wrong D components')
    need(all(ds==[2]*4 for n,m,ds in comps if n==4),'not a four-cycle')
    # Independent bipartition and all-four-subset checks, rather than trusting
    # a named component type for the later leaf-block argument.
    colouring={}
    for root in range(18):
        if root in colouring:continue
        colouring[root]=0;q=[root]
        for x in q:
            for y in adj[x]:
                if y not in colouring:colouring[y]=1-colouring[x];q.append(y)
                need(colouring[y]!=colouring[x],'odd cycle in D')
    p4_checks=0
    for vs in combinations(range(18),4):
        deg=sorted(len(adj[x]&set(vs)) for x in vs);need(deg!=[1,1,2,2],'induced P4 in D');p4_checks+=1
    mc=c['M_colours'];need(mc==[0,1,2,3,1,3,2],'wrong fixed precolouring')
    me=[(i,j) for i,j in combinations(range(7),2) if d(mi[i],mi[j])==rational(1)]
    need(len(me)==11 and all(mc[i]!=mc[j] for i,j in me),'improper spindle colouring')
    lists=[sorted(set(range(4))-{mc[i] for i in ns}) for ns in neighbours]
    need(lists==c['D_lists'] and all(len(s)>=2 for s in lists),'wrong lists')
    need(all(set(lists[i]).isdisjoint(lists[j]) for i,j in long),'long pair is not automatically nonmono')
    need(all(not(len(lists[i])==len(lists[j])==2 and lists[i]==lists[j]) for i,j in edges),'equal two-lists on a unit edge')
    S=[i for i in range(18) if len(lists[i])==2];si={v:i for i,v in enumerate(S)}
    se=[(si[i],si[j]) for i,j in edges if i in si and j in si]
    sa,sc=components(len(S),se)
    need(len(S)==15 and len(se)==2 and Counter((n,m) for n,m,ds in sc)==Counter({(1,0):12,(3,2):1}),'wrong two-list graph')
    return {'C_points':25,'external_double_neighbours':18,'exact_C_pair_norms':len(dist),
      'spindle_pairs_with_two_certified_intersections':21,'circle_unit_checks':84,'C_unit_edges':sum(q==rational(1) for q in dist.values()),
      'M_unit_edges':len(me),'D_unit_edges':len(edges),'D_sqrt7_pairs':len(long),'D_distance3_pairs':len(three),
      'D_induced_four_subsets_checked':p4_checks,'D_bipartite':True,'two_colour_lists':len(S),'three_colour_lists':18-len(S),
      'two_list_unit_edges':len(se),'two_list_component_type':'P3 + 12 isolated vertices',
      'long_pair_list_disjointness_checks':len(long),'unit_pair_list_compatibility_checks':len(edges)}

def finite_list_controls():
    pairs=list(combinations(range(4),2));cases=0
    for a,b in product(pairs,repeat=2):
        if a==b:continue
        for x in range(4):
            need(any(c!=x and d!=x and c!=d for c,d in product(a,b)),'leaf triangle failed');cases+=1
    # Equal two-lists really can fail after precolouring the articulation.
    need(not any(a!=0 and b!=0 and a!=b for a,b in product((0,1),repeat=2)),'equal-list control')
    return {'unequal_two_list_triangle_extensions':cases,'equal_two_list_obstruction_checked':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);a=p.parse_args();start=time.monotonic()
    raw=(HERE/'certificate.json').read_bytes();cert=json.loads(raw);result={**audit(cert),**finite_list_controls()}
    for label in ('circle','colour','list'):
        bad=json.loads(raw)
        if label=='circle':bad['circle_pairs'][0][3]=bad['circle_pairs'][0][2]
        if label=='colour':bad['M_colours'][1]=bad['M_colours'][0]
        if label=='list':bad['D_lists'][0]=[0,1,2,3]
        try:audit(bad)
        except ValueError:pass
        else:raise ValueError('invalid certificate accepted: '+label)
    result.update({'malformed_certificate_rejections':3,'certificate_bytes':len(raw),
      'certificate_sha256':hashlib.sha256(raw).hexdigest(),'native_solver_calls':0,'status':'PASS'})
    if (HERE/'expected.json').exists():need(result==json.loads((HERE/'expected.json').read_text()),'expected mismatch')
    work=Path(a.work);work.mkdir(parents=True,exist_ok=True)
    (work/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({**result,'seconds':time.monotonic()-start},sort_keys=True))
if __name__=='__main__':main()
