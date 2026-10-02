"""Adversarial mathematical and schema controls; no researcher inputs."""
from fractions import Fraction as F
from itertools import permutations
from copy import deepcopy
import literal as L
import signs


def determinant(a):
    n=len(a);total=F()
    for p in permutations(range(n)):
        v=F((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i,j in enumerate(p):v*=a[i][j]
        total+=v
    return total


def polynomial(terms,point):
    out=F()
    for powers,c in terms:
        v=F(c)
        for x,e in zip(point,powers):v*=x**e
        out+=v
    return out


def rational(z,point):
    return polynomial(z['numerator'],point)/polynomial(z['denominator'],point)


def run(data):
    rejected=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,ZeroDivisionError):rejected.append(label)
        else:raise ValueError('damage accepted: '+label)
    source=data['functions']['invariant_minor_1']['numerator']
    reject('negative sign certificate',lambda:signs.prove([(e,str(-F(c))) for e,c in source],'negative'))
    reject('missing Q0 strictness',lambda:signs.prove([([1,0,0,0,0],'1')],'no-origin'))
    reject('negative exponent',lambda:signs.decode([([-1,0,0,0,0],'1')]))
    reject('boolean exponent',lambda:signs.decode([([True,0,0,0,0],'1')]))
    reject('duplicate polynomial term',lambda:signs.decode([([0]*5,'1'),([0]*5,'2')]))
    reject('zero divisor',lambda:rational({'numerator':[([0]*5,'1')],'denominator':[]},[0]*5))
    for label,args in [
        ('equal loads',(3,2,1,1,1,[0,1,2])),
        ('nonpositive light',(3,2,1,2,0,[0,1,2])),
        ('boolean heavy',(3,2,1,True,1,[0,1,2])),
        ('duplicate mark',(3,2,1,2,1,[0,0,1])),
        ('unsupported one-heavy scope',(3,1,2,2,1,[0,1,2]))]:
        reject(label,lambda args=args:L.build(*args))
    reject('zero-diagonal indefinite residual',lambda:L.psd([[F(),F(1)],[F(1),F()]]))
    d=L.build(3,2,1,2,1,[2,0,1]);c=d['seed'];N=d['N'];s=d['s'];Q=L.lift(c)
    bad=deepcopy(c);i,j=next((i,j) for i in range(1,N-1) for j in range(i) if d['canonical'][i+1]&d['canonical'][j+1])
    bad[i][j]+=1;bad[j][i]+=1
    reject('mandatory intersection corruption with lift row sums retained',lambda:L.validate(d['canonical'],L.lift(bad),s,N-3,F(1)))
    bad=deepcopy(Q);bad[0][0]+=1
    reject('actual empty loop corruption',lambda:L.validate(d['canonical'],bad,s,N-3,F(1)))
    import frame
    bad_d=dict(d);bad_d['seed']=deepcopy(c);bad_d['seed'][0][0]+=1
    reject('wrong physical frame',lambda:frame.audit(bad_d))
    lower=[[x+1 for x in row] for row in Q]
    wrong=[F(bool(A&(1<<2)))-F(s,N)-1 for A in d['canonical']]
    reject('incorrectly centered forced star',lambda:L.need(L.image(lower,wrong)==[0]*N,'forced kernel'))
    # Disjoint-parameter finite checks of every symbolic sheared-budget entry;
    # ordinary metric/action construction, Fraction inversion,24-permutation
    # determinant. No SymPy, author resolvent or saved matrix input.
    budgets=[]
    for n,k,r,D,t in [(3,2,1,2,1),(4,2,2,3,1),(3,2,1,5,2),(5,3,2,3,2)]:
        d=L.build(n,k,r,D,t,list(range(k+r)));q=d['q'];a=k*D;u=r*t;m=a+u;h=d['N']-1
        ch,cl=d['c'];zh,zl=d['zeta'];alpha=F(u,a*m*m)*(u*zh+a*zl)
        metric=[[F() for _ in range(6)] for _ in range(6)]
        for i,x in enumerate([q-1,D,D*(F(q,k)-1),D*(F(q,r)-1),(q+D)*(F(1,t)-F(1,D))/r,alpha]):metric[i][i]=F(x)
        metric[2][3]=metric[3][2]=F(-D)
        block=[[F(h-q-1),F(-D)],[F(1-q),F(h-D)]];delta=determinant(block)
        inv=[[block[1][1]/delta,-block[0][1]/delta],[-block[1][0]/delta,block[0][0]/delta]]
        R=[[F() for _ in range(6)] for _ in range(6)]
        for i in range(2):
            for j in range(2):R[i][j]=sum(metric[i][v]*inv[v][j] for v in range(2))
        for i in (2,3):
            for j in (2,3):R[i][j]=metric[i][j]/(h-2*D)
        for i in (4,5):R[i][i]=metric[i][i]/h
        L.need(all(type(x) is F for row in R for x in row),'entire independent resolvent exact Fraction arithmetic')
        vectors=[[0,F(1,D),F(1,D),0,0,0],[0,F(1,D),0,F(1,D),1,0],
                 [1,F(m,D)-1,F(a,D),F(u,D),u,0],[0,0,0,0,0,1]]
        weights=[F(1,a),F(1,u),F(m+1),F(u,a*m)]
        b=[F(u,m)*ch,-F(u,m)*cl,0]
        shear=[[F(i==j) for j in range(4)] for i in range(4)]
        for i in range(3):shear[i][3]=-b[i]
        B=[[sum(shear[v][i]*weights[v]*shear[v][j] for v in range(4))-L.dot(vectors[i],L.image(R,vectors[j])) for j in range(4)] for i in range(4)]
        point=[q-4,t,D,a,u];from_cache=[[rational(z,point) for z in row] for row in data['budget']]
        L.need(B==from_cache,'every sheared symbolic budget entry matches independent Fraction reconstruction')
        minors=[determinant([row[:s] for row in B[:s]]) for s in range(1,5)]
        L.need(minors==[rational(data['functions']['invariant_minor_'+str(i)],point) for i in range(1,5)],'every full symbolic minor matches all signed permutations')
        L.need(all(v>0 for v in minors),'four finite exact leading signs')
        budgets.append({'n':n,'k':k,'r':r,'D':D,'t':t,'budget_sha256':L.fingerprint(B),'minors':[str(z) for z in minors]})
    # Full reversible binomial controls include negative raw coefficients.
    shifts=[]
    for e in [(0,0,0,0),(1,2,3,2),(2,1,0,3)]:
        p={e:3,(0,0,1,0):-5};out=signs.shift(p)
        L.need(signs.unshift(out)==p,'whole signed forward/inverse shift control')
        shifts.append(signs.digest(out))
    return {'rejected':rejected,'damage_rejections':len(rejected),'whole_fraction_budgets':budgets,
            'all_budget_entries':64,'all_permutation_minors':16,'whole_signed_shift_controls':shifts}
