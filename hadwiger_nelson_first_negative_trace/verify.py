"""Exact first-negative-trace geometries and residue-gluing certificates."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations
from math import lcm
import importlib.util,json

HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok: raise ValueError(message)

def load(name,path,pin):
    p=HERE.parent/path
    require(sha256(p.read_bytes()).hexdigest()==pin,'input pin mismatch: '+path)
    spec=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

A=load('integral_trace_arithmetic','hadwiger_nelson_integral_trace_gluing/arithmetic.py','88c522f63ddca3b26b71e21003964c52b0da89891ded6c310274b4ddb54a7b7e')
e,add,sub,mul,bar,norm,scale=A.e,A.add,A.sub,A.mul,A.bar,A.norm,A.scale
ZERO,ONE=A.ZERO,A.ONE
F=load('source_gadgets','hadwiger_nelson_mixed505_all_gadget_anchors/verify.py',
       '526b12cbd9d28217e59feb7191c93ace4e5a572ebeadd66cdf384393126aee38')


def wheel():
    h=e(Q(1,2),0,Q(1,2)); hh=mul(h,h)
    return [ZERO,ONE,h,hh,scale(ONE,-1),scale(h,-1),scale(hh,-1)]


def gadgets():
    G,V=F.read_points(159),F.read_points(214)
    B=list(dict.fromkeys([tuple(6*a for a in p) for p in G]+
        [(5*a-11*d,5*b-c,5*c+11*b,5*d+a) for a,b,c,d in G]))
    require(len(B)==292 and len(V)==214,'source sizes differ')
    return [tuple(Q(a,72) for a in p) for p in B],[tuple(Q(a,12) for a in p) for p in V]


def obstruction():
    # P: two six-step unit paths from 1/2, plus its unit neighbour -1/2.
    eta=e(Q(1,2),0,Q(1,2)); nu=e(Q(13,19),0,Q(8,19)); en=mul(eta,nu)
    require(all(norm(x)==ONE for x in (eta,nu,en)),'path direction not unit')
    p=[e(Q(1,2)),e(Q(-1,2))]
    steps=[ONE,scale(eta,-1),scale(nu,-1),scale(nu,-1),en,en]
    for direction in (steps,[bar(x) for x in steps]):
        x=p[0]
        for v in direction:
            x=add(x,v)
            if x not in p:p.append(x)
    ym=e(Q(-4,19),0,Q(-1,19));yp=bar(ym)
    q=[ONE,scale(ONE,-1),ym,yp,ZERO,scale(eta,-1),scale(bar(eta),-1)]
    xm=e(Q(-18,19),0,Q(-9,38));xp=bar(xm)
    witness=[(p.index(x),q.index(y)) for x,y in [(p[0],ONE),(p[1],scale(ONE,-1)),(xm,ym),(xp,yp)]]
    require(all(A.qvalue(p[i],q[j],e(Q(1,2)))==ONE for i,j in witness),'cross witness is not unit')
    return p,q,witness


def configurations():
    B,V=gadgets();H=wheel();P,S,witness=obstruction();rho=e(Q(-1,2),0,Q(1,2))
    def shift(G,x):return [add(sub(p,G[0]),x) for p in G]
    out=[]
    def pair(name,P,S,r=ONE,kind='residue_gluing',witness=None):
        out.append({'name':name,'P':P,'Q':[mul(bar(r),y) for y in S],'rho':r,'kind':kind,'witness':witness})
    pair('common_centre_wheels',H,H)
    x,y=e(Q(-11,17)),e(Q(-16,17))
    pair('integral_mixed506',shift(B,x),shift(V,y))
    pair('nonreal_integral_mixed506',shift(B,x),shift(V,y),rho)
    pair('nonintegral_wheels',shift(H,e(Q(1,2))),shift(H,ONE))
    pair('depth_three_wheels',shift(H,e(Q(-187,184))),shift(H,e(Q(-7,92))))
    pair('connected_saturation',P,S,kind='residue_obstruction',witness=witness)
    # Exchanging source roles and reflecting gives an isometric control.
    pair('swapped_saturation',[bar(x) for x in S],[bar(x) for x in P],kind='residue_obstruction',
         witness=[(j,i) for i,j in witness])
    return out


def graph(case):
    P,S,r=case['P'],case['Q'],case['rho'];n=len(P)
    pts=[(x,ZERO) for x in P]+[(ZERO,mul(r,y)) for y in S]
    L=lcm(*(v.denominator for p in pts for x in p for v in x))
    ints=[(tuple(int(v*L) for v in x),tuple(int(v*L) for v in y)) for x,y in pts]
    first,aliases={},[]
    for i,p in enumerate(pts):aliases.append(first.setdefault(p,i))
    edges=set();cross=[];internal=[[],[]];h=sha256()
    for i,j in combinations(range(len(pts)),2):
        x,y=sub(ints[i][0],ints[j][0]),sub(ints[i][1],ints[j][1])
        c,cb=mul(bar(x),y),mul(x,bar(y));im=sub(c,cb)
        v=add(scale(add(norm(x),norm(y)),4),add(c,cb))
        require(v[2:]==im[:2]==(0,0),'wrong distance support')
        # Basis 1,sqrt(33),sqrt(5),sqrt(165); sqrt(45)=3 sqrt(5).
        values=[Q(v[0],4*L*L),Q(v[1],4*L*L),Q(-3*im[2],4*L*L),Q(-im[3],4*L*L)]
        h.update((f'{i},{j}:'+','.join(f'{v.numerator}/{v.denominator}' for v in values)+'\n').encode())
        if values==[0,0,0,0]:require(aliases[i]==aliases[j],'unaccounted overlap')
        if values==[1,0,0,0]:
            edges.add(tuple(sorted((aliases[i],aliases[j]))))
            if j<n:internal[0].append((i,j))
            elif i>=n:internal[1].append((i-n,j-n))
            else:cross.append((i,j-n))
    return sorted(edges),cross,internal,aliases,h.hexdigest()


def connected(n,edges):
    adj=[set() for _ in range(n)]
    for i,j in edges:adj[i].add(j);adj[j].add(i)
    seen={0};todo=[0]
    for i in todo:
        for j in adj[i]-seen:seen.add(j);todo.append(j)
    return len(seen)==n


def colour_search(n,edges):
    # A positive witness generator only. Failure has no certificate status.
    adj=[set() for _ in range(n)]
    for i,j in edges:adj[i].add(j);adj[j].add(i)
    c=[-1]*n
    def visit():
        free=[i for i in range(n) if c[i]<0]
        if not free:return True
        i=max(free,key=lambda i:(len({c[j] for j in adj[i] if c[j]>=0}),len(adj[i]),-i))
        used={c[j] for j in adj[i]}
        for v in range(4):
            if v not in used:
                c[i]=v
                if visit():return True
        c[i]=-1
        return False
    require(visit(),'positive colouring not found')
    return c


def run(case):
    P,S,r=case['P'],case['Q'],case['rho'];n=len(P);N=n+len(S);T=scale(r,Q(1,2))
    require(A.local(scale(T,2),1)!=(0,0),'relative trace does not have valuation -1')
    edges,cross,internal,aliases,digest=graph(case)
    require(all(connected(len(G),es) for G,es in zip((P,S),internal)),'source disconnected')
    cp=[A.C.residue(sub(x,P[0])) for x in P];cq=[A.C.residue(sub(y,S[0])) for y in S]
    require(all(cp[i]!=cp[j] for i,j in internal[0]) and all(cq[i]!=cq[j] for i,j in internal[1]),'bad source residue colouring')
    require(all(A.qvalue(P[i],S[j],T)==ONE for i,j in cross),'cross identity failure')
    valid=[]
    for pi in permutations(range(4)):
        c=cp+[pi[v] for v in cq]
        if all(c[i]==c[aliases[i]] for i in range(N)) and all(c[i]!=c[j] for i,j in edges):valid.append(pi)
    if all(A.C.depth(x)==0 for x in P+S):
        colours=[A.C.residue(x) for x in P+S];branch='integral'
        require(all((A.C.residue(P[i])==0)!=(A.C.residue(S[j])==0) for i,j in cross),'integral zero split failed')
        # The zero-residue endpoint is actually divisible by four.
        require(all(A.local(x,2)==(0,0) for i,j in cross for x in (P[i],S[j]) if A.C.residue(x)==0),'cross endpoint is not in 4O')
    else:
        branch='nonintegral'
        i,j=cross[0];k1,k2=A.C.depth(P[i]),A.C.depth(S[j])
        require(abs(k1-k2)==1,'negative anchor depths do not differ by one')
        shallow=sorted({cq[j] for i,j in cross}) if k1>k2 else sorted({cp[i] for i,j in cross})
        require(len(shallow)==1,'shallow-side residues not constant')
        colours=cp+[valid[0][v] for v in cq] if valid else colour_search(N,edges)
    if case['kind']=='residue_obstruction':require(not valid,'expected residue obstruction missing')
    else:require(valid,'expected residue gluing failed')
    require(all(colours[i]==colours[aliases[i]] for i in range(N)) and
            all(i!=j and colours[i]!=colours[j] for i,j in edges),'positive colouring invalid')
    witness=case['witness']
    if witness is not None:
        require(set(witness)<=set(cross),'designated witness edges missing')
    parent=list(range(N));forest=True
    def root(i):
        while i!=parent[i]:i=parent[i]
        return i
    for a,b in sorted({tuple(sorted((aliases[i],aliases[n+j]))) for i,j in cross}):
        a,b=root(a),root(b)
        if a==b:forest=False
        else:parent[a]=b
    return {'case':case['name'],'kind':case['kind'],'relative_trace':list(map(str,T)),
            'source_sizes':[n,len(S)],'vertices':len(set(aliases)),'labelled_vertices':N,
            'pairs_checked':N*(N-1)//2,'strict_edges':len(edges),'source_edges':list(map(len,internal)),
            'source_connected':[True,True],'cross_edges':cross,'cross_forest':forest,
            'squared_distance_sha256':digest,'edge_sha256':sha256(''.join(f'{i},{j}\n' for i,j in edges).encode()).hexdigest(),
            'local_branch':branch,'source_depths':[A.C.depth(P[0]),A.C.depth(S[0])],
            'source_residue_colours':[''.join(map(str,cp)),''.join(map(str,cq))],
            'cross_residue_pairs':sorted({(cp[i],cq[j]) for i,j in cross}),
            'compatible_relative_permutations':len(valid),'positive_colouring':''.join(map(str,colours)),
            'witness_edges':witness,
            'explicit_sources':[[list(map(str,x)) for x in G] for G in (P,S)] if witness else None}


def main():
    rows=[run(c) for c in configurations()]
    print(json.dumps({'cases_checked':len(rows),'total_pair_checks':sum(r['pairs_checked'] for r in rows),
                      'cases':rows,'no_five_chromatic_claim':True,'uniform_claim_requires_PROOF_md':True},indent=2))

if __name__=='__main__':main()
