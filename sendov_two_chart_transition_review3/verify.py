#!/usr/bin/env python3
"""Independent two-chart transition coefficient audit by six-reviewer-3.

No author program is imported. The sparse Laurent kernel is openly reused
from this reviewer's public a51751eed3e3c0a0c16af714b9b1b176de348a2e checker.
Newton matrix traces and one symbolic full change of basis supply independent
characteristic and compression checks. Analytic proof is in REVIEW.md.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json, math
NAMES=('a','v','s','b','q','z','y','w','x','h','j','u0','u1','u2','u3','u4','u5','u6','u7')
ZERO=(0,)*len(NAMES)
LABELS=[]; SIGNS=[]; DATA={}; ORIGINAL={}
def demand(ok,label):
    if not ok: raise ValueError(label)

class P:
    def __init__(self, value=0):
        self.terms = ({e: F(c) for e, c in value.items() if c}
                      if isinstance(value, dict) else ({ZERO: F(value)} if value else {}))

    @staticmethod
    def cast(x):
        return x if isinstance(x, P) else P(x)

    def __add__(self, x):
        result = dict(self.terms)
        for e, c in P.cast(x).terms.items():
            result[e] = result.get(e, F(0))+c
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.terms.items()})

    def __sub__(self, x):
        return self+-P.cast(x)

    def __rsub__(self, x):
        return P.cast(x)+-self

    def __mul__(self, x):
        result = defaultdict(F)
        for e, c in self.terms.items():
            for f, b in P.cast(x).terms.items():
                result[tuple(a+d for a, d in zip(e, f))] += c*b
        return P(result)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = P.cast(x)
        demand(len(x.terms) == 1, 'nonzero Laurent monomial divisor required')
        f, b = next(iter(x.terms.items()))
        return P({tuple(a-d for a, d in zip(e, f)): c/b for e, c in self.terms.items()})

    def __pow__(self, n):
        demand(type(n) is int, 'integer exponent required')
        if n < 0:
            return P(1)/(self**(-n))
        result, base = P(1), self
        while n:
            if n & 1:
                result = result*base
            base, n = base*base, n//2
        return result

    def coefficient(self, name, power):
        index = NAMES.index(name)
        result = {}
        for e, c in self.terms.items():
            if e[index] == power:
                f = list(e)
                f[index] = 0
                result[tuple(f)] = c
        return P(result)

    def substitute(self, values):
        result = P()
        for e, c in self.terms.items():
            remaining, factor = list(e), P(c)
            for name, value in values.items():
                index = NAMES.index(name)
                remaining[index] = 0
                factor = factor*P.cast(value)**e[index]
            result = result+P({tuple(remaining): 1})*factor
        return result

    def record(self):
        return [[*e, c.numerator, c.denominator] for e, c in sorted(self.terms.items())]

    def univariate_v(self):
        demand(all(not any(e[1:]) for e in self.terms), 'univariate coefficient expected')
        return [[e[0], c.numerator, c.denominator] for e, c in sorted(self.terms.items())]


def variable(name):
    e = list(ZERO)
    e[NAMES.index(name)] = 1
    return P({tuple(e): 1})


def eq(label, actual, expected=0):
    demand(not (P.cast(actual)-expected).terms, label)
    LABELS.append(label)


def derivative(poly,name):
    index=NAMES.index(name)
    out={}
    for exponents,c in P.cast(poly).terms.items():
        if exponents[index]:
            reduced=list(exponents); reduced[index]-=1
            out[tuple(reduced)]=c*exponents[index]
    return P(out)


def degree(poly,name):
    return max((e[NAMES.index(name)] for e in P.cast(poly).terms),default=-1)


def remainder(poly,name,divisor):
    eq('monic '+name,divisor.coefficient(name,degree(divisor,name)),1)
    n=degree(divisor,name); symbol=variable(name)
    while degree(poly,name)>=n:
        k=degree(poly,name)
        poly=poly-poly.coefficient(name,k)*symbol**(k-n)*divisor
    return poly


def rational_jet(numerator,denominator,name,order):
    c=denominator.coefficient(name,0)
    eq('scalar series denominator',c,c.substitute({k:0 for k in NAMES}))
    inv=[P(1)/c]
    for i in range(1,order+1):
        inv.append(-sum((denominator.coefficient(name,j)*inv[i-j]
                         for j in range(1,i+1)),P())/c)
    return sum((sum((numerator.coefficient(name,j)*inv[i-j]
                    for j in range(i+1)),P())*variable(name)**i
                for i in range(order+1)),P())


def wire(poly):
    return {'terms':[[[[n,k] for n,k in sorted(zip(NAMES,e)) if k],
                      [c.numerator,c.denominator]]
                     for e,c in sorted(P.cast(poly).terms.items())]}


def save(name,value,original=None):
    DATA[name]=value
    if original: ORIGINAL[original]=value


def save_poly(name,value,original=None):
    save(name,wire(value),original)


def positive(name,value):
    demand(value>0,name); SIGNS.append(name)
    DATA[name]=[value.numerator,value.denominator]


def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),P())
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):return [list(x) for x in zip(*a)]


def inv(a):
    n=len(a); a=[[F(v) for v in row]+[F(i==j) for j in range(n)]
                for i,row in enumerate(a)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        demand(pivot is not None,'invertible rational basis')
        a[j],a[pivot]=a[pivot],a[j]
        scale=a[j][j];a[j]=[v/scale for v in a[j]]
        for i in range(n):
            if i!=j:
                scale=a[i][j];a[i]=[v-scale*w for v,w in zip(a[i],a[j])]
    return [row[n:] for row in a]


def matrix_eq(label,actual,expected):
    demand(len(actual)==len(expected) and all(len(a)==len(b) for a,b in zip(actual,expected)),label+' dimensions')
    for i,(a,b) in enumerate(zip(actual,expected)):
        for j,(v,w) in enumerate(zip(a,b)):eq(label+str((i,j)),v,w)


A,V,S,B,Q,Z,Y,W,X,H,J=(variable(n) for n in NAMES[:11])
D=1+A


def physical():
    pair=W**2+2*(1-X)*W+1
    original=(W-A)*(W+1)**6*pair
    cubic=(W+1)*pair+(W-A)*(6*pair+(W+1)*derivative(pair,'w'))
    eq('full original derivative with critical fivefold factor',derivative(original,'w'),(W+1)**5*cubic)
    reciproc=P()
    for k in range(4):
        for j in range(k+1):
            reciproc+=cubic.coefficient('w',k)*math.comb(k,j)*A**(k-j)*(-1)**j*Q**(3-j)
    quoted=D*(D**2-2*A*X)*Q**3-(7*(D**2-2*A*X)+4*D*(D-X))*Q**2+(3*D+16*(D-X))*Q-9
    eq('literal physical reciprocal cubic',reciproc,quoted)
    root=(Q-V)**6*(Q**2-J*Q+H)
    cc=Q**3-(7*V+2*J)*Q**2+(3*H+8*V*J)*Q-9*V*H
    eq('full reciprocal characteristic',9*root-Q*derivative(root,'q'),(Q-V)**5*cc)
    save_poly('physical cubic',cubic,'physical cubic')
    save_poly('cleared reciprocal cubic',reciproc,'cleared reciprocal cubic')
    save_poly('full characteristic polynomial',(Q-V)**5*cc,'full characteristic polynomial')
    # Energy identity: |u-v|^2 for one phase is 2v^4*x/(1-2av^2*x).
    eq('circle reciprocal energy cleared identity',
       ((D*(D-X)-(D**2-2*A*X))**2+D**2*(2*X-X**2)),
       2*X*(D**2-2*A*X))


def compression():
    us=[variable('u'+str(i)) for i in range(8)]
    n=[[us[i]*(1+int(i==j)) for j in range(8)] for i in range(8)]
    # Five differences e_i-e_7, the two pair coordinates, and whole block mean.
    basis=[[F(0)]*8 for _ in range(8)]
    for j in range(5):basis[j+2][j]=1;basis[7][j]=-1
    basis[0][5]=1;basis[1][6]=1
    for i in range(2,8):basis[i][7]=1
    inverse=inv(basis);matrix_eq('basis inverse',mm(inverse,basis),[[int(i==j) for j in range(8)] for i in range(8)])
    block=mm(mm(inverse,n),basis)
    q6=[[F(i==j)-F(1,6) for j in range(6)] for i in range(6)]
    differences=[row[:5] for row in basis[2:]]
    ub=us[2:];mean=sum(ub,P())/6
    qu=[sum((q6[i][j]*ub[j] for j in range(6)),P()) for i in range(6)]
    aa=mm(mm(q6,[[ub[i]*int(i==j) for j in range(6)] for i in range(6)]),differences)
    du=[sum((ub[i]*differences[i][j] for i in range(6)),P())/6 for j in range(5)]
    want=[aa[i]+[qu[i],qu[i],7*qu[i]] for i in range(5)]
    want += [[P()]*5+[2*us[0],us[0],6*us[0]],
             [P()]*5+[us[1],2*us[1],6*us[1]],du+[mean,mean,7*mean]]
    matrix_eq('universal symbolic five-plus-three compression',block,want)
    save('full_symbolic_8x8_compression',[[wire(v) for v in row] for row in block])
    # Convert independent universal basis result to the author's ambient six-space.
    ambient_a=mm(mm(q6,[[ub[i]*int(i==j) for j in range(6)] for i in range(6)]),q6)
    ambient_b=[[u,u,7*u] for u in qu]
    ambient_d=[[P()]*6,[P()]*6,[u/6 for u in qu]]
    ambient_c=[[2*us[0],us[0],6*us[0]],[us[1],2*us[1],6*us[1]],[mean,mean,7*mean]]
    for k in range(8):
        values={n:int(i==k) for i,n in enumerate(NAMES[11:])}
        controls={}
        for name,mat in [('A',ambient_a),('B',ambient_b),('D',ambient_d),('C',ambient_c)]:
            entries=[]
            for i,row in enumerate(mat):
                for j,v in enumerate(row):
                    value=v.substitute(values)
                    demand(all(e==ZERO for e in value.terms),'complete scalar compression control')
                    c=value.terms.get(ZERO,F())
                    if c:entries.append([i,j,[c.numerator,c.denominator]])
            controls[name]={'rows':len(mat),'columns':len(mat[0]),'nonzero_entries':entries}
        save('compression_coordinate_'+str(k),controls,'complete compression basis '+str(k))
    return block


def angular():
    p8=[[F(i==j)-F(1,8) for j in range(8)] for i in range(8)]
    for name,theta in [('split',[P(1),P(-1),S,-S]+[P()]*4),
                       ('relative',[1+3*B,-1+3*B]+[-B]*6)]:
        mat=mm(mm(p8,[[theta[i]*int(i==j) for j in range(8)] for i in range(8)]),p8)
        # Full ambient characteristic via Newton traces; includes the normal zero.
        power=[[P(int(i==j)) for j in range(8)] for i in range(8)]
        traces=[P(8)];coeff=[P(1)]
        for k in range(1,9):
            power=mm(power,mat);traces.append(sum((power[i][i] for i in range(8)),P()))
            coeff.append(-sum((coeff[k-j]*traces[j] for j in range(1,k+1)),P())/k)
        characteristic=sum((coeff[k]*Q**(8-k) for k in range(9)),P())
        f=P(1)
        for value in theta:f*=Q-value
        eq(name+' full ambient characteristic Newton versus original derivative',characteristic,Q*derivative(f,'q')/8)
        save_poly(name+'_ambient_characteristic',characteristic)
        vector=[[v] for v in theta];first=mm(mat,vector);second=mm(mat,first)
        moments=[sum((v**k for v in theta),P()) for k in (2,3,4)]
        moments += [mm(transpose(vector),v)[0][0]/8 for v in (vector,first,second)]
        eq(name+' literal mass',moments[3],moments[0]/8)
        eq(name+' literal first moment',moments[4],moments[1]/8)
        eq(name+' literal second moment',moments[5],moments[2]/8-moments[0]**2/64)
        # Original author calls the split slope x; rename only when comparing.
        renamed=[v.substitute({'s':X}) if name=='split' else v for v in moments]
        save(name+'_moments',[wire(v) for v in renamed],name+' complete literal moments')
    # Spectral weights reconstructed from literal moment equations.
    split_sum=3*(1+Z)/4;split_product=Z/2
    total=(1+Z)/8;first=(3-2*Z+3*Z**2)/32
    gap=split_sum**2-4*split_product
    # Psi=total^2+(2*first-sum*total)^2/gap.
    psi_num=total**2*(64*gap)+64*(2*first-split_sum*total)**2
    psi_den=64*gap
    eq('split rational Psi numerator scaling',psi_num*64*(9-14*Z+9*Z**2),
       ((1+Z)**2*(9-14*Z+9*Z**2)+(3-10*Z+3*Z**2)**2)*psi_den)
    numerator=(1+Z)**2*(9-14*Z+9*Z**2)+(3-10*Z+3*Z**2)**2
    denominator=64*(9-14*Z+9*Z**2)
    split_psi=rational_jet(numerator,denominator,'z',2)
    split_x=rational_jet(2+2*Z**2,(2+2*Z)**2,'z',2)
    split_eta=rational_jet(64*numerator,denominator*(2+2*Z)**2,'z',2)
    split_gamma=split_eta-(56*split_x-13)/30
    for name,value in [('Psi',split_psi),('X',split_x),('eta',split_eta),('Gamma',split_gamma)]:
        save_poly('split '+name+' through z2',value,'split '+name+' through z2')
    save_poly('split complete Psi rational numerator',numerator,'split complete Psi rational numerator')
    save_poly('split complete Psi rational denominator',denominator,'split complete Psi rational denominator')
    eq('split Gamma first derivative',split_gamma.coefficient('z',1),F(4,45))
    # Secular weights checked by an independent rational-function residue formula.
    quadratic=Y**2-split_sum*Y+split_product
    norm_num=2*(Y+1)*(Y-Z)**2*Y+2*(Y+Z)*(Y-1)**2*Y+4*(Y-1)**2*(Y-Z)**2
    norm_den=(Y-1)**2*(Y-Z)**2*Y
    eq('split complete secular weight',remainder((first-total*split_sum+total*Y)*norm_num-8*(2*Y-split_sum)*norm_den,'y',quadratic))
    relative_sum=5*B;relative_gap=3+B**2
    relative_mass=(2+24*B**2)/8
    relative_moment=(18*B+48*B**3)/8
    difference=2*relative_moment-relative_sum*relative_mass
    rn=relative_mass**2*relative_gap+difference**2;rd=2*relative_gap
    rpsi=rational_jet(rn,rd,'b',4)
    rx=rational_jet(2+108*B**2+168*B**4,(2+24*B**2)**2,'b',4)
    reta=rational_jet(64*rn,rd*(2+24*B**2)**2,'b',4)
    rgamma=reta-(56*rx-13)/30
    eq('relative Gamma second coefficient',rgamma.coefficient('b',2),F(1,6))
    for name,value in [('Psi',rpsi),('X',rx),('eta',reta),('Gamma',rgamma)]:
        save_poly('relative '+name+' through b4',value,'relative '+name+' through b4')
    save_poly('relative complete Psi rational numerator',rn,'relative complete Psi rational numerator')
    save_poly('relative complete Psi rational denominator',rd,'relative complete Psi rational denominator')
    rq=Q**2-5*B*Q+6*B**2-F(3,4)
    base=(Q-3*B)**2-1
    norm=2*((Q-3*B)**2+1)*(Q+B)**2+6*base**2
    eq('relative complete secular weight',remainder((relative_moment-relative_sum*relative_mass+relative_mass*Q)*norm-8*(2*Q-relative_sum)*base**2*(Q+B)**2,'q',rq))
    # At a_- the split quadratic vanishes. Exact fourth angular coefficient.
    endpoint=split_gamma-F(4,45)*(F(1,2)-split_x)
    eq('degenerate endpoint split constant',endpoint.coefficient('z',0))
    eq('degenerate endpoint split quadratic',endpoint.coefficient('z',1))
    positive('endpoint split quartic coefficient',endpoint.coefficient('z',2).terms[ZERO])
    save_poly('endpoint split loss divided by C through z2',endpoint)
    discr=9-14*Z+9*Z**2
    exact_num=9*numerator-32*(1+Z**2)*discr+14*(1+Z)**2*discr
    eq('complete degenerate endpoint split rational identity',exact_num,256*Z**2)
    eq('split discriminant positive square completion',9*discr,(9*Z-7)**2+32)
    save_poly('endpoint exact loss numerator over36(1+z)^2discriminant',exact_num)
    return endpoint


def stiffness():
    pg=2768*A**2+3080*A-2875
    sc=pg/30720;cc=(4*A+5)**2/8192
    l=(208*A**2+232*A-215)/1152
    b=(69025-73880*A-66416*A**2)/12288
    eq('whole split stiffness',2*sc+F(8,45)*cc,l)
    eq('whole relative stiffness',-60*sc+F(2,3)*cc,b)
    eq('L derivative numerator',derivative(l*1152,'a')*D-5*l*1152,1307-512*A-624*A**2)
    eq('B derivative numerator',derivative(b*12288,'a')*D-5*b*12288,199248*A**2+162688*A-419005)
    save_poly('split d5-scaled stiffness',l,'split d5-scaled stiffness')
    save_poly('relative d5-scaled stiffness',b,'relative d5-scaled stiffness')
    save_poly('physical relative d5-scaled stiffness',b/16,'physical relative d5-scaled stiffness')
    for label,poly,point in [
        ('Lpositive lower',l,F(151,250)),('Bpositive upper',b,F(121,200)),
        ('PGnegative lower',-pg,F(151,250)),('PGpositive upper',pg,F(121,200)),
        ('P local positive lower',1616*A**2+1800*A-1675,F(151,250)),
        ('Bnegative303over500',-b,F(303,500))]:
        positive(label,poly.substitute({'a':point}).terms[ZERO])
    positive('L derivative floor',F(171));positive('negative B derivative floor',F(57069))
    u,r=F(-29,52),F(3,26)
    eq('exact Qsqrt101 threshold rational part',208*(u*u+101*r*r)+232*u-215)
    eq('exact Qsqrt101 threshold radical part',416*u*r+232*r)
    positive('positive lower radical branch',F(36*101-29**2))
    positive('lower root below compact lower', (52*F(151,250)+29)**2-36*101)
    delta=F(43,56)-X;slack=Z-F(12,5)*(X-F(1,2))
    gd=F(3,4)*delta-F(25,48)*slack;gn=delta-F(5,6)*slack
    gb=F(1,7)+F(4,3)*Z;old=(56*X-13)/30
    eq('full independent stronger Gram residual',(gb-old-slack/27)*gd+gn**2,25*slack**2/1296)
    save_poly('complete credited Gram tangent residual',25*slack**2/1296,'complete credited Gram tangent residual')
    save('full Gram quantities',{k:wire(v) for k,v in [('Delta',delta),('h',slack),('D',gd),('N',gn),('B',gb)]},'full Gram quantities')
    save_poly('complete moving-pair angular lower decomposition',(sc+F(4,45)*cc)*(F(1,2)-X)+cc*Z/27,'complete moving-pair angular lower decomposition')
    slope_num=D**3*(5536*A+3080)/114688
    eq('two-family transverse slope at PG zero',
       derivative(D**3*pg/114688,'a')-slope_num,3*D**2*pg/114688)
    save_poly('transverse cubic-window slope numerator',slope_num)
    return l,b


def canon(value):
    if isinstance(value,dict) and set(value)=={'terms'}:
        items={}
        for powers,ratio in value['terms']:
            key=tuple(sorted((n,k) for n,k in powers));items[key]=items.get(key,F())+F(*ratio)
        return ('polynomial',tuple(sorted((k,v.numerator,v.denominator) for k,v in items.items() if v)))
    if isinstance(value,dict):return ('object',tuple((k,canon(v)) for k,v in sorted(value.items())))
    if isinstance(value,list):return ('list',tuple(canon(v) for v in value))
    return value


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path);parser.add_argument('--check',type=Path)
    parser.add_argument('--original',type=Path)
    args=parser.parse_args()
    physical();block=compression();endpoint=angular();l,b=stiffness()
    rejected=[]
    for label,actual,wrong in [('wrong split norm factor',l,l*2),
                             ('wrong physical mean factor16',b/16,b/4),
                             ('missing offdiagonal block',block[7][0],0),
                             ('zero endpoint quartic',endpoint.coefficient('z',2),0)]:
        try:eq('invalid '+label,actual,wrong)
        except ValueError:rejected.append(label)
        else:raise ValueError('invalid mathematical expression accepted')
    result={'agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'target_height':8276,'identity_count':len(LABELS),'identities':LABELS,
            'strict_sign_count':len(SIGNS),'strict_signs':SIGNS,
            'independent_records':DATA,'eligible_complete_original_records':len(ORIGINAL),
            'rejected_invalid_controls':rejected,'analytic_bridges_machine_checked':False}
    encoded=json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    if args.write:args.write.write_text(encoded)
    if args.check:demand(json.loads(args.check.read_text())==result,'complete independent expected records')
    if args.original:
        old=json.loads(args.original.read_text())['records']
        for name,value in ORIGINAL.items():demand(canon(old[name])==canon(value),'complete original record '+name)
        print('Complete original records compared: '+str(len(ORIGINAL)))
    print(json.dumps({'verified':True,'identities':len(LABELS),'strict_signs':len(SIGNS),
                      'complete_original_records':len(ORIGINAL),
                      'result_sha256':hashlib.sha256(encoded.encode()).hexdigest()}))


if __name__=='__main__':main()
