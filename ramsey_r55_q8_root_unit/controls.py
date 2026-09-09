"""Adversarial scope/proof/dispatch controls for the q8,r8 theorem bridge."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

import bridge
import independent_check


def run(directory, cert):
    base = bridge.load_base(directory)
    variants = []
    for key,value in [('r',7),('assumptions',[]),('assumptions',[119]),
                      ('assumptions',[-119,-802]),('vertex',2),('implied_unit',118),
                      ('blue_neighbors',list(range(4,31))),
                      ('ramsey_subset',list(range(4,28))),
                      ('base_sha256','0'*64),('proof',[])]:
        c=deepcopy(cert);c[key]=value;variants.append((key+':'+str(value)[:24],c))
    c=deepcopy(cert);c['premise']['order']=24;variants.append(('changed Ramsey premise',c))
    c=deepcopy(cert);c['proof'][0]['hints']=[99999999];variants.append(('forward proof hint',c))
    c=deepcopy(cert);c['proof'][0]['clause']=[];variants.append(('false empty clause',c))
    c=deepcopy(cert);c['proof'][0]['clause']=[0];variants.append(('zero literal',c))
    rejected=[]
    for label,c in variants:
        for method in (lambda: bridge.verify_loaded(base,c),lambda:independent_check.check(directory,c)):
            try:method()
            except (ValueError,TypeError,KeyError,IndexError):pass
            else:raise ValueError('Corruption accepted: '+label)
        rejected.append(label)
    session=bridge.Dispatcher(directory,cert)
    invalid_jobs=[dict(r=7,core_assumptions=[],edge_cube=[119]),
                  dict(r=10,core_assumptions=[],edge_cube=[119]),
                  dict(r=8,core_assumptions=[],edge_cube=[]),
                  dict(r=8,core_assumptions=[],edge_cube=[118]),
                  dict(r=8,core_assumptions=[],edge_cube=[119,120]),
                  dict(r=8,core_assumptions=[-119],edge_cube=[119]),
                  dict(r=8,core_assumptions=[802,-802],edge_cube=[119])]
    for j in invalid_jobs:
        try:session.dispatch(j,Path(directory)/'MUST_NOT_WRITE.cnf')
        except ValueError:pass
        else:raise ValueError('Invalid job dispatched')
    # A physical child does not become an original-task cover, even when a
    # caller manually tries to pass its edge cube through the parent API.
    try:bridge.worker.as_cover(dict(edge_cube=[-119]))
    except ValueError:pass
    else:raise ValueError('Physical child upgraded to an original task verdict')
    return dict(status='VERIFIED', rejected_certificate_mutations=len(rejected),
                rejection_labels=rejected, independent_checkers_per_mutation=2,
                rejected_dispatch_scopes=len(invalid_jobs),
                physical_child_to_original_cover_rejected=True,
                actual_target_solver_calls=0)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('certificate')
    a=p.parse_args();print(json.dumps(run(a.directory,json.loads(Path(a.certificate).read_text())),indent=2))
