"""Adversarial input/coverage/vertex controls, without modifying source files."""
from pathlib import Path
from copy import deepcopy
import json
import signal
import check as c

HERE=Path(__file__).resolve().parent
def run(data,plan):
    c.layout(data,plan)
    alterations=[]
    def add(name,target,path,value):alterations.append((name,target,path,value))
    add('actual_point13_in_fixed_core','data',('core_labels',0),13)
    add('missing_fixed_label','data',('core_labels',),data['core_labels'][:-1])
    add('wrong_distinguished_root','data',('root_bracket',0),'0.58')
    add('wrong_cap_bound','data',('cap_bound',),'666/250')
    add('wrong_cap_pair_parameter','data',('cap_code_parameter_upper',),'3/5')
    add('lost_strict_short_norm_cut','data',('cut_short_squared_norm_upper',),'1')
    add('lost_strict_short_norm_fourteen','data',('fourteen_short_squared_norm_upper',),'1')
    add('wrong_q_contact_planes','data',('q_active_labels',),[8,10,11])
    add('wrong_last_contact_planes','data',('other_active_labels',),[3,4,5])
    add('missing_one_complete_target','plan',('cases',),plan['cases'][:-1])
    add('swapped_target_order','plan',('cases',),list(reversed(plan['cases'])))
    add('unjustified_parameter_target','plan',('cases',0,'name'),'whole-parameter-frame')
    add('lost_cut_plane','plan',('cases',0,'labels'),plan['cases'][0]['labels'][:-1])
    add('missing_one_active_triple','plan',('cases',2,'tokens'),plan['cases'][2]['tokens'][:-1])
    add('unknown_plane_literal','plan',('cases',0,'tokens',0),'Iz')
    add('unit_from_another_target','plan',('cases',1,'tokens',0),'Uc')
    rejected=[]
    for name,target,path,value in alterations:
        d,p=deepcopy(data),deepcopy(plan);container=d if target=='data' else p
        for key in path[:-1]:container=container[key]
        container[path[-1]]=value
        try:c.layout(d,p)
        except (ValueError,KeyError,TypeError,IndexError):rejected.append(name)
        else:raise ValueError('damaged binding accepted: '+name)
    H,V,constraints,units,contacts,q,other=c.geometry(data)
    work=c.layout(data,plan)
    original=next(entry for entry in work if entry[0]==0 and entry[2]=='Ua')
    for name,token in (
        ('nonsingular_vertex_marked_singular','S'),
        ('unit_vertex_marked_strictly_short','N'),
        ('unit_vertex_identified_as_another_point','Ub'),
        ('active_plane_claimed_strictly_violated','I'+c.INDEX[original[1][0]]),
    ):
        altered=(original[0],original[1],token)
        try:c.predicate(altered,H,constraints,units)
        except (ValueError,ArithmeticError):rejected.append(name)
        else:raise ValueError('damaged exact vertex predicate accepted: '+name)
    positive=[]
    for name,d,p in (
        ('real_reversed_json_field_order',
         json.loads(json.dumps(dict(reversed(list(data.items()))))),
         json.loads(json.dumps(dict(reversed(list(plan.items())))))),
        ('harmless_metadata',data | {'uninterpreted_note':'metadata only'},plan),
    ):
        c.layout(d,p);positive.append(name)
    return {'status':'CHECKED_DAMAGE_CONTROLS','semantic_damages_rejected':rejected,
            'damages_count':len(rejected),'harmless_alterations_accepted':positive,
            'frozen_source_not_mutated':True,'active_plane_ranges_not_repeated':True}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second control guard')))
    signal.alarm(50)
    print(json.dumps(run(json.loads((HERE/'INPUT.json').read_text()),
                         json.loads((HERE/'PLAN.json').read_text())),sort_keys=True))
