"""LATE entire typed native-record correspondence, importing NO native code.

Run only after the independent primary seal. The native phase map uses B,
whereas primary independent.py uses x=B-1; a full change of variables is
therefore necessary. This is correspondence, not a second primary proof.
"""
from pathlib import Path
import argparse
import json
from independent import Q, reconstruct, stringify, need, canon, digest, coeffs_gaussian


def exact(left, right, path='record'):
    need(type(left) is type(right), 'type mismatch '+path)
    if isinstance(left,dict):
        need(left.keys()==right.keys(), 'key mismatch '+path)
        for k in left:
            exact(left[k],right[k],path+'.'+k)
    elif isinstance(left,list):
        need(len(left)==len(right), 'length mismatch '+path)
        for j,(a,b) in enumerate(zip(left,right)):
            exact(a,b,path+f'[{j}]')
    else:
        need(left==right, 'value mismatch '+path)


def build():
    p=reconstruct()
    coefficients={
        'shifted':[{'k':k,'complete_a_coefficients':[[n,str(p['general_a'][f'{k},{n}'])]for n in range(k,9)],
                    'two_routes_equal':True,'at_a1':str(p['shift'][str(k)])}for k in range(9)],
        'shifted_coefficient_count':45,
        'mixed':[{'k':k,'remaining':8-k,'all_majorant_coefficients':[str(p['majorants'][f'{k},{j}'])for j in range(9-k)]}for k in range(1,9)],
        'mixed_coefficient_count':36,'Hessian_center':'1/28','mean_square_coefficient':'1/56',
    }
    def margin(v,closed=False):
        need(v>=0 if closed else v>0,'late margin')
        return {'value':str(v),'closed':closed,'passes':True}
    classes=[]
    for name,t in zip(('broad','fine'),p['tables'][:2]):
        r,d=t['rho'],t['delta']
        margins={'RMS_order'+k:margin(v,k=='4')for k,v in t['rms_margins'].items()}
        margins.update({'negative_gradient':margin(t['g']),'negative_imaginary_energy':margin(t['c']),
                        'imaginary_energy_floor':margin(t['sminus']),'complete_coercivity_gap':margin(t['gap'])})
        classes.append({'name':name,'radial_norm_cap':str(r),'phase_cap':str(d),'real_path_norm_cap':str(r+d),
                        'RMS_scales':[str(t['scales'][str(k)])for k in (1,2,4,6)],
                        'target_lambda':str(t['lambda']),'negative_gradient':str(t['g']),
                        'Hessian_variation':str(t['h']),'negative_imaginary_energy':str(t['c']),
                        'D4':str(t['D4']),'D6':str(t['D6']),
                        'S_over_Delta_bounds':[str(t['sminus']),str(t['splus'])],
                        'all_even_tail_per_Delta':str(t['tail']),'full_coercivity':str(t['A']),'margins':margins})
    a=p['actual'];e=Q(1,12000)
    actual={'eta_cap':str(e),'amin':str(a['amin']),'fixed_H_cap':'1/320','fixed_H_root_bound':'7/125',
            'broad_divisor':str(a['f0']),'LC_centered_radius':'1/50','LC_tstar':str(Q(13,15)*e),
            'LC_H_coefficient':str(a['h1']),'fine_divisor':str(a['f1']),
            'imaginary_sum_coefficient':str(a['Yfactor']),
            'margins':{
                'entry_H37_below_fixed_h':margin(Q(1,320)-37*e),
                'actual_fixedH_root_bound':margin(a['broad_root_margin']),
                'actual_fixedH_divisor':margin(a['f0']),
                'actual_broad_norm_class':margin(a['broad_rms_margin']),
                'actual_phase_class':margin(a['phase_margin']),
                'LC_centered_radius':margin(a['zero_sum_radius_margin']),
                'LC_reciprocal_divisor':margin(a['f1']),
                'actual_fine_norm_class':margin(a['fine_rms_margin']),
                'actual_imaginary_sum8':margin(a['imaginary_sum_margin']),
            }}
    scalar={'classes':classes,'actual':actual,'margin_count':25,'strict_margin_count':23,'closed_margin_count':2}
    # Translate EVERY monomial x_X*y_I to product(B_j-1)*y_I.
    bmap={}
    for key,c in p['phase'].items():
        X,I=map(int,key.split(','))
        subset=X
        while True:
            v=c*(-1)**((X^subset).bit_count())
            bmap[(subset,I)]=bmap.get((subset,I),Q(0))+v
            if subset==0:
                break
            subset=(subset-1)&X
    bmap={k:v for k,v in bmap.items()if v}
    need(len(bmap)==3025,'full unshifted phase census')
    for (B,I),v in bmap.items():
        n=B.bit_count()+I.bit_count()
        need(v==Q(9*(-1)**(n+I.bit_count()//2+1),n+1),'every translated B coefficient')
    w=(Q(999999,1000001),Q(2000,1000001))
    need(w[0]**2+w[1]**2==1,'author literal unit input')
    controls=[]
    for name,R,signs in [
        ('total_real_collision',[Q(1)]*8,[0]*8),
        ('coherent_imaginary_mean',[Q(1)]*8,[1]*8),
        ('balanced_four_plus_four',[Q(1)]*8,[1]*4+[-1]*4),
        ('nonconjugate_five_plus_three',[1+Q((-1)**j,2000)for j in range(8)],[1]*5+[-1]*3),
        ('closed_fine_radial_zero_phase',[1+Q(1,40)]+[Q(1)]*7,[0]*8),
        ('closed_broad_radial_zero_phase',[1+Q(1,16)]+[Q(1)]*7,[0]*8),
    ]:
        z=[(r,Q(0))if s==0 else(r*w[0],s*r*w[1])for r,s in zip(R,signs)]
        coeff,O=coeffs_gaussian(z)
        radial,OR=coeffs_gaussian([(r,Q(0))for r in R])
        delta=sum(r-x for r,(x,y)in zip(R,z));Y=sum(y for x,y in z)
        rho2=sum((r-1)**2 for r in R);loss=OR[0]-O[0]
        active=[]
        for r,lam in [(Q(1,16),Q(1,8)),(Q(1,40),Q(7,48))]:
            if rho2<=r*r and delta<=Q(1,1000):
                gap=-lam*delta+Y*Y/Q(56)-loss
                need(gap>=0 and (delta==0 or gap>0),'all complete native literal comparisons')
                active.append({'rho':str(r),'complete_bound_margin':str(gap)})
        controls.append(stringify({'name':name,'radii':R,'z':z,'whole_complex_t_coefficients':coeff,
                                    'whole_radial_t_coefficients':radial,'complex_origin_value':O,
                                    'radial_origin_value':OR,'Delta':delta,'Y':Y,'radial_norm_squared':rho2,
                                    'phase_loss':loss,'active_class_margins':active,'two_full_product_routes_equal':True}))
    algebra={'full_even_identity_common_map':[[B,I,str(v)]for (B,I),v in sorted(bmap.items())],
             'map_encoding':'[real_B_mask, imaginary_y_mask, exact_coefficient]; disjoint eight-bit masks',
             'two_routes_equal':True,'common_map_terms':3025,'terms_by_even_order':p['phase_order_counts'],
             'full_balanced_s_d_coefficients':[[j,k,str(v)]for (j,k),v in sorted((tuple(map(int,key.split(','))),v)for key,v in p['paired_product'].items())],
             'full_integrated_balanced_family':[[j,str(v)]for j,v in enumerate(p['balanced_integral'])],
             'limiting_envelope_lambda_upper_bound':'9/56','literal_controls':controls,
             'controls_scope':'Algebraic envelope tuples only; no actual original-disk feasibility claim'}
    # Metadata is a typed correspondence check, not adoption of its review-status wording.
    return {'schema':1,'agent':'six-sendov-1','role':'researcher',
            'proof_status':'Complete ordinary author lemma, unformalized and independently unreviewed; same-author exact corroboration',
            'domain':'Every finite complex eight-tuple: radial norm<=1/16 or1/40, Delta<=1/1000; actual corollaries ONLY after9930 and9974 on0<eta<=1/12000',
            'coefficients':coefficients,'scalars':scalar,'algebra':algebra}


def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate key')
        out[k]=v
    return out


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('record',type=Path)
    args=ap.parse_args()
    record=json.loads(args.record.read_bytes(),object_pairs_hook=unique)
    fresh=build()
    exact(fresh,record)
    print(canon({'scope':'LATE entire recursively typed correspondence; no native code imported',
                 'whole_native_record_sha256':digest(fresh),'entire_typed_record_match':True,
                 'shifted_coefficients':45,'mixed_majorants':36,'original_margins':25,
                 'all_translated_phase_coefficients':3025,'entire_literal_controls':6,
                 'balanced_bivariate_coefficients':25,'balanced_integral_coefficients':5}))
