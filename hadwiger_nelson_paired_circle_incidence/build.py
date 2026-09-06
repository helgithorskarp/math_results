"""Generate the finite signed-incidence polynomial certificate, exactly."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import comb
import argparse, hashlib, json, time

# Sparse polynomials in X,Y,S modulo S^2=3, with rational coefficients.
def clean(p): return {m:F(c) for m,c in p.items() if c}
def add(*pp):
    z={}
    for p in pp:
        for m,c in p.items(): z[m]=z.get(m,F(0))+c
    return clean(z)
def scale(p,c): return clean({m:v*c for m,v in p.items()})
def mul(p,q):
    z={}
    for (a,b,s),u in p.items():
        for (c,d,t),v in q.items():
            m=(a+c,b+d,(s+t)%2)
            z[m]=z.get(m,F(0))+u*v*(3 if s+t==2 else 1)
    return clean(z)
def const(c): return clean({(0,0,0):F(c)})
def sq(p): return mul(p,p)
X={(1,0,0):F(1)};Y={(0,1,0):F(1)};S={(0,0,1):F(1)}
COS=[const(1),const(F(1,2)),const(F(-1,2)),const(-1),const(F(-1,2)),const(F(1,2))]
SIN=[{},scale(S,F(1,2)),scale(S,F(1,2)),{},scale(S,F(-1,2)),scale(S,F(-1,2))]
SLOTS=list(product(range(2),repeat=2))
def displacement(slot):
    i,j=slot
    return add(X,const(F(3*j,5)-i)), add(Y,const(F(4*j,5)))
def norm(z): return add(sq(z[0]),sq(z[1]))
def incidence(a,b,k):
    d=displacement(a);e=displacement(b)
    # Rotate e by -k*pi/3; the two dot constraints now share direction u.
    v=(add(mul(COS[k],e[0]),mul(SIN[k],e[1])),
       add(scale(mul(SIN[k],e[0]),-1),mul(COS[k],e[1])))
    q=norm(d);w=norm(e);h=add(mul(d[0],v[0]),mul(d[1],v[1]))
    return add(mul(mul(q,w),add(q,w,scale(h,-2),const(-4))),scale(sq(h),4))
def terms(p): return [[a,b,s,c.numerator,c.denominator] for (a,b,s),c in sorted(p.items())]
def evaluate(p,x,y):
    v=[F(0),F(0)]
    for (a,b,s),c in p.items(): v[s]+=c*x**a*y**b
    return [[z.numerator,z.denominator] for z in v]
def raw(x): return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def make():
    entries=[]
    for a in SLOTS:
        p=add(norm(displacement(a)),const(-3))
        entries.append({'id':'self_%s%s'%a,'kind':'self','a':list(a),'degree':2,'terms':terms(p)})
    for n,a in enumerate(SLOTS):
        for b in SLOTS[n+1:]:
            for k in range(6):
                if (sum(a)+sum(b)+k)%2!=1: continue
                p=incidence(a,b,k)
                entries.append({'id':'pair_%s%s_%s%s_%s'%(*a,*b,k),'kind':'pair','a':list(a),'b':list(b),'k':k,'degree':max(i+j for i,j,s in p),'terms':terms(p)})
    witness=(F(1,5),F(2,5))
    for e in entries:
        p={(a,b,s):F(n,d) for a,b,s,n,d in e['terms']}
        e['witness_value']=evaluate(p,*witness)
    return {'schema':1,'orientation':[[3,5],[4,5]],'coefficient_field':'Q(S), S^2=3, S positive',
            'term_encoding':'[X exponent,Y exponent,S exponent,rational numerator,positive denominator]',
            'witness_translation':[[1,5],[2,5]],'factors':entries,
            'midpoint_control':{'translation':[[1,5],[-2,5]],'a':[0,0],'b':[1,1],'k':3,'point_encoding':'Each axis [rational numerator,sqrt19 numerator,denominator]','x':[[1,2,10],[-2,1,10]],'y':[[9,-2,10],[2,-1,10]],'scope':'Conflicting one-sided orbit prescriptions only; full-support colourability untested.'},
            'factor_count':22,'product_degree':108,'product_leading_scalar':16*3**8,
            'product_leading_form':'104976*(X^2+Y^2)^54','target_found':False}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--discover',action='store_true');args=ap.parse_args()
    started=time.monotonic();out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    data=make();blob=raw(data)
    if not args.discover and blob!=(Path(__file__).parent/'certificate.json').read_bytes(): raise ValueError('certificate bytes differ')
    out.joinpath('certificate.json').write_bytes(blob)
    r={'status':'PASS','factor_count':len(data['factors']),'coefficient_terms':sum(len(e['terms']) for e in data['factors']),
       'certificate_bytes':len(blob),'certificate_sha256':hashlib.sha256(blob).hexdigest(),'seconds':time.monotonic()-started}
    out.joinpath('build.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
