"""Exact first unsigned beta test on all surviving asymmetric flap selectors.

Uses integer fixed-point enclosures of rational-exponential kernels.
No floating-point value participates in any certified comparison.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from math import comb
from pathlib import Path
import json, sys, time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOUNDS_SHA = '60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7'
path=ROOT/'gaussian_majorisation_hankel_transport/bounds.py'
if sha256(path.read_bytes()).hexdigest()!=BOUNDS_SHA:
    raise RuntimeError('bounds dependency changed')
spec=spec_from_file_location('first_unsigned_bounds',path)
bounds=module_from_spec(spec)
sys.modules[spec.name]=bounds
spec.loader.exec_module(bounds)
I,exp_negative,sqrt_integer=bounds.I,bounds.exp_negative,bounds.sqrt_integer
N,M,DIGITS=7,9,24
ETA=F(1,100)
MARGINS={7:F(1,1000),8:F(1,100),9:F(1,30)}
EDGES=tuple(combinations(range(4),2))
V=((0,0,1),(2,0,-1),(-1,3,-1),(-1,-1,-1))
DENOM=9
# The homogenization coefficient simplifies exactly to (-1)^m/9.
FACTORS={m:(-1)**m for m in range(2,10)}

def require(test,msg):
    if not test:raise RuntimeError(msg)

def geometry():
    x,y,labels=list(V),list(V),['anchor_'+str(i) for i in range(4)]
    arcs=[]
    for i,j in EDGES:
        for a,b in ((i,j),(j,i)):
            arcs.append((a,b))
            x.append(tuple(V[b][k]-V[a][k] for k in range(3)))
            y.append(tuple(V[b][k]+V[a][k] for k in range(3)))
            labels.append(f'flap_{a}_{b}')
    return tuple(x),tuple(y),tuple(labels),tuple(arcs)

def selectors():
    for mask in range(64):
        arcs=tuple((i,j) if mask>>e&1 else (j,i) for e,(i,j) in enumerate(EDGES))
        if any(all(i!=k for i,j in arcs) for k in range(4)):
            continue
        labels=tuple(range(4))+tuple(4+2*e+(0 if mask>>e&1 else 1) for e in range(6))
        yield mask,labels

def residual_tuples(labels):
    for a in combinations(labels,7):
        for b in combinations(a,2):yield tuple(sorted(a+b))
    for a in combinations(labels,8):
        for b in a:yield tuple(sorted(a+(b,)))
    yield from combinations(labels,9)

def distance_matrix(points):
    return tuple(tuple(sum((a-b)**2 for a,b in zip(u,v)) for v in points) for u in points)

class Cell:
    def __init__(self,eta=ETA,digits=DIGITS):
        self.x,self.y,self.labels,self.arcs=geometry()
        self.dx,self.dy=map(distance_matrix,(self.x,self.y))
        self.eta,self.digits=F(eta),digits
        require(self.eta>=0,'negative squared-distance radius')
        require(type(digits) is int and 10<=digits<=100,'invalid precision')
        require(all(self.dx[i][j]>=self.dy[i][j] for i,j in combinations(range(16),2)),
                'fixture is not a contraction')
        self.scale=10**digits
        self.kernel=lru_cache(None)(self._kernel)
        self.row=lru_cache(None)(self._row)
        self.coefficient=lru_cache(None)(self._coefficient)

    def _kernel(self,m,sy,sx,pairs):
        if pairs==0:return 0,0
        error=pairs*self.eta
        yl,yh=max(F(0),sy-error)/(2*m),(sy+error)/(2*m)
        xl,xh=max(F(0),sx-error)/(2*m),(sx+error)/(2*m)
        digits=self.digits+10
        raw=I(max(F(0),exp_negative(-yh,digits).lo-exp_negative(-xl,digits).hi),
              max(F(0),exp_negative(-yl,digits).hi-exp_negative(-xh,digits).lo))
        out=(raw/(m*sqrt_integer(m,digits))).rounded(self.digits)
        lo,hi=out.lo*self.scale,out.hi*self.scale
        require(lo.denominator==hi.denominator==1,'fixed point failure')
        return lo.numerator,hi.numerator

    def _row(self,a):
        m=len(a)
        pairs=tuple(combinations(a,2))
        sx=sum(self.dx[i][j] for i,j in pairs)
        sy=sum(self.dy[i][j] for i,j in pairs)
        for points,total in ((self.x,sx),(self.y,sy)):
            centroid=m*sum(sum(z*z for z in points[i]) for i in a)-sum(
                sum(points[i][k] for i in a)**2 for k in range(3))
            require(total==centroid,'centroid exponent disagreement')
        return self.kernel(m,sy,sx,sum(i!=j for i,j in pairs))

    def _coefficient(self,a):
        require(len(a)==M,'wrong tuple size')
        lo=hi=0
        for m,factor in FACTORS.items():
            ls=hs=0
            for sub in combinations(a,m):
                l,h=self.row(sub)
                ls+=l;hs+=h
            lo+=factor*(ls if factor>=0 else hs)
            hi+=factor*(hs if factor>=0 else ls)
        require(lo<=hi,'reversed coefficient interval')
        return lo,hi

def run(progress=False):
    start=time.monotonic()
    cell=Cell()
    denominator=DENOM*cell.scale
    minima={d:None for d in (7,8,9)}
    argmin={}
    selector_records=[]
    stream=sha256()
    for mask,labels in selectors():
        local={d:None for d in (7,8,9)}
        counts={d:0 for d in (7,8,9)}
        for a in residual_tuples(labels):
            lo,hi=cell.coefficient(a)
            d=len(set(a));counts[d]+=1
            require(F(lo,denominator)>MARGINS[d],'not signed '+str((mask,a,d)))
            if minima[d] is None or lo<minima[d]:minima[d],argmin[d]=lo,(mask,a)
            if local[d] is None or lo<local[d]:local[d]=lo
            stream.update((json.dumps([mask,a,lo,hi],separators=(',',':'))+'\n').encode())
        require(counts=={7:2520,8:360,9:10},'incomplete residual enumeration')
        selector_records.append({'mask':mask,'counts':counts,
                                 'minimum_lower_bounds':{d:str(F(v,denominator)) for d,v in local.items()}})
        if progress:print(json.dumps({'mask':mask,'seconds':time.monotonic()-start,
                                     'kernels':cell.kernel.cache_info().misses}),file=sys.stderr,flush=True)
    require(len(selector_records)==32,'wrong selector count')
    return {'status':'FIRST_UNSIGNED_FLAP_BETA_CERTIFIED',
            'beta':{'N':N,'k':0,'moment_powers':list(range(2,10))},
            'variance_normalized_squared_distance_radius':str(ETA),
            'digits':DIGITS,'coefficient_denominator':denominator,
            'geometry':{'vertices':V,'labels':cell.labels,'source':cell.x,'target':cell.y},
            'margins':{d:str(v) for d,v in MARGINS.items()},
            'minimum_lower_bounds':{d:str(F(v,denominator)) for d,v in minima.items()},
            'first_minimizers':argmin,'selectors':selector_records,
            'signed_coefficient_occurrences':32*2890,
            'distinct_coefficients':cell.coefficient.cache_info().misses,
            'distinct_rows':cell.row.cache_info().misses,
            'distinct_scalar_enclosures':cell.kernel.cache_info().misses,
            'coefficient_stream_sha256':stream.hexdigest(),'bounds_sha256':BOUNDS_SHA}

if __name__=='__main__':
    from argparse import ArgumentParser
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--progress',action='store_true')
    args=parser.parse_args()
    require(not(args.check and args.write),'choose --check or --write')
    result=run(progress=args.progress)
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write:(HERE/'EXPECTED.json').write_text(text)
    elif args.check:
        require(text==(HERE/'EXPECTED.json').read_text(),'expected record mismatch')
        print(json.dumps({k:result[k] for k in ('status','signed_coefficient_occurrences',
                          'distinct_coefficients','coefficient_stream_sha256')},indent=2))
    else:print(text,end='')
