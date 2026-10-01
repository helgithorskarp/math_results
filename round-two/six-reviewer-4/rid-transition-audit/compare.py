"""Optional partial mathematical-entry comparison; never author code execution."""
import argparse
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import re
import check as audit

HERE=Path(__file__).resolve().parent

def compare(native, own, b):
    count=0
    def rational(x):
        audit.require(type(x) is str,'rational must be a string')
        f=Fraction(x);return b.q(f.numerator,f.denominator)
    def nfield(x):
        audit.require(type(x) is list and len(x)==2,'phi field encoding')
        return rational(x[0])+b.P*rational(x[1])
    def ofield(x):
        audit.require(type(x) is str,'own exact field encoding')
        m=re.fullmatch(r'\(([^)]+)\)\+\(([^)]+)\)sqrt5',x)
        return rational(m[1])+rational(m[2])*(2*b.P-1) if m else rational(x)
    def eq(x,y,label):
        nonlocal count
        audit.require(x==y,label);count+=1
    def vectors(native_vectors,own_vectors,label):
        a=sorted(tuple(nfield(x) for x in v) for v in native_vectors)
        z=sorted(tuple(ofield(x) for x in v) for v in own_vectors)
        audit.require(len(a)==len(z) and len(set(a))==len(a),label+' vector inventory')
        for v,w in zip(a,z,strict=True):
            audit.require(len(v)==len(w)==3,label+' vector dimension')
            for x,y in zip(v,w,strict=True):eq(x,y,label)
    families=native['families'];audit.require([f['major_axis'] for f in families]==['x','y'],'native family inventory')
    tangent=native['physical_tangent_structure']
    vectors(tangent['tangent_original_vectors'],own['tangent']['vectors'],'all six tangent originals')
    audit.require(len(tangent['positive_xy_transitions'])==2,'kink inventory')
    for x,y in zip(tangent['positive_xy_transitions'],own['tangent']['x_transitions'],strict=True):eq(nfield(x),ofield(y),'actual kink')
    pieces=[p for f in tangent['families'] for p in f['piece_coefficients']]
    audit.require(len(pieces)==3,'area-piece inventory')
    for p,o in zip(pieces,own['tangent']['pieces'],strict=True):
        eq(nfield(p[0]),ofield(o[1]),'physical H');eq(nfield(p[1]),ofield(o[2]),'physical K')
    for j in (0,1):
        f=families[j];w=own['actual_widths'][j];a=own['sharper_area_pieces'][0 if j==0 else 2]
        for nk,ok in [('maximum_width_parameter','maximum_parameter'),('maximum_squared_directional_width','squared_width'),('squared_width_filter_margin','filter_margin')]:eq(nfield(f[nk]),ofield(w[ok]),'width '+nk)
        eq(nfield(f['receiving_corner_squared_area']),ofield(a['physical_receiver_corner_squared_area']),'actual receiving area')
        eq(nfield(f['paired_radius_ratio']),ofield(a['rho']),'paired radius ratio')
        eq(nfield(tangent['families'][j]['minimum_nonzero_facet_sign_corner_margin']),min(map(ofield,own['tangent']['affine_signs'][j]['all75_margins'])),'triangle minimum affine sign')
    eq(nfield(families[1]['y_major_cutoff']['positive_squared_cutoff_margin']),ofield(own['sharper_area_pieces'][2]['positive_y_source_cutoff_gate']),'positive y-major cutoff')
    m=native['full_frame_matching'];om=own['actual_matching']
    eq(nfield(m['actual_target_minor_row_face_margin']),ofield(om['actual_face_margin']),'actual exposed face margin')
    eq(rational(m['initial_roll_error_upper']),ofield(om['roll_upper']),'full roll upper')
    boot=native['actual_minor_row_bootstrap'];ob=own['minor_bootstrap_and_unsquared_branch']
    eq(rational(boot['actual_minor_row_initial_factor']),ofield(ob['initial']),'first minor factor')
    audit.require(len(boot['subsequent_factors'])==2,'minor stage inventory')
    for x,k in zip(boot['subsequent_factors'],['first','second'],strict=True):eq(rational(x),ofield(ob[k]),'actual subsequent minor factor')
    for x,y in zip(boot['wrong_branch_positive_margins'],ob['both_wrong_branch_margins'],strict=True):eq(nfield(x),ofield(y),'unsquared wrong-branch margin')
    geom=native['original_geometry'];P=b.P;Z=b.Z
    eq(nfield(geom['common_squared_radius']),7+8*P,'actual common radius')
    E=[(x*P**2,y*(2+P),Z) for x in (-1,1) for y in (-1,1)]
    vectors(geom['equatorial_originals'],[[str(x) for x in v] for v in E],'all four E labels')
    audit.require([f['axis'] for f in geom['minor_row_faces']]==[0,1],'actual minor-face inventory')
    for j in (0,1):vectors(geom['minor_row_faces'][j]['actual_originals'],om['actual_four_point_faces'][j],'all actual minor-face originals')
    e=native['new_receiving_example'];oe=own['expanded_domain_example']
    for nk,ok in [('physical_squared_area','physical_squared_area'),('old_single_x_chamber_formula_strict_shortfall','old_formula_raw_shortfall'),('complete_mirror_maximum_positive_squared_cosine','mirror_cosine_squared'),('minimum_original_height_squared','minimum_original_height_squared')]:eq(nfield(e[nk]),ofield(oe[ok]),'example '+nk)
    vectors([e['receiving_raw_normal']],[[str(b.q(1,20)),str(b.q(1,40)),str(b.S(1))]],'physical seed')
    for name in ('twofold','fivefold','endpoint'):
        eq(nfield(e['outside_specified_prior_caps'][name]['maximum_positive_squared_cosine']),ofield(oe['specified_caps'][name]['max_positive_cosine_squared']),'named cap '+name)
    audit.require(type(e['all_proper_prior_wedge_members']) is int and e['all_proper_prior_wedge_members']==0 and not oe['old_W_members'],'all proper old-W nonmembership')
    audit.require(type(e['original_shadow_hull_corners']) is int and e['original_shadow_hull_corners']==oe['corners']==16,'physical hull corner count')
    return {'shared_exact_field_values_compared':count,'all_tangent_and_equatorial_minor_face_originals_match':True,'all_three_physical_piece_coefficients_match':True,'both_family_widths_areas_ratios_and_new_bootstrap_match':True,'entire_example_and_named_cover_fields_match':True,'trust':'Partial decoded mathematical-entry comparison only. Independent checker computes its whole record separately; author full record replay is separately reported.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('native',type=Path);p.add_argument('--controls',action='store_true');args=p.parse_args()
    native=json.loads(args.native.read_text());own=json.loads((HERE/'expected.json').read_text());b,pin=audit.load_geometry()
    result=compare(native,own,b)
    if args.controls:
        cases=[]
        def damaged(name,fn):
            d=deepcopy(native);fn(d);cases.append((name,d))
        damaged('missing_area_piece',lambda d:d['physical_tangent_structure']['families'][0]['piece_coefficients'].pop())
        damaged('duplicate_family',lambda d:d['families'].__setitem__(1,deepcopy(d['families'][0])))
        damaged('wrong_kink',lambda d:d['physical_tangent_structure']['positive_xy_transitions'].__setitem__(0,['1/2','0']))
        damaged('altered_width',lambda d:d['families'][0].__setitem__('maximum_squared_directional_width',['0','0']))
        damaged('boolean_minor_factor',lambda d:d['actual_minor_row_bootstrap'].__setitem__('actual_minor_row_initial_factor',True))
        damaged('wrong_mirror_cosine',lambda d:d['new_receiving_example'].__setitem__('complete_mirror_maximum_positive_squared_cosine',['1','0']))
        damaged('missing_actual_E',lambda d:d['original_geometry']['equatorial_originals'].pop())
        damaged('altered_actual_face_original',lambda d:d['original_geometry']['minor_row_faces'][0]['actual_originals'][0].__setitem__(0,['0','0']))
        rejected=[]
        for name,d in cases:
            try:compare(d,own,b)
            except (ValueError,KeyError,TypeError):rejected.append(name)
            else:raise ValueError('damaged comparison input accepted:'+name)
        result['damaged_records_rejected']=rejected
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
