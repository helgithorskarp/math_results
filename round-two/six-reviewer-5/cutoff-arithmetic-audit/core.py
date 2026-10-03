"""Exact Z[q,k] arithmetic; no producer source or CAS is imported.

The residual expressions are the reviewer's explicitly credited parent input.
All guards fail under -O too. Canonical sparse exponents are (q,k).
"""
import ast, hashlib, json, math
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent
def require(ok,why):
    if not ok: raise ValueError(why)
def tidy(p): return {e:c for e,c in p.items() if c}
def add(a,b,s=1):
    out=dict(a)
    for e,c in b.items():out[e]=out.get(e,0)+s*c
    return tidy(out)
def scale(p,s):return tidy({e:s*c for e,c in p.items()})
def mul(a,b):
    out={}
    for (i,j),c in a.items():
        for (ii,jj),cc in b.items():
            e=(i+ii,j+jj);out[e]=out.get(e,0)+c*cc
    return tidy(out)
def derivative(p):return {(i-1,j):i*c for (i,j),c in p.items() if i}
def parse(text):
    todo=[(ast.parse(text,mode='eval').body,False)];v={}
    while todo:
        node,ready=todo.pop()
        if not ready:
            if isinstance(node,ast.Constant) and type(node.value) is int:
                v[id(node)]={(0,0):node.value} if node.value else {};continue
            if isinstance(node,ast.Name) and node.id in ('q','k'):
                v[id(node)]={(1,0) if node.id=='q' else (0,1):1};continue
            if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):
                todo.extend([(node,True),(node.operand,False)]);continue
            if isinstance(node,ast.BinOp):
                todo.extend([(node,True),(node.right,False),(node.left,False)]);continue
            raise ValueError('nonliteral original polynomial')
        if isinstance(node,ast.UnaryOp):v[id(node)]=scale(v.pop(id(node.operand)),-1);continue
        a,b=v.pop(id(node.left)),v.pop(id(node.right))
        if isinstance(node.op,ast.Add):z=add(a,b)
        elif isinstance(node.op,ast.Sub):z=add(a,b,-1)
        elif isinstance(node.op,ast.Mult):z=mul(a,b)
        elif isinstance(node.op,ast.Div):
            require(set(b)=={(0,0)},'only rational constant division')
            z=scale(a,Fraction(1,b[(0,0)]))
        elif isinstance(node.op,ast.Pow):
            require(isinstance(node.right,ast.Constant) and type(node.right.value) is int and 0<=node.right.value<=126,'derived polynomial degree bound')
            n=node.right.value;require(len(a)<=1,'expanded monomial powers')
            if n==0:z={(0,0):1}
            elif not a:z={}
            else:
                (i,j),c=next(iter(a.items()));z={(i*n,j*n):c**n}
        else:raise ValueError('integer polynomial operators only')
        v[id(node)]=z
    require(len(v)==1,'whole AST consumed');return next(iter(v.values()))
def input_polys():
    raw=(HERE/'INPUT.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()=='c0d4d2f701d299570af5b002d5849ee2f9d727107f8eacbbcb860f68f43e6bd2','whole openly credited input seal')
    record=json.loads(raw);P=parse(record['R_numerator']);D=parse(record['R_denominator'])
    denominator=math.lcm(*(Fraction(c).denominator for c in list(P.values())+list(D.values())))
    P={e:int(c*denominator) for e,c in P.items()};D={e:int(c*denominator) for e,c in D.items()}
    content=math.gcd(*P.values(),*D.values());require(content>0,'positive reviewer residual content')
    P={e:c//content for e,c in P.items()};D={e:c//content for e,c in D.items()}
    require((len(P),len(D),max(sum(e) for e in P),max(sum(e) for e in D),max(e[0] for e in P))==(743,676,64,62,63),'whole input shape, not a substitute for identities')
    return P,D
def encode(p):return [[list(e),str(p[e])] for e in sorted(p,reverse=True)]
def decode(rows):
    out={}
    for ee,c in rows:
        e=tuple(ee);require(len(e)==2 and all(type(j) is int and j>=0 for j in e) and e not in out,'canonical distinct exponents')
        cc=int(c);require(str(cc)==c and cc!=0,'canonical nonzero integer coefficient');out[e]=cc
    return out
def digest(p):return hashlib.sha256(json.dumps(encode(p),separators=(',',':')).encode()).hexdigest()
def shift_first(p,h):
    out={};weights={}
    for (i,j),c in p.items():
        if i not in weights:weights[i]=[math.comb(i,r)*h**(i-r) for r in range(i+1)]
        for r,w in enumerate(weights[i]):out[(r,j)]=out.get((r,j),0)+c*w
    return tidy(out)
def affine(p,a,b,den=1):
    """den^deg_q times p(q=(a*k+b*u)/den,k), output (k,u)."""
    d=max(e[0] for e in p);out={};weights={}
    for (i,j),c in p.items():
        if i not in weights:weights[i]=[math.comb(i,r)*a**(i-r)*b**r*den**(d-i) for r in range(i+1)]
        for r,w in enumerate(weights[i]):out[(j+i-r,r)]=out.get((j+i-r,r),0)+c*w
    return tidy(out),d
def linear_product(coeff,a,b):
    out=[0]*(len(coeff)+1)
    for i,c in enumerate(coeff):out[i]+=a*c;out[i+1]+=b*c
    return out
def univariate_product(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,c in enumerate(a):
        for j,cc in enumerate(b):out[i+j]+=c*cc
    return out
def compact(p):
    """Direct binomial numerator/denominator expansion, before k shift."""
    d=max(e[0] for e in p);out={};weights={}
    for (i,j),c in p.items():
        if i not in weights:
            A=[math.comb(i,r)*6**(i-r)*11**r for r in range(i+1)]
            B=[math.comb(d-i,r)*2**(d-i) for r in range(d-i+1)]
            weights[i]=univariate_product(A,B)
        for r,w in enumerate(weights[i]):out[(i+j,r)]=out.get((i+j,r),0)+c*w
    return tidy(out),d
def quotient_horner(p,d):
    """Fresh two-channel Horner in Z[k,m]/(m^2-7k^2-d)."""
    grouped={}
    for (i,j),c in p.items():grouped.setdefault(i,{})[j]=c
    A={};H={}
    for i in range(max(grouped),-1,-1):
        def unadd(out,e,c):out[e]=out.get(e,0)+c
        aa={};hh={}
        for j,c in A.items():unadd(aa,j,-14*c);unadd(aa,j+1,3*c);unadd(hh,j,c)
        for j,c in H.items():unadd(aa,j,d*c);unadd(aa,j+2,7*c);unadd(hh,j,-14*c);unadd(hh,j+1,3*c)
        for j,c in grouped.get(i,{}).items():unadd(aa,j,c)
        A,H=tidy(aa),tidy(hh)
    return A,H
def ushift(p,h):return {e[0]:c for e,c in shift_first({(j,0):c for j,c in p.items()},h).items()}
def quad_sign(a,b):
    if a>=0 and b>=0:return 1 if a or b else 0
    if a<=0 and b<=0:return -1
    delta=a*a-7*b*b;require(delta!=0,'irrational norm')
    return (1 if delta>0 else -1) if a>0 else (1 if delta<0 else -1)
def ev(p,q,k):return sum(c*q**i*k**j for (i,j),c in p.items())
