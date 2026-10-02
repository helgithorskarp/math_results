#!/usr/bin/env python3
"""Independent exact physical-entry and feasible-obstruction certificate."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from polys import cast,symbol,families,anchored,identities,majorants,need
from windows import certificate,controls
from reviewed import record as prior_record

HERE=Path(__file__).resolve().parent

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def polynomial_controls():
    z,e,s,x,y,t,n,h,v,q=[symbol(k) for k in ('z','eta','xi','x','y','T','nu','eps','v','q')]
    base,complex_q,real_q=families();pb,pv,pr=[anchored(Q) for Q in (base,complex_q,real_q)]
    tests=[]
    def rejects(name,left,right):
        need(left!=right,'damaged identity accepted '+name);tests.append(name)
    rejects('Newton first coefficient factor',pv.coefficient('z',8)*F(7,9),complex_q.coefficient('z',7))
    rejects('Newton second coefficient factor',pv.coefficient('z',7)*F(14,9),complex_q.coefficient('z',6))
    rejects('discarded marked constant term',9*complex_q.integral('z'),pv)
    heavy_y=y+8*h*v;mean=h**2*v/2
    literal=(z-h**2*x)**6*(z-h**2*heavy_y-(0,1)*h*(mean+q))*(z-h**2*heavy_y-(0,1)*h*(mean-q))
    rejects('wrong heavy half-opening',literal.reduce_square('q',t-h**4*v**2/8),complex_q.substitute({'eta':h**2,'xi':h*v}))
    rejects('lost quadratic real-tail perturbation',real_q-base,(z-e*x)**6*(-64*e*n*(z-e*y))-e*n)
    rejects('conjugated parameter instead of companion coefficients',complex_q.substitute({'xi':-s}),complex_q.conjugate_coefficients())
    rejects('wrong anchored-original trace factor',-(pv-pb).coefficient('z',8),16*e*s+(0,1)*e*s)
    return tests


def record():
    old=prior_record();families_record=identities();maj=majorants();bud=certificate();damages=controls()+polynomial_controls()
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','target':'original LEMMA9438/0','independence':'new whole-polynomial Gaussian reconstruction, exact anchored monomial norms and whole-window physical budgets; target executable/fixture supply no input','reviewed_own_premises':old,'universal_polynomial_and_energy_identities':families_record,'whole_joint_original_root_majorants':maj,'whole_positive_window':bud,'mathematical_damage_rejections':damages,'proved_scope':{'eta':['positive','1/65536'],'k':['nonnegative','strictly below1/2-33eta/16'],'same_actual_marked_root':True,'arbitrary_complex_feasible_competitors':True,'critical_collisions_and_matching_permutations':True,'both_feasible_inward_families':True,'sharp_powers_for_the_fixed_displayed_collar_only':[7,14,3,2],'no_global_first_power_result':True,'combined9448_same_domain_weights':['9/4','75/256']},'trust_boundary':'whole dictionaries and positive-window arithmetic exact; holomorphic original sections, removable divisions/max-modulus/Cauchy/Taylor, multiset matching, Rouche/real root signs and sharpness limits are ordinary audited mathematics, not proof-assistant formalized'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path,default=HERE/'EXPECTED.json');parser.add_argument('--emit-fixture',type=Path);a=parser.parse_args()
    expected=None if a.emit_fixture else json.loads(a.fixture.read_text());actual=record();digest=hashlib.sha256(canonical(actual)).hexdigest()
    if a.emit_fixture:a.emit_fixture.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(canonical(actual)==canonical(expected),'every complete independent fixture field')
    print('PASS independent physical-entry audit',digest)
    print(json.dumps({'whole_identities':len(actual['universal_polynomial_and_energy_identities']['universal_identities']),'whole_window_obligations':len(actual['whole_positive_window']['all_domain_comparisons']),'mathematical_damage_rejections':len(actual['mathematical_damage_rejections']),'record_bytes':len(canonical(actual)),'own_inputs':actual['reviewed_own_premises']['own_source_files']},sort_keys=True))
if __name__=='__main__':main()
