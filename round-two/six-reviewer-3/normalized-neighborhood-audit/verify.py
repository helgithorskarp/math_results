#!/usr/bin/env python3
"""Independent full universal-jet and normalized-neighborhood record."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from budgets import Q,certificate,controls,need
from kernel import radial_record
import jets


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def record():
    module,parent,digest,count=radial_record()
    checks=[]
    for name in ['whole_original_cube','review9174_19eta_cover']:
        p=parent[name]
        for key in ['even_matrix','odd_matrix']:
            need(all(max(abs(Q(x)) for x in entry)<1 for row in p[key] for entry in row),'every normalized matrix entry less1')
        need(Q(p['even_determinant'][0])>Q(9,100),'whole even determinant lower bound')
        need(Q(p['odd_determinant'][1])<-Q(3,200),'whole odd determinant upper bound')
        need(all(Q(row[0])>Q(1,9) for row in p['original_root_sine_squared']),'actual original-root sines greater1/3')
        need(1<Q(p['parameter_box'][2][0])<=Q(p['parameter_box'][2][1])<2,'actual positive opening1<T<2')
        need(all(max(abs(Q(x)) for x in p['parameter_box'][j])<2 for j in [0,1]),'actual x/y bounded2')
        checks.append(name+': full normalized inverse/moment premises regenerated')
    dots=parent['review9174_19eta_cover']['full_eta_derivative_certificate']['individual_multiplier_eta_derivatives']
    need(4<Q(dots[0][0])<=Q(dots[0][1])<17,'actual branch third multiplier derivative')
    need(-8<Q(dots[1][0])<=Q(dots[1][1])<-6,'actual branch fourth multiplier derivative')
    c=module.embedding()
    values=module.initial()[0]
    limiting=[module.enclose(value,c) for value in values[:3]]
    need(all(max(abs(x.lo),abs(x.hi))<1 for x in limiting[:2]),'limiting x/y modulus less1')
    need(1<limiting[2].lo<=limiting[2].hi<Q(3,2),'limiting opening1<Tstar<3/2')
    need((1-c*c).lo>Q(1,16),'fixed ninth-root separation greater1/2')
    mu=[module.enclose(module.K(row),c) for row in parent['exact_initial_normal_and_dual']['individual_root_multipliers']]
    loss=Q(257,2**23)
    gap3=mu[0].lo-loss-Q(9,4)
    gap4=mu[1].lo-Q(8,65536)-loss-Q(75,256)
    need(gap3>0 and gap4>0,'both stronger individual weights on complete original9373 box')
    C=module.enclose(module.K(8)-2*sum(module.K(row) for row in parent['exact_initial_normal_and_dual']['individual_root_multipliers']),c)
    need(0<C.lo<=C.hi<8 and mu[0].lo>0 and mu[1].lo>0 and mu[0].hi+mu[1].hi<4,'complete limiting positive dual and deflation constant bounds')
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','method':'Independent rational raw-moment ring, truncated generic Gaussian Newton jet, ninth-root Laurent product, exact algebraic transpose-dual cancellation, full nonnegative-monomial analytic budgets; previous own9335 source-bound interval multiplier regeneration; no target code/data inputs',
            'own_source_files_bound':count,'whole_own9335_record_sha256':digest,'input_premise_checks':checks,'limiting_raw_tuple_enclosures':[x.record() for x in limiting],'limiting_dual_constant_enclosure':C.record(),
            'all_universal_symbolic_jets':jets.record(module,parent),'complete_original9373_neighborhood':certificate(),'semantic_damage_rejections':controls()+jets.controls(),
            'multiplier_refinement':{'limiting_multipliers':[x.record() for x in mu],'complete_actual_eta_derivatives':dots,'individual_alpha_box_loss':str(loss),'pair3_fixed_weight_margin':str(gap3),'pair4_fixed_weight_margin':str(gap4),'fixed_individual_pair_weights':['9/4','75/256'],'pointwise_pair_weights':['mu3(0)+4eta-((eta+sqrteta)/128)','mu4(0)-8eta-((eta+sqrteta)/128)']},
            'proved_scope':{'eta':['positive','1/65536'],'k':['nonnegative','strictly below1/2-33eta/16'],'coefficient_radius':'delta^6*2^-1999*eta^13','fixed_k1quarter_radius':'2^-2017*eta^13','uniform_normalized_radii':True,'same_original9373_domains_for_refined_weights':True,'critical_multiset_collisions_included':True,'global_competitor_entry':False,'positive_physical_eta0_radius':False},
            'trust_boundary':'Exact universal identities and budget arithmetic plus hash-bound independently reviewed kernels. Joint complex root sections, maximum modulus with parameter-uniform divisibility, operator Cauchy, fixed-positive-eta complete holomorphic tail, ordinary real feasible-path integration, full eliminated Taylor theorem and collision-safe Rouche/moment recovery are unformalized analytic bridges audited in REVIEW.md.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=HERE/'EXPECTED.json');p.add_argument('--emit-fixture',type=Path);a=p.parse_args()
    expected=None if a.emit_fixture else json.loads(a.fixture.read_text())
    actual=record()
    if a.emit_fixture:a.emit_fixture.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(canonical(actual)==canonical(expected),'whole independent universal normalized record')
    print('PASS independent normalized-neighborhood audit',hashlib.sha256(canonical(actual)).hexdigest())
    print(json.dumps(actual['proved_scope'],sort_keys=True))


if __name__=='__main__':main()
