#!/usr/bin/env python3
"""Exact full4+2+1+1 angular certificate, standard library only.
Sparse Fraction kernel adapted from own8800/source167af56c25651784f7c8106a3ec1d85e52b51c82.
Degree-bounded integer Sylvester checks credit reviewer8859/source67721b3d70cfa96def249295f182a5f63b4969a5.
New quotient-remainder interpolation avoids high-degree lift inversion.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
from math import comb,gcd,lcm,factorial
from itertools import permutations
import argparse,hashlib,json,sys,time

def require(value, message):
    if not value:
        raise ValueError(message)


def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]:p.pop()
    return p


def pa(p,q):
    out=[Q(0)]*max(len(p),len(q))
    for i,c in enumerate(p):out[i]+=c
    for i,c in enumerate(q):out[i]+=c
    return trim(out)


def ps(p,c):return trim([x*c for x in p])


def pm(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,c in enumerate(p):
        for j,d in enumerate(q):out[i+j]+=c*d
    return trim(out)


def pd(p):return trim([i*p[i] for i in range(1,len(p))] or [Q(0)])


def pe(p,x):
    value=Q(0)
    for c in reversed(p):value=value*x+c
    return value


def pdiv(p,q):
    p,q=trim(list(map(Q,p))),trim(list(map(Q,q)))
    require(q!=[0],'zero polynomial denominator')
    quotient=[Q(0)]*max(1,len(p)-len(q)+1)
    while p!=[0] and len(p)>=len(q):
        k,c=len(p)-len(q),p[-1]/q[-1]
        quotient[k]+=c;p=pa(p,ps([Q(0)]*k+q,-c))
    return trim(quotient),p


def pgcd(p,q):
    while q!=[0]:p,q=q,pdiv(p,q)[1]
    return ps(p,1/p[-1])


class MP:
    """Sparse Q-polynomials in three indeterminates, no CAS dependency."""
    def __init__(self,value=0):
        if isinstance(value,MP):self.d=value.d;return
        if isinstance(value,dict):self.d={k:Q(v) for k,v in value.items() if v}
        else:self.d={(0,0,0):Q(value)} if value else {}
    @staticmethod
    def variable(i):
        k=[0,0,0];k[i]=1;return MP({tuple(k):1})
    def __add__(self,other):
        out=dict(self.d)
        for k,v in MP(other).d.items():out[k]=out.get(k,Q(0))+v
        return MP(out)
    __radd__=__add__
    def __neg__(self):return MP({k:-v for k,v in self.d.items()})
    def __sub__(self,other):return self+-MP(other)
    def __rsub__(self,other):return MP(other)+-self
    def __mul__(self,other):
        out={}
        for k,v in self.d.items():
            for l,w in MP(other).d.items():
                key=tuple(a+b for a,b in zip(k,l));out[key]=out.get(key,Q(0))+v*w
        return MP(out)
    __rmul__=__mul__
    def __truediv__(self,other):return self*(Q(1)/other)
    def __pow__(self,n):
        out=MP(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,other):return self.d==MP(other).d
    def __bool__(self):return bool(self.d)
    def derivative(self,i):
        out={}
        for k,v in self.d.items():
            if k[i]:
                l=list(k);l[i]-=1;out[tuple(l)]=v*k[i]
        return MP(out)
    def square_variable(self):
        require(all(k[0]%2==0 for k in self.d),'odd center power')
        return MP({(k[0]//2,k[1],k[2]):v for k,v in self.d.items()})
    def third_to_one(self):
        out={}
        for k,v in self.d.items():
            key=(k[0],k[1],0);out[key]=out.get(key,Q(0))+v
        return MP(out)
    def primitive_integer(self):
        denominator=lcm(*(v.denominator for v in self.d.values()))
        ints={k:int(v*denominator) for k,v in self.d.items()}
        content=gcd(*ints.values())
        return MP({k:v//content for k,v in ints.items()})


def zpm(p,q):
    out=[MP(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]=out[i+j]+x*y
    return out
def zpow(p,n):
    out=[MP(1)]
    for _ in range(n):out=zpm(out,p)
    return out
def det3(G):
    out=MP(0)
    for p in permutations(range(3)):
        sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        out+=sign*G[0][p[0]]*G[1][p[1]]*G[2][p[2]]
    return out


def sturm(p):
    def norm(a):return ps(a,1/abs(a[-1]))
    a,b=norm(trim(list(map(Q,p)))),norm(pd(list(map(Q,p))));out=[a,b]
    while True:
        r=ps(pdiv(a,b)[1],-1)
        if r==[0]:break
        r=norm(r);out.append(r);a,b=b,r
    return out
def variations(chain,x):
    signs=[]
    for p in chain:
        if x=='+inf':a=p[-1]
        else:a=pe(p,x)
        if a:signs.append(1 if a>0 else -1)
    return sum(a!=b for a,b in zip(signs,signs[1:]))
def count(chain,a,b):return variations(chain,a)-variations(chain,b)
def ivadd(a,b):return a[0]+b[0],a[1]+b[1]
def ivmul(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def ivpoly(p,x):
    out=(Q(0),Q(0))
    for c in reversed(p):out=ivadd(ivmul(out,x),(c,c))
    return out
def ivquot(n,d,x):
    a,b=ivpoly(n,x),ivpoly(d,x);require(b[0]>0 or b[1]<0,'lift interval denominator containszero')
    return ivmul(a,(1/b[1],1/b[0]))
def ivmp(p,boxes):
    powers=[]
    for box in boxes:
        values=[(Q(1),Q(1))]
        for _ in range(10):values.append(ivmul(values[-1],box))
        powers.append(values)
    out=(Q(0),Q(0))
    for exponents,c in p.d.items():
        term=(c,c)
        for i,k in enumerate(exponents):term=ivmul(term,powers[i][k])
        out=ivadd(out,term)
    return out


def at_first_one(poly):
    out={}
    for (i,j,k),v in poly.d.items():
        key=(j,k,0);out[key]=out.get(key,Q(0))+v
    return MP(out)


def family_kernel():
    a,b,V=[MP.variable(i) for i in range(3)];c=-2*a-b
    moments=[4*a**k+2*b**k+2*sum(comb(k,j)*c**(k-j)*V**(j//2)
              for j in range(0,k+1,2)) for k in range(1,5)]
    N,S3,S4=moments[1:];mu2=S4-N*N/8
    A=[-a,MP(1)];B=[-b,MP(1)];S=[c*c-V,-2*c,MP(1)]
    f=zpm(zpm(zpow(A,4),zpow(B,2)),S)
    h=[-a**3-Q(5,2)*a*a*b-2*a*b*b-b**3/2+V*a/4+V*b/2,
       Q(3,2)*a*a-b*b/2-Q(3,4)*V,3*a+b,MP(1)]
    derivative=[Q(i,8)*f[i] for i in range(1,9)]
    require(derivative==zpm(zpm(zpow(A,3),B),h),'original derivative factorization')
    powers=[MP(3)]
    for k in range(1,5):
        if k<=3:val=-k*h[3-k]-sum(h[3-j]*powers[k-j] for j in range(1,k))
        else:val=-sum(h[3-j]*powers[k-j] for j in range(1,4))
        powers.append(val)
    G=[[powers[i+j] for j in range(3)] for i in range(3)]
    D=det3(G);mu=[N,S3,mu2];E=MP(0)
    for i in range(3):
        for j in range(3):
            rows=[a for a in range(3) if a!=j];cols=[a for a in range(3) if a!=i]
            minor=G[rows[0]][cols[0]]*G[rows[1]][cols[1]]-G[rows[0]][cols[1]]*G[rows[1]][cols[0]]
            E+=(-1)**(i+j)*mu[i]*minor*mu[j]
    nraw,dra=N*N*D-E,mu2*D
    den=lcm(*(v.denominator for p in [nraw,dra] for v in p.d.values()))
    content=gcd(*(int(v*den) for p in [nraw,dra] for v in p.d.values()))
    scalar=Q(den,content)
    require(scalar>0,'nonpositive ratio normalization')
    return {'balance':moments[0],'N':N,'S3':S3,'S4':S4,'mu2':mu2,'h':h,'D':D,
            'n':scalar*nraw,'d':scalar*dra,'positive_scalar':scalar}


def coeff_in_V(poly):
    deg=max(k[1] for k in poly.d);out=[[Q(0)] for _ in range(deg+1)]
    for (i,j,k),v in poly.d.items():
        require(k==0 and v.denominator==1,'noninteger chart coefficient')
        if len(out[j])<=i:out[j]+=[Q(0)]*(i+1-len(out[j]))
        out[j][i]+=v
    return [trim(x) for x in out]


def sylvester(p,q,j):
    m,n=len(p)-1,len(q)-1;width=m+n-j;rows=[]
    for coefficients,shifts in [(p,n-j),(q,m-j)]:
        for shift in range(shifts-1,-1,-1):
            row=[[Q(0)]]*width
            for degree,entry in enumerate(coefficients):row[width-1-degree-shift]=entry
            rows.append(row)
    return rows


def integer_det(matrix):
    require(all(Q(x).denominator==1 for row in matrix for x in row),'noninteger determinant entry')
    A=[[int(x) for x in row] for row in matrix];n=len(A);previous=1;sign=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if A[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:A[k],A[pivot]=A[pivot],A[k];sign=-sign
        value=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                raw=value*A[i][j]-A[i][k]*A[k][j]
                require(raw%previous==0,'inexact integer Bareiss division')
                A[i][j]=raw//previous
            A[i][k]=0
        previous=value
    return sign*A[-1][-1]


def evaluate_matrix(rows,x):
    return [[int(pe(p,Q(x))) for p in row] for row in rows]


def interpolation_remainder(values,modulus):
    """Newton forward interpolation at0,1,..., followed by exact remainder.

    Written degree bounds make this the true determinant residue, not a fit.
    """
    differences=list(map(Q,values));basis=[Q(1)];result=[Q(0)]
    for j in range(len(values)):
        result=pdiv(pa(result,ps(basis,differences[0])),modulus)[1]
        differences=[differences[i+1]-differences[i] for i in range(len(differences)-1)]
        basis=pdiv(ps(pm(basis,[Q(-j),Q(1)]),Q(1,j+1)),modulus)[1]
    return result


def strip_bernstein(n,d,interval,constant=Q(49,2)):
    # Write(c0*d-n)(b,(b+2)^2*t) as a power polynomial in t.
    compare=constant*d-n;deg=max(k[1] for k in compare.d);power=[]
    require(deg==5,'wrong vertical comparison degree')
    for j in range(deg+1):
        coefficient=[Q(0)]*(1+max(k[0] for k in compare.d))
        for (i,l,k),v in compare.d.items():
            if l==j:coefficient[i]+=v
        coefficient=pm(trim(coefficient),[Q(comb(2*j,k)*2**(2*j-k)) for k in range(2*j+1)])
        power.append(ivpoly(coefficient,interval))
    return [tuple(sum(power[j][endpoint]*Q(comb(k,j),comb(deg,j)) for j in range(k+1))
                  for endpoint in range(2)) for k in range(deg+1)]


def encode(value):
    if isinstance(value,MP):return [[list(k),str(v)] for k,v in sorted(value.d.items())]
    if isinstance(value,dict):return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [encode(v) for v in value]
    if isinstance(value,Q):return str(value)
    return value



RESULTANT_CONSTANT=64746450275303866948070372892066447360000000000
FACTORS=[([5, 3], 1, []), ([3, 1], 14, []), ([1, 1], 30, []), ([-1, 1], 36, []), ([135, 279, 213, 59], 5, [['-154950537/110721848', '-17167585/12267313']]), ([4575, 11695, 11175, 4737, 746], 1, [['-43415548/37051287', '-72058245/61495267']]), ([153420, 493235, 670890, 501005, 221896, 58173, 8290, 483], 1, [['-2053727671/1035289221', '-2051999328/1034417959'], ['-56942787/41994212', '-35402656/26108779']]), ([13577625, 69971850, 162173745, 222802920, 201912750, 127491060, 57859454, 19116664, 4513161, 694210, 52001], 1, []), ([2052772875, 12939306525, 38099967975, 70219787625, 91155693375, 88475160985, 66282475115, 38979362325, 18145203945, 6702541551, 1956044829, 444070515, 75732717, 9058107, 665201, 22063], 1, [['-49436476/58960831', '-55626425/66343326']]), ([3943145899579423764375, 52294782664648540449000, 277273132842475952080425, 585057794944484553903000, -1007058072488799528943425, -10960956860201698466611800, -38817312296090116148504055, -86584913744758376943360960, -136294279570097039635950645, -155399503503795392258461800, -124955609426870310119943531, -62830711401591952407502728, -11609473977804115003748877, -1031511953184568425125928, -25310258226242287735706955, -55728126179692434052727616, -68815969637535702905598027, -60843443607469303450279464, -41967455314093502492638709, -23491371010652216416684920, -10884096115581244319029587, -4211632374326947877250664, -1362759347316683664775701, -366577032451086702738432, -80845374432701763954903, -14259343653712327407192, -1928004644844433400073, -185143522331993163160, -10689523856761888671, -188493371233567512, 9999080315788183], 1, [['-49066144/26819333', '-79574451/43495036'], ['-173564627/131671605', '-16097627/12212168'], ['-6659153/7061687', '-165070926/175049171'], ['-134862634/319382803', '-3903617/9244578']])]


def verify(progress=False):
    records={}
    def check(name,actual,expected):
        require(actual==expected,name+' failed');records[name]=encode(actual)
    def note(message):
        if progress:print(message,file=sys.stderr,flush=True)
    derived=family_kernel();note('universal moment kernel regenerated')
    check('balance',derived['balance'],MP(0))
    a,b,V=[MP.variable(i) for i in range(3)]
    check('normalization',derived['N'],12*a*a+8*a*b+4*b*b+2*V)
    for name in ['N','S3','S4','mu2','h','D','n','d','positive_scalar']:records[name]=encode(derived[name])
    n,d=at_first_one(derived['n']),at_first_one(derived['d'])
    require(all(i+j+2*k==10 for poly in [derived['n'],derived['d']] for i,j,k in poly.d),
            'ratio weighted-homogeneity failed')
    check('ratio coefficient counts',[len(n.d),len(d.d)],[36,36])
    P=(n.derivative(0)*d-n*d.derivative(0)).primitive_integer()
    Qp=(n.derivative(1)*d-n*d.derivative(1)).primitive_integer()
    p,q=coeff_in_V(P),coeff_in_V(Qp)
    check('gradient V degrees',[len(p)-1,len(q)-1],[9,8])
    wp,wq=max(i+2*j for i,j,k in P.d),max(i+2*j for i,j,k in Qp.d)
    check('gradient weighted degrees',[wp,wq],[19,18])
    # Rows have shifts0..7 and0..8, columns powers16..0.
    resultant_bound=8*wp+9*wq-2*(sum(range(17))-sum(range(8))-sum(range(9)))
    check('resultant proven degree bound',resultant_bound,170)
    rows=sylvester(p,q,0);check('resultant matrix dimensions',[len(rows),len(rows[0])],[17,17])
    check('factored resultant degree',sum((len(f)-1)*multiplicity for f,multiplicity,boxes in FACTORS),162)
    values=[]
    for x in range(resultant_bound+1):
        actual=integer_det(evaluate_matrix(rows,x));expected=RESULTANT_CONSTANT
        for factor,multiplicity,boxes in FACTORS:expected*=int(pe(factor,Q(x)))**multiplicity
        require(actual==expected,'degree-bounded resultant identity at'+str(x));values.append(actual)
    records['171 integer Sylvester determinant comparisons']=len(values)
    records['resultant determinant values sha256']=hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()
    note('171 universal resultant comparisons complete')
    # Two15x15 coefficient minors of the15x16 row matrix.
    lift_rows=sylvester(p,q,1);check('linear-cofactor row dimensions',[len(lift_rows),len(lift_rows[0])],[15,16])
    bound1=7*wp+8*wq-2*(sum(range(1,16))-sum(range(7))-sum(range(8)))
    bound0=7*wp+8*wq-2*(sum(range(2,16))-sum(range(7))-sum(range(8)))
    check('linear minor proven degree bounds',[bound1,bound0],[135,137])
    F4=next(f for f,m,boxes in FACTORS if len(f)==5)
    first,second=[],[]
    for x in range(bound0+1):
        matrix=evaluate_matrix(lift_rows,x)
        if x<=bound1:first.append(integer_det([row[:14]+[row[14]] for row in matrix]))
        second.append(integer_det([row[:14]+[row[15]] for row in matrix]))
    A=interpolation_remainder(first,F4);B=interpolation_remainder(second,F4)
    check('quartic linear leading cofactor nonvanishing',pgcd(A,F4),[Q(1)])
    collision=[Q(4),Q(8),Q(4)]
    check('quartic forced original-level collision',pdiv(pa(B,pm(collision,A)),F4)[1],[Q(0)])
    records['quartic cofactor residues']={'A':encode(A),'B':encode(B)}
    records['degree-bounded cofactor determinant counts']=[len(first),len(second)]
    records['cofactor determinant values sha256']=hashlib.sha256(json.dumps([first,second],separators=(',',':')).encode()).hexdigest()
    note('quartic collision proved by remainder interpolation')
    minus_one_gcd=pgcd([pe(f,Q(-1)) for f in p],[pe(f,Q(-1)) for f in q])
    check('special b=-1 common-gradient gcd',minus_one_gcd,[Q(0)]*4+[Q(1)])
    check('special b=-5/3 common-gradient gcd',pgcd([pe(f,Q(-5,3)) for f in p],[pe(f,Q(-5,3)) for f in q]),[Q(-16,9),Q(1)])
    # Sturm exhausts each factor's roots in the entire competitive b interval.
    positive_strips=0
    for factor,multiplicity,boxes0 in FACTORS:
        degree=len(factor)-1
        if degree==1:continue
        boxes=[tuple(map(Q,box)) for box in boxes0];chain=sturm(factor)
        require(pe(factor,Q(-2)) and pe(factor,Q(0)),'competitive-domain endpoint root')
        check('degree'+str(degree)+' all competitive roots',count(chain,Q(-2),Q(0)),len(boxes))
        previous=Q(-2)
        for j,box in enumerate(boxes):
            require(previous<box[0]<box[1]<0,'overlapping/out-of-domain isolations')
            require(all(pe(factor,x) for x in box),'root at isolation endpoint')
            previous=box[1]
            check('degree'+str(degree)+' root'+str(j+1)+' Sturm isolation',count(chain,*box),1)
            records['degree'+str(degree)+' root'+str(j+1)+' endpoints']=encode(box)
            if degree==4:continue
            coefficients=strip_bernstein(n,d,box)
            require(all(co[0]>0 for co in coefficients),'vertical-strip positive Bernstein bound')
            records['degree'+str(degree)+' root'+str(j+1)+' positive coefficients']=encode(coefficients)
            positive_strips+=1
    check('full nonquartic strip count',positive_strips,8)
    check('exception -5/3 entire strip positive',all(x[0]>0 for x in strip_bernstein(n,d,(Q(-5,3),Q(-5,3)))),True)
    # Rational specialization by the literal original integer profile.
    bn=Q(-75,64);vn=Q(121,1024)
    def at(poly,x,y):return sum(c*x**i*y**j for (i,j,k),c in poly.d.items())
    check('literal (-64^4,75^3,31) benchmark',at(n,bn,vn)/at(d,bn,vn),Q(27899524,1137183))
    note('all stationary branches separated exactly')
    controls=0
    bad=[values[0]==-values[0],pdiv(pa(B,pm([Q(3),Q(6),Q(3)],A)),F4)[1]==[Q(0)],
         count(sturm(FACTORS[-1][0]),Q(-2),Q(0))==3,
         minus_one_gcd==[Q(0)]*3+[Q(1)]]
    for condition in bad:
        try:require(condition,'mathematical damaged certificate')
        except ValueError:controls+=1
    require(controls==4,'damage controls failed')
    return {'records':records,'checks':len(records),'damage_controls':controls}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-expected',action='store_true')
    parser.add_argument('--expected',type=Path);parser.add_argument('--progress',action='store_true')
    args=parser.parse_args();start=time.monotonic();output=verify(args.progress)
    raw=json.dumps(output,sort_keys=True,separators=(',',':')).encode()
    output['record_sha256']=hashlib.sha256(raw).hexdigest()
    fixture=args.expected or Path(__file__).with_name('expected.json')
    if args.write_expected:fixture.write_text(json.dumps(output,sort_keys=True,indent=2)+'\n')
    else:require(json.loads(fixture.read_text())==output,'expected fixture differs')
    summary={k:v for k,v in output.items() if k!='records'};summary['elapsed_seconds']=round(time.monotonic()-start,6)
    print(json.dumps(summary,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as error:
        print('verification failed: '+str(error),file=sys.stderr);sys.exit(1)
