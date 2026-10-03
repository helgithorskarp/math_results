"""Canonical QQ(h,q) execution of the unchanged sealed row reconstruction."""
import argparse, importlib.util, json, pathlib
from sympy.polys.fields import field
from sympy.polys.domains import QQ

K, h, q = field('h,q', QQ)

class Mat:
    def __init__(self,n,m=None,data=None):
        self.n=n; self.m=n if m is None else m
        self.a=data if data is not None else [[K.zero for _ in range(self.m)] for _ in range(n)]
    def __getitem__(self,ij):
        i,j=ij if isinstance(ij,tuple) else (ij,0)
        return self.a[i][j]
    def __setitem__(self,ij,x):
        i,j=ij if isinstance(ij,tuple) else (ij,0)
        self.a[i][j]=K(x)
    def __iter__(self):
        return iter(x for row in self.a for x in row)
    def __add__(self,b):
        if b==0:return self
        return Mat(self.n,self.m,[[x+b.a[i][j] for j,x in enumerate(row)] for i,row in enumerate(self.a)])
    __radd__=__add__
    def __neg__(self):return self*(-1)
    def __sub__(self,b):return self+(-b)
    def __mul__(self,b):
        if not isinstance(b,Mat):
            b=K(b);return Mat(self.n,self.m,[[x*b for x in row] for row in self.a])
        if self.m!=b.n:raise ValueError('matrix shape')
        out=Mat(self.n,b.m)
        for i in range(self.n):
            for k in range(self.m):
                if self.a[i][k]:
                    for j in range(b.m):
                        if b.a[k][j]:out.a[i][j]+=self.a[i][k]*b.a[k][j]
        return out
    __rmul__=__mul__
    def __truediv__(self,b):return self*(K.one/K(b))
    @property
    def T(self):return Mat(self.m,self.n,[list(row) for row in zip(*self.a)])
    def tolist(self):return self.a

class Exact:
    zeros=staticmethod(Mat)
    Integer=staticmethod(int)
    Rational=staticmethod(QQ)
    @staticmethod
    def diag(*a):
        out=Mat(len(a))
        for i,x in enumerate(a):out[i,i]=x
        return out

def encode(x):
    x=K(x)
    return {label:[[list(m),str(c)] for m,c in sorted(poly.terms(),reverse=True)]
            for label,poly in [('num',x.numer),('den',x.denom)]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--damage');args=ap.parse_args()
    p=pathlib.Path(__file__).with_name('independent.py')
    spec=importlib.util.spec_from_file_location('sealed',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.S=Exact;module.q=q;module.h=h;module.tidy=lambda x:x;module.enc=encode
    out=module.forms(args.damage)
    print(json.dumps(out,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
