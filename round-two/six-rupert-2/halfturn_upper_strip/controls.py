#!/usr/bin/env python3
"""False mathematical fixtures; no hash-only rejection or assertion checks."""
from pathlib import Path
import copy,json
import check as c
g=c.g
HERE=Path(__file__).resolve().parent
def fails(label,fn):
    try:fn()
    except (ValueError,IndexError,KeyError,TypeError):return {'fixture':label,'rejected':True}
    raise ValueError('false mathematical fixture accepted: '+label)
def record():
    data=json.loads((HERE/'certificate.json').read_text());tests=[]
    def changed(label,modify):
        d=copy.deepcopy(data);modify(d);tests.append(fails(label,lambda:c.record(d)))
    changed('negative actual separating weight',lambda d:d['separating_dual'][0].update(weight=['-1','0']))
    changed('false positive coordinate-dual coefficient',lambda d:d['signed_coordinate_duals'][0]['nonnegative_weights'][0].update(weight=['1','0']))
    changed('lost original positive tau_x direction',lambda d:d['signed_coordinate_duals'].pop(7))
    changed('actual source point is not the claimed contact',lambda d:d['source_contacts'][0].update(source=1))
    changed('wrong receiving edge orientation',lambda d:d['receiving_edges'][0].reverse())
    changed('unproved enlarged physical radius1/100',lambda d:d.update(physical_Cayley_radius=['1/100','0']))
    changed('unproved height1/100 with these exact remainders',lambda d:d.update(receiver_upper_height=['1/100','0']))
    changed('false zero separating receiving coefficient',lambda d:d.update(separating_beta_claim=['0','0']))
    tests.append(fails('improper original reflection asserted as proper source',lambda:g.proper(g.MX)))
    # The upper-sector edge 27->3 is an actual different lower support below t.
    e=g.a.sub(g.V[3],g.V[27]);n=g.a.cross(g.raw(g.x0,g.t-g.dy),e);h=g.a.dot(n,g.V[27])
    tests.append(fails('false receiving support transferred to y<t',lambda:g.require(min(h-g.a.dot(n,v) for v in g.V)>=0,'actual all60 lower-sector support fails')))
    return {'agent':'six-rupert-2','role':'researcher','scope':'false geometric contacts, source orientation, exact duals, finite remainder domains and asymmetric support transfer; no independent review',
            'false_mathematical_fixtures':tests,'rejected_count':len(tests),'all_checks_explicit_under_optimized_python':True}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args();r=record()
    if args.output:Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'agent':'six-rupert-2','role':'researcher','rejected_count':r['rejected_count'],'WHOLE_control_record_SHA256':g.digest(r)},indent=2))
