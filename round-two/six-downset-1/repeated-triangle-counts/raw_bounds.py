"""PRIVATE raw QQ(h,q) anchor and nonexpanding coefficient degree bounds.

No interpolation is performed and no arbitrary-h signs are claimed.
Row denominator products remain factored, retaining the existing guard.
"""
from fractions import Fraction as F
from pathlib import Path
import sys,json,signal,time
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom
from clearing import encode,shift
from sectors import sectors
from exact import require

def degree(p,j):return max((e[j] for e in p.a),default=-1)
def assignment_bound(a):
    dp={0:0};k=len(a)
    for i in range(k):
        out={}
        for mask,v in dp.items():
            for j in range(k):
                if not (mask>>j)&1 and a[i][j]>=0:
                    new=mask|(1<<j);out[new]=max(out.get(new,-1),v+a[i][j])
        dp=out
    require((1<<k)-1 in dp,'nonzero determinant permutation bound')
    return dp[(1<<k)-1]

def main():
    def alarm(signum,frame):raise TimeoutError('unchanged60s raw-bound guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear();h=R(P({(1,0):1}));q=R(P({(0,1):1}))
    for z in [h,h-1,3*h+4,q,q-1,q+3*h-4,q+3*h-3,q+3*h]:atom(z.num)
    p,G,S,C=sectors(h,q);forms={};bounds=[]
    catalogue=[(name,[[p[name]]]) for name in ['alphaH','betaH','alphaL','betaL','nu','muL']]+list(C.items())
    for name,matrix in catalogue:
        raw=[[R(z) for z in row] for row in matrix];powers=[];degree_matrices=[[],[]]
        for row in raw:
            common={}
            for z in row:
                for key,e in z.den.items():common[key]=max(common.get(key,0),e)
            for key in common:require(shift(ATOMS[key]).positive(),'EVERY original common denominator factor positive on h>=2,q>=4')
            powers.append(common)
            for j in range(2):degree_matrices[j].append([degree(z.num,j)+sum((e-z.den.get(key,0))*degree(ATOMS[key],j) for key,e in common.items()) if z.num else -1 for z in row])
        forms[name]=dict(raw=[[dict(numerator=encode(z.num),denominator_factors=[dict(factor=encode(ATOMS[key]),power=e) for key,e in z.den.items()]) for z in row] for row in raw],positive_row_domains=[[dict(factor=encode(ATOMS[key]),power=e) for key,e in common.items()] for common in powers],cleared_entry_separate_degree_upper_bounds=degree_matrices)
        for k in range(1,len(raw)+1):
            dh,dq=[assignment_bound([row[:k] for row in a[:k]]) for a in degree_matrices]
            bounds.append(dict(group=name,order=k,h_degree_bound=dh,q_degree_bound=dq,h_grid_size=dh+1,q_coefficient_columns=dq+1))
    signal.alarm(0);out=dict(agent='six-downset-1',role='researcher',status='Raw exact field anchors and explicit nonexpanding degree bounds only; no coefficient reconstruction or new uniform signs',original_domain='QQ(h,q),h>=2,q>=4',forms=forms,bounds=bounds,maximum_h_grid_size=max(z['h_grid_size'] for z in bounds),maximum_q_columns=max(z['q_coefficient_columns'] for z in bounds))
    Path('work/raw-bounds.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('forms','bounds')}))
    print(json.dumps(bounds))
if __name__=='__main__':main()
