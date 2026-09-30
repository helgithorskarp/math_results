"""Independent exact coordinate, Euler-color and spatial-capacity checker.

Imports neither discovery code nor numerical libraries. Does not rely on
enumeration completeness, numerical feasibility, or solver optimality.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path

P,N,C = 617,3704,1852


def need(value,msg):
    if not value:
        raise ValueError(msg)


need(all(P%d for d in range(2,isqrt(P)+1)),'Prime617')
q = [-1]+[0 if pow(r,308,P)==1 else 1 for r in range(1,P)]
need(all(pow(r,308,P) in (1,P-1) for r in range(1,P)),'Euler values')


def check(data,budgets=(196,),return_loads=False):
    need(type(data) is dict and set(data)=={'format','P','N','terms','seam','s','t','g',
         'inner','denominator','mu_numerator','color0_APs'},'Schema')
    need(data['format']=='QR617_SPATIAL_WEIGHTS_1','Format')
    need(all(type(data[k]) is int for k in ['P','N','terms','seam','s','t','g',
         'denominator','mu_numerator']),'Integer fields')
    need((data['P'],data['N'],data['terms'],data['seam'])==(P,N,7,C),'Geometry')
    s,t = data['s'],data['t']
    need(0<=s<P and t==(1-s)%P and data['g']==1,'Reference key')
    need(type(data['inner']) is list and len(data['inner'])==2 and
         all(type(v) is int for v in data['inner']),'Band')
    lo,hi = data['inner']
    need(0<=lo<hi<=N and lo+hi==N,'Reflection-invariant band')
    den,mu = data['denominator'],data['mu_numerator']
    need(den>0 and mu>=0,'Denominator/mu positivity')
    need(type(data['color0_APs']) is list and data['color0_APs'],'Positive support')
    load = [0]*N
    sums = [0,0]
    seen = set()
    for e in data['color0_APs']:
        need(type(e) is list and len(e)==3 and all(type(v) is int for v in e),'Entry')
        a,d,w = e
        need(d>0 and w>0,'Positive AP step/weight')
        for c,aa in [(0,a),(1,N-1-a-6*d)]:
            need(0<=aa<C<=aa+6*d<N,'Crossing integer AP')
            need((aa,d) not in seen,'Duplicate AP')
            seen.add((aa,d))
            for j in range(7):
                x=aa+j*d
                r=(x-C+(s if x<C else t))%P
                need(r!=0,'Free pole in AP')
                need((q[r]^int(x>=C))==c,'Reference monochromatic color')
                load[x]+=w
            sums[c]+=w
    for x,v in enumerate(load):
        need(v<=mu+(0 if lo<=x<hi else den),'Spatial point capacity')
    need(sums[0]==sums[1]>0,'Reflected sums')
    total=sums[0]
    conditional={}
    for budget in budgets:
        need(type(budget) is int and 0<=budget<=N,'Budget')
        conditional[str(budget)]=max(0,(total-budget*mu+den-1)//den)
    out = {'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_EXACT_SPATIAL_CUT',
            'phase':s,'key':[s,t,1],'inner':[lo,hi],
            'per_color_weight':str(Fraction(total,den)),'mu':str(Fraction(mu,den)),
            'sum_numerator':total,'denominator':den,'mu_numerator':mu,
            'maximum_inner_load':str(Fraction(max(load[lo:hi]),den)),
            'maximum_far_load':str(Fraction(max(load[:lo]+load[hi:],default=0),den)),
            'conditional_far_edits_per_color':conditional,
            'checked_APs':len(seen),'checked_incidences':7*len(seen),
            'candidate_arbitrary':True,'candidate_symmetry_assumed':False,
            'pole_colors_free':True,'solver_trusted':False,'edit_optimum_claim':False}
    return (out,load) if return_loads else out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('certificate',type=Path)
    ap.add_argument('--budgets',type=int,nargs='+',default=[196])
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    raw=args.certificate.read_bytes()
    out=check(json.loads(raw),args.budgets)
    out['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    if args.output:args.output.write_text(json.dumps(out,sort_keys=True)+'\n')
    print(json.dumps(out),flush=True)


if __name__=='__main__':
    main()
