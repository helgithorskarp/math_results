"""Post-seal data-only comparison. Never imports or executes author source.
The proof core/record remain sealed; native Gaussian inputs are read only now.
The full source replay is recorded separately. This adapter requires the pinned
public author's EXPECTED.json, not a private ledger or hidden proof corpus.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import comb,factorial
import argparse,json,hashlib
import core
from validate import pairs,reject_constant,strict_equal

def main():
    p=argparse.ArgumentParser();p.add_argument('author_fixture',type=Path);p.add_argument('--output',type=Path);args=p.parse_args()
    raw=args.author_fixture.read_bytes();core.need(hashlib.sha256(raw).hexdigest()=='a1ce9f93ecc73f38c158879d42610c3f09d0f95da026db97fd21066ace53ee4a','entire pinned native fixture')
    native=json.loads(raw,object_pairs_hook=pairs,parse_constant=reject_constant);own=json.loads(Path(__file__).with_name('EXPECTED.json').read_text(),object_pairs_hook=pairs,parse_constant=reject_constant)
    seal=json.loads(Path(__file__).with_name('PRE_NATIVE_SEAL.json').read_text());d=Path(__file__).resolve().parent
    core.need(all(hashlib.sha256((d/('PRE_NATIVE_PROOF.txt' if name=='PROOF.md' else name)).read_bytes()).hexdigest()==value for name,value in seal['byte_hashes'].items()),'all pre-native core/proof/record bytes unchanged')
    checks=[]
    def equal(name,a,b):strict_equal(a,b);checks.append(name)
    equal('endpoint',native['eta_endpoint'],own['eta_endpoint'])
    equal('whole-polar-balanced',native['whole_polar']['whole_balanced_integral'],own['polar']['B']);equal('whole-polar-tail',native['whole_polar']['whole_tail'],own['polar']['T'])
    for n,o in [('mean','mean'),('modulus','balanced'),('variance','variance')]:equal('entire-polar-stream-'+n,native['whole_polar']['scalar_certificates'][n]['polynomial'],own['polar']['streams'][o]['coefficients'])
    for stage,key in [(1,'first_majorant_polynomials'),(2,'second_majorant_polynomials')]:
        record=own['whole_newton_majorants'][stage-1]
        for k in range(8):
            polynomial={(i,j):Q(v)for i,j,v in record['whole_majorants'][str(k)]}
            equal('whole-majorant-'+str(stage)+'-'+str(k),list(map(Q,native[key][str(k)])),list(map(Q,core.coefficients(polynomial))))
        equal('whole-radial-gap-'+str(stage),native['first_gap'if stage==1 else'second_gap'],record['exact_coercivity'])
    for row in own['sector']['complete_15_sector_integrals']:
        m,d0,k=row['m'],row['weight_degree'],row['negative_factors'];n=native['whole_envelopes'][str(m)+':'+str(d0)]['all_sectors'][k]
        equal('whole-sector-polynomial-'+str((m,d0,k)),['0']*d0+n['whole_polynomial'],row['whole_integrand_coefficients'])
        equal('whole-sector-support-'+str((m,d0,k)),n['support_lower'],row['threshold'])
        equal('whole-sector-integral-'+str((m,d0,k)),Q(n['monomial_integral']),9*Q(row['integral']))
        equal('whole-positive-sector-integral-'+str((m,d0,k)),Q(n['positive_bernstein_integral']),9*Q(row['integral']))
    w=own['budgets']['widened_centered'];n=native['local_basic_coefficients']
    for key,a in [('A','A'),('Bj','B_lower'),('Cd','Cd'),('Bd','Bd'),('Nc','Nc'),('errorB','Be'),('kappa','kappa')]:equal('whole-widened-centered-'+key,n[key],w[a])
    # Compare every native scalar against independent arithmetic or an
    # explicitly stronger sealed inequality. Data equality is not inferred
    # from equal counts or positive signs.
    ms={k:Q(v)for k,v in own['budgets']['strict_margins'].items()};ms.update({k:Q(v)for k,v in own['polar']['strict_margins'].items()});ms.update({k:Q(v)for k,v in own['sector']['strict_margins'].items()})
    mapping={
      'whole_polar_mean':'mean-whole-coefficient-budget','whole_polar_modulus':'balanced-whole-coefficient-budget','whole_polar_variance':'variance-whole-coefficient-budget',
      'global_derivative_7':'gradient-whole-sector-budget','global_derivative_6':'mixed-Hessian-whole-sector-budget','global_phase_l1_under_eps':'whole-phase1/12','global_product_grad_under2':'global-product-gradient2','a_over255over256':'normalization-a255/256','delta10':'angular10',
      'initial_E2_over7over4':'global-E2-7/4','first_radial_norm15over32':'local1-squared-norm15/32','first_individual_radius':'local1-individual2/3','first_norm_root11over16':'local1-radial11/16','first_phase_root3over80':'local1-phase3/80','first_whole_ball3over5':'local1-whole-path3/5','first_maclaurin_scale':'local1-Cauchy8/25','first_gradient2over7':'local1-gradient2/7','first_hessian3over25':'local1-Hessian3/25','first_signed_gradient7over200':'local1-negative-gradient7/200','first_complex_radial_sign':'local1-complex-negative-gradient','skewness_at_first_ball':'zero-sum-skew-linear6/11','first_var_under375eta':'first-proportional-375','first_var_entry1over64':'first-proportional-entry1/64',
      'second_radial_norm_root17over128':'local2-squared-norm17/128','second_individual_radius':'local2-individual1/8','second_phase_root1over32':'local2-phase1/32','second_whole_ball1over36':'local2-whole-path1/36','second_maclaurin_scale':'local2-Cauchy1/14','second_gradient3over20':'local2-gradient3/20','second_hessian1over22':'local2-Hessian1/22','second_product_gradient23over20':'local2-product23/20','second_var_under83over4eta':'original-Vr83/4','reciprocal_norm_under39eta':'original-qenergy39','radius_lower97over100':'critical-radius97/100','sqrt39_under25over4':'sqrt39-25/4','sqrt8eta_under9over500':'sqrt8eta-9/500','energy_under42eta':'original-H42','fixed_energy_entry1over512':'fixed-H-entry',
      'local_basic_positive_rminus':'centered-positive-rminus','local_basic_centered_tau':'centered-radius17/384','local_basic_full_Rouche':'widened-Rouche-whole','local_basic_nine_circle_separation':'widened-Rouche-disjoint','local_basic_positive_Bd':'widened-Bd','local_basic_whole_normal_error_paired':'widened-paired-whole-normal','local_basic_whole_normal_error_individual':'widened-individual-whole-normal','local_basic_initial_tail3over5':'widened-initial-reciprocal3/5','local_basic_radius_rzero':'widened-radius4999/5000','local_basic_Q_coefficient_positive':'widened-Q-coefficient','local_basic_initial_divisor_over1over2500':'widened-firstpower-positive-kappa','local_basic_slope13over5':'widened-basic13/5'}
    for i in range(5):
        mapping['bootstrap_'+str(i)+'_variance']='global-stage'+str(i)+'-variance'
        if i<4:mapping['bootstrap_'+str(i)+'_E2']='global-stage'+str(i)+'-E2'
    extra={'transfer65over64':Q(65,64)-Q(256,255)**2,'first_gap_over1over20':Q(own['whole_newton_majorants'][0]['exact_coercivity'])-Q(1,20),'second_gap_over3over7':Q(own['whole_newton_majorants'][1]['exact_coercivity'])-Q(3,7),'local_basic_cube_delta':ms['widened-delta-W/6']/6,'local_basic_cube_delta0':ms['widened-leading-W/6']/6,'local_basic_initial_divisor_positive':Q(w['kappa'])}
    core.need(set(mapping)|set(extra)==set(native['strict_full_window_margins']),'every native scalar accounted for')
    for key,value in native['strict_full_window_margins'].items():equal('whole-native-scalar-'+key,Q(value),ms[mapping[key]]if key in mapping else extra[key])
    for row in native['whole_skew_controls']:
        k=row['positive_count'];xs=[Q(8-k)]*k+[Q(-k)]*(8-k);v=sum(x*x for x in xs);p3=sum(x**3 for x in xs)
        equal('whole-native-skew-tuple-'+str(k),row['whole_tuple'],list(map(str,xs)));equal('whole-native-skew-variance-'+str(k),row['variance'],str(v));equal('whole-native-skew-p3-'+str(k),row['p3'],str(p3));equal('whole-native-skew-ratio-'+str(k),row['skew_ratio_squared'],str(p3*p3/v**3))
    # Independent primitives reconstruct ALL native Gaussian products,
    # gradients, ordered Hessians, centered tuples and traces after seal.
    z=core.centered;g=z.ga;ga=z.gadd;gm=z.gmul;gs=z.gsc;gp=z.gp;sumg=z.gsum
    def factors(q,a):
        out=[g(1)]
        for x in q:
            nxt=[g(0)for _ in range(len(out)+1)]
            for k,c in enumerate(out):nxt[k]=ga(nxt[k],c);nxt[k+1]=ga(nxt[k+1],gs(gm(c,x),-a))
            out=nxt
        return out
    def encoded(xs):return [[str(v)for v in x]for x in xs]
    def integ(cs,shift,c):return sumg(gs(v,Q(c,k+shift+1))for k,v in enumerate(cs))
    def symmetric(q):
        from itertools import combinations
        def product(q):
            v=g(1)
            for x in q:v=gm(v,x)
            return v
        return [sumg(product(group)for group in combinations(q,k))for k in range(len(q)+1)]
    for row in native['whole_literal_controls']:
        qs=[tuple(map(Q,x))for x in row['whole_q']];a=Q(row['a']);name=row['name'];coeff=factors(qs,a)
        equal('native-entire-product-'+name,row['whole_origin_product_coefficients'],encoded(coeff));equal('native-origin-'+name,row['origin'],encoded([integ(coeff,0,9)])[0])
        gradients=[gs(integ(factors([q for j,q in enumerate(qs)if j!=i],a),1,9),-a)for i in range(8)]
        hessian=[[g(0)if i==j else gs(integ(factors([q for k,q in enumerate(qs)if k not in (i,j)],a),2,9),a*a)for j in range(8)]for i in range(8)]
        equal('native-all-eight-gradients-'+name,row['all_eight_gradients'],encoded(gradients));equal('native-all-64-ordered-Hessian-'+name,row['whole_ordered_hessian'],[encoded(xs)for xs in hessian])
        mean=gs(sumg(qs),Q(1,8));xs=[ga(q,gs(mean,-1))for q in qs];es=symmetric(xs);traces=[sumg(gp(q,k)for q in xs)for k in range(9)]
        equal('native-whole-centered-tuple-'+name,row['whole_centered_tuple'],encoded(xs));equal('native-all-centered-elementary-'+name,row['all_centered_elementary_coefficients'],encoded(es));equal('native-all-centered-traces-'+name,row['all_centered_traces'],encoded(traces))
    report={'agent':'six-reviewer-1','role':'independent mathematical reviewer','method':'post-seal data-only full object comparisons; no author imports; new native Gaussian inputs are late corroboration only','independent_record_sha256':core.digest(own),'native_fixture_byte_sha256':hashlib.sha256(raw).hexdigest(),'complete_checks':checks,'check_count':len(checks),'all65_native_scalar_values':True,'all15_full_sector_polynomials_and_integrals':True,'all_whole_polar_and_majorant_streams':True,'all7_full_Gaussian_objects':True,'all_sealed_source_original_draft_record_bytes_unchanged':True,'actual_disk_feasibility_of_controls_asserted':False}
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='complete_checks'},sort_keys=True))
if __name__=='__main__':main()
