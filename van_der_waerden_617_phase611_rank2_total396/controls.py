"""Corruption controls and finite truth models for packing defect transfer."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).absolute().parent))
import base_verify
import check_rank2
import check_transfer

need=base_verify.need


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--shared',type=Path,required=True)
    p.add_argument('--packing',type=Path,required=True);p.add_argument('--trace',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();ctx=check_transfer.Context(a.base,a.shared,a.packing)
    cert=json.loads(a.packing.read_text());trace=json.loads(a.trace.read_text());positive=ctx.check(trace)
    pack_checked=check_rank2.check(a.base,a.shared,cert,context=ctx);rejected=[]

    def reject(name,action):
        try:action()
        except ValueError:rejected.append(name);return
        raise ValueError('Corruption unexpectedly accepted: '+name)

    def pack_bad(name,edit):
        bad=copy.deepcopy(cert);edit(bad)
        reject(name,lambda:check_rank2.check(a.base,a.shared,bad,context=ctx))

    def trace_bad(name,edit):
        bad=copy.deepcopy(trace);edit(bad);reject(name,lambda:ctx.check(bad))

    pack_bad('wrong_base_hash',lambda b:b.update(base_certificate_sha256='0'*64))
    pack_bad('wrong_shared_hash',lambda b:b.update(shared_trace_sha256='0'*64))
    pack_bad('boolean_denominator',lambda b:b.update(denominator=True))
    pack_bad('zero_denominator',lambda b:b.update(denominator=0))
    pack_bad('boolean_class',lambda b:b.update(original_class=False))
    pack_bad('hidden_branch',lambda b:b.update(root=1725))
    pack_bad('weaker_unchecked_caps',lambda b:b.update(caps=[197,199]))
    pack_bad('duplicate_AP',lambda b:b['AP_weights'].append(b['AP_weights'][0].copy()))
    pack_bad('zero_AP_weight',lambda b:b['AP_weights'][0].__setitem__(2,0))
    pack_bad('float_AP_weight',lambda b:b['AP_weights'][0].__setitem__(2,1.0))
    pack_bad('zero_AP_difference',lambda b:b['AP_weights'][0].__setitem__(1,0))
    pack_bad('AP_outside_interval',lambda b:b['AP_weights'][0].__setitem__(0,3704))
    pack_bad('full_domain_overload',lambda b:b.update(denominator=1))
    pack_bad('duplicate_triple',lambda b:b['triple_weights'].append(copy.deepcopy(b['triple_weights'][0])))
    pack_bad('repeated_AP_in_triple',lambda b:b['triple_weights'][0][0].__setitem__(1,b['triple_weights'][0][0][0].copy()))
    incidence={}
    for aa,d,w in cert['AP_weights']:
        for x in base_verify.actual_ap(aa,d)-set(ctx.known):incidence.setdefault(x,[]).append([aa,d])
    common=next(aps[:3] for aps in incidence.values() if len(aps)>=3)
    pack_bad('triple_with_common_unknown',lambda b:b['triple_weights'].__setitem__(0,[common,1]))
    pack_bad('negative_triple_weight',lambda b:b['triple_weights'][0].__setitem__(1,-1))
    trace_bad('wrong_packing_dependency',lambda b:b.update(packing_sha256='0'*64))
    trace_bad('noninteger_trace_caps',lambda b:b.update(caps=[197.0,198]))
    trace_bad('root_already_shared',lambda b:b.update(root=next(x for x in ctx.known if ctx.colors[x]==0)))
    trace_bad('unsupported_pack_terminal',lambda b:b.update(steps=[],terminal={'kind':'packing_defect','class':0}))
    trace_bad('wrong_pack_terminal_class',lambda b:b.update(steps=[],terminal={'kind':'packing_defect','class':1}))
    x=next(x for x in ctx.new_V if not ctx.can_budget_fix(ctx.known,x,0))
    trace_bad('unsupported_new_budget_fact',lambda b:b.update(steps=[{'kind':'budget_fix','point':x,'value':0}],terminal=None))
    pole=next(x for x in range(3704) if ctx.colors[x]<0 and x not in ctx.known)
    trace_bad('uncounted_pole_budget_fact',lambda b:b.update(steps=[{'kind':'budget_fix','point':pole,'value':0}],terminal=None))
    trace_bad('budget_fix_as_edit',lambda b:b.update(steps=[{'kind':'budget_fix','point':x,'value':1}],terminal=None))
    if trace['steps']:
        trace_bad('repeated_top_fact',lambda b:b['steps'].append(copy.deepcopy(b['steps'][0])))
    f=next((i for i,r in enumerate(trace['steps']) if r['kind']=='failed_literal'),None)
    if f is not None:
        trace_bad('failed_literal_without_contradiction',lambda b:b['steps'][f]['trial'].update(terminal=None))
        trace_bad('trial_assumes_accepted_fact',lambda b:b['steps'][f]['trial'].__setitem__('assumption',[b['steps'][f]['point'],b['steps'][f]['value']]))
        def duplicate_assumption(b):
            r=b['steps'][f];r['trial']['steps'].insert(0,{'kind':'budget_fix','point':r['point'],'value':1-r['value']})
        trace_bad('trial_freshness_and_scope',duplicate_assumption)

    # Every nonempty three-edge family on four vertices; every exact edit set.
    triple_models=weighted_models=defect_models=screen_models=0
    universe=set(range(4));edges=[{x for x in universe if mask>>x&1} for mask in range(1,16)]
    for A,B,C in itertools.combinations(edges,3):
        if A&B&C:continue
        triple_models+=1;U=A|B|C
        loads={x:int(x in A)+2*int(x in B)+3*int(x in C)+2*int(x in U) for x in universe}
        W=1+2+3+2*2;D=max(loads.values());delta={x:D-loads[x] for x in universe}
        hits=[E for E in edges if E&A and E&B and E&C]
        for E in hits:
            weighted_models+=1;need(len(E&U)>=2,'Empty common intersection needs two edits')
            need(W<=sum(loads[x] for x in E),'Weighted actual-cover inequality')
            cost=sum(delta[x] for x in E)
            for cap in range(len(E),5):
                defect_models+=1;need(cost<=cap*D-W,'Residual nonnegative packing defect bound')
        for mask in range(16):
            F={x for x in universe if mask>>x&1};cost=sum(delta[x] for x in F)
            for cap in range(5):
                budget=cap*D-W
                if budget<0:continue
                compatible=[E for E in hits if F<=E and len(E)<=cap]
                for x in universe-F:
                    if delta[x]>budget-cost:
                        screen_models+=1;need(all(x not in E for E in compatible),'Strict defect screen forbids an extra edit')
    out={'agent':'six-vdw-3','role':'researcher','python':sys.version.split()[0],'optimized':not __debug__,
         'positive_positions':positive['total_positions'],'positive_integer_floor':pack_checked['conditional_integer_floor'],
         'corruption_rejections':len(rejected),'rejected_cases':rejected,'four_vertex_triple_families':triple_models,
         'weighted_hitting_models':weighted_models,'defect_budget_models':defect_models,'strict_screen_models':screen_models,
         'formal_or_external_review_claimed':False}
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)


if __name__=='__main__':main()
