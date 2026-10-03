"""Stdlib-only sparse QQ polynomial checker, independent of symbolic solver.

Every shifted coefficient is checked against the complete original
rational expression; aggregate term counts are not accepted as evidence.
"""
import ast,json,sys
from fractions import Fraction as F
from pathlib import Path
from math import comb
from literal_check import require
from bind_lower import value
P=Path(__file__).resolve().parent

def tidy(p):return {e:c for e,c in p.items() if c}
def add(a,b):
    c=dict(a)
    for e,v in b.items():c[e]=c.get(e,F(0))+v
    return tidy(c)
def scale(p,c):return tidy({e:v*c for e,v in p.items()})
def mul(a,b):
    out={}
    for (i,j),c in a.items():
        for (ii,jj),cc in b.items():
            e=(i+ii,j+jj);out[e]=out.get(e,F(0))+c*cc
    return tidy(out)
ONE={(0,0):F(1)};Q={(1,0):F(1)};K={(0,1):F(1)}
def power(a,n):
    require(type(n) is int and 0<=n<=128,'polynomial degree guard')
    b=ONE
    for _ in range(n):b=mul(b,a)
    return b
def poly(node):
    if isinstance(node,ast.Constant) and type(node.value) is int:return {(0,0):F(node.value)} if node.value else {}
    if isinstance(node,ast.Name) and node.id in ('q','k'):return Q if node.id=='q' else K
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return scale(poly(node.operand),-1)
    if isinstance(node,ast.BinOp):
        a=poly(node.left)
        if isinstance(node.op,ast.Pow):
            require(isinstance(node.right,ast.Constant) and type(node.right.value) is int,'literal integral exponent')
            return power(a,node.right.value)
        b=poly(node.right)
        if isinstance(node.op,ast.Add):return add(a,b)
        if isinstance(node.op,ast.Sub):return add(a,scale(b,-1))
        if isinstance(node.op,ast.Mult):return mul(a,b)
        if isinstance(node.op,ast.Div):
            require(set(b)=={(0,0)},'only rational constant division inside polynomial')
            return scale(a,1/b[(0,0)])
    raise ValueError('nonliteral polynomial')

def rational(text):
    node=ast.parse(text,mode='eval').body
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div):return poly(node.left),poly(node.right)
    return poly(node),ONE

def radd(a,b):return add(mul(a[0],b[1]),mul(b[0],a[1])),mul(a[1],b[1])
def rmul(a,b):return mul(a[0],b[0]),mul(a[1],b[1])
def rdiv(a,b):return mul(a[0],b[1]),mul(a[1],b[0])
def equal(a,b):return mul(a[0],b[1])==mul(a[1],b[0])

def substitute(poly,qform,kform):
    qa={0:ONE};ka={0:ONE}
    out={}
    for (i,j),c in poly.items():
        if i not in qa:qa[i]=power(qform,i)
        if j not in ka:ka[j]=power(kform,j)
        out=add(out,scale(mul(qa[i],ka[j]),c))
    return out

SHIFTS={'univariate4':(add(Q,scale(ONE,4)),K),
        'univariate21':(add(Q,scale(ONE,21)),K),
        'quadrant':(add(add(scale(ONE,21),scale(Q,3)),K),add(scale(ONE,7),Q))}
def certified(record,strict=True):
    vars=record['variables'];require(vars in (['x'],['x','u']),'certificate variables')
    out={};last=None
    for exponents,text in record['coefficients']:
        require(len(exponents)==len(vars) and all(type(i) is int and i>=0 for i in exponents),'complete coefficient exponents')
        e=tuple(exponents)+(0,) if len(exponents)==1 else tuple(exponents)
        require(e not in out,'no duplicated coefficient')
        c=F(text);require(c>0,'all serialized nonzero coefficients strictly positive')
        out[e]=c
    require(out.get((0,0),F(0))>0 if strict else (0,0) not in out,'required endpoint constant')
    return out

def compare(name,expression,record,shift,strict=True):
    c=certified(record,strict)
    require(c==substitute(expression,*SHIFTS[shift]),'ENTIRE coefficient identity '+name)
    return len(c)

def main():
    rec=json.loads((P/'lower-signs.json').read_text());ref=json.loads((P/'lower-refinement.json').read_text())
    base=rec['certificates'];extra=ref['certificates']
    if '--damage' in sys.argv:
        base['F_strict_bound']['coefficients'][0][1]=str(F(base['F_strict_bound']['coefficients'][0][1])+1)
    fields={name:rational(rec[name]) for name in ('nu0','nu_prime0','tau0','tau_prime0','F','a0')}
    nu,nd,tau,td,fun,a=[fields[n] for n in ('nu0','nu_prime0','tau0','tau_prime0','F','a0')]
    Fbuilt=radd(rmul((scale(ONE,2),ONE),rdiv(nd,rmul(nu,nu))),rdiv(td,rmul(tau,tau)))
    require(equal(fun,Fbuilt),'ENTIRE F derivative rational identity')
    # a=qk*nu*tau / ((q-k)*tau+k*nu), full two-variable identity.
    abuilt=rdiv(rmul((mul(Q,K),ONE),rmul(nu,tau)),radd(rmul((add(Q,scale(K,-1)),ONE),tau),rmul((K,ONE),nu)))
    require(equal(a,abuilt),'ENTIRE original zero separation field')
    counts={}
    for name,field,sgn in (('nu',nu,1),('tau',tau,1),('nu_derivative',nd,-1),('tau_derivative',td,1)):
        for part,expr in (('numerator',scale(field[0],sgn)),('denominator',field[1])):
            key=name+'_'+part;counts[key]=compare(key,expr,base[key],'univariate4')
    Fn,Fd=fun;an,ad=a
    counts['F_denominator']=compare('F_denominator',Fd,base['F_denominator'],'univariate21')
    counts['F_strict_bound']=compare('F_strict_bound',add(scale(mul(power(Q,5),Fn),-2),scale(Fd,-1)),base['F_strict_bound'],'univariate21')
    counts['a_denominator']=compare('a_denominator',ad,base['a_denominator'],'quadrant')
    counts['a_gt_q']=compare('a_gt_q',add(an,scale(mul(Q,ad),-1)),base['a_gt_q'],'quadrant')
    # Compare reduced b/2-a certificates by the complete cleared rational identity.
    bnum=mul(add(scale(Q,3),scale(ONE,4)),add(add(scale(power(Q,2),3),scale(Q,3)),scale(ONE,-2)))
    bden=add(add(scale(power(Q,2),6),scale(Q,5)),scale(ONE,-2))
    raw_n=add(mul(bnum,ad),scale(mul(bden,an),-1));raw_d=mul(bden,ad)
    cert_n=certified(base['b_half_minus_a']);cert_d=certified(base['b_half_minus_a_denominator'])
    require(mul(cert_n,substitute(raw_d,*SHIFTS['quadrant']))==mul(cert_d,substitute(raw_n,*SHIFTS['quadrant'])),'ENTIRE b/2-a sign fraction')
    counts.update(b_half_minus_a=len(cert_n),b_half_minus_a_denominator=len(cert_d))
    counts['a_gt_7q_over5']=compare('a_gt_7q_over5',add(scale(an,5),scale(mul(Q,ad),-7)),extra['a_gt_7q_over5'],'quadrant')
    counts['F_lt_minus25_over49q5']=compare('F_lt_minus25_over49q5',add(scale(mul(power(Q,5),Fn),-49),scale(Fd,-25)),extra['F_lt_minus25_over49q5'],'univariate21')
    c=F(ref['point_sharp_constant']);require(c==-21**5*value(rec['F'],{'q':21}) and c>F(25,49),'exact optimal F endpoint')
    counts['sharp_F_normalization']=compare('sharp_F_normalization',add(scale(mul(power(Q,5),Fn),-1),scale(Fd,-c)),extra['sharp_F_normalization'],'univariate21',False)
    require((1,0) in certified(extra['sharp_F_normalization'],False),'strict sharp bound for EVERY q>21')
    out={'status':'complete stdlib coefficient and rational identities verified','certificates':len(counts),'coefficients':sum(counts.values()),
         'counts':counts,'new_bound':'a0_prime<-1/q^4','CAS_imported':False,'producer_code_used':False}
    (P/'polynomial-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
