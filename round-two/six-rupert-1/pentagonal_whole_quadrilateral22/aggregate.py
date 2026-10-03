#!/usr/bin/env python3
"""Bind every original support, closed source address, fan and actual control."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
def require(b,s):
    if not b:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(args):
    cfg=json.loads((HERE/'configuration.json').read_text());cell=cfg['cells']['22'];work=Path(args.work)
    local=json.loads((work/'local.json').read_text());cert=json.loads((HERE/'local_certificate.json').read_text())
    require(sha(HERE/'local_certificate.json')==cfg['local_certificate_sha256'],'same whole certificate bytes')
    require(sha(work/'local.json')==cfg['expected_private_local_sha256'],'all migrated actual local interval entries retain verified reference')
    require(local['closed_cell_geometry']==cell['expected_closed_support_geometry'],'all actual support/tie/wall/fan fields')
    require(local['certificate_sha256']==hashlib.sha256(json.dumps(cert,sort_keys=True).encode()).hexdigest(),'complete mathematical certificate content')
    require(local['closed_relative_cayley_euclidean_radius']=='1/41'and local['strict_coordinate_mass_bounds']==['17/2','57/4','43/4']and local['squared_coordinate_closure_upper']=='3127/3362','fresh rational closure')
    domain=json.loads((work/'domain.json').read_text())
    target=json.loads((HERE/'target.json').read_text())
    require(domain['exact_polygon']==cert['polygon']==target['exact_polygon']and domain['exact_facet_signs']==cert['facet_signs']==target['exact_facet_signs'],'same current exact entire receiving cell')
    require(domain['receiver_cell_index']==22 and domain['exact_side_wall_indices']==[[1],[61],[13],[52]]and domain['closed_halfspace_corner_checks']==252 and domain['strict_global_turn_checks']==8,'complete closed domain and true sides')
    require(domain['literal_prior_regions']==12 and domain['signed_receiving_image_cases']==720 and len(domain['image_rejection_side_indices'])==60 and all(len(row)==12 and all(type(v)==int and v>=0 for v in row)for row in domain['image_rejection_side_indices']),'strict rejection of all prior signed/projective images; no chart-zero case')
    supports=json.loads((work/'supports.json').read_text())
    require(supports['all_original_edges']==150 and supports['genuine_phase_horizon_edges']==26 and supports['endpoint_rows']==52 and supports['closed_corner_all_original_support_comparisons']==9568 and supports['exact_closed_support_ties']==271 and supports['exact_offendpoint_grazing_ties']==63,'ALL current original horizon supports, BOTH endpoints, original grazing comparisons')
    require(supports['target_sha256']==cfg['target_sha256'] and supports['named_model_fresh_this_mode_sha256']==sha(work/'named_geometry.json'),'fresh all-horizon record bound to same current domain/body')
    rows={tuple(row['contact'])for row in supports['rows']}
    require(all(tuple(c)in rows for d in cert['duals']for c in d['contacts']),'all selected local contacts are literal current genuine phase-horizon endpoints')
    require(domain['directly_reconstructed_all_sixty_phase_halfspaces'] is True and len(domain['clipping_polygon_sizes'])==60,'direct reconstruction by every actual phase halfspace')
    positive=0;positive_min=None
    require([(d['receiver_path'],d['coordinate'],d['sign'])for d in local['duals']]==[(str(p),j,s)for p in range(2)for j in range(3)for s in(-1,1)],'all twelve signed actual5-wrench duals')
    for d in local['duals']:
        require(len(d['triangle_records'])==1,'one whole fan for each dual')
        z=d['triangle_records'][0];den=z['denominator_degree5_integer_intervals'];nums=z['cramer_degree5_integer_intervals']
        require(len(den)==21 and len(nums)==5 and all(len(row)==21 for row in nums),'every actual common-degree5 entry')
        for lo,hi in den+[v for row in nums for v in row]:
            require(type(lo)==type(hi)==int and 0<lo<=hi,'actual strict positive local controls')
            positive+=1;positive_min=lo if positive_min is None else min(lo,positive_min)
    require(positive==1512,'complete positive control count')
    forest=json.loads((work/'forest.json').read_text());geometry=json.loads((work/'geometry.json').read_text());source=json.loads((work/'source.json').read_text())
    require(sha(work/'forest.json')==cell['expanded_forest_sha256']==geometry['forest_sha256'],'entire decoded closed forest')
    require(geometry['source_ratio']==forest['ratio']=='1/17'and geometry['local_whole_record_sha256']==sha(work/'local.json'),'same new local/core source link')
    require(geometry['complete_named_geometry_record']==local['complete_named_geometry_record']and geometry['complete_source_quotient_record']==source,'complete named and proper-source reconstructions linked')
    require(geometry['receiver_polygon']==cert['polygon']and geometry['receiver_triangle_indices']==[[0,1,2],[0,2,3]],'whole literal closed quadrilateral')
    require(max(l['depth']for l in forest['leaves'])==9,'entire actual source depth inventory')
    records=[]
    for start in range(0,cell['source_leaves'],200):
        b=json.loads((work/f'leaves_{start}.json').read_text());stop=min(start+200,cell['source_leaves'])
        require(b['status']=='DECLARED_EXACT_LEAF_RANGE_PASSED'and b['start']==start==len(records)and b['requested_stop']==b['completed_stop']==stop,'consecutive complete leaf ranges, no timeout gap')
        require(b['geometry_sha256']==sha(work/'geometry.json')and b['forest_sha256']==cell['expanded_forest_sha256'],'current exact geometry/forest input')
        require(b['exact_cover_roots']==108 and b['exact_midpoint_internal_nodes']==1360 and b['exact_cover_leaves']==1468,'complete exact source-root/tree inventory')
        records.extend(b['exact_leaf_records'])
    require([r['index']for r in records]==list(range(1468))and len(records)==len(forest['leaves']),'every actual source leaf exactly once')
    import verify_shell as V
    products=0;negative=0;upper=None;weight=None
    for r,l in zip(records,forest['leaves']):
        require((r['root'],r['path'],r['kind'])==(l['root'],l['path'],l['kind']),'literal complete source addresses')
        stresses=V.receiver_stress_cover(l,geometry);require(len(stresses)==len(r['exact_checks'])==2,'both entire closed receiving/source products')
        for c,s in zip(r['exact_checks'],stresses):
            for k in ('receiver_triangle','receiver_path','edges','moving_originals','cofactor_orientation'):require(c[k]==s[k],'all actual physical selected stress labels')
            values=c['coefficient_integer_intervals'];require(c['coefficient_count']==len(values)==60 and all(type(lo)==type(hi)==int and lo<=hi<0 for lo,hi in values),'EVERY actual outward tensor control strictly negative')
            require(V.raw_hash(values)==c['coefficient_hash']and F(c['minimum_positive_vertex_weight'])>0,'every actual entry and positive physical corner-weight bound')
            actual_hi=max(F(hi,V.E.SCALE)for lo,hi in values)
            require(actual_hi==F(c['maximum_upper_coefficient']),'actual upper endpoint reconstructed from every current interval')
            products+=1;negative+=60;hi=actual_hi;w=F(c['minimum_positive_vertex_weight']);upper=hi if upper is None else max(upper,hi);weight=w if weight is None else min(weight,w)
    ref=hashlib.sha256((json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
    require(ref==cell['reference_full_actual_leaf_records_sha256'],'ALL migrated actual interval entries retain the complete verified source records')
    require(products==2936 and negative==176160 and str(upper)==cell['maximum_upper_coefficient']and str(weight)==cell['minimum_positive_weight'],'all exact stress counts and margins')
    lc=json.loads((work/'local_controls.json').read_text());sc=json.loads((work/'source_controls.json').read_text())
    require(lc['status']=='WHOLE_CLOSED_QUADRILATERAL22_INDEPENDENT_AUTHOR_LOCAL_CONTROLS_PASSED'and lc['local_sha256']==sha(work/'local.json')and len(lc['damaged_certificate_rejections'])==14,'complete current local author controls')
    require(sc['status']=='WHOLE_QUADRILATERAL22_INDEPENDENT_SOURCE_AND_COVER_CONTROLS_PASSED'and sc['local_record_sha256']==sha(work/'local.json')and sc['local_controls_sha256']==sha(work/'local_controls.json')and len(sc['damages_rejected'])==22,'complete current source/physical/closed-cover author controls')
    require(source['proper_body_count']==60 and source['vertices_count']==20 and source['all_proper_signed_vertex_comparisons']==2400 and geometry['source_face_global_turn_checks']==180,'complete proper-source quotient and convex faces')
    require(geometry['source_ratio']=='1/17'and geometry['strict_core_margin_phi_pair']==['-65270/485809','24/289'],'fresh closed core inclusion')
    require(geometry['actual_original_support_comparisons']==7360 and local['closed_cell_geometry']['exact_closed_support_ties']==202 and local['closed_cell_geometry']['exact_offendpoint_grazing_ties']==42,'every current original support and retained grazing')
    record=dict(agent='six-rupert-1',role='researcher',status='WHOLE_CLOSED_QUADRILATERAL22_ALL_ORIGINAL_SOURCES_AND_PHYSICAL_TRANSLATION_SCALE_VERIFIED',
      source_roots=108,source_leaves=1468,source_midpoint_nodes=1360,source_maximum_depth=9,receiving_stress_products=products,positive_degree5_controls=positive,negative_joint_controls=negative,total_exact_coefficient_controls=positive+negative,
      maximum_upper_joint_control=str(upper),minimum_positive_cofactor_corner_weight=str(weight),minimum_positive_local_degree5_control=str(F(positive_min,10**24)),
      all_original_horizon_edges=26,all_original_endpoint_rows=52,all_original_support_comparisons=9568,all_exact_support_ties=271,all_offendpoint_grazing_ties=63,all_original_horizon_supports_sha256=sha(work/'supports.json'),whole_local_record_sha256=sha(work/'local.json'),whole_domain_nonredundancy_cases=720,strict_core_margin_phi_pair=geometry['strict_core_margin_phi_pair'],fresh_named_geometry_sha256=sha(work/'named_geometry.json'),literal_forest_sha256=sha(work/'forest.json'),source_geometry_sha256=sha(work/'geometry.json'),source_quotient_sha256=sha(work/'source.json'),whole_domain_nonredundancy_sha256=sha(work/'domain.json'),full_actual_source_leaf_records_sha256=ref,whole_source_batch_sha256={str(i):sha(work/f'leaves_{i}.json')for i in range(0,cell['source_leaves'],200)},independent_local_author_controls_sha256=sha(work/'local_controls.json'),independent_source_author_controls_sha256=sha(work/'source_controls.json'),
      local_collar='1/41',strict_rational_coordinate_masses=['17/2','57/4','43/4'],squared_closure_upper='3127/3362',physical_gap='1/1200',source_core_ratio='1/17',all_original_translations_and_scales_retained=True,all_original_source_halfturns_retained=True,centrality_or_improper_source_fold_used=False,equality_inventory_concluded_after_complete_source_proof=True,
      public_old_fifteen_dependency=cfg['public_fifteen_cell_dependency'],literal_union_cells=[14,28,13,11,20,34,19,18,16,33,32,31,29,30,15,22],scope='Every original proper Q and arbitrary physical b/lambda>=1 is classified on the ENTIRE new closed quadrilateral22, equality IFF Q in actualG60,b0,lambda1. Explicit10093 old-fifteen dependency gives literal16-cell union and signed/projective proper-body images, no hull/area/whole37atlas/global claim. Ordinary author-checked bridge, unformalized and independently unreviewed; global Rupert property OPEN.')
    raw=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if(HERE/'expected.json').exists():require(record==json.loads((HERE/'expected.json').read_text()),'entire compact expected mathematical record')
    if args.compare:require(raw==Path(args.compare).read_bytes(),'whole normal/O aggregate agrees byte for byte')
    Path(args.output).write_bytes(raw);print(json.dumps(dict(status=record['status'],controls=positive+negative,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--output',required=True);p.add_argument('--compare');main(p.parse_args())
