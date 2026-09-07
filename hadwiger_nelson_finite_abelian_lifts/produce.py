#!/usr/bin/env python3
"""Generate the complete q^2<=508 norm-one Cayley lift gate; stdlib only."""
import argparse
import itertools
import json
from pathlib import Path


def digits(x, p, n):
    return tuple((x // p**i) % p for i in range(n))


def rem(a, b, p):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    while len(a) >= len(b):
        c = a[-1] * pow(b[-1], -1, p) % p
        k = len(a) - len(b)
        for j, v in enumerate(b):
            a[k+j] = (a[k+j] - c*v) % p
        while a and a[-1] == 0:
            a.pop()
    return a


def irreducible(f, p):
    n = len(f)-1
    return all(rem(f, digits(i,p,d)+(1,), p)
               for d in range(1,n//2+1) for i in range(p**d))


class Field:
    def __init__(self, p, n):
        self.p, self.n, self.size = p, n, p**n
        self.f = next(digits(i,p,n)+(1,) for i in range(p**n)
                      if irreducible(digits(i,p,n)+(1,),p))
        self.vec = [digits(i,p,n) for i in range(self.size)]

    def enc(self, v):
        return sum((a % self.p)*self.p**i for i,a in enumerate(v))

    def add(self, a, b):
        return self.enc(x+y for x,y in zip(self.vec[a],self.vec[b]))

    def scale(self, c, a):
        return self.enc(c*x for x in self.vec[a])

    def mul(self, a, b):
        v = [0]*(2*self.n-1)
        for i,x in enumerate(self.vec[a]):
            for j,y in enumerate(self.vec[b]):
                v[i+j] += x*y
        return self.enc(rem([x%self.p for x in v], self.f, self.p))

    def power(self, a, n):
        r = 1
        while n:
            if n&1:
                r = self.mul(r,a)
            a = self.mul(a,a)
            n >>= 1
        return r


def prime_powers(limit=508):
    for q in range(2,limit+1):
        if q*q > limit:
            break
        for p in range(2,q+1):
            if any(p%d == 0 for d in range(2,p)):
                continue
            n, f = q, 0
            while n%p == 0:
                n//=p
                f+=1
            if n == 1:
                yield q,p,f
                break


def graph(q,p,f):
    F = Field(p,2*f)
    S = [x for x in range(1,F.size) if F.power(x,q+1)==1]
    edges = sorted({tuple(sorted((x,F.add(x,s))))
                    for x in range(F.size) for s in S})
    return F,S,edges


def relation(F, S):
    reps = [s for s in S if s <= F.scale(-1,s)]
    for s in reps:
        others = [t for t in reps if t != s]
        span = {0: [0]*len(others)}
        for j,t in enumerate(others):
            old = list(span.items())
            for x, coeff in old:
                for c in range(1,F.p):
                    y = F.add(x,F.scale(c,t))
                    if y not in span:
                        v = coeff.copy();v[j] = c;span[y] = v
            if s in span:
                return {'target':s,'terms':[[t,c] for t,c in zip(others,span[s]) if c]}
    return None


def main():
    ap = argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    rows = []
    for q,p,f in prime_powers():
        F,S,edges = graph(q,p,f)
        row = {'q':q,'p':p,'f':f,'modulus':list(F.f),'generators':S,
               'vertices':q*q,'edges':len(edges),'redundancy':relation(F,S)}
        rows.append(row)
    args.output.write_text(json.dumps({'version':1,'limit':508,'cases':rows},indent=2)+'\n')
    print(json.dumps({'cases':len(rows),'obstructed':sum(r['redundancy'] is not None for r in rows)}))


if __name__ == '__main__':
    main()
