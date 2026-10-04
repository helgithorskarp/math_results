"""Separate dense Horner/INVERSE Bernstein proof for the entire sector data.

SymPy1.14.0; no native arithmetic imported. Same author, not independent review.
Both whole rational maps and all3200 inverse-basis images are compared.
"""
from argparse import ArgumentParser
from pathlib import Path
import json
from math import comb
import sympy as sp
from derive_actual import need, exact_same, canonical, sha256

BASE=Path(__file__).resolve().parent
COVER=[["0","1/2"],["1/2","3/4"],["3/4","7/8"],["7/8","1"]]

def run(input_path,record_path):
    need(sp.__version__=="1.14.0","documented SymPy version")
    data=json.loads(input_path.read_text());cert=data["inherited_defining_data"]
    need(sha256(canonical(cert)).hexdigest()=="080a36d30d22e43eccb52aa67fcaace9c71b569f617967d23db1d309aac004d5",
         "entire credited defining source")
    record=json.loads(record_path.read_text())
    v,b,y,tau=sp.symbols("v b y tau")
    def rows(poly):
        return [{"powers":list(k),"coefficient":str(c)}for k,c in sorted(poly.as_dict().items())if c]
    def decode(rr):
        return {(r["powers"][0],r["powers"][1]):sp.Rational(r["coefficient"])for r in rr}
    num=decode(cert["angular_numerator_y_tau"]);den=decode(cert["angular_denominator_y_tau"])
    Yn=sp.Poly(-v*v-v**3,v,b,domain=sp.QQ)
    Tn=sp.Poly(-v*(v+2)**2-b,v,b,domain=sp.QQ)
    def polynomial_horner(original,Y,T):
        degree=max(j for i,j in original)
        columns=[sp.Poly(sum(c*Y.as_expr()**i for(i,j),c in original.items()if j==k),v,b,domain=sp.QQ)for k in range(degree+1)]
        result=columns[-1]
        for k in range(degree-1,-1,-1):result=T*result+columns[k]
        return result
    dn=polynomial_horner(den,Yn,Tn)
    gn=dn*16-polynomial_horner(num,Yn,Tn)
    need(len(dn.as_dict())==210 and len(gn.as_dict())==202 and
         all(c>0 for p in [dn,gn]for c in p.coeffs()),"all412 negative-sector coefficients")
    def leading(p):
        eps=sp.Symbol("epsilon")
        e=sp.Poly(p.as_expr().subs({v:eps*eps,b:eps},simultaneous=True),eps,domain=sp.QQ)
        degree=min(k[0]for k in e.as_dict())
        return {"degree":degree,"coefficient":str(e.nth(degree))}
    neg={"Y":rows(Yn),"T":rows(Tn),"whole_den":rows(dn),"whole_gap16":rows(gn),
         "sharp_den_leading":leading(dn),"sharp_gap_leading":leading(gn)}
    exact_same(neg,record["negative_sector"])
    Y=sp.Poly(-v*v+v**3,v,b,domain=sp.QQ)
    M=sp.Poly(1-v*v+v**3,v,b,domain=sp.QQ)
    L=sp.Poly(v*(2-v)**2,v,b,domain=sp.QQ)
    T=L*M+sp.Poly(b,v,b,domain=sp.QQ)*(sp.Poly(1,v,b,domain=sp.QQ)-L*M)
    def clear(original):
        degree=9
        columns=[sp.Poly(sum(c*Y.as_expr()**i for(i,j),c in original.items()if j==k),v,b,domain=sp.QQ)for k in range(degree+1)]
        result=columns[-1]
        for k in range(degree-1,-1,-1):result=T*result+columns[k]*M**(degree-k)
        return result
    de=clear(den);gap=de*sp.Rational(47,2)-clear(num)
    positive=record["positive_sector"]
    exact_same({"Y":rows(Y),"M":rows(M),"L":rows(L),"T_numerator":rows(T)},positive["substitution"])
    exact_same(rows(gap),positive["whole_cleared_gap"])
    exact_same([r["b_interval"]for r in positive["closed_gap_cover"]],COVER)
    def affine(poly,c,d):
        coefficients=poly.as_dict();degree=poly.degree(b)
        columns=[sp.Poly(sum(a*v**i for(i,j),a in coefficients.items()if j==k),v,b,domain=sp.QQ)for k in range(degree+1)]
        result=columns[-1];linear=sp.Poly(c+(d-c)*b,v,b,domain=sp.QQ)
        for k in range(degree-1,-1,-1):result=linear*result+columns[k]
        return result
    def inverse_check(poly,field):
        exact_same(field["degrees"],[63,9])
        exact_same(rows(poly),field["whole_polynomial"])
        expected={k:c*sp.Rational(5,9)**k[0]for k,c in poly.as_dict().items()}
        exact_same(rows(sp.Poly.from_dict(expected,v,b,domain=sp.QQ)),field["whole_unit_polynomial"])
        vector=field["whole_Bernstein"]
        need(type(vector)is list and len(vector)==64 and all(type(r)is list and len(r)==10 for r in vector),
             "every tensor slot present")
        values=[]
        for rr in vector:
            for c in rr:
                need(type(c)is str,"exact Bernstein string")
                q=sp.Rational(c);need(str(q)==c and q>=0,"canonical whole nonnegative controls")
                values.append(q)
        # Full inverse basis expansion, independent of native forward conversion.
        lv=sp.Matrix(64,64,lambda k,i:0 if k<i else(-1)**(k-i)*comb(63,i)*comb(63-i,k-i))
        lb=sp.Matrix(10,10,lambda k,j:0 if k<j else(-1)**(k-j)*comb(9,j)*comb(9-j,k-j))
        controls=sp.Matrix(64,10,values);image=lv*controls*lb.T
        actual={(i,j):image[i,j]for i in range(64)for j in range(10)if image[i,j]}
        need(actual==expected,"ENTIRE640 inverse Bernstein image")
        endpoints=[sum(1 for i in range(64) if controls[i,j]>0)for j in [0,9]]
        need(all(endpoints),"every closed endpoint strict")
        exact_same(endpoints,field["endpoint_positive"])
        exact_same(sum(1 for c in values if c>0),field["positive"])
        exact_same(sum(1 for c in values if c==0),field["zero"])
        return {"slots":640,"whole_inverse_basis_matches":True,
                "endpoint_positive":endpoints,"positive":field["positive"],"zero":field["zero"]}
    inverse=[inverse_check(de,positive["denominator"])]
    for leaf in positive["closed_gap_cover"]:
        c,d=map(sp.Rational,leaf["b_interval"])
        inverse.append(inverse_check(affine(gap,c,d),leaf))
    exact_same(positive["whole_Bernstein_slots"],3200)
    return {"actual_agent":"six-sendov-2","role":"researcher","sympy_version":sp.__version__,
        "complete_negative412_and_positive3200":True,
        "whole_negative_sector_sha256":sha256(canonical(neg)).hexdigest(),
        "whole_positive_sector_sha256":sha256(canonical(positive)).hexdigest(),
        "entire_inverse_basis_records":inverse,"whole_Bernstein_slots":3200,
        "closed_endpoint_strictness_paid":True,"same_author_not_independent_review":True}

def main():
    p=ArgumentParser();p.add_argument("--input",type=Path,default=BASE/"INPUT.json")
    p.add_argument("--record",type=Path,required=True);p.add_argument("--receipt",type=Path)
    a=p.parse_args();result=run(a.input,a.record)
    if a.receipt:a.receipt.write_bytes(canonical(result))
    print(json.dumps(result))
if __name__=="__main__":main()
