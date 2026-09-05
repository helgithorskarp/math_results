"""Complete necessary-contact census for B292/uV214, u=(1+i sqrt(15))/4."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
from collections import defaultdict,Counter
from itertools import product
from math import isqrt
import importlib.util,json

HERE=Path(__file__).resolve().parent
PRIMES=(1321,5281)

def require(ok,msg):
    if not ok:raise ValueError(msg)

def load(name,path,pin):
    p=HERE.parent/path
    require(sha256(p.read_bytes()).hexdigest()==pin,'source pin mismatch: '+path)
    s=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m

A=load('local_arithmetic','hadwiger_nelson_integral_trace_gluing/arithmetic.py',
       '88c522f63ddca3b26b71e21003964c52b0da89891ded6c310274b4ddb54a7b7e')
F=load('gadget_source','hadwiger_nelson_mixed505_all_gadget_anchors/verify.py',
       '526b12cbd9d28217e59feb7191c93ace4e5a572ebeadd66cdf384393126aee38')

def gadgets():
    G,V=F.read_points(159),F.read_points(214)
    B=list(dict.fromkeys([tuple(6*a for a in x) for x in G]+
        [(5*a-11*d,5*b-c,5*c+11*b,5*d+a) for a,b,c,d in G]))
    P=[tuple(Q(a,72) for a in x) for x in B]
    S=[tuple(Q(a-b,12) for a,b in zip(x,V[0])) for x in V]
    require(len(P)==292 and len(S)==214 and len(set(P))==292 and len(set(S))==214,'bad sources')
    require(set(S)=={A.bar(x) for x in S},'second source not conjugation-invariant')
    return P,S

def sigma(x):a,b,c,d=x;return a,-b,c,-d

def local_tables(P,S):
    return [[[A.local(x,3) for x in G],[A.local(sigma(x),3) for x in G]] for G in (P,S)]

def colour(tables,side,place,label):
    a,b=tables[side][place][label]
    return a%2+2*(b%2)

def prime_data(p):
    require(p>=2 and all(p%d for d in range(2,isqrt(p)+1)),'modulus not prime')
    roots=[next(x for x in range(p) if x*x%p==d) for d in (3,5,11)]
    require(all(r*r%p==d for r,d in zip(roots,(3,5,11))),'radical root failure')
    return roots

def modular_offsets(P,S,p,roots):
    r3,r5,r11=roots;r33=r3*r11%p;den=pow(4,-1,p)
    def image(x):
        a,b,c,d=[v.numerator*pow(v.denominator,-1,p)%p for v in x]
        return (a+b*r33)%p,(c*r3+d*r11)%p
    p0=[image(x) for x in P];q0=[image(y) for y in S]
    cosine=den;sine=r3*r5*den%p
    q0=[((cosine*x-sine*y)%p,(sine*x+cosine*y)%p) for x,y in q0]
    return [((x-X)%p,(y-Y)%p) for x,y in p0 for X,Y in q0]

def circle_polynomial(pts,ids,p):
    x0,y0=pts[ids[0]]
    v,w=[((pts[e][0]-x0)%p,(pts[e][1]-y0)%p) for e in ids[1:]]
    aa=(v[0]*v[0]+v[1]*v[1])%p;bb=(w[0]*w[0]+w[1]*w[1])%p
    delta=(v[0]*w[1]-v[1]*w[0])%p
    nx=(aa*w[1]-bb*v[1])%p;ny=(bb*v[0]-aa*w[0])%p
    return (nx*nx+ny*ny-4*delta*delta)%p

def update_hash(h,key,ids):
    h.update((','.join(map(str,key))+'|'+','.join(map(str,ids))+'\n').encode())

def run():
    P,S=gadgets();n=len(S);tables=local_tables(P,S)
    roots=[prime_data(p) for p in PRIMES]
    offsets=[modular_offsets(P,S,p,r) for p,r in zip(PRIMES,roots)]
    # Pin every local source image, including both places and both sources.
    table_hash=sha256((json.dumps(tables,separators=(',',':'))+'\n').encode()).hexdigest()
    rows=[]
    for directions in product((0,1),repeat=2):
        cells=defaultdict(list)
        for i in range(len(P)):
            for j in range(len(S)):
                key=[]
                for place,side in enumerate(directions):
                    deep=tables[side][place][(i,j)[side]]
                    shallow=tables[1-side][place][(i,j)[1-side]]
                    key.extend((shallow[c]-2*deep[c])%8 for c in (0,1))
                cells[tuple(key)].append(i*n+j)
        counts=Counter();hist=Counter(map(len,cells.values()));cell_hash=sha256();all_hash=sha256();pass_hash=sha256()
        for key,es in sorted(cells.items()):
            masks=[]
            for place,side in enumerate(directions):
                masks.append({colour(tables,side,place,divmod(e,n)[side]) for e in es})
            if any(len(mask)<4 for mask in masks):continue
            counts['saturated_cells']+=1;counts['contacts_in_saturated_cells']+=len(es)
            update_hash(cell_hash,key,es)
            classes=[[e for e in es if colour(tables,directions[0],0,divmod(e,n)[directions[0]])==c] for c in range(3)]
            require(all(classes),'empty required colour class')
            for ids in product(*classes):
                counts['necessary_triples']+=1;update_hash(all_hash,key,ids)
                if circle_polynomial(offsets[0],ids,PRIMES[0]):continue
                counts['pass_first_prime']+=1;update_hash(pass_hash,key,ids)
                if circle_polynomial(offsets[1],ids,PRIMES[1]):continue
                counts['pass_both_primes']+=1
        require(counts['pass_both_primes']==0,'unclosed exact contact frontier')
        rows.append({'deeper_sources':directions,'total_cells':len(cells),
                     'cell_size_histogram':sorted(hist.items()),
                     'saturated_cells':counts['saturated_cells'],
                     'contacts_in_saturated_cells':counts['contacts_in_saturated_cells'],
                     'necessary_triples':counts['necessary_triples'],'pass_first_prime':counts['pass_first_prime'],
                     'pass_both_primes':counts['pass_both_primes'],
                     'saturated_cell_stream_sha256':cell_hash.hexdigest(),
                     'triple_stream_sha256':all_hash.hexdigest(),'first_prime_survivors_sha256':pass_hash.hexdigest()})
    return {'source_sizes':[len(P),len(S)],'prospective_contacts':len(P)*len(S),'local_modulus':8,
            'local_table_sha256':table_hash,'prime_roots':[{'prime':p,'sqrt3_sqrt5_sqrt11':r} for p,r in zip(PRIMES,roots)],
            'rows':rows,'total_necessary_triples':sum(r['necessary_triples'] for r in rows),
            'total_first_prime_survivors':sum(r['pass_first_prime'] for r in rows),
            'total_both_prime_survivors':sum(r['pass_both_primes'] for r in rows),
            'all_translations_closed_requires_PROOF_md':True}

if __name__=='__main__':print(json.dumps(run(),indent=2))
