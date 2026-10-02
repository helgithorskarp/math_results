#!/usr/bin/env python3
"""Whole exact four-normal/multiplier record; every field regenerated."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from prior import F, I, K, need, embedding, enclose
from normal import initial,certify
from eta_derivative import multiplier_derivatives
from literal import run

HERE = Path(__file__).resolve().parent


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def record():
    controls = run()
    values, first = initial()
    c = embedding()
    covers=[]
    for radius in [F(1,1024),F(19,65536)]:
        covered=certify(values,radius)
        box=[enclose(k,c)+I(-radius,radius) for k in values]
        rec,dots=multiplier_derivatives(box,c)
        bases=[enclose(K(row),c) for row in first['individual_root_multipliers']]
        refined=[base+I(0,F(1,65536))*dot for base,dot in zip(bases,dots)]
        need(F(73,32)<refined[0].lo<=refined[0].hi<F(147,64), 'sharper third-pair individual multiplier')
        need(F(75,256)<refined[1].lo<=refined[1].hi<F(19,64), 'sharper fourth-pair individual multiplier')
        need(-9<dots[1].lo<=dots[1].hi<-5, 'whole-cube fourth multiplier deflated difference')
        if radius==F(19,65536):
            need(4<dots[0].lo<=dots[0].hi<17 and -8<dots[1].lo<=dots[1].hi<-6, 'both actual-branch first-order multiplier differences')
        rec['multipliers_refined_by_eta_mean_value']=[x.record() for x in refined]
        covered['full_eta_derivative_certificate']=rec
        covers.append(covered)
    prior=json.loads((HERE.parent/'complex-sector-audit'/'EXPECTED.json').read_text())
    for new,old in zip(covers,[prior['full_original_cube'],prior['review9174_19eta_box']]):
        need(new['odd_matrix']==old['odd_matrix'] and new['odd_determinant']==old['odd_determinant'] and new['physical_circle_denominators']==old['physical_circle_denominators'], 'complete previous independently audited odd certificate regenerated')
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
        'eta_domain':['positive','1/65536'],'method':'literal anchored critical products; full actual original-root half squared-modulus normals; cancelled transpose dual; complete interval eta derivatives and mean-value theorem; independent Gaussian products and simple-original-root controls',
        'controls':controls,'exact_initial_normal_and_dual':first,'whole_original_cube':covers[0],'review9174_19eta_cover':covers[1],
        'proved_refinements':{'even_determinant_window':['9/100','3/32'],'four_normal_determinant_over_eta5_window':['-1/560','-1/600'],
            'individual_mu3_window':['73/32','147/64'],'individual_mu4_window':['75/256','19/64'],
            'actual_branch_deflated_mu3_difference_window':['4','17'],'actual_branch_deflated_mu4_difference_window':['-8','-6'],
            'admissible_explicit_individual_slack_weights':['mu3(0)+4eta','mu4(0)-8eta'],
            'admissible_uniform_individual_slack_weights':['9/4','75/256'],
            'joint_nonnegative_coefficient_closure':'[0,kappa12] x [0,mu3] x [0,mu4]; every componentwise strict triple is locally admissible; boundary attainment not asserted',
            'full_feasible_anisotropic_energy':'review9289 four fixed quadratic coefficients plus both stronger independent original-root slack weights, on a pointwise coefficient neighborhood',
            'all_nonlinear_radii':'pointwise existential; no numerical or uniform radius'},
        'necessary_dependencies':['9174 legal simple-original-root branch and tighter19eta cover','9289 independently audited9225 full zero-slack theorem and anisotropic energy;9203 real eigenvalue'],
        'trust_boundary':'own hash-bound reviewed field/interval/circle/Gaussian kernels, new actual four-normal/dual and interval eta derivative calculation. Ordinary root IFT, fixed-tail mean value, critical-multiset continuity, product feasibility, slack integration and sharp coefficient necessity unformalized. No researcher executable or fixture supplies independent calculation inputs.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=HERE/'EXPECTED.json');p.add_argument('--emit-fixture',type=Path);args=p.parse_args()
    expected=None if args.emit_fixture else json.loads(args.fixture.read_text())
    actual=record()
    if args.emit_fixture:args.emit_fixture.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(canonical(actual)==canonical(expected),'entire independent frozen radial record')
    print('PASS independent original-root radial certificate',hashlib.sha256(canonical(actual)).hexdigest())
    print(json.dumps(actual['proved_refinements'],sort_keys=True))


if __name__=='__main__':main()
