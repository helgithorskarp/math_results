"""Exact rational critical-vertex identities and positive branch signs.
All geometry is recomputed with SymPy over QQ; no float signs.
"""
import sympy as s
import json,math,time
def critical():
    started=time.monotonic();t,z=s.symbols('t z');one=s.Integer(1)
    H=(1-t)*s.eye(3)+t*s.ones(3);HI=H.inv()
    r=2*t/(1+t);D=(1-t)**2*(1+2*t);C=1+D*z*z
    B={1:s.Matrix([1,0,0]),2:s.Matrix([0,1,0]),4:s.Matrix([0,0,1])}
    for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
        B[n]=(r*(B[i]+B[j])-B[o]).applyfunc(s.cancel)
    W=(t*B[12]+(D*z*z-1)/C*(B[1]-t*B[12])+2*D*z/C*HI*(B[12].cross(B[1]))).applyfunc(s.cancel)
    a=s.cancel((W.T*H*B[1])[0]);b=s.cancel((W.T*H*B[4])[0])
    de=s.factor(1+2*t*a*b-t*t-a*a-b*b)
    cof=3-t*t-a*a-b*b+2*(a*b-t-a-b+t*a+t*b)
    norm=s.factor(s.cancel(t*t*cof/de))
    gap=s.factor(s.cancel(norm-1));derivative=s.factor(s.cancel(s.diff(norm,z)))
    def bernstein(p):
        L,R=s.Rational(577,1000),s.Rational(593,1000)
        A,B=s.Rational(9,10),s.Rational(7,5)
        p=s.Poly(p,t,z,domain=s.QQ);nt,nz=p.degree(t),p.degree(z)
        shifted=s.Poly(p.as_expr().subs({t:L+(R-L)*t,z:A+(B-A)*z}),t,z,domain=s.QQ)
        coeffs=[]
        for i in range(nt+1):
            for j in range(nz+1):
                coeffs.append(sum(shifted.coeff_monomial(t**u*z**v)*s.Rational(math.comb(i,u),math.comb(nt,u))*s.Rational(math.comb(j,v),math.comb(nz,v)) for u in range(i+1) for v in range(j+1)))
        return {'degrees':[nt,nz],'min':str(min(coeffs)),'max':str(max(coeffs)),
                'strict_positive':bool(min(coeffs)>0),'strict_negative':bool(max(coeffs)<0)}
    expressions={'a':a,'b':b,'gram_det':de,'norm2':norm,'norm2_minus_one':gap,'z_derivative_norm2':derivative}
    out={key:{'expression':str(v)} for key,v in expressions.items()}
    for key in ('gram_det','z_derivative_norm2'):
        nu,dn=s.fraction(expressions[key]);out[key]['numerator_bernstein']=bernstein(nu);out[key]['denominator_bernstein']=bernstein(dn)
    result={'status':'EXACT_IDENTITIES_AND_RECTANGLE_SIGNS','agent':'six-tammes-2','role':'researcher',
            'domain':['577/1000','593/1000','9/10','7/5'],'results':out}
    return result

def boundary():
    started=time.monotonic();t=s.Symbol('t');z=2*t*t/(t**3-3*t*t+t+1)
    H=(1-t)*s.eye(3)+t*s.ones(3);HI=H.inv()
    r=2*t/(1+t);D=(1-t)**2*(1+2*t);C=1+D*z*z
    k=t*(9*t*t-2*t-3)/(1+t)**2;gam=k/(1+k)
    mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/(9*t**3-t*t-t+1)
    B={1:s.Matrix([1,0,0]),2:s.Matrix([0,1,0]),4:s.Matrix([0,0,1])}
    for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
        B[n]=(r*(B[i]+B[j])-B[o]).applyfunc(s.cancel)
    W=(t*B[12]+(D*z*z-1)/C*(B[1]-t*B[12])+2*D*z/C*HI*B[12].cross(B[1])).applyfunc(s.cancel)
    ss=s.cancel((W.T*H*B[10])[0]);de=1-ss*ss
    R=s.factor(s.cancel(D*(de-k*k-t*t+2*ss*k*t)))
    V0=(((k-ss*t)*W+(t-ss*k)*B[10])/de).applyfunc(s.cancel)
    V1=(-HI*W.cross(B[10])/de).applyfunc(s.cancel)
    U0=(gam*(W+V0)+mu*HI*W.cross(V0)).applyfunc(s.cancel)
    U1=(gam*V1+mu*HI*W.cross(V1)).applyfunc(s.cancel)
    a=s.factor(s.cancel((U0.T*H*B[8])[0]-t))
    b=s.factor(s.cancel((U1.T*H*B[8])[0]))
    delta=s.factor(s.cancel(a*a-b*b*R))
    def bernstein(p):
        L,R=s.Rational(577,1000),s.Rational(593,1000)
        p=s.Poly(p,t,domain=s.QQ);n=p.degree()
        shifted=s.Poly(p.as_expr().subs(t,L+(R-L)*t),t,domain=s.QQ)
        coeffs=[sum(shifted.nth(i)*s.Rational(math.comb(j,i),math.comb(n,i)) for i in range(j+1)) for j in range(n+1)]
        return {'degree':n,'min':str(min(coeffs)),'max':str(max(coeffs)),
                'strict_positive':bool(min(coeffs)>0),'strict_negative':bool(max(coeffs)<0)}
    expressions={'z_unit_boundary':z,'radicand':R,'raw_de':s.factor(s.cancel(de)),'raw_C':s.factor(s.cancel(C)),'one_plus_k':s.factor(s.cancel(1+k)),'A_denominator':t**3-3*t*t+t+1,'rational_gap_a':a,'radical_gap_b':b,'squared_gap_difference':delta}
    out={key:{'expression':str(value)} for key,value in expressions.items()}
    for key in ('radicand','raw_de','raw_C','one_plus_k','A_denominator','rational_gap_a','radical_gap_b'):
        nu,dn=s.fraction(expressions[key]);out[key]['numerator_bernstein']=bernstein(nu);out[key]['denominator_bernstein']=bernstein(dn)
    result={'status':'EXACT_BOUNDARY_IDENTITIES','domain':['577/1000','593/1000'],'results':out}
    return result

def simplify(data):
    started=time.monotonic();t=s.Symbol('t')
    data=data['results']
    a,b,R=[s.sympify(data[key]['expression'],locals={'t':t}) for key in ('rational_gap_a','radical_gap_b','radicand')]
    P5=4*t**5-19*t**4-2*t**3+4*t**2-2*t-1
    P4=8*t**4-3*t**3-t**2+3*t+1
    root=-(t-1)**2*(2*t+1)*(3*t+1)*P5/((t+1)**2*P4)
    if s.cancel(root*root-R)!=0:raise ValueError('exact positive square-root identity')
    F=13*t**5-t**4+6*t**3+2*t*t-3*t-1
    gap=s.factor(s.cancel(a+b*root))
    quotient=s.factor(s.cancel(gap/F))
    def bernstein(p):
        L,H=s.Rational(577,1000),s.Rational(593,1000)
        p=s.Poly(p,t,domain=s.QQ);n=p.degree()
        u=s.Poly(p.as_expr().subs(t,L+(H-L)*t),t,domain=s.QQ)
        rows=[sum(u.nth(i)*s.Rational(math.comb(j,i),math.comb(n,i)) for i in range(j+1)) for j in range(n+1)]
        return {'degree':n,'min':str(min(rows)),'max':str(max(rows)),
                'strict_positive':bool(min(rows)>0),'strict_negative':bool(max(rows)<0)}
    A=t**3-3*t*t+t+1
    wanted={'A':A,'19_20_A_minus_2t2':s.Rational(19,20)*A-2*t*t,
            'P5':P5,'P4':P4,'F_derivative':s.diff(F,t)}
    for name,value in [('positive_square_root',root),('gap_over_F',quotient)]:
        n,d=s.fraction(value);wanted[name+'_numerator']=n;wanted[name+'_denominator']=d
    out={'status':'EXACT_BOUNDARY_GAP_FACTOR_AND_SIGNS','gap_at_unit_boundary':str(gap),
         'positive_square_root':str(root),'gap_over_F':str(quotient),
         'bernstein_signs':{k:bernstein(p) for k,p in wanted.items()},
         'F_values':{str(v):str(F.subs(t,v)) for v in (s.Rational(577,1000),s.Rational(593,1000),s.Rational('0.59260590292507377809642492233275'),s.Rational('0.59260590292507377809642492233276'))},
}
    return out

def derive():
    x=critical();y=boundary();z=simplify(y)
    need=lambda ok,msg: None if ok else (_ for _ in ()).throw(ValueError(msg))
    need(x['results']['gram_det']['numerator_bernstein']['strict_positive'],'critical Gram numerator')
    need(x['results']['gram_det']['denominator_bernstein']['strict_positive'],'critical Gram denominator')
    need(x['results']['z_derivative_norm2']['numerator_bernstein']['strict_negative'],'critical norm derivative numerator')
    need(x['results']['z_derivative_norm2']['denominator_bernstein']['strict_positive'],'critical norm derivative denominator')
    for key in ('radicand','raw_de','raw_C','one_plus_k','A_denominator'):
        for side in ('numerator','denominator'):
            need(y['results'][key][side+'_bernstein']['strict_positive'],'strict boundary domain '+key+' '+side)
    for key,item in z['bernstein_signs'].items():
        expected='strict_negative' if key in ('P5','gap_over_F_numerator') else 'strict_positive'
        need(item[expected],'boundary factor sign '+key)
    vals=list(z['F_values'].values())
    need(s.Rational(vals[0])<0<s.Rational(vals[1]),'incumbent root in J')
    need(s.Rational(vals[2])<0<s.Rational(vals[3]),'exact incumbent root bracket')
    return {'critical':x,'boundary':y,'boundary_factor_signs':z}
