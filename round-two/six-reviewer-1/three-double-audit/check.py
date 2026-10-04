"""Independent QQ[r] companion norm/adjugate audit; no author program import.

The displayed Num/Den are exposed mathematical claim inputs, not a blind fixture.
The generic rational engine is credited unchanged reviewer source.
All complete coefficient/matrix records are regenerated, not public bulk inputs.
"""
from pathlib import Path
from itertools import permutations
from math import comb
import argparse, hashlib, json
from arithmetic import F, require, add, scale, mul, power, btopower, encode


def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return p


def plus(a,b):return trim(add(a,b))
def times(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:out[i+j]+=x*y
    return trim(out)
def neg(p):return trim(scale(p,-1))
def minus(a,b):return plus(a,neg(b))
def const(x):return [F(x)]
def rp(terms):
    out=[F(0)]*(max(terms,default=0)+1)
    for k,v in terms.items():out[k]=F(v)
    return trim(out)
def peval(p,x):return sum((v*x**i for i,v in enumerate(p)),F(0))


def zadd(a,b):
    return [plus(a[i]if i<len(a)else const(0),b[i]if i<len(b)else const(0))
            for i in range(max(len(a),len(b)))]
def zscale(p,x):return [times(a,x)for a in p]
def zmul(a,b):
    out=[const(0)for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=plus(out[i+j],times(x,y))
    return out
def zdiff(a):return [scale(a[i],i)for i in range(1,len(a))]
def zsub(a,b):return zadd(a,zscale(b,const(-1)))
def zeval(p,x):
    out=const(0)
    for v in p[::-1]:out=plus(v,times(out,x))
    return out


def matrix(n):return [[const(0)for _ in range(n)]for _ in range(n)]
def ident(n):
    out=matrix(n)
    for i in range(n):out[i][i]=const(1)
    return out
def madd(a,b):return [[plus(x,y)for x,y in zip(ar,br)]for ar,br in zip(a,b)]
def mscale(a,p):return [[times(x,p)for x in row]for row in a]
def mmul(a,b):
    n=len(a);out=matrix(n)
    for i in range(n):
        for k in range(n):
            if a[i][k]!=const(0):
                for j in range(n):out[i][j]=plus(out[i][j],times(a[i][k],b[k][j]))
    return out
def trace(a):
    out=const(0)
    for i in range(len(a)):out=plus(out,a[i][i])
    return out
def determinant(a):
    n=len(a);out=const(0)
    for perm in permutations(range(n)):
        term=const((-1)**sum(perm[i]>perm[j]for i in range(n)for j in range(i+1,n)))
        for i,j in enumerate(perm):term=times(term,a[i][j])
        out=plus(out,term)
    return out
def adjugate(a):
    n=len(a);out=matrix(n)
    for i in range(n):
        for j in range(n):
            minor=[[a[k][l]for l in range(n)if l!=i]for k in range(n)if k!=j]
            out[i][j]=scale(determinant(minor),(-1)**(i+j))
    return out
def companion(p):
    n=len(p)-1;require(p[-1]==const(1),'monic whole quotient')
    out=matrix(n)
    for i in range(1,n):out[i][i-1]=const(1)
    for i in range(n):out[i][-1]=neg(p[i])
    return out
def meval(p,a):
    out=matrix(len(a));eye=ident(len(a))
    for v in p[::-1]:out=madd(mmul(out,a),mscale(eye,v))
    return out
def newton(p,count):
    n=len(p)-1;out=[const(n)]
    for k in range(1,count+1):
        row=const(0)
        for j in range(1,k):row=minus(row,times(p[n-j],out[k-j]))
        out.append(minus(row,scale(p[n-k],k)))
    return out


NUM=list(map(F,[11664,-140292,390636,2706508,4127676,-4018836,-10848244,-4236516,
               17047308,12783956,-6621324,-9943644,-1928908,1914084,1688580,
               864756,315252,69984,11664]))
DEN=list(map(F,[972,-12555,49377,-112415,-740283,-494007,1712969,1974573,-484767,
               -1842073,-739929,173139,269519,231123,166179,76383,27135,5832,972]))


def bernstein(p):
    n=len(p)-1
    translated=[sum((p[j]*comb(j,k)*F(1,4)**k for j in range(k,n+1)),F(0))for k in range(n+1)]
    # Independent translation by repeated multiplication of u=1+v/4.
    second=const(0)
    for j,a in enumerate(p):second=plus(second,scale(power([F(1),F(1,4)],j),a))
    require(trim(translated)==second,'whole affine translation')
    controls=[sum((translated[k]*F(comb(i,k),comb(n,k))for k in range(i+1)),F(0))
              for i in range(n+1)]
    require(btopower(controls)==translated,'whole closed Bernstein reconstruction')
    return controls


def run(damage=None):
    one=const(1);r=rp({1:1});p=rp({1:1,3:1});B=rp({0:1,2:2,4:-1,6:-1})
    L=[one,neg(p),one];g= zmul(L,L)
    q=[plus(times(p,p),one),scale(p,-2),one]
    tau=times(power(rp({0:-1,2:1}),2),rp({0:1,2:1}))
    beta=rp({3:1});companion_quartet=zsub(g,zscale(q,tau))
    fact=zmul([times(beta,beta),scale(beta,-2),one],[B,scale(r,-2),one])
    require(companion_quartet==fact,'whole actual companion classification identity')
    require(zeval(companion_quartet,beta)==const(0)and
            zeval(zdiff(companion_quartet),beta)==const(0),'double value and derivative')
    # The stationary identity in an independent symbolic parameter p.
    pp=rp({1:1});lp=[one,neg(pp),one];gp=zmul(lp,lp)
    qp=[plus(times(pp,pp),one),scale(pp,-2),one]
    cubic=[neg(times(times(pp,pp),pp)),plus(scale(times(pp,pp),3),one),scale(pp,-3),one]
    require(zsub(zmul(zdiff(gp),qp),zmul(gp,zdiff(qp)))==
            zscale(zmul(lp,cubic),const(2)),'all stationary numerator coefficients')
    D3=zmul(L,[beta,one]);Q2=[B,scale(r,2),one];f=zmul(zmul(D3,D3),Q2)
    negative_quartet=[scale(v,(-1)**i)for i,v in enumerate(companion_quartet)]
    require(f==zmul(g,negative_quartet),'all9 original octic coefficients')
    H=[rp({0:F(1,4),2:F(1,2),4:F(-1,4),6:-1,8:F(-1,4),10:F(1,2),12:F(1,4)}),
       rp({1:F(1,4),3:F(-3,4),5:F(-1,4),7:F(-1,4)}),
       rp({0:F(5,4),2:F(1,4),4:F(-5,4),6:F(-5,4)}),r,one]
    h=zscale(zdiff(f),const(F(1,8)))
    require(h==zmul(D3,H),'entire derivative retains all7 slots')
    powers=newton(f,5);N=rp({0:-6,2:2,4:6,6:6});X=powers[4]
    require(powers[1]==powers[3]==powers[5]==const(0)and powers[2]==N,
            'whole first5 physical original moments and norm')
    M=companion(H);require(meval(H,M)==matrix(4),'complete quotient relation')
    R=meval(zdiff(H),M);delta=determinant(R);adj=adjugate(R)
    require(delta!=const(0),'nonzero polynomial norm')
    require(mmul(R,adj)==mscale(ident(4),delta)==mmul(adj,R),
            'all16 left/right adjugate inverse coefficients')
    mass=mscale(mmul(meval(zmul(D3,Q2),M),adj),const(-8))
    if damage=='lost-mass-factor':mass=mscale(mass,const(F(1,8)))
    mass1=trace(mass);mass2=trace(mmul(mass,mass))
    require(mass1==times(N,delta),'all4 positive mass trace plus3zero masses')
    energy=minus(X,scale(times(N,N),F(1,8)))
    rawtop=minus(times(times(N,N),times(delta,delta)),mass2)
    def ur(p):
        out=[F(0)]*(2*len(p)-1)
        for i,v in enumerate(p):out[2*i]=v
        return trim(out)
    num=NUM[:];den=DEN[:]
    if damage=='lost-terminal-num':num[-1]=F(0)
    cleared_left=times(rawtop,ur(den))
    cleared_right=times(times(energy,times(delta,delta)),ur(num))
    require(max(len(cleared_left),len(cleared_right))<=121,'whole actual cleared degree bound')
    full=minus(cleared_left,cleared_right)
    require(full==const(0),'entire cleared degree<=120 angular identity')
    gap=minus(scale(den,16),num)
    quotient=[-gap[0]]
    for k in range(1,len(gap)-1):quotient.append(quotient[-1]-gap[k])
    require(times([F(-1),F(1)],quotient)==gap,'whole divided gap polynomial')
    db=bernstein(den);gb=bernstein(quotient)
    require(len(db)==19 and len(gb)==18 and min(db)>0 and min(gb)>0,'entire closed strict sign vectors')
    stronger=minus(quotient,scale(den,34))
    if damage=='wrong-rigidity-constant':stronger=minus(quotient,scale(den,35))
    sb=bernstein(stronger);require(min(sb)>0,'quantitative34 entire enlarged-interval margin')
    require(peval(num,F(1))==16*peval(den,F(1)) and peval(den,F(1))==262144,
            'actual sharp endpoint ratio')
    # Squared-distance control uses N>=2p^2 and a complete positive shift.
    normdiff=minus(N,scale(times(p,p),2))
    require(normdiff==times(rp({0:-1,2:1}),rp({0:6,2:6,4:4})),
            'whole sign-collapsed distance numerator')
    a=rp({0:6,2:6,4:4});distance=minus(plus(N,scale(times(p,p),2)),a)
    require(distance==times(rp({0:-1,2:1}),rp({0:12,2:14,4:8})),
            'whole squared-distance upper factor')
    discQ=minus(scale(times(r,r),4),scale(B,4))
    require(discQ==scale(times(power(rp({0:1,2:1}),2),rp({0:-1,2:1})),4),
            'all actual companion quadratic-root discriminant')
    record={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'original_octic':f,'positive_quartet':g,'negative_magnitudes_quartet':companion_quartet,
            'stationary_identity':zsub(zmul(zdiff(gp),qp),zmul(gp,zdiff(qp))),
            'all_first5_original_powers':powers[1:],'D3':D3,'Q2':Q2,'H4':H,
            'companion4':M,'derivative_matrix4':R,'norm_discriminant':delta,'adjugate4':adj,
            'all_raw_mass_numerator_matrix4':mass,'raw_mass_trace':mass1,'raw_squared_mass_trace':mass2,
            'angular_energy':energy,'cleared_left':cleared_left,'cleared_right':cleared_right,
            'cleared_degree120_zero_vector':[F(0)]*121,
            'Num':num,'Den':den,'divided_gap':quotient,'Den_Bernstein':db,'gap_Bernstein':gb,
            'quantitative34_polynomial':stronger,'quantitative34_Bernstein':sb,
            'N_minus2p_squared':normdiff,'squared_distance_factor':distance,'companion_quadratic_discriminant':discQ}
    encoded=json.dumps(encode(record),sort_keys=True,separators=(',',':')).encode()
    summary={'agent':'six-reviewer-1','role':'independent mathematical reviewer','generic_matrix_size':4,
             'all_original_slots':9,'all_critical_slots':7,'zero_masses':3,'nonzero_masses':4,
             'norm_discriminant_degree':len(delta)-1,'cleared_identity_degree_bound':120,
             'Den_Bernstein':db,'gap_Bernstein':gb,'quantitative34_Bernstein':sb,
             'sharp_limit':16,'squared_distance_rigidity_constant':17,'complete_record_bytes':len(encoded),
             'complete_record_sha256':hashlib.sha256(encoded).hexdigest()}
    return encode(summary),encoded


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--record',type=Path);parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('EXPECTED.json'));parser.add_argument('--derive',action='store_true');parser.add_argument('--damage');args=parser.parse_args()
    summary,data=run(args.damage)
    if not args.derive:require(summary==json.loads(args.expected.read_text()),'entire independent summary and complete-record seal')
    if args.record:args.record.write_bytes(data)
    print(json.dumps(summary,sort_keys=True,indent=2))
