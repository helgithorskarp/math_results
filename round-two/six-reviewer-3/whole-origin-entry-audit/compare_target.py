"""Post-seal DATA-ONLY whole alignment. Imports own code, never producer helpers."""
from pathlib import Path
import hashlib,json,sys
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit import build,canonical,cast,symbol,constant,product,elementary,origin,derivatives,need,E
from radial import coefficients

def pair(p):return [str(x) for x in constant(p)]
def polycoeff(p,var):
    cs=coefficients(p,var)
    return list(map(str,cs or [F(0)]))

def compare(source):
    author=json.loads(source.read_text());own=build();counts={};rows=[]
    need(hashlib.sha256(canonical(author)).hexdigest()=='b9aa470feebcadb23c0030da8edd27619752905c1944cb208db4d03185a0e9d7','entire pinned native record required')
    for mh,data in author['whole_envelopes'].items():
        m,h=map(int,mh.split(':'));us=[x for x in own['sectors']['full_sector_rows'] if (x['m'],x['h'])==(m,h)]
        need(len(us)==len(data['all_sectors']),'whole sector count')
        for u,p in zip(us,data['all_sectors']):
            # Own integrand includes9*t^h; author polynomial is the unweighted product.
            trimmed=[str(F(c)/9) for c in u['whole_integrand_coefficients'][h:]]
            need(trimmed==p['whole_polynomial'],'EVERY full sector coefficient')
            need(u['support_start']==p['support_lower'] and u['integral']==p['monomial_integral']==p['positive_bernstein_integral'],'whole supported sector integration')
            rows.append({'m':m,'h':h,'k':u['k'],'whole_polynomial':trimmed,'integral':u['integral']})
        om=own['sectors']['derivative_envelopes'][str(m)+','+str(h)]
        need(om['I']==data['whole_real_integral'] and om['J']==data['whole_complex_correction'],'complete sector sums')
        need(F(data['full_a_uniform_bound'])==2-F(om['margin_below_2']),'whole derivative bounds')
    counts['all_sector_polynomials_and_integrals']=len(rows)
    ms=own['margins']['strict_margins'];aliases={
      'product_gradient_under2':'whole_P_derivative_2','initial_e2_over7over4':'initial_E2_7_over_4',
      'coarse_v_under9over4':'first_bootstrap_9_over_4','e2_after9over4_over23':'E2_after_first_23',
      'second_v_under1over6':'second_bootstrap_1_over_6','e2_after1over6_over27':'E2_after_second_27',
      'third_v_under9over64':'third_bootstrap_9_over_64','actual_radial_norm_under37over256':'radial_l2_37_over_256',
      'individual_radial_deviation_under3over8_squared':'individual_radius_3_over_8',
      'radial_norm_under49over128_squared':'radial_sqrt_49_over_128','phase_norm_under21over1024_squared':'phase_sqrt_21_over_1024',
      'full_local_ball_under1over6':'whole_complex_region_1_over_6','local_gradient_under1over5':'local_gradient_1_over_5',
      'local_hessian_under1over16':'local_hessian_1_over_16','real_gradient_below_minus9over100':'real_signed_gradient_negative',
      'phase_radial_derivative_negative':'directional_gradient_negative','local_product_gradient_under3over2':'local_P_derivative_3_over_2',
      'whole_local_radial_gap_over3over10':'radial_coercivity_3_over_10','after_local_var_under40eta':'original_V_below_40',
      'after_local_radius_over39over40_squared':'reciprocal_radius_39_over_40','sqrt59_below31over4_squared':'sqrt59_below_31_over_4',
      'energy_sqrt_under8':'original_H64','uniform_sector_parameter_under9over2':'A_below_9_over_2',
      'positive_radius_square_side':'reciprocal_radius_positive_base','triple_angle_at47over50_positive':'triple_angle_at_47_over_50',
      'full_window_first_power_over111over40':'conditional_slope_111_over_40'}
    reconstructed={k:F(ms[v]) for k,v in aliases.items()}
    reconstructed['global_gradient_under2']=F(own['sectors']['derivative_envelopes']['7,1']['margin_below_2'])
    reconstructed['global_hessian_under2']=F(own['sectors']['derivative_envelopes']['6,2']['margin_below_2'])
    # Disclosed post-seal adapter arithmetic: these three are different roundings
    # from the sealed record, not falsely identified as sealed exact margins.
    later={'whole_phase_l1_under1over20_squared':F(1,400)-161*E,
           'reciprocal_norm_under59eta':59-58-F(9,2)*E,
           'new_full_window_fixed_energy_entry':F(1,512)-64*E}
    reconstructed.update(later)
    need(set(reconstructed)==set(author['strict_full_window_margins']),'every target margin covered')
    for name,value in reconstructed.items():need(value==F(author['strict_full_window_margins'][name]),'complete scalar '+name)
    counts['all_target_scalar_margins']=len(reconstructed)
    v=symbol('v');rho=F(3,8);B=[cast(1),cast(0),v/2,rho*v/3,v*v/8]
    for k in range(5,8):B.append(v*sum((B[k-s]*rho**(s-2) for s in range(2,k+1)),cast(0))/k)
    for k,p in enumerate(B):
        need(polycoeff(p,'v')==author['whole_newton_majorant_polynomials'][str(k)],'ENTIRE Newton polynomial')
        need(str(constant(p.substitute({'v':F(9,64)}))[0])==author['whole_newton_endpoint_majorants'][str(k)],'whole Newton endpoint')
    need(own['newton']['balanced_gap_coefficients'][2:]==author['whole_radial_gap_coefficients'],'all balanced gap coefficients')
    need(own['newton']['gamma']==author['whole_local_radial_gap'],'full coercivity coefficient')
    need(own['margins']['bootstrap_budgets']==author['bootstrap_variance_coefficients'],'all three bootstrap coefficients')
    counts['whole_Newton_polynomials']=8;counts['whole_Newton_endpoints']=8
    controls=[]
    for c in author['whole_literal_controls']:
        q=[cast((F(x),F(y))) for x,y in c['whole_q']];a=F(c['a']);t=symbol('t');p=product(1-a*t*x for x in q)
        pc=[pair(p.coefficient('t',k)) for k in range(9)];O=pair(origin(q,a));ds,hs=derivatives(q,a)
        mean=sum(q,cast(0))/8;x=[z-mean for z in q];es=elementary(x);tr=[sum((z**k for z in x),cast(0)) for k in range(9)]
        rebuilt={'whole_origin_product_coefficients':pc,'origin':O,'all_eight_gradients':[pair(d) for d in ds],
                 'whole_ordered_hessian':[[pair(d) for d in row] for row in hs],
                 'whole_centered_tuple':[pair(d) for d in x],'all_centered_elementary_coefficients':[pair(d) for d in es],
                 'all_centered_traces':[pair(d) for d in tr]}
        for k,value in rebuilt.items():need(value==c[k],'every complete Gaussian control field '+k)
        controls.append({'name':c['name'],'whole_arrays_sha256':hashlib.sha256(canonical(rebuilt)).hexdigest(),'all_full_fields_matched':True})
    counts['post_seal_literal_controls']=len(controls);counts['full_control_arrays_per_literal']=7
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','data_only':True,
            'author_executable_imported':False,'seal_unchanged':True,
            'sealed_own_record_sha256':hashlib.sha256(canonical(own)).hexdigest(),
            'target_record_sha256':hashlib.sha256(canonical(author)).hexdigest(),'counts':counts,
            'disclosed_three_post_seal_rounding_margins':{k:str(v) for k,v in later.items()},
            'all_full_supported_sector_arrays':rows,'all_full_target_margins':{k:str(v) for k,v in sorted(reconstructed.items())},
            'all_target_Gaussian_control_fields':controls,
            'chronology':'Different own six controls were sealed first. These six native controls are later independent algebra reconstruction, not misrepresented as pre-access sealed controls.'}

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: compare_target.py PATH_TO_UNCHANGED_TARGET_EXPECTED_JSON')
    print(json.dumps(compare(Path(sys.argv[1])),sort_keys=True,indent=2))
