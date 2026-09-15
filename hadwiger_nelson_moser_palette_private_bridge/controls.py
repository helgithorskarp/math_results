"""Entrywise arithmetic comparison and malformed-certificate rejection."""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import json
import produce
import verify

def controls():
    cert=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
    p,mp,edges,base=produce.geometry()
    q,qe,qb,distances=verify.check_geometry(cert)
    verify.need(p==q and edges==qe and base==qb and mp==list(range(19)),'point/edge entrywise audit')
    count=0
    for a,b in combinations(range(19),2):
        x=produce.norm(produce.psub(p[a],p[b]));y=verify.norm(verify.pminus(q[a],q[b]))
        verify.need(x==y,'norm entrywise audit');count+=1
    mutations=[]
    bad=deepcopy(cert);bad['coordinates'][18][0][0]='0';mutations.append(('coordinate',bad))
    bad=deepcopy(cert);bad['coordinates'][18]=deepcopy(bad['coordinates'][17]);mutations.append(('collision',bad))
    bad=deepcopy(cert);bad['edges'].remove([1,16]);mutations.append(('missing_cross_contact',bad))
    bad=deepcopy(cert);bad['five_colouring'][1]=bad['five_colouring'][0];mutations.append(('improper_five_word',bad))
    bad=deepcopy(cert);bad['terminals'][0],bad['terminals'][1]=bad['terminals'][1],bad['terminals'][0];mutations.append(('terminal_order',bad))
    bad=deepcopy(cert);bad['relation']['full_canonical']+=1;mutations.append(('overstated_relation',bad))
    rejected=[]
    for name,bad in mutations:
        try:verify.verify(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted mutation '+name)
    return {'norm_pairs_compared_entrywise':count,'point_rows_compared_entrywise':19,'complete_edges_compared_entrywise':34,'rejected_mutations':rejected}

if __name__=='__main__':print(json.dumps(controls(),indent=2,sort_keys=True))
