"""Reject false radical branches and damaged positive certificates."""
from pathlib import Path
from copy import deepcopy
import json
import verify as v
v.arithmetic_controls()
# Dependent radicals: sqrt(2)*(1,sqrt3) = sqrt(6)*(sqrt3/3,1).
sqrt3=(v.F(0),v.F(1),v.F(0),v.F(0))
p=((v.Z,v.Z),(v.ONE,sqrt3),v.scale(v.ONE,2))
q=((v.Z,v.Z),(v.scale(sqrt3,v.F(1,3)),v.ONE),v.scale(v.ONE,6))
v.need(v.distance_equal(p,q,0),'dependent-radical collision')
v.need(not v.distance_equal(p,q,1),'dependent-radical false unit')
# Same squared candidate can have the wrong real branch.
v.need(not v.linear_zero(v.scale(v.ONE,2),v.ONE,v.scale(v.ONE,4)),'false plus-root equality')
cert=json.loads((Path(__file__).parent/'certificate.json').read_text())
rejected=[]
for name in ['new_vertex_edge_colour','boundary_word','physical_count']:
    c=deepcopy(cert)
    if name=='new_vertex_edge_colour':
        # First added lens touches a prescribed boundary pin.
        _,_,edges,_,_=v.reconstruct()
        a,b=next(e for e in edges if e[0]<373<=e[1])
        w=list(c['colour4']);w[b]=w[a];c['colour4']=''.join(w)
    elif name=='boundary_word':c['boundary_word']='3'+c['boundary_word'][1:]
    else:c['expected']['points']-=1
    try:v.verify(c)
    except ValueError as e:rejected.append({'mutation':name,'rejection':str(e)})
    else:raise ValueError('accepted damaged certificate: '+name)
print(json.dumps({'status':'CONTROLS_PASS','dependent_radical_cases':2,'false_root_branch_rejected':True,'certificate_corruptions_rejected':rejected},indent=2))
