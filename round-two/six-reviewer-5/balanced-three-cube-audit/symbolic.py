"""Independent original-row frame reconstruction; QQ(h), no producer imports.

Representative facet categories have multiplicities 1,1,h-2. Products are
evaluated from primitive Gram rules; cap determinants use permutation sums.
"""
import argparse
from itertools import permutations
import json
from pathlib import Path
import sympy as sp

h = sp.Symbol('h')
s, D, ell, N = 3*h+4, 3*h, 6*h+1, 12*h+8
w = s-1
q = 4
weights = [sp.Integer(1), sp.Integer(1), h-2]
Aold = sp.Matrix(7, 7, lambda i,j: (q+D)*int(i==j)
                 +(q-D)*int((i+1)+(j+1)==7)-1)
G = sp.ones(7,1)
gF = sp.zeros(7,1); gF[6]=1
Hx = sp.Matrix([-int((i+1)&1!=0) for i in range(7)])
Hy = sp.Matrix([-int((i+1)&2!=0) for i in range(7)])
K = G+Hx+Hy
z = -K/ell
B2 = s*(h-1)/(3*h)
a = 3*h*(3*h-1)/(ell*s*(h-1))
b = -2*a
c = 9*(3*h-1)/(ell*s)
c0 = sp.cancel((K.T*Aold*K)[0]/ell**2)
etaL = sp.cancel(w-c0-a*a*B2-2*s*c*c/3)
etaF = sp.cancel(w-c0-b*b*B2-2*s*c*c/(3*(h-1)))
p = sp.cancel(-1-c0-a*b*B2)
mu = sp.cancel((2*p+etaF)/3)
alpha = sp.cancel(2*(2*etaL-p-etaF))
beta = sp.cancel(etaF-mu)
nu = sp.cancel(2*h*mu/(2*h-1))

def require(condition, message):
    if not condition: raise ValueError(message)

def simplify(x):
    return sp.cancel(x)

def newvec(old=None):
    return dict(old=sp.zeros(7,1) if old is None else old,
                B=[[sp.Integer(0)]*3 for _ in range(2)],
                T=[[[sp.Integer(0)]*3 for _ in range(3)] for _ in range(2)],
                M=[[sp.Integer(0)]*3 for _ in range(2)],
                WA=[[sp.Integer(0)]*3 for _ in range(2)],
                WF=[[sp.Integer(0)]*3 for _ in range(2)])

def inner(u,v):
    result=(u['old'].T*Aold*v['old'])[0]
    for group in range(2):
        ub,vb=u['B'][group],v['B'][group]
        result += s/3*(sum(weights[i]*ub[i]*vb[i] for i in range(3))
                       -sum(weights[i]*ub[i] for i in range(3))
                       *sum(weights[i]*vb[i] for i in range(3))/h)
        for i in range(3):
            ut,vt=u['T'][group][i],v['T'][group][i]
            result += weights[i]*s*(sum(ut[j]*vt[j] for j in range(3))
                                    -sum(ut)*sum(vt)/3)
            result += weights[i]*(alpha*u['WA'][group][i]*v['WA'][group][i]
                                   +beta*u['WF'][group][i]*v['WF'][group][i])
    um=sum(weights[i]*u['M'][g][i] for g in range(2) for i in range(3))
    vm=sum(weights[i]*v['M'][g][i] for g in range(2) for i in range(3))
    result += nu*(sum(weights[i]*u['M'][g][i]*v['M'][g][i]
                      for g in range(2) for i in range(3))-um*vm/(2*h))
    return simplify(result)

def row_dot(v,kind,group=0,i=0,leaf=0,oldmask=1):
    if kind=='old': return simplify((Aold*v['old'])[oldmask-1])
    if kind=='empty': return simplify((z.T*Aold*v['old'])[0])
    vb=v['B'][group]
    Bdot=s/3*(vb[i]-sum(weights[j]*vb[j] for j in range(3))/h)
    def Tdot(index,coord):
        row=v['T'][group][index]
        return s*(row[coord]-sum(row)/3)
    if kind=='marked':
        old=Hx if group==0 else Hy
        return simplify((old.T*Aold*v['old'])[0]/D+Bdot+Tdot(i,leaf))
    olddot=(z.T*Aold*v['old'])[0]
    mdot=nu*(v['M'][group][i]-sum(weights[j]*v['M'][g][j]
                                  for g in range(2) for j in range(3))/(2*h))
    if leaf<2:
        result=olddot+a*Bdot+c*Tdot(i,1-leaf)+mdot
        result += alpha*v['WA'][group][i]*(1 if leaf==0 else -1)/2
        result -= beta*v['WF'][group][i]/2
    else:
        result=olddot+b*Bdot+c/(h-1)*(sum(weights[j]*Tdot(j,2)
                                          for j in range(3))-Tdot(i,2))+mdot
        result += beta*v['WF'][group][i]
    return simplify(result)

def basis_blocks():
    leaf=[newvec(),newvec()]
    leaf[0]['T'][0][0]=[sp.Integer(1),sp.Integer(-1),sp.Integer(0)]
    leaf[1]['WA'][0][0]=sp.Integer(1)
    standard=[newvec() for _ in range(4)]
    for i,sign in [(0,sp.Integer(1)),(1,sp.Integer(-1))]:
        standard[0]['B'][0][i]=sign
        standard[1]['T'][0][i]=[sign,sign,-2*sign]
        standard[2]['WF'][0][i]=sign
        standard[3]['M'][0][i]=sign
    even=[newvec(G-gF),newvec(G+gF),newvec(K+gF),newvec(),newvec()]
    odd=[newvec(Hx-Hy),newvec(),newvec(),newvec()]
    for group in range(2):
        sign=sp.Integer(1 if group==0 else -1)
        for i in range(3):
            even[3]['T'][group][i]=[sp.Integer(1),sp.Integer(1),sp.Integer(-2)]
            even[4]['WF'][group][i]=sp.Integer(1)
            odd[1]['T'][group][i]=[sign,sign,-2*sign]
            odd[2]['WF'][group][i]=sign
            odd[3]['M'][group][i]=sign
    old=[newvec(sp.Matrix(x)) for x in
         [[1,-1,0,0,-1,1,0],[1,1,-2,-2,1,1,0],[1,1,0,0,-1,-1,0]]]
    return dict(leaf=leaf,standard=standard,even=even,odd=odd,untouched=old)

def frame_forms(blocks):
    vectors=[v for block in blocks.values() for v in block]
    rows=[]
    for mask in range(1,8):
        rows.append((sp.Integer(1),[row_dot(v,'old',oldmask=mask) for v in vectors]))
    rows.append((sp.Integer(1),[row_dot(v,'empty') for v in vectors]))
    for group in range(2):
        for i in range(3):
            for leaf in range(3):
                for kind in ['marked','private']:
                    rows.append((weights[i],[row_dot(v,kind,group,i,leaf) for v in vectors]))
    metric=sp.Matrix(len(vectors),len(vectors),lambda i,j: inner(vectors[i],vectors[j]))
    frame=sp.zeros(len(vectors))
    for i in range(len(vectors)):
        for j in range(i,len(vectors)):
            frame[i,j]=frame[j,i]=simplify(sum(mult*row[i]*row[j] for mult,row in rows))
    index=0
    out={}
    slices=[]
    for name,block in blocks.items():
        size=len(block); slices.append((name,index,index+size))
        gram=metric[index:index+size,index:index+size]
        sf=frame[index:index+size,index:index+size]
        require(all(gram[i,j]==0 for i in range(size) for j in range(size) if i!=j),
                'diagonal physical metric '+name)
        out[name]=dict(metric=gram,frame=sf,cap=((N-1)*gram-sf).applyfunc(simplify))
        index+=size
    for name,start,end in slices:
        for other,lo,hi in slices:
            if name==other: continue
            require(all(metric[i,j]==0 and frame[i,j]==0
                        for i in range(start,end) for j in range(lo,hi)),
                    'full cross-sector forms '+name+' '+other)
    return out

def det_permutation(matrix):
    n=matrix.rows
    out=sp.Poly(0,h,domain=sp.QQ)
    for permutation in permutations(range(n)):
        sign=(-1)**sum(permutation[i]>permutation[j] for i in range(n) for j in range(i+1,n))
        term=sp.Poly(sign,h,domain=sp.QQ)
        for i,j in enumerate(permutation): term *= sp.Poly(matrix[i,j],h,domain=sp.QQ)
        out += term
    return out

def positive_denominator(expression):
    polynomial=sp.Poly(expression,h,domain=sp.QQ)
    constant,factors=sp.factor_list(polynomial)
    require(constant>0,'positive denominator scalar')
    for factor,power in factors:
        coefficients=sp.Poly(factor,h).all_coeffs()
        require(len(coefficients)==2 and factor.eval(2)>0 and coefficients[0]>0,
                'known strictly positive affine pole')
    return dict(constant=constant,factors=[dict(polynomial=f.as_expr(),power=k) for f,k in factors])

def signs(forms):
    record=[]
    for name,value in [('mu',mu),('alpha',alpha),('beta',beta)]:
        num,den=sp.fraction(value)
        denominator=positive_denominator(den)
        shifted=sp.Poly(num.subs(h,h+2),h,domain=sp.QQ)
        require(shifted.eval(0)>0 and all(v>=0 for v in shifted.all_coeffs()),'scalar '+name)
        record.append(dict(name=name,original=value,denominator=den,
                           denominator_factors=denominator,shifted_numerator=shifted.as_expr()))
    for name in ['leaf','standard','even','odd']:
        matrix=forms[name]['cap']
        denominators=[]
        cleared=sp.zeros(matrix.rows)
        for i in range(matrix.rows):
            den=sp.Poly(1,h,domain=sp.QQ)
            for j in range(matrix.cols):
                den=sp.lcm(den,sp.Poly(sp.denom(matrix[i,j]),h,domain=sp.QQ))
            den=den.monic()
            denominators.append(den.as_expr())
            positive_denominator(den.as_expr())
            for j in range(matrix.cols): cleared[i,j]=simplify(den.as_expr()*matrix[i,j])
        minors=[]
        for k in range(1,matrix.rows+1):
            polynomial=det_permutation(cleared[:k,:k])
            shifted=sp.Poly(polynomial.as_expr().subs(h,h+2),h,domain=sp.QQ)
            require(shifted.eval(0)>0 and all(v>=0 for v in shifted.all_coeffs()),
                    'all-h strict cap leading minor '+name+str(k))
            minors.append(dict(size=k,polynomial=polynomial.as_expr(),degree=polynomial.degree(),
                               shifted=shifted.as_expr()))
        record.append(dict(name=name,row_denominators=denominators,
                           original=matrix,cleared=cleared,minors=minors))
    for i in range(3):
        value=forms['untouched']['cap'][i,i]
        polynomial=sp.Poly(value.subs(h,h+2),h,domain=sp.QQ)
        require(polynomial.eval(0)>0 and all(v>=0 for v in polynomial.all_coeffs()),
                'untouched positive direction')
    return record

def encode(value):
    if isinstance(value,sp.MatrixBase): return [[encode(x) for x in value.row(i)] for i in range(value.rows)]
    if isinstance(value,sp.Basic):
        num,den=sp.fraction(value)
        def coefficients(expr):
            p=sp.Poly(expr,h,domain=sp.QQ)
            return [[int(c.p),int(c.q)] for c in reversed(p.all_coeffs())]
        return dict(numerator=coefficients(num),denominator=coefficients(den))
    if isinstance(value,dict): return {k:encode(v) for k,v in sorted(value.items())}
    if isinstance(value,(tuple,list)): return [encode(v) for v in value]
    return value

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    blocks=basis_blocks()
    forms=frame_forms(blocks)
    obligations=signs(forms)
    kappa=simplify(2/nu+4/beta)
    delta=simplify(1/(4*(8+kappa)))
    record=dict(schema='reviewer5-q4-balanced-original-frame-v1',
                field='QQ(h), characteristic0; h>=2 for signs, integer h>=2 for family',
                scalars=dict(h=h,s=s,D=D,ell=ell,N=N,w=w,a=a,b=b,c=c,c0=c0,
                             etaL=etaL,etaF=etaF,p=p,mu=mu,alpha=alpha,beta=beta,
                             nu=nu,kappa=kappa,delta=delta),forms=forms,signs=obligations)
    payload=(json.dumps(encode(record),sort_keys=True,separators=(',',':'))+'\n').encode()
    args.output.write_bytes(payload)
    print(json.dumps(dict(status='all-h original-row forms and strict signs proved',
                         record_bytes=len(payload),sign_obligations=18,
                         cap_minor_degrees={r['name']:[x['degree'] for x in r['minors']]
                                           for r in obligations if 'minors' in r}),sort_keys=True))

if __name__=='__main__': main()
