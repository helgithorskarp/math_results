"""Small negative and original-coordinate controls, separate from main audit."""
import argparse
from fractions import Fraction as Q
import json
from math import comb
from pathlib import Path
import signal
from algebra import vars, zero
from check import layer_checks, literal, profile, require, trade


def run():
    controls = []
    n=11
    s,h,r,mu,v,f,S,eta=profile(n)
    eta_root2=eta+Q(4*comb(n,2)*(n-1)**2,h)
    require(eta_root2==5 and eta_root2>0,"root2 control")
    controls.append({'damage':'replace boundary r=2s/h by2',
                     'failed_exclusion_scalar':str(eta_root2)})
    z=literal(6)['damaged_kernel_identity']
    require(Q(z[0])!=Q(z[1]) and Q(z[0])==Q(z[1])+Q(z[2]),
            'kernel omitted control')
    controls.append({'damage':'omit cardinality defect on a free original matrix',
                     'exact_missing_term':z[2]})
    t=trade()
    require(Q(t['Phi_change'])!=h*mu*Q(t['weighted_M_change']),
            'unordered factor damage')
    controls.append({'damage':'lose factor2 on unordered original pairs',
                     'correct_change':t['Phi_change']})
    s,h,r,mu,v,f,S,eta=profile(8)
    lost=sum(comb(8,a)*(mu-f[a]*f[8-a])/2 for a in v)
    require(lost>0,'complement endpoint multiplicity damage')
    controls.append({'damage':'count complement deficits by one endpoint instead of both',
                     'exact_missing_term':str(lost)})
    n=vars(1)[0]
    correct=(3*n*n-2*n)/16
    damaged=(3*n*n-n)/16
    try:
        zero(correct-damaged,'damaged fourth moment')
    except ValueError:
        controls.append({'damage':'replace binomial fourth moment linear coefficient',
                         'rejected':True})
    else:
        raise ValueError('Fourth moment damage accepted')
    for bad in [True,5]:
        try:
            layer_checks(bad)
        except ValueError:
            controls.append({'damage':'out of domain n='+str(bad),'rejected':True})
        else:
            raise ValueError('Invalid order accepted')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'controls':controls,'all_rejected_or_exposed':True}


def main():
    signal.alarm(45)
    p=argparse.ArgumentParser();p.add_argument('--check',type=Path);a=p.parse_args()
    raw=json.dumps(run(),sort_keys=True,indent=2)+'\n'
    if a.check:
        require(a.check.read_text()==raw,'entire control fixture mismatch')
    print(raw,end='')


if __name__=='__main__':
    main()
