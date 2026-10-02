"""Exact small positive/negative support kernels and literal semantic damage."""
import copy
import importlib.util
import json
from pathlib import Path

S=Path('round-two/six-code-3/scratch');R=Path('round-two/six-code-3/four_hub_p21_endpoint_cut')
spec=importlib.util.spec_from_file_location('independent_support',S/'pass17-check-support-census.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def main():
    rows=json.loads((S/'pass16-hub-role-catalogue.json').read_text())['records']
    types=json.loads((R/'expected.json').read_text())['types']
    fixtures=json.loads((R/'fixtures.json').read_text())['stars']
    d=(1,0,0,0);lb=(2,0,0,0)
    c.need(c.local_factor([(d,lb)],2,(2,0,0,0))=={(2,0,0,0,2,0,0,0,2,0,0,0)},'positive support polynomial control')
    c.need(c.local_factor([(d,lb)],1,(1,0,0,0))==set(),'single center cannot supply another support friend')
    c.need(c.local_factor([(d,lb)],2,(1,0,0,0))==set(),'integer target capacity control')
    positive=next(r for r in rows if r['hub_deficits'][0]>0)
    rejected=0
    for field in ('HH_leave_mask','hub_deficits','witness','q'):
        damaged=copy.deepcopy(positive);basis=copy.deepcopy(types)
        if field=='HH_leave_mask':damaged[field]^=1
        elif field=='hub_deficits':damaged[field][0]+=1
        elif field=='witness':damaged[field]['hub_roles'][1]=damaged[field]['hub_roles'][0]
        else:basis[damaged['type_id']]['q']+=1
        try:c.physical_audit([damaged],basis,fixtures)
        except ValueError:rejected+=1
        else:raise ValueError('literal semantic damage accepted: '+field)
    out=S/'pass17-support-controls.json';c.need(not out.exists(),'fresh control output')
    result=dict(agent='six-code-3',role='researcher',status='PRIVATE_SUPPORT_POSITIVE_NEGATIVE_CONTROLS_PASS',
                positive_polynomial_kernels=1,negative_polynomial_kernels=2,literal_semantic_damages_rejected=rejected,
                new_pair_total_claim=None)
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
