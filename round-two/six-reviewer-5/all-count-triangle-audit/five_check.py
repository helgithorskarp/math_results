"""Portable whole-coefficient verification, separate from the CAS producer.

No SymPy import, evaluation encoding, floating arithmetic or author certificate.
All identities are checked by exact expanded rational coefficient comparison.
"""
import argparse,hashlib,json,pathlib
from fractions import Fraction as R

def need(ok,msg):
    if not ok:raise ValueError(msg)
def const(x):return {(0,0,0):R(x)} if x else {}
def add(a,b):
    out=a.copy()
    for m,c in b.items():out[m]=out.get(m,0)+c
    return {m:c for m,c in out.items() if c}
def neg(a):return {m:-c for m,c in a.items()}
def mul(a,b):
    out={}
    for i,c in a.items():
        for j,d in b.items():
            m=tuple(x+y for x,y in zip(i,j));out[m]=out.get(m,0)+c*d
    return {m:c for m,c in out.items() if c}
def read_poly(v):
    need(isinstance(v,list) and len(v)<=1800,'bounded whole polynomial input')
    out={}
    for m,c in v:
        need(len(m)==3 and all(type(i) is int and 0<=i<=30 for i in m),'entire monomial domain')
        need(tuple(m) not in out,'no duplicate coefficient');cc=R(c);need(cc!=0,'no zero coefficient');out[tuple(m)]=cc
    return out
class RF:
    def __init__(self,n=0,d=1):self.n=n if isinstance(n,dict) else const(n);self.d=d if isinstance(d,dict) else const(d)
    def __add__(self,b):
        b=lift(b)
        if not self.n:return b
        if not b.n:return self
        if self.d==b.d:return RF(add(self.n,b.n),self.d)
        return RF(add(mul(self.n,b.d),mul(b.n,self.d)),mul(self.d,b.d))
    __radd__=__add__
    def __neg__(self):return RF(neg(self.n),self.d)
    def __sub__(self,b):return self+-lift(b)
    def __rsub__(self,b):return lift(b)+-self
    def __mul__(self,b):
        b=lift(b)
        if not self.n or not b.n:return RF()
        return RF(mul(self.n,b.n),mul(self.d,b.d))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=lift(b);need(bool(b.n),'nonzero whole rational divisor')
        return RF(mul(self.n,b.d),mul(self.d,b.n))
    def __rtruediv__(self,b):return lift(b)/self
    def __pow__(self,k):
        need(type(k) is int and k>=0,'nonnegative polynomial power');out=RF(1)
        for _ in range(k):out=out*self
        return out
    def __eq__(self,b):
        b=lift(b);return mul(self.n,b.d)==mul(b.n,self.d)
def lift(x):return x if isinstance(x,RF) else RF(x)
def read(v):
    need(set(v)=={'n','d'},'entire rational encoding');out=RF(read_poly(v['n']),read_poly(v['d']));need(bool(out.d),'nonzero denominator');return out
def physical():
    u=RF({(1,0,0):R(1)});v=RF({(0,1,0):R(1)});w=RF({(0,0,1):R(1)})
    h=3+u+v;l=2+v;q=3*h+w;s=q+3*h;d=h-l;ell=3*(h+l)+1;N=2*q+6*(h+l);D=3*h
    G=[4*(q-1),4*D,2*D*(q-2),2*q*D,s*d/(3*h*l)]
    S=[[RF() for _ in G] for _ in G]
    S[0][0]=4*(q*q-1);S[0][1]=S[1][0]=-4*D*(q-1);S[1][1]=4*D*D
    S[2][2]=4*D*D*(q-2);S[3][3]=4*D*D*q
    for x,c in (([RF(),-2,q-2,q,RF()],3*h),([RF(),-2,q-2,-q,G[4]],3*l),([-2*(q-1),6*l,-3*(q-2)*(h+l),-3*q*d,-s*d/h],1/ell)):
        for i in range(5):
            for j in range(5):S[i][j]+=c*lift(x[i])*lift(x[j])
    return [[(N-1 if i==j else 0)-S[i][j]/G[i] for j in range(5)] for i in range(5)]
def check(path):
    raw=pathlib.Path(path).read_bytes();need(len(raw)<=100000,'compact complete input');r=json.loads(raw)
    need(r['domain']=='QQ(u,v,w); order lex; l=2+v,h=3+u+v,q=3h+w','exact high-q parameter domain')
    need(len(r['entries'])==5 and len(r['pivots'])==5 and len(r['stages'])==5,'complete five-block coverage')
    A=[[read(x) for x in row] for row in r['entries']];need(all(len(row)==5 for row in A),'complete original rows')
    expected=physical();identities=0;terms=0
    for i in range(5):
        for j in range(5):need(A[i][j]==expected[i][j],'entire physical cap entry');identities+=1
    print('bound all 25 original entries by complete coefficients',flush=True)
    for i in range(5):
        pivot=read(r['pivots'][i]);need(pivot==A[i][i],'entire pivot-stage link')
        for poly in (pivot.n,pivot.d):need(poly.get((0,0,0),0)>0 and all(c>=0 for c in poly.values()),'all shifted pivot coefficients positive')
        terms+=len(pivot.n)
        st=r['stages'][i];need(len(st['column'])==len(st['row'])==4-i,'entire stage interfaces')
        for j in range(i+1,5):
            need(read(st['column'][j-i-1])==A[j][i],'whole stage column')
            need(read(st['row'][j-i-1])==A[i][j],'whole stage row')
        need([(v['j'],v['k']) for v in st['updates']]==[(j,k) for j in range(i+1,5) for k in range(i+1,5)],'all ordered Schur updates')
        new={}
        for item in st['updates']:
            j,k=item['j'],item['k'];z=read(item['value']);need(z==A[j][k]-A[j][i]*A[i][k]/pivot,'whole coefficient Schur identity');new[j,k]=z;identities+=1
        for (j,k),z in new.items():A[j][k]=z
        print('complete coefficient pivot '+str(i+1),flush=True)
    return dict(complete=True,domain=r['domain'],original_entry_identities=25,ordered_local_identities=identities-25,
                pivots=5,positive_pivot_numerator_terms=terms,certificate_bytes=len(raw),certificate_sha256=hashlib.sha256(raw).hexdigest(),
                method='entire expanded rational coefficients; no CAS, integer encoding or sample evaluation')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--input',required=True);a.add_argument('--out',required=True);arg=a.parse_args()
    r=check(arg.input);data=(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n').encode();pathlib.Path(arg.out).write_bytes(data);print(data.decode().strip())
