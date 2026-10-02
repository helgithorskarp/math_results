"""Post-seal data-only full mathematical correspondence. No producer imports."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
from itertools import combinations
import argparse,hashlib,json
import core
from validate import equal as typed_equal,pairs,constant
def main():
    ap=argparse.ArgumentParser();ap.add_argument('native_fixture',type=Path);ap.add_argument('--output',type=Path);args=ap.parse_args()
    root=Path(__file__).resolve().parent;raw=args.native_fixture.read_bytes()
    core.need(hashlib.sha256(raw).hexdigest()=='f967e6ed3c36b9d26b5cb90400550421dcb98794c715f6161b9a229af0393fb5','whole pinned native fixture bytes')
    n=json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)
    own=json.loads((root/'EXPECTED.json').read_text(),object_pairs_hook=pairs,parse_constant=constant)
    seal=json.loads((root/'PRE_NATIVE_SEAL.json').read_text())
    core.need(all(hashlib.sha256((root/k).read_bytes()).hexdigest()==v for k,v in seal['byte_hashes'].items()if k!='VALIDATION.json'),'ALL six pre-native mathematical files unchanged')
    view=json.loads((root/'VALIDATION.json').read_text())
    projection=json.loads((root/'VALIDATION_PROJECTION.json').read_text())
    core.need(view['original_pre_native_validation_receipt_sha256']==seal['byte_hashes']['VALIDATION.json']==projection['original_full_validation_receipt_sha256'],'original private validation receipt hash')
    core.need(projection['public_validation_sha256']==hashlib.sha256((root/'VALIDATION.json').read_bytes()).hexdigest()and not projection['full_raw_receipt_published']and not projection['mathematical_record_changed'],'explicit compact receipt projection')
    checks=[]
    def same(label,a,b):typed_equal(a,b);checks.append(label)
    same('endpoint',n['eta_endpoint'],own['eta_endpoint'])
    same('whole-balanced-polar',n['whole_polar']['whole_balanced_integral'],own['polar']['whole_B'])
    same('whole-polar-tail',n['whole_polar']['whole_tail'],own['polar']['whole_T'])
    for key in ['mean','modulus','variance']:same('whole-polar-'+key,n['whole_polar']['scalar_certificates'][key]['polynomial'],own['polar']['streams'][key]['coefficients'])
    for row in own['sectors']['whole15_sector_integrals']:
        m,d,k=row['m'],row['weight_degree'],row['negative_factors'];native=n['whole_envelopes'][str(m)+':'+str(d)]['all_sectors'][k]
        same('whole-sector-poly'+str((m,d,k)),['0']*d+native['whole_polynomial'],row['whole_integrand_coefficients'])
        same('whole-sector-support'+str((m,d,k)),native['support_lower'],row['threshold'])
        same('whole-sector-monomial'+str((m,d,k)),Q(native['monomial_integral']),9*Q(row['integral']))
        same('whole-sector-positive'+str((m,d,k)),Q(native['positive_bernstein_integral']),9*Q(row['integral']))
    for key,value in [('real_gradient','7:1'),('complex_gradient','7:1'),('complex_Hessian','6:2')]:
        same('whole-global-bound-'+key,n['whole_envelopes'][value]['real'if key=='real_gradient'else'complex'],own['sectors']['whole_bounds'][key])
    for stage,nkey in [(1,'first_majorant_polynomials'),(2,'second_majorant_polynomials')]:
        o=own['whole_majorants'][stage-1]
        for k in range(8):
            p={(i,j):Q(v)for i,j,v in o['whole_polynomials'][str(k)]}
            same('whole-majorant'+str((stage,k)),list(map(Q,n[nkey][str(k)])),list(map(Q,core.old.coefficients(p))))
            same('majorant-endpoint'+str((stage,k)),Q(n['first_majorants'if stage==1 else'second_majorants'][str(k)]),core.ev(p,Q(o['endpoint'])))
        same('whole-radial-gap'+str(stage),n['first_gap'if stage==1 else'second_gap'],o['full_gap'])
    for row in own['whole_radial_faces39over5']:
        k=row['free'];nr=n['whole_radial_faces'][k-1]
        same('entire-face-residual'+str(k),nr['whole_residual'],row['whole_coefficients'])
        same('face-leading-order'+str(k),nr['leading_degree'],row['leading_order'])
        same('face-entire-endpoint-budget'+str(k),nr['lower'],row['positive_endpoint_margin'])
        eta,t=core.atom(0),core.atom(1);a=core.add(core.poly(1),core.sc(eta,-1))
        f=core.add(core.poly(1),a,core.sc(core.mul(a,t),-1))
        g=core.add(f,core.sc(core.mul(core.pw(a,2),t),Q(-8,k)))
        full=core.sc(core.integrate(core.mul(core.pw(f,8-k),core.pw(g,k))),9)
        same('entire-face-scaled-origin'+str(k),nr['whole_scaled_origin'],core.old.coefficients(full))
        dm=Q(64*(k-1),k)-Q(256*(k-1)*(k-2),3*k*k)
        same('entire-face-defect'+str(k),nr['defect_coefficient'],str(dm))
    same('whole-radial-beta-coefficients',list(map(Q,n['whole_radial_gap_coefficients'])),[Q((-1)**k,comb(8,k))-1 for k in range(2,9)])
    centered=own['budgets']['new_centered']
    for nk,ok in [('A','A'),('Bj','lower_B'),('Cd','Cd'),('Bd','Bd'),('Nc','Nc'),('errorB','Be'),('beta','beta'),('kappa','kappa')]:
        same('whole-fixed-energy-'+nk,n['local_basic_coefficients'][nk],centered[ok])
    square=own['whole_mean_square']
    same('whole-mean-square-coefficients',n['whole_mean_square_coefficients'],{str((i,j)):v for i,j,v in square['whole_original']})
    ps=[{(i,j):Q(v)for i,j,v in square[key]}for key in ['whole_original','whole_completed']]
    for i,c in enumerate(n['mean_square_controls']):
        t,w=Q(c['t']),Q(c['W'])
        same('native-full-square-left'+str(i),Q(c['left']),core.ev(ps[0],t,w))
        same('native-full-square-right'+str(i),Q(c['right']),core.ev(ps[1],t,w))
    ms={k:Q(v)for k,v in own['budgets']['strict_margins'].items()}
    sm={k:Q(v)for k,v in own['sectors']['strict_margins'].items()}
    mapping={
     'whole_phase_eps':'whole-phase1/9','phase_cost_real_dominates_hessian':'phase-real-and-mixed','product_grad2':'product-gradient2','whole_origin253eta':'complete-origin-cost253','initial_E2_over7over4':'coarse-E2-7/4',
     'first_radial_squared_7over25':'first-radial-7/25','first_individual_radius':'first-individual1/2','first_radial_root53over100':'first-radial-root53/100','first_phase_root9over200':'first-phase9/200','first_whole_ball1over3':'first-path1/3','first_maclaurin_scale':'first-scale6/25','first_gradient2over9':'first-gradient2/9','first_hessian1over12':'first-Hessian1/12','first_signed_gradient3over40':'first-signed-gradient3/40','first_complex_samephase_sign':'first-complex-radial-sign','first_skew_factor1over7':'first-linear-skew3/7','first_var_under91eta':'first-v91','first_entry1over128':'first-entry1/128',
     'second_radial_root9over100':'second-radial9/100','second_individual_radius':'second-individual1/10','second_phase_root3over80':'second-phase3/80','second_whole_ball1over60':'second-path1/60','second_maclaurin_scale':'second-scale1/18','second_gradient1over7':'second-gradient1/7','second_hessian1over23':'second-Hessian1/23','second_product10over9':'second-product10/9','Vr_under77over4eta':'Vr77/4','actual_reciprocal_norm_under38eta':'reciprocal-squared38','actual_radius24over25':'radius24/25','sqrt38_under37over6':'sqrt38-37/6','sqrt8eta_under9over400':'sqrt8e-9/400','actual_energy42eta':'actual-H42','absoluteH_entry1over375':'actual-H-entry1/375','a_over255over256':'a255/256','delta10':'phase-deficit10',
     'fixed_RMS_and_mean_bound':'centered-mean-rho','fixed_centered_tau':'centered-nu-tau','fixed_full_Rouche':'Rouche-entire','fixed_nine_circle_separation':'nine-circle-disjoint','fixed_positive_Bd':'entire-Bd','fixed_full_pair_normal':'whole-paired-normal','fixed_full_individual_normal':'whole-individual-normal','fixed_initial_tail3over5':'entire-geometric-tail3/5','fixed_initial_rzero':'positive-radius3999/4000','fixed_Q_coefficient_sign':'positive-Q-coefficient','fixed_retained_mean_divisor1over1000':'whole-square-kappa1/1000','fixed_slope13over5':'basic-slope13/5'}
    for i in range(3):
        mapping['bootstrap_var_'+str(i)]='bootstrap'+str(i)+'-endpoint'
        if i<2:mapping['bootstrap_E2_'+str(i)]='bootstrap'+str(i)+'-E2'
    extras={**{'complete_polar_'+k:Q(v)for k,v in own['polar']['strict_margins'].items()},'real_gradient_7over5':sm['real-gradient7/5'],'complex_gradient_14over5':sm['complex-gradient14/5'],'complex_hessian_7over3':sm['complex-Hessian7/3'],'first_full_gap1over6':Q(own['whole_majorants'][0]['full_gap'])-Q(1,6),'second_full_gap4over9':Q(own['whole_majorants'][1]['full_gap'])-Q(4,9),'transfer65over64':Q(65,64)-Q(256,255)**2,'fixed_rminus_tau_positive':1-core.END-Q(1,54)-Q(1,19),'fixed_cube_displacement':ms['whole-delta-W/5']/5,'fixed_cube_linear_displacement':ms['whole-delta0-W/5']/5}
    extras.update({'radial_face_'+str(r['free']):Q(r['positive_endpoint_margin'])for r in own['whole_radial_faces39over5']})
    core.need(set(mapping)|set(extras)==set(n['strict_full_window_margins']),'ALL72 native scalar fields accounted for')
    for k,v in n['strict_full_window_margins'].items():same('native-scalar-'+k,Q(v),ms[mapping[k]]if k in mapping else extras[k])
    for row in n['whole_skew_controls']:
        k=row['positive_count'];xs=[Q(8-k)]*k+[Q(-k)]*(8-k);v=sum(x*x for x in xs);p3=sum(x**3 for x in xs)
        for name,a,b in [('tuple',row['whole_tuple'],list(map(str,xs))),('variance',row['variance'],str(v)),('p3',row['p3'],str(p3)),('ratio',row['skew_ratio_squared'],str(p3*p3/v**3))]:same('whole-native-skew-'+name+str(k),a,b)
    z=core.center;ga=z.ga;plus=z.gadd;times=z.gmul;scale=z.gsc;power=z.gp;total=z.gsum
    def product(xs):
        out=ga(1)
        for x in xs:out=times(out,x)
        return out
    def factors(qs,a):
        out=[ga(1)]
        for x in qs:
            nxt=[ga(0)for _ in range(len(out)+1)]
            for k,c in enumerate(out):nxt[k]=plus(nxt[k],c);nxt[k+1]=plus(nxt[k+1],scale(times(c,x),-a))
            out=nxt
        return out
    def encoded(xs):return [[str(v)for v in x]for x in xs]
    def integ(cs,shift,c):return total(scale(v,Q(c,k+shift+1))for k,v in enumerate(cs))
    for row in n['whole_literal_controls']:
        qs=[tuple(map(Q,x))for x in row['whole_q']];a=Q(row['a']);name=row['name'];coeff=factors(qs,a)
        same('native-entire-product-'+name,row['whole_origin_product_coefficients'],encoded(coeff));same('native-entire-origin-'+name,row['origin'],encoded([integ(coeff,0,9)])[0])
        grad=[scale(integ(factors([q for j,q in enumerate(qs)if j!=i],a),1,9),-a)for i in range(8)]
        hess=[[ga(0)if i==j else scale(integ(factors([q for k,q in enumerate(qs)if k not in [i,j]],a),2,9),a*a)for j in range(8)]for i in range(8)]
        same('native-all8gradients-'+name,row['all_eight_gradients'],encoded(grad));same('native-all64orderedHessian-'+name,row['whole_ordered_hessian'],[encoded(xs)for xs in hess])
        mean=scale(total(qs),Q(1,8));xs=[plus(q,scale(mean,-1))for q in qs]
        es=[total(product(c)for c in combinations(xs,k))for k in range(9)]
        traces=[total(power(q,k)for q in xs)for k in range(9)]
        same('native-whole-centered-tuple-'+name,row['whole_centered_tuple'],encoded(xs));same('native-all-elementary-'+name,row['all_centered_elementary_coefficients'],encoded(es));same('native-all-traces-'+name,row['all_centered_traces'],encoded(traces))
    same('first-whole-upper-cost',n['B1'],'136/9');same('second-whole-upper-cost',n['B2'],own['budgets']['new_refinement']['Bstar'])
    report={'agent':'six-reviewer-1','role':'independent mathematical reviewer','method':'post-seal data-only whole correspondence, no producer code import; late native input controls not pre-native evidence','independent_record_sha256':core.digest(own),'native_fixture_byte_sha256':hashlib.sha256(raw).hexdigest(),'all72_native_scalar_values':True,'all15_whole_sector_objects':True,'all8_whole_radial_faces':True,'both_whole_majorant_streams':True,'whole_mean_square_and4_controls':True,'all7_complete_Gaussian_objects':True,'all_six_pre_native_sealed_math_bytes_unchanged':True,'public_run_receipt_is_explicit_projection':True,'complete_checks':checks,'check_count':len(checks),'late_scalar_scope':'native fixed255/256 transfer matches its weaker margin, while sealed proof uses stronger actual-endpoint transfer; fixed rminus-tau explicitly evaluated here, its positivity already follows from written fixed parameters','actual_disk_feasibility_asserted':False}
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='complete_checks'},sort_keys=True))
if __name__=='__main__':main()
