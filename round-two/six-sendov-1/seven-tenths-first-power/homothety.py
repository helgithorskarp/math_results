"""Same-author10322 controls adapted to the new marked interval.
No prior/reviewer runtime; new endpoint formulas are fully regenerated.
"""
#!/usr/bin/env python3
"""Local exact Gaussian controls for the ordinary homothety proof.

The original-root fixtures are explicitly disk rooted. The separately
prescribed critical-root fixtures are formal and carry no disk-root claim.
All coefficients and all eight critical slots are compared, not sampled.
"""
from fractions import Fraction as Q
from math import comb
from hashlib import sha256
from pathlib import Path
import argparse,json,resource,time

ZERO=(Q(0),Q(0));ONE=(Q(1),Q(0))
def need(ok,why):
    if not ok:raise ValueError(why)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def scale(x,c):return x[0]*c,x[1]*c
def mul(x,y):return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def norm2(x):return x[0]**2+x[1]**2
def inverse(x):
    need(norm2(x)>0,'finite nonzero reciprocal slot')
    return scale((x[0],-x[1]),1/norm2(x))
def power(x,n):
    z=ONE
    for _ in range(n):z=mul(z,x)
    return z
def pmul(a,b):
    z=[ZERO]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]=add(z[i+j],mul(x,y))
    return z
def peval(a,x):
    z=ZERO
    for c in reversed(a):z=add(mul(z,x),c)
    return z
def derivative(p):return [scale(c,Q(i)) for i,c in enumerate(p) if i]
def marked_order(p,a):
    degree=len(p)-1
    for order in range(degree+1):
        if peval(p,a)!=ZERO:return order
        p=derivative(p)
    raise ValueError('nonzero polynomial must have finite marked multiplicity')
def root_product(roots,c=ONE):
    p=[c]
    for z in roots:p=pmul(p,[scale(z,-1),ONE])
    return p
def compose(p,offset,slope):
    # Literal repeated polynomial factors, followed by separate binomial sums.
    terms=[ONE];out=[ZERO]*len(p)
    for c in p:
        for k,x in enumerate(terms):out[k]=add(out[k],mul(c,x))
        terms=pmul(terms,[offset,(slope,Q(0))])
    other=[]
    for k in range(len(p)):
        z=ZERO
        for j in range(k,len(p)):
            z=add(z,scale(mul(p[j],power(offset,j-k)),Q(comb(j,k))*slope**k))
        other.append(z)
    need(out==other,'ALL affine coefficients by convolution and binomial sums')
    return out
def transform_point(a,z,lam):return add(a,scale(add(z,scale(a,-1)),lam))
def transform_polynomial(p,a,lam,damage):
    need(0<lam<=1,'positive contraction domain')
    offset=scale(a,1-1/lam)
    if damage=='transform-centre-sign':offset=scale(offset,-1)
    degree=8 if damage=='transform-leading-power-eight' else 9
    result=[scale(x,lam**degree) for x in compose(p,offset,1/lam)]
    if damage=='last-polynomial-coefficient':result[-1]=ZERO
    need(len(p)==len(result)==10 and result[-1]==p[-1]!=ZERO,
         'entire degree-nine leading coefficient and normalization')
    need(peval(result,a)==ZERO,'marked original root retained')
    chain=[scale(x,lam**(9 if damage=='derivative-leading-power-nine' else 8))
           for x in compose(derivative(p),offset,1/lam)]
    need(derivative(result)==chain,'ALL NINE derivative chain coefficients')
    return result
def clean(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x

DAMAGES=('transform-leading-power-eight','transform-centre-sign',
 'derivative-leading-power-nine','last-polynomial-coefficient','omit-critical-slot',
 'reciprocal-orientation','mass-ratio-inversion','zero-contraction','disk-majorant')

def compute(damage=''):
    rows=[];coefficients=0;critical_slots=0;disk_slots=0
    endpoints=[(Q(11,16),Q(0)),(Q(69,100),Q(0)),(Q(7,10),Q(0)),(Q(3,5),Q(4,5))]
    leading=(Q(2,3),Q(1,5))
    # Includes a repeated marked original zero, repeated nonmarked zeros,
    # real and complex directions, boundary zeros, identity and strict maps.
    for a in endpoints:
        rho=a[0] if not a[1] else Q(1)
        need(norm2(a)==rho*rho and rho<=1,'exact marked norm')
        ordinary=[a,ONE,(-Q(1),Q(0)),(Q(0),Q(1)),(Q(0),-Q(1)),
                  (Q(3,5),Q(4,5)),(Q(3,5),-Q(4,5)),ZERO,ZERO]
        for repeated in (False,True):
            roots=ordinary.copy()
            if repeated:roots[1]=a
            p=root_product(roots,leading)
            need(all(norm2(z)<=1 for z in roots),'ALL nine actual disk originals')
            for lam in (Q(1),Q(3,4),Q(1,4)):
                if damage=='zero-contraction':lam=Q(0)
                changed=[transform_point(a,z,lam) for z in roots]
                direct=root_product(changed,leading)
                composite=transform_polynomial(p,a,lam,damage)
                need(composite==direct,'ALL TEN affine versus original-factor coefficients')
                bound=lam if damage=='disk-majorant' else (1-lam)*rho+lam
                need(all(norm2(z)<=bound*bound<=1 for z in changed),
                     'ALL nine exact closed-disk contraction bounds')
                multiplicity=sum(z==a for z in roots)
                need(marked_order(p,a)==marked_order(composite,a)==multiplicity,
                     'actual marked multiplicity and collision stratum retained')
                need(all((roots[i]==roots[j])==(changed[i]==changed[j])
                         for i in range(9) for j in range(9)),
                     'all original multiplicity equivalence pairs retained')
                rows.append(dict(kind='actual original-factor fixture',a=a,lambda_value=lam,
                    leading=leading,marked_multiplicity=multiplicity,
                    repeated_marked_input=repeated,originals=roots,contracted=changed,
                    all_polynomial_coefficients=composite,
                    all_derivative_coefficients=derivative(composite),disk_majorant=bound))
                coefficients+=19;disk_slots+=9
    units=[(Q(4,5),Q(3,5))]*4+[(Q(4,5),-Q(3,5))]*4
    for a in endpoints[:3]:
        for F in (Q(6),Q(15,2),Q(8)):
            radii=[F/8]*8;q=[scale(x,r) for x,r in zip(units,radii)]
            need(sum(radii,Q(0))==F and all(norm2(x)==r*r for x,r in zip(q,radii)),
                 'complete finite reciprocal-mass fixture')
            lam=8/F if damage=='mass-ratio-inversion' else F/8
            need(0<lam<=1,'finite positive mass threshold contraction')
            critical=[add(a,scale(inverse(x),-1)) for x in q]
            if damage=='omit-critical-slot':critical.pop()
            need(len(critical)==8,'ALL eight critical multiplicity slots')
            dp=[scale(x,9) for x in root_product(critical,leading)]
            p=[ZERO]+[scale(x,Q(1,j+1)) for j,x in enumerate(dp)]
            p[0]=scale(peval(p,a),-1)
            composite=transform_polynomial(p,a,lam,damage)
            changed=[transform_point(a,z,lam) for z in critical]
            need(all((critical[i]==critical[j])==(changed[i]==changed[j])
                     for i in range(8) for j in range(8)),
                 'all critical multiplicity equivalence pairs retained')
            direct=[scale(x,9) for x in root_product(changed,leading)]
            need(derivative(composite)==direct,'ALL nine literal critical-factor coefficients')
            recovered=[inverse(add(z,scale(a,-1)) if damage=='reciprocal-orientation'
                               else add(a,scale(z,-1))) for z in changed]
            expected=[scale(x,1/lam) for x in q]
            need(recovered==expected,'ALL eight affine reciprocal coordinates')
            new_radii=[r/lam for r in radii]
            need(sum(new_radii,Q(0))==8 and
                 all(norm2(x)==r*r for x,r in zip(recovered,new_radii)),
                 'EXACT all-eight mass-eight normalization')
            rows.append(dict(kind='formal critical-factor fixture; no original disk assertion',
                a=a,F=F,lambda_value=lam,critical=critical,contracted_critical=changed,
                original_reciprocals=q,contracted_reciprocals=recovered,
                contracted_radii=new_radii,all_polynomial_coefficients=composite,
                all_derivative_coefficients=direct))
            coefficients+=19;critical_slots+=8
    return clean(dict(agent='six-sendov-1',role='researcher',status='PASS',
        degree=9,fixtures=len(rows),whole_coefficient_entries=coefficients,
        actual_original_slots=disk_slots,formal_critical_slots=critical_slots,
        all_fixtures=rows,ordinary_trust='General affine and convexity proof is written separately; '
        'these finite exact structural controls do not replace it.'))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--damage',choices=DAMAGES,default='')
    p.add_argument('--record');args=p.parse_args();start=time.monotonic()
    try:
        result=compute(args.damage);raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode()
        if args.record:Path(args.record).write_bytes(raw)
        print(json.dumps(dict(status='PASS',fixtures=result['fixtures'],
              full_bytes=len(raw),full_sha256=sha256(raw).hexdigest(),seconds=time.monotonic()-start,
              peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),sort_keys=True))
    except ValueError as exc:
        import sys
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
