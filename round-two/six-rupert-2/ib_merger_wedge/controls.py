"""Semantic false-fixture rejection, without an EXPECTED/hash comparison."""
from copy import deepcopy
from pathlib import Path
import argparse,json
import check as c
g,Q=c.g,c.Q
def changed(cert,key,value):
    cc=deepcopy(cert);cc[key]=value;return cc
def run():
    cert=c.read_certificate();data,small=c.contact_data(cert,{})
    wrong_pre=deepcopy(cert);wrong_pre['contacts'][0]['B_source']=0
    wrong_support=deepcopy(cert);wrong_support['contacts'][0]={'edge':[7,3],'endpoint':7,'B_source':45}
    wrong_cycle=deepcopy(cert);wrong_cycle['cell_cycles'][0][4]=55
    wrong_mass=deepcopy(cert['duals'][0]);wrong_mass['mass_bound']=1
    improper=tuple(tuple(-x if i==0 else x for x in row) for i,row in enumerate(g.B))
    fixtures=[
      ('false actual B spatial preimage',lambda:c.contact_data(wrong_pre,{})),
      ('eta=0 edge falsely used inside receiving wedge',lambda:c.contact_data(wrong_support,{})),
      ('false enlarged delta=1 support domain',lambda:c.contact_data(changed(cert,'delta',['1','0']),{})),
      ('zero base weight falsely called strict on all30 contacts',lambda:c.parameters(changed(cert,'strict_base_weight',['0','0']))),
      ('false C=1 nonlinear normal bound',lambda:c.contact_data(changed(cert,'quadratic_bound_C',['1','0']),{})),
      ('false closed rho=1 absorption',lambda:c.parameters(changed(cert,'closed_Cayley_radius',['1','0']))),
      ('improper B source matrix',lambda:g.proper(improper)),
      ('negative original excess cofactor',lambda:c.dual_record(cert['duals'][0],data,{},damage='negative_cofactor')),
      ('nonzero original force target falsely called cancelled',lambda:c.dual_record(cert['duals'][0],data,{},damage='false_force_target')),
      ('false normalized mass bound1',lambda:c.dual_record(wrong_mass,data,{})),
      ('real interior receiving corner27 replaced by55 in wrong cell',lambda:c.phase_geometry(wrong_cycle,{})),
      ('fictitious strict18-corner q hull',lambda:c.q_geometry(changed(cert,'q_cycle',cert['cell_cycles'][0]),{})),
    ]
    out=[]
    for name,f in fixtures:
        try:f()
        except ValueError as e:out.append({'false_mathematical_fixture':name,'rejected_by_original_mathematical_gate':str(e)})
        else:raise ValueError('false fixture accepted: '+name)
    return {'agent':'six-rupert-2','role':'researcher','fixtures':out,'all_semantic_false_fixtures_rejected':len(out),'EXPECTED_or_fingerprint_not_consulted':True}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args();out=run()
    if args.output:Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
