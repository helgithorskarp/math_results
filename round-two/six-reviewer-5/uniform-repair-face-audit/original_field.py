"""Independent definition-level original orbit Grams over QQ(q,k).

Input: credited original affine table at source 628c20b9..., literal.py.
No target program, certificate or output is read or imported.
Bit 0=a, bit 1=b, bit 2=c. Coordinates are values on actual sets.
"""
import json
from pathlib import Path
from sympy import QQ, symbols

qs, ks = symbols('q k')
FIELD = QQ.frac_field(qs, ks)
q, k = (FIELD.convert(s) for s in (qs,ks))
ZERO, ONE = FIELD.zero, FIELD.one

def require(value, message):
    if not value:
        raise ValueError(message)

def choose(x, r):
    if r == 0: return ONE
    if r == 1: return x
    if r == 2: return x*(x-1)/2
    raise ValueError('orbit size outside literal carrier')

def table():
    s = 3*q+4; h = 1/(3*q+5)
    o,p,a,b,c,d,e = (0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)
    out = {}
    def add(x,y,u,v=ZERO): out[tuple(sorted((x,y)))] = (u,v)
    add(o,o,(6/q-q-4)/(q-1),1/(q-1))
    add(o,p,q*(q-3)/((q-1)*(q-2)))
    den=(q-2)*(q-3)/2
    add(p,p,(6/q+2*q/(q-1)-s+q*(q-1)/2)/den,
        (1-6*h*(q+1)/(q*(q-1)))/den)
    for leaf,vs in ((o,((1-1/q,ZERO),(1+1/q,ZERO),(1+6/q,ZERO))),
                    (p,((ONE,2*h/(q*(q-1))),
                        (1+2*(q-1)/(q*(q-2)),2*h/((q-1)*(q-2))),
                        (1+6/q,-6*h*(q+1)/(q*(q-1)))))):
        for typ, i in ((a,0),(c,0),(b,1),(d,1),(e,2)):
            add(leaf,typ,*vs[i])
    rr=3+2/q; ww=(s-rr)/(q-1)
    for x,y,u in ((a,a,ZERO),(a,b,ZERO),(b,b,ZERO),(a,c,2),
                  (a,d,rr),(b,c,rr),(b,d,ww)):
        add(x,y,u)
    return out

def flip(c): return (c&1) | ((c&2)<<1) | ((c&4)>>1)

def original():
    """23 literal S_Z x S_W orbit indicators; no harmonic short imported."""
    keys = sorted((c,z,w) for c in range(8) for z in range(3) for w in range(3)
                  if (1 <= c.bit_count()+z+w <= 2 or
                      c.bit_count()+z+w == 3 and c.bit_count() >= 2)
                  and (c,z,w) != (6,1,0))
    require(len(keys)==23,'complete original orbit count')
    masses=[choose(k,z)*choose(q-k,w) for c,z,w in keys]
    N=(q*q+13*q+16)/2-k; s=3*q+4
    require(sum(masses,ZERO)==N-1,'entire original member count')
    T=table(); C=[]; D=[]; U=[]
    for i,(c,z,w) in enumerate(keys):
        cr=[]; dr=[]; ur=[]
        for j,(cc,zz,ww) in enumerate(keys):
            count=ZERO if c&cc else choose(k-z,zz)*choose(q-k-w,ww)
            a,b=T[tuple(sorted(((c.bit_count(),z+w),(cc.bit_count(),zz+ww))))] if count else (ZERO,ZERO)
            diag=s*masses[i] if i==j else ZERO
            val=diag-masses[i]*masses[j]+masses[i]*count*a
            cr.append(val); dr.append(masses[i]*count*b)
            ur.append((N*masses[i] if i==j else ZERO)-masses[i]*masses[j]-val)
        C.append(cr); D.append(dr); U.append(ur)
    require(all(A[i][j]==A[j][i] for A in (C,D,U) for i in range(23) for j in range(23)),
            'all original coefficient forms symmetric')
    return keys,masses,C,D,U

def even():
    keys,masses,C,D,U=original()
    reps=sorted(set((min(c,flip(c)),z,w) for c,z,w in keys))
    groups=[[i for i,(c,z,w) in enumerate(keys) if (min(c,flip(c)),z,w)==rep] for rep in reps]
    require(len(groups)==17,'all even original orbits')
    def gram(A):
        return [[sum((A[i][j] for i in I for j in J),ZERO) for J in groups] for I in groups]
    return reps,[sum((masses[i] for i in I),ZERO) for I in groups],gram(C),gram(D),gram(U)

def solve(A,B):
    """Our row-normalized rational-field Gaussian elimination, all equations checked."""
    zero=A[0][0]*0
    n=len(A); r=len(B[0]); W=[list(A[i])+list(B[i]) for i in range(n)]
    for p in range(n):
        pivot=next((i for i in range(p,n) if W[i][p]),None)
        require(pivot is not None,'nonzero original solve pivot')
        W[p],W[pivot]=W[pivot],W[p]
        d=W[p][p]
        W[p]=[x/d for x in W[p]]
        for i in range(p+1,n):
            f=W[i][p]
            if f: W[i]=[W[i][j]-f*W[p][j] for j in range(n+r)]
    X=[[zero]*r for _ in range(n)]
    for i in range(n-1,-1,-1):
        for j in range(r): X[i][j]=W[i][n+j]-sum((W[i][l]*X[l][j] for l in range(i+1,n)),zero)
    require(all(sum((A[i][l]*X[l][j] for l in range(n)),zero)==B[i][j]
                for i in range(n) for j in range(r)),'every original stationary equation')
    return X

def short(A, anchors, excluded=(), masses=None):
    zero=A[0][0]*0; one=zero+1
    rest=[i for i in range(len(A)) if i not in anchors and i not in excluded]
    weights=[masses[i] if masses else one for i in rest]
    B=[[A[i][j]/weights[ii] for j in rest] for ii,i in enumerate(rest)]
    X=[[-A[i][j]/weights[ii] for j in anchors] for ii,i in enumerate(rest)]
    Y=solve(B,X)
    V=[[zero]*len(anchors) for _ in A]
    for i,j in enumerate(anchors): V[j][i]=one
    for i,j in enumerate(rest): V[j]=Y[i]
    S=[[A[i][j]+sum((A[i][l]*V[l][jj] for l in rest),zero)
        for jj,j in enumerate(anchors)] for i in anchors]
    require(all(S[i][j]==S[j][i] for i in range(len(S)) for j in range(len(S))), 'symmetric short')
    return S,V

def energy(A,V):
    zero=A[0][0]*0
    r=len(V[0])
    return [[sum((V[i][a]*A[i][j]*V[j][b] for i in range(len(A)) for j in range(len(A)) if V[i][a] and A[i][j] and V[j][b]),zero)
             for b in range(r)] for a in range(r)]

def serialize(x):
    if hasattr(x,'as_expr'):return str(x.as_expr())
    if isinstance(x,dict): return {a:serialize(b) for a,b in x.items()}
    if isinstance(x,list): return [serialize(y) for y in x]
    if isinstance(x,tuple): return list(x)
    return x

def write(name, data):
    p=Path(__file__).resolve().parent/(name+'.json')
    p.write_text(json.dumps(serialize(data),indent=2)+'\n')

def cap():
    keys,m,C,D,U=even()
    anchors=[keys.index(t) for t in ((1,0,0),(3,0,0),(2,0,0))]
    print('cap complete17 original Gram; short14',flush=True)
    M,V=short(U,anchors,masses=m)
    write('cap-original',dict(keys=keys,masses=m,M=M,V=V,Delta=energy(D,V)))
    print('cap original solve and derivative saved',flush=True)

def lower():
    keys,m,C,D,U=even()
    anchors=[keys.index(t) for t in ((2,0,0),(3,0,0))]
    excluded=[keys.index((1,0,0)),keys.index((0,1,0))]
    print('lower complete17 original Gram; star and zeta gauge; short13',flush=True)
    S,V=short(C,anchors,excluded,m)
    require(S[0][0]==S[0][1]==S[1][0]==S[1][1],'even lower rank-one normalization')
    a=S[0][0]
    z=[ONE if c==0 else -ONE if c==7 else ZERO for c,z,w in keys]
    alpha=sum((z[i]*D[i][j]*z[j] for i in range(17) for j in range(17) if z[i] and D[i][j] and z[j]),ZERO)
    require(alpha==q*(q+1)/2+3*(q+1)/(3*q+5),'literal zeta energy')
    ed=energy(D,V)
    cross=[sum((z[i]*D[i][j]*V[j][a] for i in range(17) for j in range(17) if z[i] and D[i][j] and V[j][a]),ZERO) for a in range(2)]
    deriv=[[ed[i][j]-cross[i]*cross[j]/alpha for j in range(2)] for i in range(2)]
    require(deriv[0][0]==deriv[0][1]==deriv[1][0]==deriv[1][1],'best-gauge derivative normalization')
    write('lower-original',dict(keys=keys,masses=m,a=a,V=V,alpha=alpha,best_gauge=cross[0]/alpha,derivative=deriv[0][0]))
    print('lower original solve and derivative saved',flush=True)

if __name__=='__main__':
    import sys
    {'cap':cap,'lower':lower}[sys.argv[1]]()
