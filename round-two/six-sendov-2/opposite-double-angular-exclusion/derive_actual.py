"""Separate dense QQ derivation of every actual-identity field and actual case.

SymPy1.14.0, same author six-sendov-2/researcher. Imports no native arithmetic.
Written reduction exposed; this is an algebra check, not independent review.
"""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import json
import sympy as sp

BASE=Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def exact_same(a,b):
    need(type(a)is type(b),"exact record type")
    if type(a)is dict:
        need(set(a)==set(b),"entire record keys")
        for k in a:exact_same(a[k],b[k])
    elif type(a)is list:
        need(len(a)==len(b),"entire record list length")
        for x,y in zip(a,b):exact_same(x,y)
    else:need(a==b,"entire record scalar")
def canonical(x):return (json.dumps(x,sort_keys=True,indent=2)+"\n").encode()

def run(input_path,record_path):
    need(sp.__version__=="1.14.0","documented SymPy version")
    data=json.loads(input_path.read_text());cert=data["inherited_defining_data"]
    need(sha256(canonical(cert)).hexdigest()=="080a36d30d22e43eccb52aa67fcaace9c71b569f617967d23db1d309aac004d5",
         "entire credited defining source")
    p,tau,s,l,z,y=sp.symbols("p tau s lambda z y")
    def decode(rows,a,b):return sum(sp.Rational(r["coefficient"])*a**r["powers"][0]*b**r["powers"][1]for r in rows)
    def rows(expr):
        return [{"powers":list(k),"coefficient":str(c)}for k,c in sorted(sp.Poly(expr,s,l,domain=sp.QQ).as_dict().items())if c]
    def zrows(expr):
        poly=sp.Poly(expr,z)
        if poly.is_zero:return [[]]
        return [rows(poly.nth(k))for k in range(poly.degree()+1)]
    def check(expr,gate):need(sp.expand(expr)==0,gate)
    oldH=sum(decode(r,p,tau)*z**k for k,r in enumerate(cert["critical_quintic"]))
    oldI=sum(decode(r,p,tau)*z**k for k,r in enumerate(cert["inverse_numerators"]))
    oldDelta=decode(cert["inverse_common_denominator"],p,tau)
    oldDisc=decode(cert["discriminant"],p,tau)
    num=decode(cert["angular_numerator_y_tau"],y,tau)
    den=decode(cert["angular_denominator_y_tau"],y,tau)
    d=z*z+s*z-1
    quartic=sp.expand((z*z-s*z-1)**2+l*((z-s)**2-1))
    f=sp.expand(d*d*quartic);h=sp.diff(f,z)/8
    H,rem=sp.div(h,d,z);check(rem,"actual canceled factor")
    oldf=sp.expand((z*z-p*z+1)**2*((z*z+p*z+1)**2-tau*((z+p)**2+1)))
    rotation={p:-sp.I*s,tau:l,z:sp.I*z}
    check(oldf.subs(rotation,simultaneous=True)-f,"whole octic rotation")
    check((sp.diff(oldf,z)/8).subs(rotation,simultaneous=True)+sp.I*h,"whole derivative rotation")
    check(oldH.subs(rotation,simultaneous=True)-sp.I*H,"whole quintic rotation")
    Delta=sp.expand(oldDelta.subs({p:-sp.I*s,tau:l},simultaneous=True))
    I=sp.expand(oldI.subs(rotation,simultaneous=True))
    disc=sp.discriminant(H,z)
    check(oldDelta-16*oldDisc,"entire inherited discriminant")
    check(Delta-16*disc,"whole actual inverse/discriminant")
    iq,rem=sp.div(sp.diff(H,z)*I,H,z);check(rem-Delta,"whole actual inverse")
    mass=sp.rem(sp.expand(-8*d*quartic*I),H,z)
    mass2=sp.rem(sp.expand(mass*mass),H,z)
    def trace(expr,poly):
        hc=sp.Poly(poly,z).all_coeffs();degree=len(hc)-1
        tr={0:sp.Integer(degree)}
        for k in range(1,degree):
            tr[k]=sp.expand(-sum(hc[j]*tr[k-j]for j in range(1,k))-k*hc[k])
        return sp.expand(sum(c*tr[k[0]]for k,c in sp.Poly(expr,z).terms()))
    N=4*s*s+8-2*l
    X=sp.expand(N*N/2-4*f.coeff(z,4))
    D=sp.expand(X-N*N/8)
    mt=trace(mass,H);eta=trace(mass2,H)
    check(mt-N*Delta,"all five gap masses")
    nn=sp.expand(num.subs({y:-s*s,tau:l},simultaneous=True))
    dd=sp.expand(den.subs({y:-s*s,tau:l},simultaneous=True))
    check(dd-8192*D*disc,"actual positive denominator")
    lhs=sp.expand((N*N*Delta*Delta-eta)*dd)
    rhs=sp.expand(D*Delta*Delta*nn)
    check(lhs-rhs,"whole500-monomial trace identity")
    need(len(sp.Poly(lhs,s,l).terms())==500,"entire identity support")
    identity={
        "whole_f":zrows(f),"whole_h":zrows(h),"whole_quartic":zrows(quartic),
        "whole_H5":zrows(H),"whole_discriminant":rows(disc),
        "whole_inverse_denominator":rows(Delta),"whole_inverse_numerators":zrows(I),
        "whole_inverse_quotient":zrows(iq),"whole_mass_remainder":zrows(mass),
        "whole_squared_mass_remainder":zrows(mass2),
        "whole_mass_trace":rows(mt),"whole_eta_numerator":rows(eta),
        "whole_raw_N":rows(N),"whole_raw_X":rows(X),"whole_raw_D":rows(D),
        "whole_transferred_num":rows(nn),"whole_transferred_den":rows(dd),
        "whole_cleared_identity":rows(lhs),
    }
    def sturm(poly):
        poly=sp.Poly(poly,z,domain=sp.QQ)
        chain=[poly,poly.diff()]
        while True:
            rem=chain[-2].rem(chain[-1])
            if rem.is_zero:break
            chain.append(-rem)
        zero=int(poly.nth(0)==0)
        return {"positive_distinct":int(poly.count_roots(0,sp.oo))-zero,
                "negative_distinct":int(poly.count_roots(-sp.oo,0))-zero,
                "zero_distinct":zero,"gcd_degree":int(poly.gcd(poly.diff()).degree()),
                "entire_sturm_chain":[[str(row.nth(i))for i in range(row.degree()+1)]for row in chain]}
    cases=[]
    for sv,lv in [(sp.Rational(36,125),sp.Integer(1)),(sp.Rational(171,1000),sp.Rational(4,5)),
                  (sp.Rational(66,125),sp.Integer(-3)),(sp.Integer(0),None)]:
        if lv is None:qv=sp.Poly(z**4-5*z*z+6,z,domain=sp.QQ);fv=sp.Poly((z*z-1)**2*qv.as_expr(),z,domain=sp.QQ)
        else:qv=sp.Poly(quartic.subs({s:sv,l:lv}),z,domain=sp.QQ);fv=sp.Poly(f.subs({s:sv,l:lv}),z,domain=sp.QQ)
        hv=sp.Poly(fv.diff().as_expr()/8,z,domain=sp.QQ)
        inverse=sp.invert(hv.diff(),hv)
        mr=sp.rem(-8*fv.as_expr()*inverse.as_expr(),hv.as_expr(),z)
        mr2=sp.rem(mr*mr,hv.as_expr(),z)
        mat=sp.zeros(7)
        for j in range(6):mat[j+1,j]=1
        for j in range(7):mat[j,6]=-hv.nth(j)
        def evaluate(expr):
            result=sp.zeros(7);poly=sp.Poly(expr,z)
            for k,c in poly.terms():result+=c*mat**k[0]
            return result
        invmatrix=evaluate(inverse.as_expr());massmatrix=evaluate(mr)
        need(evaluate(hv.diff().as_expr())*invmatrix==sp.eye(7),"whole actual inverse matrix")
        moments=[sp.Integer(8)]
        for k in range(1,6):
            moments.append(sp.cancel(-k*fv.nth(8-k)-sum(fv.nth(8-j)*moments[k-j]for j in range(1,k))))
        nv=moments[2];xv=moments[4];dv=xv-nv*nv/8
        etav=trace(mr2,hv.as_expr());cv=sp.cancel((nv*nv-etav)/dv)
        need(trace(mr,hv.as_expr())==nv and sp.trace(massmatrix*massmatrix)==etav,"actual all-seven mass trace")
        need(moments[1]==moments[3]==moments[5]==0 and dv>0 and cv<sp.Rational(47,2),"actual normalization")
        if lv is not None:need(cv==sp.cancel(nn.subs({s:sv,l:lv})/dd.subs({s:sv,l:lv})),"all-seven generic specialization")
        cases.append({"s":str(sv),"lambda":None if lv is None else str(lv),
            "whole_quartic":[str(qv.nth(k))for k in range(5)],
            "whole_f":[str(fv.nth(k))for k in range(9)],
            "whole_h":[str(hv.nth(k))for k in range(8)],
            "whole_Q_Sturm":sturm(qv),"whole_f_Sturm":sturm(fv),"whole_h_Sturm":sturm(hv),
            "whole_derivative_inverse":[[str(invmatrix[i,j])for j in range(7)]for i in range(7)],
            "whole_mass_matrix":[[str(massmatrix[i,j])for j in range(7)]for i in range(7)],
            "moments":[str(c)for c in moments[1:]],"N":str(nv),"X":str(xv),"D":str(dv),
            "eta_raw":str(etav),"C":str(cv),"all_seven_slots_retained":True,
            "equal_magnitude_separate_even_branch":lv is None})
    record=json.loads(record_path.read_text())
    exact_same(identity,record["actual_identity"])
    exact_same(cases,record["actual_cases"])
    return {"actual_agent":"six-sendov-2","role":"researcher","sympy_version":sp.__version__,
            "complete_actual_identity_and_all4cases":True,"whole_identity_monomials":500,
            "whole_matrix_positions_compared":4*2*49,
            "whole_actual_identity_sha256":sha256(canonical(identity)).hexdigest(),
            "whole_actual_cases_sha256":sha256(canonical(cases)).hexdigest(),
            "ordinary_bridges_unformalized":True,"same_author_not_independent_review":True}

def main():
    p=ArgumentParser();p.add_argument("--input",type=Path,default=BASE/"INPUT.json")
    p.add_argument("--record",type=Path,required=True);p.add_argument("--receipt",type=Path)
    a=p.parse_args();result=run(a.input,a.record)
    if a.receipt:a.receipt.write_bytes(canonical(result))
    print(json.dumps(result))
if __name__=="__main__":main()
