#!/usr/bin/env python3
"""Independent exact all-pairs checker and full reduced-polynomial case audit."""
import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def trim(v):
    v = list(v)
    while v and v[-1] == 0:
        v.pop()
    return tuple(v)


def remainder(a, b):
    require(b and b[-1] == 1, 'monic divisor required')
    a = list(trim(a))
    while len(a) >= len(b):
        t = a[-1]
        shift = len(a)-len(b)
        for j, value in enumerate(b):
            a[shift+j] = (a[shift+j]-t*value)%3
        a = list(trim(a))
    return tuple(a)


def quotient(a, b):
    a = list(a)
    out = [0]*max(0,len(a)-len(b)+1)
    while len(a) >= len(b):
        t = a[-1]; shift = len(a)-len(b)
        out[shift] = t
        for j, value in enumerate(b):
            a[shift+j] = (a[shift+j]-t*value)%3
        a = list(trim(a))
    require(not a, 'nonexact factor division')
    return trim(out)


def monics(d):
    return [v+(1,) for v in product(range(3),repeat=d)]


def irreducibles():
    out = []
    for d in range(1,5):
        for f in monics(d):
            if not any(not remainder(f,g) for g in out if len(g)-1 <= d//2):
                out.append(f)
    return out


class Quotient:
    """Multiplication by repeated application of the companion linear map."""
    def __init__(self, modulus):
        self.mod = tuple(modulus)
        self.d = len(modulus)-1
        self.q = 3**self.d
        self.vectors = [tuple(a//3**i%3 for i in range(self.d)) for a in range(self.q)]
        require(self.mod in irreducibles(), 'reducible field modulus')

    def encode(self, v):
        return sum((x%3)*3**i for i,x in enumerate(v))

    def minus(self, a, b):
        return self.encode([x-y for x,y in zip(self.vectors[a],self.vectors[b])])

    def times(self, a, b):
        v = self.vectors[a]
        out = [0]*self.d
        for digit in self.vectors[b]:
            out = [(x+digit*y)%3 for x,y in zip(out,v)]
            top = v[-1]
            v = tuple(((v[i-1] if i else 0)-top*self.mod[i])%3 for i in range(self.d))
        return self.encode(out)

    def power(self, a, n):
        out = 1
        for _ in range(n):
            out = self.times(out,a)
        return out


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def cases():
    irr = irreducibles()
    require(dict(Counter(len(f)-1 for f in irr)) == {1:3,2:3,3:8,4:18}, 'irreducible census')
    factors = []
    types = set()
    for d in range(1,5):
        for p in monics(d):
            left = p; fac = []
            for f in irr:
                while len(left) >= len(f) and not remainder(left,f):
                    fac.append(f);left=quotient(left,f)
            require(left == (1,), 'incomplete polynomial factorization')
            factors.append([p,fac])
            distinct = sorted(set(fac))
            for f in distinct:
                r = len(f)-1
                for g in distinct:
                    s = len(g)-1
                    if f == g:
                        for k in range(r):
                            types.add(('same',r,k,gcd(3**r-1,3**k+1)))
                    else:
                        require(r+s<=4, 'distinct degree budget')
                        types.add(('different',r,s,3**gcd(r,s)-1))
    expected = {('same',d,k,gcd(3**d-1,3**k+1)) for d in range(1,5) for k in range(d)}
    expected |= {('different',r,s,3**gcd(r,s)-1) for r in range(1,4) for s in range(1,4) if r+s<=4}
    require(types == expected and len(types)==16, 'residue graph classification')
    for kind,r,s,size in types:
        require(size in (2,4,10) if kind=='same' else size in (2,8), 'unclassified connection')
        if kind=='same' and size==10:
            require((r,s)==(4,2), 'wrong norm81 case')
        if kind=='different' and size==8:
            require((r,s)==(2,2), 'wrong hyperbola81 case')
    return {'monic_polynomials':len(factors), 'irreducible_polynomials':len(irr),
            'case_types':[list(t) for t in sorted(types)], 'factorization_sha256':digest(factors)}


def verify(certificate):
    require(certificate.get('schema')==1, 'certificate schema')
    rows = certificate.get('graphs')
    require(isinstance(rows,dict) and set(rows)=={'norm81','hyperbola81'}, 'missing graph')
    result = {'verified':True,'record_improvement':False,'collision_branch_chromatic_number':3,
              'case_audit':cases(), 'graphs':{}}
    for name, mod, expected_e in [('norm81',[2,1,0,0,1],405),('hyperbola81',[1,0,1],324)]:
        row=rows[name]
        require(row['modulus_low_first']==mod, 'wrong presentation')
        F=Quotient(mod)
        require(all(F.power(a,F.q-1)==1 for a in range(1,F.q)), 'field identity')
        w=row['weights']; word=row['colour_word']
        require(len(w)==4 and all(type(x) is int and x in range(3) for x in w), 'invalid weights')
        require(type(word) is str and len(word)==81 and set(word)<=set('012'), 'invalid word')
        if name=='norm81':
            coords=F.vectors
            adjacent=lambda u,v: F.power(F.minus(u,v),10)==1
            S=[a for a in range(F.q) if F.power(a,10)==1]
        else:
            coords=[F.vectors[v%9]+F.vectors[v//9] for v in range(81)]
            adjacent=lambda u,v: F.times(F.minus(u%9,v%9),F.minus(u//9,v//9))==1
            S=[[a,b] for a in range(9) for b in range(9) if F.times(a,b)==1]
        require(row['connection']==S, 'connection set mismatch')
        require(word==''.join(str(sum(a*b for a,b in zip(w,v))%3) for v in coords), 'word formula')
        E=[]
        for u in range(81):
            require(not adjacent(u,u), 'loop')
            for v in range(u+1,81):
                if adjacent(u,v):
                    require(word[u]!=word[v], 'monochromatic exact edge')
                    E.append([u,v])
        require(len(E)==expected_e==row['edges'] and row['vertices']==81, 'graph count')
        require(digest(E)==row['edge_sha256'], 'edge digest')
        require(all(sum(u==a or u==b for a,b in E)==2*expected_e//81 for u in range(81)), 'regularity')
        result['graphs'][name]={'vertices':81,'edges':len(E),'pair_tests':3240,
                               'colours':len(set(word)), 'edge_sha256':digest(E)}
    # The size-four connection case in F9 is exactly +/-1,+/-i.
    F=Quotient([1,0,1])
    S=[a for a in range(1,9) if F.power(a,4)==1]
    require(S==[1,2,3,6], 'size-four case')
    require(all(sum(F.vectors[a])%3 for a in S), 'grid three-colouring')
    result['small_case_connection_checks']=len(S)
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--certificate',type=Path,default=ROOT/'certificate.json')
    ap.add_argument('--check-expected',action='store_true')
    args=ap.parse_args()
    result=verify(json.loads(args.certificate.read_text()))
    if args.check_expected:
        require(result==json.loads((ROOT/'EXPECTED.json').read_text()), 'expected mismatch')
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
