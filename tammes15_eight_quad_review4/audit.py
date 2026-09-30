#!/usr/bin/env python3
"""Independent incidence and exact SymPy/Sturm audit of the local exclusion."""
import argparse
import json
from pathlib import Path
import metric
import dependencies
import incidence


def controls():
    bad=[('interior_zero',(metric.c-metric.K(11)/20)**2),
         ('interior_pole',metric.ONE/(metric.c-metric.K(11)/20)),
         ('zero_polynomial',metric.Z)]
    rejected=[]
    for name,value in bad:
        try:metric.certify(value,'control_'+name)
        except ValueError:rejected.append(name)
        else:raise ValueError('invalid strict sign accepted: '+name)
    try:metric.third((metric.ONE,metric.Z,metric.Z),(metric.ONE,metric.Z,metric.Z),1)
    except ValueError:rejected.append('noncontact_seed_pair')
    else:raise ValueError('noncontact seed accepted')
    endpoint=metric.certify(metric.c-metric.K(1)/2,'control_open_endpoint',1)
    metric.require(endpoint['numerator']['endpoint_root_multiplicities']==[1,0]
                   and endpoint['numerator']['endpoint_signs'][0]==0,'open endpoint control')
    return {'rejected':rejected,'open_endpoint_root_handled':True}


def run():
    metric.require(metric.sp.__version__=='1.14.0','use pinned SymPy1.14.0')
    a=metric.run();b=dependencies.run();c=incidence.run()
    return {'agent':'six-reviewer-4','role':'independent mathematical reviewer',
            'metric':a,'local_prerequisite_arithmetic':b,'incidence':c,'controls':controls(),
            'scope':'Independent local degree-pattern exclusion. Eight-Q beta specialization is conditional on the cited degree-pattern theorem, not a fresh profile classification.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args();result=run()
    if args.check:
        metric.require(result==json.loads(Path(__file__).with_name('expected.json').read_text()),'expected-output mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
