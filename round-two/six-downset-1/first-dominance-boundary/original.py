"""NEW free-level original resolvent and FIRST-derivative controls.

six-downset-1/researcher; same-author exact validation, not review.
VERBATIM original geometry producer b7d and exact primitive helpers6b
are credited in PROVENANCE. No closed cap reader/count program or
EXPECTED/factor is called/imported. New levels theta3/2,5/2 replace
the parent's CLOSED original N-level and theta1,2 math controls.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
import argparse
import json
import resource
import signal
import time
from hashlib import sha256
from common import require,barrier,dot,matrix,vector,original_gram,full_positive_solve
from counts import scalars,level,shift,stringify
import geometry


class Jet:
    """Exact first derivative in an independent rational dual-number algebra."""
    def __init__(self,value,derivative=0): self.value=F(value); self.derivative=F(derivative)
    @staticmethod
    def convert(value): return value if isinstance(value,Jet) else Jet(value)
    def __add__(self,other):
        b=self.convert(other); return Jet(self.value+b.value,self.derivative+b.derivative)
    __radd__=__add__
    def __neg__(self): return Jet(-self.value,-self.derivative)
    def __sub__(self,other): return self+-self.convert(other)
    def __rsub__(self,other): return self.convert(other)+-self
    def __mul__(self,other):
        b=self.convert(other); return Jet(self.value*b.value,self.derivative*b.value+self.value*b.derivative)
    __rmul__=__mul__
    def __truediv__(self,other):
        b=self.convert(other); require(b.value!=0,'nonzero derivative-jet divisor')
        return Jet(self.value/b.value,(self.derivative*b.value-self.value*b.derivative)/b.value**2)
    def __rtruediv__(self,other): return self.convert(other)/self
    def __pow__(self,power):
        require(type(power) is int and 0<=power<=2,'bounded exact derivative powers')
        if power==0: return Jet(1)
        if power==1: return self
        return self*self


def endpoints(form,A,B,u,v,alpha,beta,mixed):
    square=beta/alpha; den=mixed*mixed-alpha*beta
    require(den<0 and alpha>0 and beta>0,'strict full original radical roots')
    records=[]
    for sign in (1,-1):
        delta=(mixed/den,-sign*alpha/den)
        def multiply(a,b):
            return (a[0]*b[0]+a[1]*b[1]*square,a[0]*b[1]+a[1]*b[0])
        ax=(dot(A,v),sign*dot(A,u)); bx=(dot(B,v),sign*dot(B,u))
        kernel=[(vi,sign*ui) for ui,vi in zip(u,v)]
        for i,row in enumerate(form):
            left=(dot(row,v),sign*dot(row,u))
            right=multiply(delta,(A[i]*bx[0]+B[i]*ax[0],A[i]*bx[1]+B[i]*ax[1]))
            require(left==right,'EVERY new original free-level endpoint kernel')
        dsquare=multiply(delta,delta)
        require((1-2*mixed*delta[0]+den*dsquare[0],-2*mixed*delta[1]+den*dsquare[1])==(0,0),
                'both coefficients of exact endpoint polynomial')
        require(sum((x[0] for x in kernel),F(0))==sum((x[1] for x in kernel),F(0))==0,
                'both entire original kernel coefficients centered')
        records.append(dict(sign=sign,radical_square=square,delta_coefficients=delta,
            full_original_centered_kernel=kernel,original_zero_pairs=len(form),polynomial_zero=True))
    return records


def check_labels(data,n,counts):
    N=geometry.preflight(n,counts)
    require(data['n']==n and data['counts']==list(counts) and data['N']==N
            and data['dimension']==N-3 and data['q']==2**(n-1),
            'original metadata matches guarded geometry')
    labels=list(range(2**n)); marked=[]; private=[]; facet=0
    for group,count in enumerate(counts):
        for _ in range(count):
            left=1<<(n+2*facet); right=1<<(n+2*facet+1)
            private.extend((left,right,left|right))
            marked.extend(((1<<group)|left,(1<<group)|right,(1<<group)|left|right))
            facet+=1
    labels+=marked+private
    require(data['family']==labels and len(set(labels))==N and labels[0]==0,
            'whole original downset label sequence and ACTUAL empty')


def read(n,counts,data=None):
    barrier(); geometry.preflight(n,counts)  # Literal N80 before ANY original arrays.
    if data is None: data=geometry.build(n,counts)
    check_labels(data,n,counts)
    N=data['N']; dimension=data['dimension']; oldsize=2**n-1
    require(N<=80 and dimension==N-3,'complete guarded original dimension')
    metric=matrix(data['metric'],dimension,dimension); rows=matrix(data['rows'],N,dimension)
    A=[F(-3)]+vector(data['a'],N-1); B=[F(-1)]+vector(data['b'],N-1)
    require(sum(A,F(0))==sum(B,F(0))==0,'both original repair directions centered')
    Q=original_gram(rows,metric)
    require(all(sum(row,F(0))==0 for row in Q),'ALL original constant equations')
    seed=scalars(2**(n-1),counts); blocks=[]; offset=oldsize
    for group,count in enumerate(counts):
        width=count-1 if group==0 else count
        if group: blocks.append(range(offset,offset+width))
        offset+=width
    basis=[[F(i==j) for i in range(dimension)] for j in range(oldsize)]
    basis += [[F(i in block) for i in range(dimension)] for block in blocks]
    metric_basis=[[dot(row,b) for row in metric] for b in basis]
    original_first_images=[[dot(row,b) for row in rows] for b in metric_basis]
    require(all(dot(A,b)==dot(B,b)==0 for b in original_first_images),
            'ENTIRE original FIRST annihilations BEFORE restricted claim')
    Gm=[[dot(a,b) for b in metric_basis] for a in basis]; width=len(basis)
    first_rows=[row[:oldsize]+[sum((row[i] for i in block),F(0))/len(block) for block in blocks]
                for row in rows]
    images=[[dot(row,b) for b in Gm] for row in first_rows]
    frame=[[sum((row[i]*row[j] for row in images),F(0)) for j in range(width)] for i in range(width)]
    ell=seed['ell']; K=[sum((row[j] for row in first_rows[1:oldsize+seed['m']+1]),F(0))
                        for j in range(width)]
    G=[F(i<oldsize) for i in range(width)]; W=[k-g for k,g in zip(K,G)]
    require(first_rows[0]==[-x/ell for x in K],'ACTUAL empty in full FIRST')
    gmG,gmW,gmK=[[dot(row,v) for row in Gm] for v in (G,W,K)]
    Afirst=[[frame[i][j]+gmG[i]*gmG[j]-gmK[i]*gmK[j]/ell for j in range(width)]
            for i in range(width)]
    records=[]
    for theta in (F(3,2),F(5,2)):
        x=2*seed['s']-theta
        V=[[x*F(i==j)-Q[i][j] for j in range(N)] for i in range(N)]
        require(all(sum(row,F(0))==x for row in V),'EVERY original free-level constant action')
        (u,v),factor=full_positive_solve(V,[A,B])
        energies=[dot(A,u),dot(B,v),dot(A,v)]
        require(energies[2]==dot(B,u),'BOTH original free-level mixed energies')
        predicted=level(seed,x)
        require(energies==predicted['inverse_Gram'],'three new free-level count/original inverse products')
        require(all(dot(u,b)==dot(v,b)==0 for b in original_first_images),
                'BOTH new entire inverse images lie in FIRST-perp')
        D=[[x*Gm[i][j]-Afirst[i][j] for j in range(width)] for i in range(width)]
        (diW,diG),dfactor=full_positive_solve(D,[gmW,gmG],original_centered=False)
        Bform=[[D[i][j]+gmG[i]*gmG[j] for j in range(width)] for i in range(width)]
        (biK,),bfactor=full_positive_solve(Bform,[gmK],original_centered=False)
        count=shift(seed['q'],counts,Jet(theta,1))
        physical=dict(w=dot(gmW,diW),z=dot(gmG,diW),g=dot(gmG,diG),sigma=ell-dot(gmK,biK))
        require(physical['z']==dot(gmW,diG),'BOTH physical FIRST mixed inverse products')
        require(all(physical[key]==count[key].value for key in ('w','z','g','sigma')),
                'ALL original FIRST count inverse/Schur identities at new levels')
        physical_derivative=-dot(biK,[dot(row,biK) for row in Gm])
        require(physical_derivative==count['sigma'].derivative<0,
                'exact count derivative equals ENTIRE physical inverse-square energy')
        require(all(Bform[i][j]-gmK[i]*gmK[j]/ell==x*Gm[i][j]-frame[i][j]
                    for i in range(width) for j in range(width)),
                'EVERY original shifted-FIRST identity at new levels')
        records.append(dict(theta=theta,x=x,original_inverse_Gram=energies,
            full_original_inverse_images=[u,v],whole_original_positive_solve=factor,
            count_free_level=predicted,original_endpoint_kernels=endpoints(V,A,B,u,v,*energies),
            original_first_dimension=width,original_first_annihilations=2*width,
            inverse_first_annihilations=2*width,shifted_identity_positions=width*width,
            D_positive_factor=dfactor,B_positive_factor=bfactor,D_inverse_images=[diW,diG],
            B_inverse_image=biK,physical_inverse_products=physical,
            physical_sigma_derivative=physical_derivative,count_sigma_derivative=count['sigma'].derivative))
    return dict(agent='six-downset-1',role='researcher',status='NEW FREE-LEVEL ORIGINAL/FIRST-DERIVATIVE CONTROLS',
        n=n,counts=counts,N=N,all_original_pairs=N*N,full_original_rows=N,
        full_original_FIRST_dimension=width,records=records,
        universal_and_singular_space_bridge='ORDINARY UNFORMALIZED proof, not these finite levels',
        independent_review=False,source_commit=None,graph_ref=None)


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--counts',required=True)
    parser.add_argument('--out',type=Path,required=True); args=parser.parse_args()
    require(not args.out.exists(),'unique new original output')
    counts=[int(x) for x in args.counts.split(',')]
    geometry.preflight(4,counts)
    def expire(a,b): raise TimeoutError('unchanged60s; incomplete original check is not nonexistence')
    signal.signal(signal.SIGALRM,expire); signal.alarm(60); start=time.monotonic()
    result=read(4,counts)
    raw=json.dumps(stringify(result),sort_keys=True,separators=(',',':')).encode()+b'\n'
    require(len(raw)<=32*1024*1024,'32MiB whole output'); args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(raw); signal.alarm(0)
    print(json.dumps(dict(status=result['status'],bytes=len(raw),sha256=sha256(raw).hexdigest(),
        seconds=time.monotonic()-start,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        counts=counts,N=result['N'],exact_positive_original_levels=[str(x['x']) for x in result['records']])))


if __name__=='__main__': main()
