#!/usr/bin/env python3
"""Exact five-variable quadratic pencil, author six-sendov-2, researcher.
Arithmetic kernels credit own9496; no independent review is claimed.
QQ[B,E,r,s,t,t^-1,F,G,J,p0,p1], t>0 in the feasible chart.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json

def require(condition, message):
    if not condition:
        raise ValueError(message)

class P:
    """Sparse rational polynomial in ten variables, Laurent only in t."""
    zero = (0,)*10

    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): F(v) for k, v in value.items() if v}
            require(all(len(k) == 10 for k in self.c), 'polynomial variable count')
            require(all(all(isinstance(e,int) and (i==4 or e>=0) for i,e in enumerate(k))for k in self.c), 'Laurent only in t')
        else:
            self.c = {self.zero: F(value)} if value else {}

    def __add__(self, other):
        out = dict(self.c)
        for k, v in P(other).c.items():
            out[k] = out.get(k, F(0))+v
            if not out[k]:
                del out[k]
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self+-P(other)

    def __rsub__(self, other):
        return P(other)+-self

    def __mul__(self, other):
        out = {}
        for k, a in self.c.items():
            for l, b in P(other).c.items():
                key = tuple(i+j for i, j in zip(k, l))
                out[key] = out.get(key, F(0))+a*b
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, 'bad power')
        out = P(1)
        for _ in range(exponent):
            out = out*self
        return out

    def __eq__(self, other):
        return self.c == P(other).c

    def encoded(self):
        return [[list(k), str(v)] for k, v in sorted(self.c.items())]

def variable(index):
    key = [0]*10
    key[index] = 1
    return P({tuple(key): 1})

def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':')).encode()

def ut(poly):
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out or [0]

def ua(left, right):
    return ut([(left[i] if i < len(left) else 0)+(right[i] if i < len(right) else 0)
               for i in range(max(len(left), len(right)))])

def us(value, poly):
    return ut([value*x for x in poly])

def um(left, right):
    out = [0]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i+j] = out[i+j]+a*b
    return ut(out)

def ud(poly):
    return ut([i*poly[i] for i in range(1, len(poly))] or [0])

def uq(poly, h):
    require(len(h) == 8 and h[-1] == 1, 'monic degree-seven quotient')
    poly = ut(poly)
    q = [0]*max(1, len(poly)-7)
    while len(poly) >= 8:
        k, a = len(poly)-8, poly[-1]
        q[k] = q[k]+a
        poly = ua(poly, [0]*k+us(-a, h))
    return ut(q), ut(poly)

def ur(poly, h):
    return uq(poly, h)[1]

def nth(poly, k):
    return poly[k] if k < len(poly) else 0

def moment_list(h, last=12):
    out = [F(7)]
    for k in range(1, last+1):
        if k <= 7:
            value = -sum((nth(h, 7-i)*out[k-i] for i in range(1, k)), 0)
            value -= k*nth(h, 7-k)
        else:
            value = -sum((nth(h, 7-i)*out[k-i] for i in range(1, 8)), 0)
        out.append(value)
    return out

def adj(poly, h, moments=None, damage=None):
    """Adjoint to derivative of the UNIQUE normal representative, not a derivation."""
    poly = ur(poly, h)
    moments = moments or moment_list(h, 6)
    out = [0]*6
    for k in range(1, len(poly)):
        for j in range(k):
            out[k-1-j] = out[k-1-j]+poly[k]*moments[j]
        if damage != 'adjoint_boundary':
            out[k-1] = out[k-1]-k*poly[k]
    return ut(out)

def primitive(h, constant=0):
    return [constant]+[F(8, i+1)*h[i] for i in range(8)]

def algebra(p, h, f=None, damage=None):
    f = primitive(h) if f is None else f
    Q, residual = uq(ua(us(8, f), um(p, ud(h))), h)
    if damage == 'quotient_constant':
        Q = ua(Q, [0, -8])
    ode = ua(um(p, ud(ud(h))), um(ua(ud(p), us(-1, Q)), ud(h)))
    ode = ua(ode, um(ua([64], us(-1, ud(Q))), h))
    moments = moment_list(h, 6)
    p2 = ur(um(p, p), h)
    W = ur(um(p, ua(Q, us(-1, ud(p)))), h)
    K = ua(us(-16, p), us(F(-1, 4), adj(adj(p2, h, moments, damage), h, moments, damage)))
    K = ua(K, us(F(1, 4), adj(W, h, moments, damage)))
    return {'Q': Q, 'residual': residual, 'ODE': ode, 'K': K, 'p2': p2, 'W': W}

def polydigest(poly):
    coeff = [P(x).encoded() for x in ut(poly)]
    return {'degree': len(ut(poly))-1,
            'coefficient_terms': [len(P(x).c) for x in ut(poly)],
            'sha256': hashlib.sha256(canonical(coeff)).hexdigest()}


def sub(a, index, value):
    a=P(a);out=P(0);value=P(value)
    for key,c in a.c.items():
        exponent=key[index]
        require(exponent>=0,'substitute only a polynomial variable')
        k=list(key);k[index]=0
        out+=P({tuple(k):c})*value**exponent
    return out


def diffvar(a,index):
    out={}
    for key,c in P(a).c.items():
        if key[index]:
            k=list(key);k[index]-=1
            out[tuple(k)]=c*key[index]
    return P(out)


def polysub(a,index,value):
    return [sub(x,index,value)for x in a]


def scalar(a):
    a=P(a)
    require(all(key==P.zero for key in a.c),'constant exact scalar')
    return a.c.get(P.zero,F(0))


def extract(a,index,power):
    out={}
    for key,c in P(a).c.items():
        if key[index]==power:
            k=list(key);k[index]=0;out[tuple(k)]=c
    return P(out)


def coefficients(a,index):
    a=P(a)
    require(all(key[index]>=0 for key in a.c),'ordinary polynomial coefficient extraction')
    highest=max((key[index]for key in a.c),default=0)
    return [extract(a,index,k)for k in range(highest+1)]


def primitive_integer(poly):
    from math import gcd,lcm
    poly=[F(x)for x in poly]
    while len(poly)>1 and poly[-1]==0:poly.pop()
    denominator=lcm(*(x.denominator for x in poly))
    integers=[int(x*denominator)for x in poly]
    common=0
    for x in integers:common=gcd(common,abs(x))
    require(common>0,'nonzero primitive polynomial')
    if integers[-1]<0:common=-common
    return [F(x//common)for x in integers]


def ftrim(a):
    a=[F(x)for x in a]
    while len(a)>1 and a[-1]==0:a.pop()
    return a


def fadd(a,b):
    return ftrim([(a[i]if i<len(a)else 0)+(b[i]if i<len(b)else 0)
                  for i in range(max(len(a),len(b)))])


def fscale(c,a):return ftrim([c*x for x in a])


def fmul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,c in enumerate(a):
        for j,d in enumerate(b):out[i+j]+=c*d
    return ftrim(out)


def fdiv(a,b):
    a,b=ftrim(a),ftrim(b);require(b!=[0],'nonzero univariate divisor')
    q=[F(0)]*max(1,len(a)-len(b)+1)
    while a!=[0]and len(a)>=len(b):
        k,c=len(a)-len(b),a[-1]/b[-1];q[k]+=c
        a=fadd(a,[F(0)]*k+fscale(-c,b))
    return ftrim(q),a


def bezout(a,b):
    r0,r1=ftrim(a),ftrim(b);x0,x1=[F(1)],[F(0)];y0,y1=[F(0)],[F(1)]
    while r1!=[0]:
        q,rem=fdiv(r0,r1);r0,r1=r1,rem
        x0,x1=x1,fadd(x0,fscale(-1,fmul(q,x1)))
        y0,y1=y1,fadd(y0,fscale(-1,fmul(q,y1)))
    require(r0!=[0],'nonzero gcd')
    c=1/r0[-1]
    return fscale(c,x0),fscale(c,y0),fscale(c,r0)


def independent_rank(matrix):
    a=[[F(x)for x in row]for row in matrix];rank=0
    for col in range(3):
        pivot=next((i for i in range(rank,len(a))if a[i][col]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank];c=a[rank][col]
        a[rank]=[x/c for x in a[rank]]
        for i in range(len(a)):
            if i!=rank:
                c=a[i][col];a[i]=[x-c*y for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank


def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]


def rank_conic(matrix,damage=None):
    rows=[[F(x)for x in row]for row in matrix];rank=independent_rank(rows)
    if rank==3:return {'rank':rank,'positive_common_root':False}
    if rank==0:return {'rank':rank,'positive_common_root':True,'root':'any t>0'}
    if rank==1:
        a,b,c=next(row for row in rows if any(row))
        if a:
            if a<0:a,b,c=-a,-b,-c
            yes=b*b-4*a*c>=0 and(b<0 or c<0)
        else:yes=bool(b and -c/b>0)
        return {'rank':rank,'positive_common_root':yes,'single_quadratic':[str(x)for x in [a,b,c]]}
    pair=next(cross(a,b)for i,a in enumerate(rows)for b in rows[i+1:]if any(cross(a,b)))
    X,Y,Z=pair
    if Z==0:return {'rank':rank,'positive_common_root':damage=='infinity_as_root','kernel':[str(x)for x in pair]}
    yes=(damage=='drop_conic' or X*Z==Y*Y)and(damage=='drop_positive' or Y/Z>0)
    return {'rank':rank,'positive_common_root':yes,'kernel':[str(x)for x in pair],
            'root':str(Y/Z)if yes else None}


def rank_controls(damage=None):
    controls=[
      ('rank2_positive',[[0,1,-2],[1,-1,-2],[1,0,-4],[2,-1,-6],[0,3,-6]],True),
      ('rank2_nonconic',[[1,0,-1],[0,1,-2],[1,1,-3],[2,0,-2],[0,2,-4]],False),
      ('rank2_negative',[[0,1,2],[1,1,-2],[1,0,-4],[2,1,-6],[0,3,6]],False),
      ('rank2_infinity',[[0,1,0],[0,0,1],[0,2,3],[0,-1,4],[0,0,0]],False),
      ('rank3',[[1,0,0],[0,1,0],[0,0,1],[1,1,1],[0,0,0]],False),
      ('rank1_two_positive',[[1,-3,2],[2,-6,4],[-1,3,-2],[0,0,0],[3,-9,6]],True),
      ('rank1_irrational_positive',[[1,-3,1],[2,-6,2],[0,0,0],[0,0,0],[-1,3,-1]],True),
      ('rank1_double_positive',[[1,-2,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],True),
      ('rank1_nonreal',[[1,0,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],False),
      ('rank1_negative',[[1,3,2],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],False),
      ('rank1_zero_and_positive',[[1,-2,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],True),
      ('rank1_zero_only',[[1,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],False),
      ('rank1_linear',[[0,2,-4],[0,1,-2],[0,0,0],[0,0,0],[0,0,0]],True),
      ('rank1_constant',[[0,0,2],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],False),
      ('rank0',[[0,0,0]]*5,True)]
    out=[]
    for name,rows,expected in controls:
        result=rank_conic(rows,damage)
        require(result['positive_common_root']==expected,'rank/conic positive finite root '+name)
        if result['rank']==2 and result['positive_common_root']:
            t=F(result['root']);require(all(a*t*t+b*t+c==0 for a,b,c in rows),'entire five-row root check')
        out.append({'name':name,'matrix':rows,'result':result})
    return out


def make_certificate(export=None):
    B,E,r,s,t,F0,G,J,p0,p1=[variable(i)for i in range(10)]
    key=[0]*10;key[4]=-1;ti=P({tuple(key):1})
    checks={}
    def eq(name,a,b=0):
        require(P(a)==P(b),'universal '+name);checks[name]=True
    h=[J,G,F0,E,B,F(-3,8),0,1]
    p2=8+t*(F(5,7)*B-F(27,56)*s-r*s)
    raw=[p0,p1,p2,r*t,s*t,t]
    aa=algebra(raw,h)
    eq('ODE5_p0_pivot',diffvar(nth(aa['ODE'],5),8),42)
    eq('ODE4_p1_pivot',diffvar(nth(aa['ODE'],4),9),F(15,4))
    x0=F(-1,42)*sub(nth(aa['ODE'],5),8,0)
    x1=F(-4,15)*sub(nth(aa['ODE'],4),9,0)
    eq('p0_no_p1',diffvar(x0,9));eq('p1_no_p0',diffvar(x1,8))
    expr0=F(-5,7)+t*(F(3,7)*B*r+F(75,392)*B+F(4,7)*E*s+F(5,7)*F0+F(3,28)*r*s+F(9,784)*s)
    expr1=F(128,5)*B+t*(F(-8,7)*B*B-4*B*r*s+F(4,7)*B*s+F(16,3)*E*r+3*E+F(20,3)*F0*s+8*G-F(3,8)*r-F(9,64))
    eq('explicit_p0',x0,expr0);eq('explicit_p1',x1,expr1)
    K=[sub(sub(a,8,x0),9,x1)for a in aa['K']]
    O=[sub(sub(a,8,x0),9,x1)for a in aa['ODE']]
    eq('first_ODE5',nth(O,5));eq('first_ODE4',nth(O,4));eq('first_K5',nth(K,5))
    eq('G_pivot',diffvar(nth(K,4),6),24*t*t)
    gF=F(-1,24)*ti**2*sub(nth(K,4),6,0)
    eq('G_solution_no_J',diffvar(gF,7))
    k3=sub(nth(K,3),6,gF)
    eq('F_pivot_after_G',diffvar(k3,5),F(-15,14)*t*t)
    fstar=F(14,15)*ti**2*sub(k3,5,0)
    eq('F_solution_no_J',diffvar(fstar,7))
    gstar=sub(gF,5,fstar)
    o3=sub(sub(nth(O,3),6,gstar),5,fstar)
    eq('J_pivot_after_GF',diffvar(o3,7),-28*t)
    jstar=F(1,28)*ti*sub(o3,7,0)
    P0=sub(sub(x0,5,fstar),6,gstar);P1=sub(sub(x1,5,fstar),6,gstar)
    hp=[jstar,gstar,fstar,E,B,F(-3,8),0,1]
    pp=[P0,P1,p2,r*t,s*t,t]
    final=algebra(pp,hp)
    for i in [5,4,3]:eq('final_ODE'+str(i),nth(final['ODE'],i))
    for i in [5,4,3]:eq('final_K'+str(i),nth(final['K'],i))
    require(len(final['ODE'])<=6 and len(final['K'])<=6,'full ODE/kernel degree coverage')
    residuals=[t*nth(final['ODE'],i)for i in [2,1,0]]+[nth(final['K'],1),nth(final['K'],0)+4]
    for a in residuals:
        require(all(0<=key[4]<=2 and all(x==0 for x in key[5:])for key in P(a).c),
                'five ordinary quadratic-in-t residuals')
    for a in hp:
        require(all(-1<=key[4]<=0 and all(x==0 for x in key[5:])for key in P(a).c),'h affine in inverse t')
    for a in pp:
        require(all(0<=key[4]<=1 and all(x==0 for x in key[5:])for key in P(a).c),'mass affine in t')
    gamma=F(1,4)*nth(final['K'],2)
    require(all(0<=key[4]<=2 and all(x==0 for x in key[5:])for key in P(gamma).c),'C quadratic in t')
    eq('C_constant_coefficient',extract(gamma,4,0),16)
    matrix=[[extract(a,4,k)for k in [2,1,0]]for a in residuals]
    for i,row in enumerate(matrix):eq('whole_matrix_row'+str(i),row[0]*t*t+row[1]*t+row[2],residuals[i])
    # A separate universal primitive differentiation bridge retains ALL low ODEs.
    f=us(F(1,8),ua(um(final['Q'],hp),us(-1,um(pp,ud(hp)))))
    bridge=ua(ud(f),us(-8,hp))
    require(bridge==us(F(-1,8),final['ODE']),'entire inverse primitive derivative/ODE identity')
    checks['full_primitive_bridge']=True
    require(nth(f,8)==1 and nth(f,7)==0 and nth(f,6)==F(-1,2),'reconstructed monic balance/norm')
    # Exact eliminated slice: B=s=0; K1 determines E since t>0.
    sliceR=[sub(sub(a,0,0),3,0)for a in residuals]
    e0=F(-1,2112)*(10976*r*r+7344*r+1143)
    eq('slice_K1_E_pivot',diffvar(sliceR[3],1),F(-88,7)*t)
    eq('slice_K1_at_E',sub(sliceR[3],1,e0))
    after=[sub(a,1,e0)for a in sliceR]
    cubic=primitive_integer([scalar(x)for x in coefficients(F(-1,1)*ti*after[1],2)])
    require(cubic==[157599,1459368,4606896,4934272],'entire slice cubic coefficients')
    a2=extract(after[0],4,2);b2=extract(after[0],4,0)
    a0=extract(after[2],4,2);b0=extract(after[2],4,0)
    eq('slice_ODE2_even_t',after[0],a2*t*t+b2)
    eq('slice_ODE0_even_t',after[2],a0*t*t+b0)
    resultant=a2*b0-a0*b2
    elim=primitive_integer([scalar(x)for x in coefficients(resultant,2)])
    expectedR=[22016043,343903887,2215220832,7523113824,14186807040,14058198784,5704007680]
    require(elim==expectedR,'entire degree-six slice eliminant')
    x,y,d=bezout(cubic,elim)
    require(d==[1]and fadd(fmul(x,cubic),fmul(y,elim))==[1],'entire exact unit Bezout identity')
    modular=None
    for prime in [11,13,17,19,23,29,31]:
        if any(v.denominator%prime==0 for v in x+y)or int(cubic[-1])%prime==0 or int(elim[-1])%prime==0:continue
        def reduce_mod(v):return (v.numerator%prime)*pow(v.denominator%prime,-1,prime)%prime
        xm,ym=[reduce_mod(v)for v in x],[reduce_mod(v)for v in y]
        pm,rm=[int(v)%prime for v in cubic],[int(v)%prime for v in elim]
        product=fadd(fmul(xm,pm),fmul(ym,rm))
        require(ftrim([int(v)%prime for v in product])==[1],'small finite-field unit certificate')
        modular={'prime':prime,'P':pm,'R':rm,'P_multiplier':xm,'R_multiplier':ym,'identity':['1'],
                 'both_leading_coefficients_nonzero':True}
        break
    require(modular is not None,'small modular certificate found')
    damage_receipts=[]
    probes={
      'wrong_ODE4_pivot':lambda:eq('damaged_ODE4',F(35)*x1+sub(nth(aa['ODE'],4),9,0)),
      'wrong_G_pivot':lambda:eq('damaged_G',24*t*t*(-gF)+sub(nth(K,4),6,0)),
      'wrong_F_sign':lambda:eq('damaged_F',F(-15,14)*t*t*(-fstar)+sub(k3,5,0)),
      'wrong_J_sign':lambda:eq('damaged_J',-28*t*(-jstar)+sub(o3,7,0)),
      'wrong_Bezout':lambda:require(fadd(fmul(fadd(x,[1]),cubic),fmul(y,elim))==[1],'damaged Bezout'),
      'drop_conic':lambda:rank_controls('drop_conic'),
      'drop_positive':lambda:rank_controls('drop_positive'),
      'infinity_as_root':lambda:rank_controls('infinity_as_root')}
    for name,probe in probes.items():
        try:probe()
        except ValueError:damage_receipts.append(name)
        else:raise ValueError('mathematical damage survived '+name)
    record={'actual_agent':'six-sendov-2','role':'researcher','domain':'QQ[B,E,r,s,t,t^-1],N1,t>0',
      'universal_identities':sorted(checks),'solved_polynomials':{n:polydigest([a])for n,a in
        [('F',fstar),('G',gstar),('J',jstar),('p0',P0),('p1',P1),('p2',p2),('C',gamma)]},
      'entire_residual_polynomials':{n:polydigest([a])for n,a in zip(['tODE2','tODE1','tODE0','K1','K0plus4'],residuals)},
      'whole_matrix_rows':[polydigest(row)for row in matrix],
      'slice_cubic':[str(x)for x in cubic],'slice_degree_six':[str(x)for x in elim],
      'slice_modular_unit':modular,
      'slice_Bezout':{'cubic_multiplier':[str(v)for v in x],'eliminant_multiplier':[str(v)for v in y],'gcd':['1']},
      'rank_conic_controls':rank_controls(),'rejected_mathematical_damages':damage_receipts,
      'ordinary_bridges':'9496 feasible stationarity, linear pivot elimination, rank/conic linear algebra and Bezout incompatibility; unformalized',
      'feasibility_required':['seven SIMPLE REAL criticals','STRICT p(lambda)>0','ALL FIVE residuals','t>0'],
      'degree_five_stationary_solutions_classified':False,'complex_first_power_proved':False,'global_Cstar_c3_proved':False}
    if export is not None:
        def encode(a):return [[list(key[:5]),str(c)]for key,c in sorted(P(a).c.items())]
        export.write_text(json.dumps({'actual_agent':'six-sendov-2','role':'researcher',
          'variables':['B','E','r','s','t'],'domain':'QQ[B,E,r,s,t,t^-1],t>0,N1',
          'h_ascending':[encode(a)for a in hp],'p_ascending':[encode(a)for a in pp],
          'C':encode(gamma),'residuals_ascending':[encode(a)for a in residuals],
          'matrix_rows_ABC':[[encode(a)for a in row]for row in matrix],
          'monomial_format':'[five integral exponents,exact rational coefficient]; only t may have negative powers',
          'feasibility_required':record['feasibility_required'],
          'all_stationary_profiles_classified':False},indent=2,sort_keys=True)+'\n')
    return record


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit',action='store_true');parser.add_argument('--export',type=Path);args=parser.parse_args()
    record=make_certificate(args.export)
    if args.emit:args.expected.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    else:require(record==json.loads(args.expected.read_text()),'whole expected record mismatch')
    print(json.dumps({'status':'PASS','record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
      'universal_identities':len(record['universal_identities']),'quadratic_rows':5,
      'rank_conic_controls':len(record['rank_conic_controls']),
      'mathematical_damages':len(record['rejected_mathematical_damages'])}))


if __name__=='__main__':main()
