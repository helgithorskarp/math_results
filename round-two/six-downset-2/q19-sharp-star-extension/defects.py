"""Semantic controls against actual original/basis/degree obligations."""
import argparse
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import time
import resource
import model
import physical
import capacity
from diagnose import entry_audit
from model import canonical, coefficient_input, comparison, exact_ldl, literal_point, q19_candidate, require, type_budgets, TAU_MAX


def run(path):
    start=time.monotonic();raw=coefficient_input(path);rejections=[]
    def reject(name,fn):
        try:fn()
        except ValueError as e:rejections.append(dict(name=name,exception='ValueError',reason=str(e)))
        else:raise ValueError('Defective mathematics accepted: '+name)
    base_table=comparison(raw,9,10);base=literal_point(base_table,9,10);b=type_budgets(base_table,9,10)
    table,_=q19_candidate(raw,TAU_MAX);point=literal_point(table,9,10)
    require(entry_audit(point,base,b,TAU_MAX)['all_entry_inequalities_paid'],'positive control: complete original endpoint')
    # Defect in an actual matrix must fail mathematics, not an expected hash.
    bad=deepcopy(point);bad['L'][0][0]+=F(1,1024)
    reject('actual_empty_loop_row',lambda:entry_audit(bad,base,b,TAU_MAX))
    # Omit each of the two essential new repairs independently.
    by=(0,0,2);bc=(6,0,1)
    bad_table=table.copy();bad_table[(by,bc)]=base_table[(by,bc)]
    bad_point=literal_point(bad_table,9,10)
    reject('omit_YY_bcY_decrease',lambda:entry_audit(bad_point,base,b,TAU_MAX))
    ay,x=(1,0,1),(0,1,0);key=tuple(sorted((ay,x)))
    bad_table=table.copy();bad_table[key]=base_table[key]
    bad_point=literal_point(bad_table,9,10)
    reject('omit_positive_aY_anchor_supply',lambda:require(
        entry_audit(bad_point,base,b,TAU_MAX)['all_entry_inequalities_paid'],'all actual anchor/entry floors'))
    beyond_table,_=q19_candidate(raw,TAU_MAX+F(1,32768));beyond=literal_point(beyond_table,9,10)
    reject('beyond_declared_recipe_entry_endpoint',lambda:require(
        entry_audit(beyond,base,b,TAU_MAX+F(1,32768))['all_entry_inequalities_paid'],
        'fixed original empty/X-singleton entry prohibits this floor'))
    # New orbit is essential: deleting or reversing it violates actual anchors.
    key=tuple(sorted(((7,0,0),(0,0,2))))
    missing=table.copy();missing[key]+=TAU_MAX
    missing_point=literal_point(missing,9,10)
    reject('omit_new_abc_YY_anchor_release',lambda:require(
        entry_audit(missing_point,base,b,TAU_MAX)['all_entry_inequalities_paid'],
        'complete actual a/YY floor after essential star release'))
    reversed_trade=table.copy();reversed_trade[key]+=2*TAU_MAX
    reversed_point=literal_point(reversed_trade,9,10)
    reject('reverse_new_unpenalized_star_trade',lambda:require(
        entry_audit(reversed_point,base,b,TAU_MAX)['all_entry_inequalities_paid'],
        'actual original entries reject wrong star direction'))
    # Every basis image and both endpoints have separate literal matrices.
    origin=physical.original(table,9,10);basis,_=physical.complete_basis(origin)
    require(physical.literal_actions(origin,table,basis)['both_endpoints_every_original_row_every_basis_checked'],
            'positive control: full original lower/upper actions')
    altered=deepcopy(origin);altered['T'][0][0]+=1
    reject('physical_lower_entry',lambda:physical.literal_actions(altered,table,basis))
    altered=deepcopy(origin);altered['cap'][0][0]+=1
    reject('physical_upper_inverse_metric_entry',lambda:physical.literal_actions(altered,table,basis))
    reject('missing_mixed_basis_direction',lambda:physical.literal_actions(origin,table,basis[:-1]))
    doubled=basis[:-1]+[basis[0]]
    reject('duplicated_direction_hides_missing_mode',lambda:physical.literal_actions(origin,table,doubled))
    # Actual group counts, not the quotient formula, catch a wrong degree.
    _,_,data=capacity.q19_data(raw);iv=capacity.interval(10,*data,TAU_MAX)
    capacity.literal_flow(10,*data,TAU_MAX,iv['lower'])
    reject('zeta_outside_complete_capacity_interval',lambda:
           capacity.literal_flow(10,*data,TAU_MAX,iv['lower']-F(1,32768)))
    old_interval=capacity.interval
    def incorrect_beta(*args):
        out=old_interval(*args);out['beta']+=F(1,32768);return out
    capacity.interval=incorrect_beta
    try:
        reject('wrong_bcY_degree_coefficient',lambda:capacity.literal_flow(10,*data,TAU_MAX,iv['lower']))
    finally:capacity.interval=old_interval
    def incorrect_light_interval(*args):
        out=old_interval(*args);out['upper']=out['lower']-F(1,32768);return out
    capacity.interval=incorrect_light_interval
    try:
        reject('inconsistent_capacity_elimination_bounds',lambda:capacity.literal_flow(10,*data,TAU_MAX,iv['lower']))
    finally:capacity.interval=old_interval
    maximum=F(25083,32768)
    reject('KK_endpoint_exceeded',lambda:capacity.literal_flow(10,*data,maximum+F(1,32768),F(0)))
    # Hand controls for exact PD, negative and singular forms, plus type safety.
    pd=exact_ldl([[2,1],[1,2]],[1,1],F(0))
    require(pd['positive_definite'] and pd['pivots']==['2','3/2'],'hand PD control')
    ng=exact_ldl([[1,0],[0,-1]],[1,1],F(0))
    sg=exact_ldl([[1,0],[0,0]],[1,1],F(0))
    require(not ng['positive_definite'] and ng['witness_quadratic']=='-1' and
            not sg['positive_definite'] and sg['witness_quadratic']=='0','hand negative/singular controls')
    reject('floating_point_form_input',lambda:exact_ldl([[1.0,0],[0,1]],[1,1],F(0)))
    reject('unweighted_zero_metric',lambda:exact_ldl([[1,0],[0,1]],[1,0],F(0)))
    reject('asymmetric_block_form',lambda:exact_ldl([[1,1],[0,1]],[1,1],F(0)))
    penalties=capacity.penalty_data(base_table,b);first=F(3755,8192)
    envelope=capacity.envelope(first+F(1,8192),b,penalties)
    require(F(envelope['unavoidable_capacity_penalty'])==F(405,16384),
            'hand first individual KG penalty and factor1/2')
    reject('floating_point_capacity_input',lambda:capacity.interval(10,*data,0.0))
    require(len(rejections)==18,'all18 actual semantic rejections completed')
    return dict(agent='six-downset-2',role='researcher',semantic_rejections=rejections,
                rejection_count=len(rejections),positive_original_endpoint_and_complete_basis_controls=True,
                hand_PD_negative_singular_controls=True,hand_first_capacity_penalty='405/16384',
                no_expected_or_hash_mismatch_used_as_mathematical_rejection=True,
                observed_seconds=time.monotonic()-start,
                peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--coefficients',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();result=run(args.coefficients);raw=canonical(result)+b'\n';Path(args.out).write_bytes(raw)
    import hashlib
    print(json.dumps(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                          rejections=result['rejection_count'],observed_seconds=result['observed_seconds'],peak_RSS_KiB=result['peak_RSS_KiB'])))
