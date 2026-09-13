"""Exact algebraic interface and Groebner producer decomposition over Q.

The decomposition adapts the degree-four package's shape-position method,
adding *each* exceptional rational vertical fiber. The independent verifier
uses a resultant and Euclidean gcds over quotient fields instead.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
import sympy as sp
from flint import fmpq, fmpq_poly

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT/'hadwiger_nelson_complex_radix_architecture'
sys.path.insert(0,str(ARCH))
import geometry
spec = importlib.util.spec_from_file_location('hn_c0_architecture',ARCH/'verify.py')
architecture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(architecture)
RESIDUAL_HASH = '42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def expression(sparse,x,y):
    return sum(c*x**i*y**j for i,j,c in sparse)


def primitive(p,v):
    p = sp.Poly(p,v,domain=sp.QQ)
    _, p = p.clear_denoms(convert=True)
    _, p = p.primitive()
    return sp.Poly(p if p.LC()>0 else -p,v,domain=sp.QQ)


def coefficients(p):
    return [str(p.nth(i)) for i in range(max(0,p.degree())+1)]


def encode(q,xx,yy,s):
    xx,yy = xx.rem(q),yy.rem(q)
    if q.degree()==1:
        # All rational points have the same auxiliary parameter s=0.
        q = sp.Poly(s,s,domain=sp.QQ)
    return {'q':coefficients(q),'x':coefficients(xx),'y':coefficients(yy)}


def select(residual_path, factors):
    pairs = json.loads((Path(__file__).parent/'pairs.json').read_text())
    if residual_path is not None:
        residual = json.loads(Path(residual_path).read_text())
        need(digest(residual)==RESIDUAL_HASH,'pinned h4195 residual')
        need(pairs==[row[:2] for row in residual['remaining_six'] if 0 in row[:2]],'entrywise residual class')
    need(len(pairs)==76 and len(set(map(tuple,pairs)))==76,'C0 star selection')
    need(all(type(a)==int and type(b)==int and a==0 and 0<b<len(factors) for a,b in pairs),'named pair indices')
    degrees = [architecture.degree(f) for f in factors]
    need(degrees[0]==6,'C0 degree')
    need(sum(degrees[b]==6 for a,b in pairs)==68 and sum(degrees[b]==8 for a,b in pairs)==8,'partner degrees')
    # Independently identify curve 0 by its named Eisenstein displacement.
    row = ((0,0),(-1,0),(1,-1),(-1,0),(0,0))
    need(geometry.distance_event(row)==factors[0],'named C0 event')
    return pairs


def groebner_components(f,g,x,y,s):
    basis = sp.groebner([f,g],y,x,order='lex',domain=sp.QQ)
    eliminants = [p.as_expr() for p in basis.polys if p.degree(y)==0]
    linear = [p.as_expr() for p in basis.polys if p.degree(y)==1]
    need(len(eliminants)==1 and len(linear)<=1,'Groebner shape')
    out = []
    for q0,_ in sp.factor_list(sp.Poly(eliminants[0],x))[1]:
        qx = primitive(q0,x)
        q = sp.Poly(qx.as_expr().subs(x,s),s,domain=sp.QQ)
        if linear:
            aa = sp.Poly(sp.diff(linear[0],y).subs(x,s),s,domain=sp.QQ).rem(q)
            bb = sp.Poly(linear[0].subs(y,0).subs(x,s),s,domain=sp.QQ).rem(q)
            if sp.gcd(aa,q).degree()==0:
                yy = (-bb*sp.invert(aa,q)).rem(q)
                out.append((q,sp.Poly(s,s,domain=sp.QQ),yy))
                continue
        need(qx.degree()==1,'unsupported nonrational exceptional fiber')
        x0 = -qx.nth(0)/qx.nth(1)
        h = sp.gcd(sp.Poly(f.subs(x,x0),y),sp.Poly(g.subs(x,x0),y))
        for h0,_ in sp.factor_list(h)[1]:
            out.append((primitive(h0.as_expr().subs(y,s),s),sp.Poly(x0,s,domain=sp.QQ),sp.Poly(s,s,domain=sp.QQ)))
    return out


def evaluator(component):
    conv = lambda values:fmpq_poly([fmpq(v) for v in values])
    q,xx,yy = [conv(component[k]) for k in ('q','x','y')]
    one,zero = fmpq_poly([1]),fmpq_poly([])
    xp,yp = [one],[one]
    for _ in range(8):
        xp.append(xp[-1]*xx%q)
        yp.append(yp[-1]*yy%q)
    monomials = {(i,j):xp[i]*yp[j]%q for i in range(9) for j in range(9-i)}
    return lambda sparse:sum((c*monomials[i,j] for i,j,c in sparse),zero)==zero
