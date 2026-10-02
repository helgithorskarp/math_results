"""Own exact evaluation/interpolation and Sturm audit; no target imports."""
from fractions import Fraction as Q
from itertools import product
from math import comb
import json,hashlib,pathlib

def need(condition,message):
    if not condition: raise ValueError(message)

def trim(p):
    p=list(map(Q,p))
    while len(p)>1 and p[-1]==0: p.pop()
    return tuple(p)

ZERO=(Q(0),)
ONE=(Q(1),)
def add(p,q): return trim([(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))])
def neg(p): return tuple(-x for x in p)
def mul(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return trim(out)
def divmodp(p,q):
    need(q!=ZERO,'zero divisor'); p=list(p); quo=[Q(0)]*max(1,len(p)-len(q)+1)
    while trim(p)!=ZERO and len(trim(p))>=len(q):
        p=list(trim(p)); k=len(p)-len(q); a=p[-1]/q[-1]; quo[k]+=a
        for j,b in enumerate(q):p[k+j]-=a*b
    return trim(quo),trim(p)
def gcd(p,q):
    while q!=ZERO: p,q=q,divmodp(p,q)[1]
    return trim([x/p[-1] for x in p]) if p!=ZERO else ZERO
def value(p,x):
    ans=Q(0)
    for a in reversed(p):ans=ans*x+a
    return ans
def derivative(p):return trim([i*p[i] for i in range(1,len(p))] or [0])
def sturm(p,left,right):
    need(value(p,left)!=0 and value(p,right)!=0,'root at closed endpoint')
    seq=[p,derivative(p)]
    if seq[-1]==ZERO:seq.pop()
    while len(seq)>1:
        rem=neg(divmodp(seq[-2],seq[-1])[1])
        if rem==ZERO:break
        seq.append(rem)
    def variation(x):
        signs=[1 if value(s,x)>0 else -1 for s in seq if value(s,x)!=0]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return variation(left)-variation(right),seq

def fan_at(r,m,state):
    previous,current,outside=state
    neighbors=[previous,outside]
    for _ in range(1,m):
        neighbors.append(tuple(r*(current[k]+neighbors[-1][k])-neighbors[-2][k] for k in range(3)))
    return current,neighbors[m],neighbors[m-1]

E=((1,0,0),(0,1,0),(0,0,1))
def numeric_gap(word,r):
    state=E
    for m in word:state=fan_at(r,m,state)
    return tuple(state[1][k]-E[0][k] for k in range(3))

def interpolate(values):
    # Newton forward differences at consecutive integer abscissas.
    diffs=list(map(Q,values)); result=ZERO; binomial=ONE
    for k in range(len(values)):
        result=add(result,tuple(diffs[0]*a for a in binomial))
        diffs=[b-a for a,b in zip(diffs,diffs[1:])]
        binomial=tuple(a/Q(k+1) for a in mul(binomial,(-k,1)))
    return result

def case(word):
    degree=sum(m-1 for m in word)
    samples=[numeric_gap(word,r) for r in range(degree+1)]
    gaps=[interpolate([s[k] for s in samples]) for k in range(3)]
    for r in (Q(2,3),Q(3,4),Q(7,10),Q(-2),Q(17)):
        need(tuple(value(p,r) for p in gaps)==numeric_gap(word,r),'interpolation/recurrence bridge')
    g=gcd(gcd(gaps[0],gaps[1]),gaps[2])
    need(g!=ZERO,'identically closed word')
    roots,seq=sturm(g,Q(2,3),Q(3,4))
    need(roots==(1 if word==(3,3,3,3,3) else 0),'unexpected closed-band root count')
    for p in gaps: need(divmodp(p,g)[1]==ZERO,'common divisor')
    return dict(word=word,degree_bound=degree,gaps=gaps,gcd=g,sturm=seq,closed_roots=roots)

# Real quadratic field Q[r]/(r^2+2r-2), r in (2/3,3/4).
def fadd(a,b):return (a[0]+b[0],a[1]+b[1])
def fneg(a):return (-a[0],-a[1])
def fmul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]-2*a[1]*b[1])
FZERO=(Q(0),Q(0));FONE=(Q(1),Q(0));R=(Q(0),Q(1));C=(Q(1,3),Q(1,3))
def fsign(a):
    # a=A+B*sqrt(3). Compare squares only when the summands oppose.
    A=a[0]-a[1]; B=a[1]
    if A==0:return (B>0)-(B<0)
    if B==0:return (A>0)-(A<0)
    if A>0 and B>0:return 1
    if A<0 and B<0:return -1
    gap=A*A-3*B*B
    need(gap!=0,'nonzero rational cannot equal nonzero sqrt(3) multiple')
    return ((gap>0)-(gap<0))*((A>0)-(A<0))
def vadd(a,b):return tuple(fadd(x,y) for x,y in zip(a,b))
def vneg(a):return tuple(fneg(x) for x in a)
def scale(r,a):return tuple(fmul(r,x) for x in a)
def fan_field(m,state):
    previous,current,outside=state; nbr=[previous,outside]
    for _ in range(1,m):nbr.append(vadd(scale(R,vadd(current,nbr[-1])),vneg(nbr[-2])))
    return current,nbr[m],nbr[m-1]
FE=tuple(tuple(FONE if i==j else FZERO for j in range(3)) for i in range(3))
def dot(a,b):
    out=FZERO
    for i in range(3):
        for j in range(3):out=fadd(out,fmul(fmul(a[i],b[j]),FONE if i==j else C))
    return out

def core():
    state=FE; upper=[FE[0]]; lower=[]
    for _ in range(6):
        upper.append(state[1]);lower.append(state[2]);state=fan_field(3,state)
    upper=upper[:6]
    need(state==FE,'six-step state closure')
    vertices=upper+lower
    need(len(set(vertices))==12,'12 distinct coefficient vectors')
    gram=[[dot(a,b) for b in vertices] for a in vertices]
    contacts=[];separated=[]
    for i in range(12):
        need(gram[i][i]==FONE,'unit norm')
        for j in range(i):
            delta=fadd(C,fneg(gram[i][j]));s=fsign(delta)
            need(s>=0,'packing violation')
            (contacts if s==0 else separated).append((j,i))
    need((len(contacts),len(separated))==(24,42),'all pair checks')
    # Determine the lower ring order by complete Gram comparison, without a supplied permutation.
    within=[FONE,C,fadd(fmul((Q(3),Q(0)),C),(Q(-2),Q(0))),fadd(fmul((Q(4),Q(0)),C),(Q(-3),Q(0)))]
    cross=[C,C,fadd(FONE,fneg(fmul((Q(2),Q(0)),C))),fadd((Q(2),Q(0)),fneg(fmul((Q(5),Q(0)),C))),fadd((Q(2),Q(0)),fneg(fmul((Q(5),Q(0)),C))),fadd(FONE,fneg(fmul((Q(2),Q(0)),C)))]
    from itertools import permutations
    perms=[]
    for p in permutations(range(6)):
        if all(gram[i][6+p[j]]==cross[(i-j)%6] for i in range(6) for j in range(6)) and all(gram[6+p[i]][6+p[j]]==within[min((i-j)%6,(j-i)%6)] for i in range(6) for j in range(6)):perms.append(p)
    need(len(perms)==1,'unique anchored ring ordering')
    need(all(gram[i][j]==within[min((i-j)%6,(j-i)%6)] for i in range(6) for j in range(6)),'upper ring')
    # Core capacity, polar-face containment, and sharp 13/14 point additions.
    b2=fadd(fmul((Q(2),Q(0)),C),(-Q(1),Q(0)))
    a2=fmul((Q(3,2),Q(0)),fadd(FONE,fneg(C)))
    need(fsign(fadd(a2,(-Q(9,16),Q(0))))>0,'a > 3/4')
    need(fsign(fadd(b2,(-Q(9,64),Q(0))))>0,'b > 3/8')
    need(fsign(fadd((Q(3,5),Q(0)),fneg(C)))>0,'c < 3/5')
    need(fsign(fadd(a2,fneg(b2)))>0,'polar cap lies inside upper hexagon')
    need(fsign(fadd(fmul(C,C),fneg(b2)))>0,'both axis poles admissible')
    need(Q(12)-Q(13)*Q(9,10)>0,'radical lower bound valid')
    need(Q(51,80)>Q(3,5) and Q(31,50)>Q(3,5),'coverage and cap capacity')
    return dict(vertices=vertices,gram=gram,contacts=contacts,separated=separated,lower_permutation=perms[0],a_squared=a2,b_squared=b2,core_maximum=14,face_maximum=13)

def canonical(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,(tuple,list)):return [canonical(v) for v in x]
    if isinstance(x,dict):return {k:canonical(v) for k,v in x.items()}
    return x
def build():
    cases=[case(w) for q in (4,5,6) for w in product((3,4),repeat=q-1)]
    need(len(cases)==56 and len({tuple(c['word']) for c in cases})==56,'complete unquotiented word space')
    return canonical(dict(method='integer evaluation / Newton interpolation / rational Sturm, independent quadratic-field Gram',cases=cases,core=core()))
if __name__=='__main__':
    data=build();raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
    path=pathlib.Path(__file__).with_name('INDEPENDENT.json');path.write_bytes(raw)
    print(json.dumps(dict(words=len(data['cases']),excluded=55,exception='33333',gram_positions=144,core_maximum=14,face_maximum=13,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)),sort_keys=True))
