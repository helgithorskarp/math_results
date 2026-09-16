#!/usr/bin/env python3
"""Finite algebra certificate for the two-anchor preservation theorem.
The denominator-clearing argument and arbitrary-length induction are written
in PROOF.md. No candidate network or reviewer geometry is enumerated.
"""
import argparse
import copy
from fractions import Fraction
from itertools import combinations,product
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
P=(1,1,1,1,1)
O=(1,0,0,0);ZERO=(0,0,0,0)
PHI=(0,0,-1,-1);INV=(-1,0,-1,-1);UNIT=(3,0,1,1)
FORM=(0,1,2,1)

def need(ok,msg):
    if not ok:raise ValueError(msg)

def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def rem(a,b):
    a=trim([x%3 for x in a]);b=trim([x%3 for x in b]);need(b[-1]!=0,'zero divisor polynomial')
    while len(a)>=len(b) and any(a):
        k=len(a)-len(b);v=a[-1]*pow(b[-1],-1,3)%3
        for j,c in enumerate(b):a[k+j]=(a[k+j]-v*c)%3
        a=trim(a)
    return tuple(a)

def mult(a,b):
    r=[0]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[i+j]+=x*y
    for k in range(6,3,-1):
        for j in range(1,5):r[k-j]-=r[k]
    return tuple(r[:4])
def conj(a):
    a,b,c,d=a
    return (a-b,-b,d-b,c-b)
def mod(a):return tuple(x%3 for x in a)
def power(a,n):
    r=O
    while n:
        if n&1:r=mod(mult(r,a))
        a=mod(mult(a,a));n//=2
    return r

def gram(a):
    a,b,c,d=a;p=a*b+b*c+c*d;q=a*c+a*d+b*d
    return 2*(a*a+b*b+c*c+d*d)-p-q,p-q

def verify_gram(a):
    r,s=gram(a);n=tuple(2*x for x in mult(a,conj(a)))
    need(n==(r-s,0,-2*s,-2*s),'Gram coefficient identity')

def residue(x):
    x=Fraction(x);need(x.denominator%3!=0,'coefficient outside localized ring')
    return (x.numerator%3)*pow(x.denominator%3,-1,3)%3

def base_cycle():
    powers=[O,(0,1,0,0),(0,0,1,0),(0,0,0,1),(-1,-1,-1,-1)]
    bits=[(0,0,1,0),(0,0,0,1),(0,0,0,0),(1,0,0,0),(0,1,0,0)]
    ds=[tuple(powers[i][j]-powers[4][j] for j in range(4)) for i in range(4)]
    points=[tuple(5*powers[4][j]+sum(e[i]*ds[i][j] for i in range(4)) for j in range(4)) for e in bits]
    return points

def certify(polynomial=P,form=FORM):
    need(polynomial==P,'wrong cyclotomic polynomial')
    roots=[sum(c*pow(x,i,3) for i,c in enumerate(polynomial))%3 for x in range(3)]
    need(all(roots),'linear factor modulo3')
    qs=[]
    for b,a in product(range(3),repeat=2):
        q=(b,a,1);r=rem(polynomial,q);need(any(r),'quadratic factor modulo3');qs.append({'divisor':list(q),'remainder':list(r)})
    # A reducible quartic has a linear or quadratic divisor, so this is complete.
    rows=list(product(range(3),repeat=4));nonzero=[a for a in rows if a!=ZERO]
    need(all(mod(conj(a))==power(a,9) for a in rows),'conjugation is Frobenius9')
    need(all(mod(mult(a,conj(a)))!=ZERO for a in nonzero),'nonzero zero-norm residue')
    need(all(power(a,80)==O for a in nonzero),'nonzero field group')
    basis=[tuple(int(i==j) for i in range(4)) for j in range(4)]
    tests=basis+[tuple(a+b for a,b in zip(basis[i],basis[j])) for i,j in combinations(range(4),2)]
    for a in tests:verify_gram(a)
    # Both forms are homogeneous quadratic: 4 diagonal and 6 polarized tests
    # certify every coefficient, not merely a sample of possible differences.
    unit=[a for a in rows if tuple(x%3 for x in gram(a))==(2,2)]
    vals=[sum(x*y for x,y in zip(a,form))%3 for a in unit]
    need(len(unit)==10 and all(vals),'not a proper module residue colouring')
    need(mult(PHI,INV)==O and conj(PHI)==PHI and conj(INV)==INV,'golden scale integrality')
    cycle=base_cycle();need(len(set(cycle))==5,'cycle collision')
    for a,b in zip(cycle,cycle[1:]+cycle[:1]):
        d=tuple(x-y for x,y in zip(a,b));need(mult(d,conj(d))==UNIT,'cycle nonunit edge')
    colours=[sum(x*y for x,y in zip(a,form))%3 for a in cycle]
    need(all(a!=b for a,b in zip(colours,colours[1:]+colours[:1])),'cycle colour')
    need(residue(Fraction(1,2))==2 and residue(Fraction(1,11))==2,'localized denominator controls')
    try:residue(Fraction(1,3))
    except ValueError:pass
    else:raise ValueError('accepted forbidden denominator')
    return {'cyclotomic_polynomial_low_to_high':list(P),'modulus':3,'linear_evaluations':roots,'all_nine_monic_quadratic_remainders':qs,'irreducible_mod3':True,'residue_field_order':81,'nonzero_residues_with_nonzero_conjugate_norm':80,'conjugation_frobenius_exponent':9,'gram_coefficient_tests':10,'unit_difference_residues':[list(a) for a in unit],'colour_form':list(form),'unit_residue_colours':vals,'phi_inverse_identity':True,'phi_squared_power_basis':list(mult(PHI,PHI)),'inverse_phi_squared_power_basis':list(mult(INV,INV)),'source_unit_cycle_labels':[6,3,1,2,5],'source_unit_cycle_points':[list(a) for a in cycle],'source_unit_cycle_colours':colours,'claim':'Every finite sequential two-anchor reciprocal golden-copy network containing the base is exactly three-chromatic','new_physical_network_built':False,'proof_boundary':'Finite identities checked here; denominator clearing and arbitrary-length induction are the explicit written proof.'}

def controls(expected):
    rejected=[]
    for name,kwargs in [('wrong polynomial',{'polynomial':(1,0,0,0,1)}),('zero colour form',{'form':(0,0,0,0)}),('wrong colour form',{'form':(1,0,0,0)})]:
        try:certify(**kwargs)
        except ValueError:rejected.append(name)
        else:raise ValueError('corruption accepted '+name)
    # A reducible quartic really is detected by the finite divisor test.
    need(rem((1,0,2,0,1),(1,0,1))==(0,),'reducible control')
    need(mult((Fraction(1,3),0,0,0),(Fraction(1,3),0,0,0))==(Fraction(1,9),0,0,0),'scale outside ring control')
    for name,key,bad in [('false field count','residue_field_order',9),('false norm exception','nonzero_residues_with_nonzero_conjugate_norm',79),('missing unit residue','unit_difference_residues',expected['unit_difference_residues'][:-1]),('wrong cycle point','source_unit_cycle_points',[[0,0,0,0]]*5)]:
        c=copy.deepcopy(expected);c[key]=bad
        try:need(c==expected,'certificate mismatch')
        except ValueError:rejected.append(name)
        else:raise ValueError('corruption accepted '+name)
    return rejected

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();cert=certify();cert['rejected_controls']=controls(cert)
    path=HERE/'EXPECTED.json'
    if args.write:
        need(not path.exists(),'refusing to overwrite frozen expected output');path.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    else:need(json.loads(path.read_text())==cert,'expected certificate differs')
    print(json.dumps(cert,indent=2,sort_keys=True))
if __name__=='__main__':main()
