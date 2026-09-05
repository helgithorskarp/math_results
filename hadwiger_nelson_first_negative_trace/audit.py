"""Independent real-radical reconstruction; imports neither verify.py nor its arithmetic."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
from math import lcm
from itertools import combinations,permutations
import importlib.util,json

HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise ValueError(message)

def inputs():
    p=HERE.parent/'hadwiger_nelson_mixed506_single_hub_reduction/check_examples.py'
    require(sha256(p.read_bytes()).hexdigest()=='8405039707b294ace3af5fd9deffc0a738c17133d442056a4013b9b4b588a50f','source pin mismatch')
    s=importlib.util.spec_from_file_location('radical_source',p)
    R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
    return R

def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def minus(x,y):return tuple(a-b for a,b in zip(x,y))


def configurations():
    R=inputs()
    def extract(z):
        x,y=z
        require(all(x[i]==0 for i in range(8) if i not in (0,6)) and
                all(y[i]==0 for i in range(8) if i not in (2,4)),'source support changed')
        return tuple(Q(v) for v in (x[0],x[6],y[2],y[4]))
    G,V=R.read(159),R.read(214)
    B=list(dict.fromkeys([R.cscale(x,6) for x in G]+[R.cmul(R.e(5,0,0,1),x) for x in G]))
    B=[tuple(a/72 for a in extract(x)) for x in B];V=[tuple(a/12 for a in extract(x)) for x in V]
    def elem(a=0,c=0):return Q(a),Q(0),Q(c),Q(0)
    def times(x,y):return extract(R.cmul(R.e(*x),R.e(*y)))
    def bar(x):return x[0],x[1],-x[2],-x[3]
    zero=elem();one=elem(1);eta=elem(Q(1,2),Q(1,2));nu=elem(Q(13,19),Q(8,19))
    H=[zero,one,eta,elem(Q(-1,2),Q(1,2)),elem(-1),elem(Q(-1,2),Q(-1,2)),bar(eta)]
    # Reconstruct the short paths independently, then compare the explicit source table.
    P=[elem(Q(1,2)),elem(Q(-1,2))]
    steps=[one,minus(zero,eta),minus(zero,nu),minus(zero,nu),times(eta,nu),times(eta,nu)]
    for path in (steps,[bar(x) for x in steps]):
        v=P[0]
        for x in path:
            v=plus(v,x)
            if v not in P:P.append(v)
    S=[one,elem(-1),elem(Q(-4,19),Q(-1,19)),elem(Q(-4,19),Q(1,19)),zero,minus(zero,eta),minus(zero,bar(eta))]
    def shift(G,x):return [plus(minus(v,G[0]),x) for v in G]
    configs={'common_centre_wheels':(H,H),'integral_mixed506':(shift(B,elem(Q(-11,17))),shift(V,elem(Q(-16,17)))),
             'nonintegral_wheels':(shift(H,elem(Q(1,2))),shift(H,one)),
             'depth_three_wheels':(shift(H,elem(Q(-187,184))),shift(H,elem(Q(-7,92)))),
             'connected_saturation':(P,S),'swapped_saturation':([bar(x) for x in S],[bar(x) for x in P])}
    configs['nonreal_integral_mixed506']=configs['integral_mixed506']
    return configs

# Full real ring Q(sqrt(3),sqrt(5),sqrt(11)), basis mask order 0,...,7.
RAD=(3,5,11)
FACT=[1]*8
for mask in range(8):
    for bit,p in enumerate(RAD):
        if mask&(1<<bit):FACT[mask]*=p

def multiply(x,y):
    z=[0]*8
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:z[i^j]+=a*b*FACT[i&j]
    return tuple(z)

def placed(x,rotate=False):
    a,b,c,d=x;re=[0]*8;im=[0]*8
    re[0],re[5],im[1],im[4]=a,b,c,d
    if not rotate:return tuple(re),tuple(im)
    sine=[0]*8;sine[3]=1
    si,sr=multiply(im,sine),multiply(re,sine)
    return tuple(Q(a-b)/4 for a,b in zip(re,si)),tuple(Q(a+b)/4 for a,b in zip(im,sr))

def connected(n,edges):
    visited={0}
    while True:
        more={j for i,j in edges if i in visited}|{i for i,j in edges if j in visited}
        nxt=visited|more
        if nxt==visited:return len(nxt)==n
        visited=nxt

def small_residue(x):
    a,b,c,d=x;require(b==d==0,'small witness left Q(i sqrt(3))')
    # alpha=1+2 omega, so the two coefficients are a+c and 2c.
    coefficients=(a+c,2*c)
    require(all(v.denominator%2 for v in coefficients),'nonintegral small witness')
    return sum((v.numerator%2)*(1<<i) for i,v in enumerate(coefficients))

def run(row,config):
    P,S=config;n=len(P);N=n+len(S)
    if row['explicit_sources'] is not None:
        actual=[[[str(v) for v in x] for x in G] for G in (P,S)]
        require(actual==row['explicit_sources'],'explicit source tables differ')
    points=[placed(x) for x in P]+[placed(y,True) for y in S]
    L=lcm(*(Q(v).denominator for p in points for x in p for v in x))
    pts=[(tuple(int(v*L) for v in x),tuple(int(v*L) for v in y)) for x,y in points]
    aliases=[];first={}
    for i,p in enumerate(pts):aliases.append(first.setdefault(p,i))
    h=sha256();edges=set();cross=[];internal=[[],[]]
    for i,j in combinations(range(N),2):
        x,y=minus(pts[i][0],pts[j][0]),minus(pts[i][1],pts[j][1])
        vv=plus(multiply(x,x),multiply(y,y))
        require(all(vv[k]==0 for k in range(8) if k not in (0,5,2,7)),'unexpected real-radical support')
        values=[Q(vv[k],L*L) for k in (0,5,2,7)]
        h.update((f'{i},{j}:'+','.join(f'{v.numerator}/{v.denominator}' for v in values)+'\n').encode())
        if values==[0,0,0,0]:require(aliases[i]==aliases[j],'unrecorded coincidence')
        if values==[1,0,0,0]:
            edges.add(tuple(sorted((aliases[i],aliases[j]))))
            if j<n:internal[0].append((i,j))
            elif i>=n:internal[1].append((i-n,j-n))
            else:cross.append([i,j-n])
    edges=sorted(edges);colours=list(map(int,row['positive_colouring']))
    require(len(colours)==N and all(c in range(4) for c in colours),'invalid colours')
    require(all(colours[i]==colours[aliases[i]] for i in range(N)),'overlap colours differ')
    require(all(i!=j and colours[i]!=colours[j] for i,j in edges),'improper positive colouring')
    require(len(set(aliases))==row['vertices'] and len(edges)==row['strict_edges'],'graph size mismatch')
    require([len(P),len(S)]==row['source_sizes'] and list(map(len,internal))==row['source_edges'],'source size mismatch')
    require(all(connected(len(G),es) for G,es in zip((P,S),internal)),'source disconnected')
    require(h.hexdigest()==row['squared_distance_sha256'],'full distance stream differs')
    require(sha256(''.join(f'{i},{j}\n' for i,j in edges).encode()).hexdigest()==row['edge_sha256'],'edge stream differs')
    require(cross==row['cross_edges'],'cross edges differ')
    checked_permutations=None
    if row['kind']=='residue_obstruction':
        colours0=[[small_residue(minus(x,G[0])) for x in G] for G in (P,S)]
        require([''.join(map(str,c)) for c in colours0]==row['source_residue_colours'],'residue strings differ')
        # Enumerate both arbitrary permutations (576), not only the producer's relative 24.
        successes=0
        for pi in permutations(range(4)):
            for sigma in permutations(range(4)):
                successes+=all(pi[colours0[0][i]]!=sigma[colours0[1][j]] for i,j in cross)
        require(successes==row['compatible_relative_permutations']==0,'permutation obstruction not reproduced')
        require(N==20 and len(edges)==28 and len(cross)==4,'small witness sizes differ')
        require(len({i for i,j in cross})==len({j for i,j in cross})==4,'cross edges not a matching')
        require(set(colours)=={0,1,2},'three-colouring changed')
        # Find and check a triangle, establishing chi=3 for this witness.
        es=set(edges);triangle=next((i,j,k) for i,j,k in combinations(range(N),3) if {(i,j),(i,k),(j,k)}<=es)
        checked_permutations=576
    else:triangle=None
    return {'case':row['case'],'vertices':len(first),'strict_edges':len(edges),'pairs_checked':N*(N-1)//2,
            'all_distance_entries_edges_colours_match':True,'both_sources_connected':True,
            'independently_checked_permutation_pairs':checked_permutations,'three_colour_triangle':triangle}

if __name__=='__main__':
    rows=json.loads((HERE/'expected.json').read_text())['cases'];configs=configurations()
    require(set(configs)=={r['case'] for r in rows},'fixture list differs')
    results=[run(r,configs[r['case']]) for r in rows]
    print(json.dumps({'cases_checked':len(results),'total_pair_checks':sum(r['pairs_checked'] for r in results),
                      'cases':results,'all_entries_match':True},indent=2))
