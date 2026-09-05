"""Independent source construction, local images, and Heron-polynomial census."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product,groupby,combinations
from collections import Counter
from math import isqrt
import importlib.util,json

HERE=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise ValueError(msg)

def source():
    p=HERE.parent/'hadwiger_nelson_mixed506_single_hub_reduction/check_examples.py'
    require(sha256(p.read_bytes()).hexdigest()=='8405039707b294ace3af5fd9deffc0a738c17133d442056a4013b9b4b588a50f','source arithmetic pin mismatch')
    spec=importlib.util.spec_from_file_location('generic_radical_source',p)
    R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
    def extract(z):
        x,y=z
        require(all(x[i]==0 for i in range(8) if i not in (0,6)) and
                all(y[i]==0 for i in range(8) if i not in (2,4)),'unexpected source radical support')
        return x[0],x[6],y[2],y[4]
    G,V=R.read(159),R.read(214)
    B=list(dict.fromkeys([R.cscale(x,6) for x in G]+[R.cmul(R.e(5,0,0,1),x) for x in G]))
    # Both source arrays have the common denominator 72.
    P=[extract(x) for x in B]
    S=[tuple(6*(a-b) for a,b in zip(extract(x),extract(V[0]))) for x in V]
    return P,S

def graph_info(G):
    n=len(G);edges=[];visited={0}
    for i,j in combinations(range(n),2):
        a,b,c,d=(x-y for x,y in zip(G[i],G[j]))
        if (a*a+33*b*b+3*c*c+11*d*d,2*(a*b+c*d))==(72**2,0):edges.append((i,j))
    while True:
        enlarged=visited|{j for i,j in edges if i in visited}|{i for i,j in edges if j in visited}
        if enlarged==visited:break
        visited=enlarged
    require(len(visited)==n,'disconnected source')
    return {'vertices':n,'edges':len(edges),'connected':True}

def local_images(P,S):
    # Independent finite lift: r=1+8t and 4t^2+t-2=0.
    # t mod 64 uniquely determines the needed r mod 512, more than the six bits used.
    ts=[t for t in range(64) if (4*t*t+t-2)%64==0]
    require(len(ts)==1,'local root not unique')
    r=1+8*ts[0]
    require((r*r-33)%1024==0 and r%8==1,'local branch failure')
    def image(x,rr):
        a,b,c,d=x
        aa=(3*a+3*b*rr+3*c+d*rr)%64
        bb=(6*c+2*d*rr)%64
        require(aa%8==bb%8==0,'source is not locally integral')
        return (aa//8*pow(27,-1,8))%8,(bb//8*pow(27,-1,8))%8
    return [[[image(x,r) for x in G],[image(x,-r) for x in G]] for G in (P,S)]

def modular_complex(P,S,p,roots,denominator=72):
    require(all(p%d for d in range(2,isqrt(p)+1)),'composite modulus')
    r3,r5,r11=roots
    require(all(r*r%p==d for r,d in zip(roots,(3,5,11))),'invalid radical roots')
    ii=next(t for t in range(p) if t*t%p==p-1)
    inv72=pow(denominator,-1,p);inv4=pow(4,-1,p)
    def pair(x):
        a,b,c,d=x
        re=(a+b*r3*r11)*inv72%p
        im=(c*r3+d*r11)*inv72%p
        return (re+ii*im)%p,(re-ii*im)%p
    p0,q0=[pair(x) for x in P],[pair(x) for x in S]
    u,ub=(1+ii*r3*r5)*inv4%p,(1-ii*r3*r5)*inv4%p
    require(u*ub%p==1,'modular rotation not unit')
    return [((z-u*w)%p,(zb-ub*wb)%p) for z,zb in p0 for w,wb in q0]

def heron(pts,ids,p):
    def n(i,j):return ((pts[i][0]-pts[j][0])*(pts[i][1]-pts[j][1]))%p
    a,b,c=n(ids[0],ids[1]),n(ids[0],ids[2]),n(ids[1],ids[2])
    return (a*b*c-4*a*b+(a+b-c)**2)%p

def digest_line(h,key,ids):
    h.update((','.join(map(str,key))+'|'+','.join(map(str,ids))+'\n').encode())

def run(expected):
    P,S=source();n=len(S);info=[graph_info(G) for G in (P,S)]
    require(info==[{'vertices':292,'edges':1251,'connected':True},{'vertices':214,'edges':977,'connected':True}],'source graph differs')
    require(set(S)=={(a,b,-c,-d) for a,b,c,d in S},'reflection invariance failed')
    tables=local_images(P,S)
    th=sha256((json.dumps(tables,separators=(',',':'))+'\n').encode()).hexdigest()
    require(th==expected['local_table_sha256'],'complete local source image streams differ')
    primes=[r['prime'] for r in expected['prime_roots']]
    require(primes==[1321,5281],'unexpected finite fields')
    offsets=[modular_complex(P,S,r['prime'],r['sqrt3_sqrt5_sqrt11']) for r in expected['prime_roots']]
    rows=[]
    for directions in product((0,1),repeat=2):
        records=[]
        for i in range(len(P)):
            for j in range(n):
                key=[];colours=[]
                for place,side in enumerate(directions):
                    z=tables[side][place][i if side==0 else j]
                    w=tables[1-side][place][j if side==0 else i]
                    key.extend(((w[0]-2*z[0])%8,(w[1]-2*z[1])%8))
                    colours.append((z[0]&1)+2*(z[1]&1))
                records.append((tuple(key),i*n+j,*colours))
        records.sort()
        groups=0;hist=Counter();counts=Counter();cell_hash=sha256();triple_hash=sha256();first_hash=sha256()
        for key,iterator in groupby(records,key=lambda r:r[0]):
            data=list(iterator);groups+=1;hist[len(data)]+=1
            masks=[0,0]
            for _,e,c,d in data:masks[0]|=1<<c;masks[1]|=1<<d
            if masks!=[15,15]:continue
            counts['cells']+=1;counts['contacts']+=len(data)
            digest_line(cell_hash,key,[r[1] for r in data])
            classes=[[r[1] for r in data if r[2]==c] for c in (0,1,2)]
            for ids in product(*classes):
                counts['triples']+=1;digest_line(triple_hash,key,ids)
                if heron(offsets[0],ids,primes[0]):continue
                counts['first']+=1;digest_line(first_hash,key,ids)
                if heron(offsets[1],ids,primes[1]):continue
                counts['both']+=1
        row={'deeper_sources':list(directions),'total_cells':groups,'cell_size_histogram':[list(x) for x in sorted(hist.items())],
             'saturated_cells':counts['cells'],'contacts_in_saturated_cells':counts['contacts'],
             'necessary_triples':counts['triples'],'pass_first_prime':counts['first'],'pass_both_primes':counts['both'],
             'saturated_cell_stream_sha256':cell_hash.hexdigest(),'triple_stream_sha256':triple_hash.hexdigest(),
             'first_prime_survivors_sha256':first_hash.hexdigest()}
        require(row==expected['rows'][len(rows)],'entry streams or census differ')
        require(counts['both']==0,'surviving necessary contact')
        rows.append(row)
    require(sum(r['necessary_triples'] for r in rows)==849532 and sum(r['pass_first_prime'] for r in rows)==693,'total census mismatch')
    return {'source_graphs':info,'independent_local_images_match':True,'contact_streams_match':True,
            'circle_formula':'Heron identity using complex/conjugate modular images',
            'total_triples':849532,'first_prime_survivors':693,'both_prime_survivors':0,
            'all_four_source_orderings_verified':True}

if __name__=='__main__':
    print(json.dumps(run(json.loads((HERE/'expected.json').read_text())),indent=2))
