"""Damaged-certificate controls; no discovery or numerical dependencies."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('literal_small_groups',ROOT/'check.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)


def controls(data):
    mutations=[]
    d=deepcopy(data);d['fixture']['available_moduli'].remove(20);mutations.append(('missing free20',d))
    d=deepcopy(data);d['fixture']['anchors'][-1]=[16,1];mutations.append(('older odd16 domain',d))
    d=deepcopy(data);d['maximum_outside_group_size']=6;mutations.append(('unsupported group size',d))
    d=deepcopy(data);d['outside_credit']='mu';mutations.append(('missing quadratic loss',d))
    d=deepcopy(data);d['resource_marginals'][0]['entries'][0]['numerator']+=1;mutations.append(('marginal load changed',d))
    d=deepcopy(data);d['resource_marginals'][0]['entries'][0]['phase_representative']=d['resource_marginals'][0]['resource'];mutations.append(('illegal marginal phase',d))
    d=deepcopy(data);d['joint_mixture'][0]['phases']['top'][0][1]=288;mutations.append(('illegal TOP label',d))
    d=deepcopy(data);d['resource_marginals'][0]['entries'][0]['orbit_size']+=1;mutations.append(('false phase-orbit size',d))
    # This keeps every domain, load and phase legal; actual orbit domination
    # must reject it, rather than a schema or probability guard.
    d=deepcopy(data);N=d['fixture']['period'];P=d['fixture']['anchors'];gens=c.swaps(N,P)
    for group in d['resource_marginals']:
        n=group['resource'];dsu=c.DSU(n)
        for gen in gens:
            for a in range(n):dsu.join(a,c.image(a,n,gen))
        orbit=next(o for o in dsu.orbits() if o[0]==0)
        group['entries']=[{'phase_representative':0,'orbit_size':len(orbit),'numerator':d['denominator']}]
    d['joint_mixture']=[{'numerator':d['denominator'],'phases':{'outside':[0,0],'top':[[dd,0,0] for dd in(1,5,7,35)]}}]
    mutations.append(('legal marginals fail orbit domination',d))
    results=[]
    for label,damaged in mutations:
        try:c.check(damaged)
        except (ValueError,KeyError,TypeError) as e:results.append({'control':label,'rejected':True,'reason':str(e)})
        else:raise ValueError('damaged control was accepted: '+label)
    return {'agent':'six-covering-3','role':'researcher','damaged_controls':results,'rejected':len(results)}


if __name__=='__main__':
    import time,resource
    start=time.monotonic();print(json.dumps(controls(json.loads((ROOT/'certificate.json').read_text()))))
    print(json.dumps({'seconds':round(time.monotonic()-start,3),'peak_self_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
