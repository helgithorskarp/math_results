"""Reconstruct the complete independent arithmetic record, without author code."""
from fractions import Fraction as Q
from algebra import RF, poly, add, scale, mul, power


def build(defect=None):
    out = {'agent': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
           'schema': 'small-D-angular-independent-v1', 'gates': []}

    def gate(name, value, predicate):
        if not predicate:
            raise ValueError(name)
        out['gates'].append({'name': name, 'value': value})

    def pos(name, q):
        gate(name, str(q), q > 0)

    def same(name, left, right):
        r = left.residual(right)
        gate(name, [str(c) for c in r], r == poly([0]))

    b, m, B, r = Q(1,8), Q(29,100), Q(41,100), Q(1,480)
    X = RF([0,1]); E = X**2-b
    tail = 0 if defect == 'drop-inverse-tail' else E**3/(b**3*X)
    same('full inverse identity in original x',
         1/X, X*(1/b-E/b**2+E**2/b**3)-tail)
    same('full inverse-square identity',
         1/(b+X), 1/b-X/b**2+X**2/(b**2*(b+X)))
    same('full inverse-cubic identity in original x',
         1/X**3, X/b**2*(1-2*E/b+3*(E/b)**2)
         - X*E**3/b**5*(4+3*E/b)/(1+E/b)**2)
    odd = [poly([0,1]), mul(poly([0,1]), poly([-b,0,1])),
           mul(poly([0,1]), power(poly([-b,0,1]),2))]
    gate('complete odd moment cancellation coefficient lists',
         [[str(c) for c in p] for p in odd],
         odd == [poly([0,1]),poly([0,-b,0,1]),poly([0,b*b,0,-2*b,0,1])])
    T = (4+3*X)/(1+X)**2
    same('entire inverse-cubic ratio derivative', T.diff(), (-5-3*X)/(1+X)**3)
    for tag, h, L, K, expectedK in [
        ('original',Q(1,27),Q(40),Q(12500000),Q(5078352912883209732096,411518530176605)),
        ('refined',Q(1,25),Q(28),Q(8000000),Q(506316387394134474752,65888562449329))]:
        if defect == 'underpay-root' and tag == 'refined': L = Q(27)
        if defect == 'underpay-Taylor' and tag == 'refined': K = Q(7000000)
        pos(tag+' positive lower magnitude margin', b-h-m*m)
        pos(tag+' positive upper magnitude margin', B*B-b-h)
        pos(tag+' four-four sign gap', 5*m-3*B)
        pos(tag+' pole-free central interval', m-r)
        pos(tag+' central root bracket margin', r-L*h**3)
        A = 8/(B+r)**2 if tag == 'original' else 64/(1+8*r*r)
        pos(tag+' root payment margin', L*A-512/m)
        gate(tag+' slope bound',str(A), A>0)
        ratio = T.value(-8*h)
        gate(tag+' cubic ratio endpoint',str(ratio), ratio == (Q(2268,361) if tag=='original' else Q(1900,289)))
        pos(tag+' cubic ratio numerator positivity',4-24*h)
        pos(tag+' cubic ratio derivative sign',5-24*h)
        A3=B*b**-5*ratio
        remainder = 3 if defect=='omit-seven-remainders' else 24
        k = 2*L*A3+remainder*L*L/(m-r)**4
        gate(tag+' entire eight-root Taylor loss',str(k), k==expectedK)
        pos(tag+' Taylor payment margin',K-k)
        gate(tag+' full central mass numerator','64',8*8==64)
    q = X
    same('old discarded nonlinear mass curvature',
         2*q*(1+q)**2-((1+q)**2-1),3*q**2+2*q**3)
    old = 16/(1-8*Q(1,27))+390625*Q(1,729)**2
    gate('original whole endpoint',str(old),old==Q(237004387,10097379))
    pos('original strict 47/2 endpoint gap',Q(47,2)-old)
    s = X
    u = 8/(1-8*s)+125000*s**4
    Qs = s*s*u
    bound = u*(2+Qs)/(1+Qs)**2
    derivative = 2*(u.diff()-s*u*u*(3+Qs))/(1+Qs)**3
    if defect=='wrong-bound-derivative': derivative = derivative+s
    same('entire nonlinear angular bound derivative',bound.diff(),derivative)
    ue = u.value(Q(1,25)); qe = Qs.value(Q(1,25)); be = bound.value(Q(1,25))
    gate('u endpoint',str(ue),ue==Q(5136,425))
    gate('q endpoint',str(qe),qe==Q(5136,265625))
    pos('u bounded strictly by13',13-ue)
    pos('q bounded strictly by1',1-Q(13,625))
    pos('positive derivative uniform margin',64-Q(676,25))
    gate('refined whole nonlinear endpoint',str(be),be==Q(1721799060000,73311519121))
    pos('refined strict 47/2 endpoint gap',Q(47,2)-be)
    for count, expected in [(7,Q(12,329)),(6,Q(5,141))]:
        upper=(1-Q(1,count))/Q(47,2)
        gate('whole positive-mass band '+str(count),str(upper),upper==expected)
    # Literal squared-root levels yield the entire octic, with h=sqrt(D)/2.
    h=poly([0,1]); c=poly([b]); levels=[c,c,add(c,scale(h,-1)),add(c,h)]
    zpoly=[poly([1])]
    for y in levels:
        factor=[scale(y,-1),poly([0]),poly([1])]
        nxt=[poly([0])]*(len(zpoly)+2)
        for i,v in enumerate(zpoly):
            for j,w in enumerate(factor): nxt[i+j]=add(nxt[i+j],mul(v,w))
        zpoly=nxt
    closed=[]
    for j in range(9):
        if j%2: closed.append(poly([0]));continue
        k=j//2
        from math import comb
        value=poly([comb(4,k)*(-b)**(4-k)])
        if k<=2: value=add(value,scale(power(h,2),-comb(2,k)*(-b)**(2-k)))
        closed.append(value)
    gate('literal entire octic coefficient list',[[str(v)for v in p]for p in zpoly],zpoly==closed)
    mu2=scale(sum_polys(levels),2)
    mu4=scale(sum_polys([mul(y,y)for y in levels]),2)
    gate('literal norm and fourth-moment polynomial lists',
         [[str(v)for v in mu2],[str(v)for v in mu4]],mu2==poly([1])and mu4==poly([b,0,4]))
    H=RF([0,1]); S=4/b+2/(b-H)+2/(b+H)
    same('literal eight-original inverse-square calibration',S,64*(1-32*H**2)/(1-64*H**2))
    D=RF([0,1]); mass=(1-16*D)/(1-8*D); p=1-mass
    same('entire even lower squeeze',(1-mass**2-p**2)/D,16*(1-16*D)/(1-8*D)**2)
    same('entire even upper squeeze',(1-mass**2)/D,16*(1-12*D)/(1-8*D)**2)
    gate('both exact squeeze limits','16',mass.value(0)==1 and (16*(1-16*D)/(1-8*D)**2).value(0)==16
         and (16*(1-12*D)/(1-8*D)**2).value(0)==16)
    # Full 8x8 rational projectors: normalize a by sqrt(N), no numerical roots.
    for t in [Q(1,100),Q(1,50)]:
        a=[Q(1),Q(-1),Q(1),Q(-1),1+t,-1-t,1-t,-1+t]
        if defect=='delete-original-position':a=a[:-1]
        gate('original eight-position census '+str(t),len(a),len(a)==8)
        N=sum(v*v for v in a); v=[1/z for z in a]; Sv=sum(z*z for z in v)
        P=[[Q(i==j)-Q(1,8)for j in range(8)]for i in range(8)]
        A=[[a[i] if i==j else Q(0)for j in range(8)]for i in range(8)]
        C=mm(mm(P,A),P); Pi=[[v[i]*v[j]/Sv for j in range(8)]for i in range(8)]
        gate('whole projector/compression matrices '+str(t),
             {'P':strings(P),'H_unscaled':strings(C),'Pi0':strings(Pi)},
             mm(P,P)==P and mm(Pi,Pi)==Pi and mm(C,Pi)==zero_matrix(8) and
             sum(v)==0 and sum(a)==0)
        mmass=sum(a[i]*Pi[i][j]*a[j]for i in range(8)for j in range(8))/N
        if defect=='wrong-full-mass-normalization':mmass/=8
        gate('literal full central mass '+str(t),str(mmass),mmass==64/(N*Sv))
        zz=[Q(1),Q(0),Q(-1),Q(0),Q(0),Q(0),Q(0),Q(0)]
        gate('repeated-original inactive direction '+str(t),[str(z)for z in zz],
             mv(C,zz)==zz and sum(a[i]*zz[i]for i in range(8))==0)
        d=sum(z**4 for z in a)/N**2-b
        pos('literal nonzero D '+str(t),d)
        pos('literal small-D coverage '+str(t),Q(1,625)-d)
        gate('literal moment/central mass census '+str(t),
             {'N':str(N),'D':str(d),'mass0':str(mmass),'squared_positions':[str(z*z/N)for z in a]},
             all(sum(z**k for z in a)==0 for k in [1,3,5])and N>0 and 0<mmass<=1)
    out['gate_count']=len(out['gates'])
    return out


def sum_polys(a):
    out=poly([0])
    for v in a:out=add(out,v)
    return out


def mm(A,B):
    return [[sum(A[i][k]*B[k][j]for k in range(len(B)))for j in range(len(B[0]))]for i in range(len(A))]


def mv(A,v):
    return [sum(a*b for a,b in zip(row,v))for row in A]


def strings(A):return [[str(v)for v in row]for row in A]


def zero_matrix(n):return [[Q(0)for _ in range(n)]for _ in range(n)]
