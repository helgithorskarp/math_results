#!/usr/bin/env python3
"""Bind every fresh local proof, source address, closed fan and coefficient."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,copy
import expand
HERE=Path(__file__).resolve().parent
def require(b,s):
    if not b:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(args):
    config=json.loads((HERE/'configuration.json').read_text());work=Path(args.work);result={}
    for cell in (19,18,16,33):
        cfg=config['cells'][str(cell)];where=work/str(cell);local=json.loads((where/'local.json').read_text())
        require(local['status']=='EXACT_WHOLE_CLOSED_LOCAL_RIGIDITY_AND_PHYSICAL_GAP_PASSED'and local['cell_id']==cell,'same freshly replayed complete local cell')
        require(local['closed_cell_geometry']==cfg['expected_closed_support_geometry'],'every actual receiver support, tie, side and fan matches its certificate')
        forest=json.loads((where/'forest.json').read_text());records=[]
        require(sha(where/'forest.json')==cfg['expanded_forest_sha256'],'all literal source and receiving inputs')
        for start in range(0,cfg['source_leaves'],1000):
            batch=json.loads((where/f'leaves_{start}.json').read_text());stop=min(start+1000,cfg['source_leaves'])
            require(batch['status']=='DECLARED_EXACT_LEAF_RANGE_PASSED'and batch['start']==start==len(records)and batch['completed_stop']==batch['requested_stop']==stop,'consecutive complete exact source ranges, no timeout gap')
            require(batch['forest_sha256']==cfg['expanded_forest_sha256']and batch['geometry_sha256']==sha(where/'geometry.json'),'fresh geometry and identical entire decoded forest')
            require(batch['exact_cover_roots']==108 and batch['exact_midpoint_internal_nodes']==cfg['source_midpoint_nodes']and batch['exact_cover_leaves']==cfg['source_leaves'],'complete exact source cover')
            records.extend(batch['exact_leaf_records'])
        require([r['index']for r in records]==list(range(cfg['source_leaves'])),'every declared exact leaf occurs once')
        import verify_shell as V
        geometry=json.loads((where/'geometry.json').read_text())
        for r,l in zip(records,forest['leaves']):
            require((r['root'],r['path'],r['kind'])==(l['root'],l['path'],l['kind']),'every actual source address and terminal status')
            stresses=V.receiver_stress_cover(l,geometry)
            require(len(r['exact_checks'])==len(stresses),'all closed receiving products')
            for c,s in zip(r['exact_checks'],stresses):
                for key in ('receiver_triangle','receiver_path','edges','moving_originals','cofactor_orientation'):require(c[key]==s[key],'same selected literal physical stress')
                values=c['coefficients']
                require(c['coefficient_count']==len(values)==60 and all(type(lo)==type(hi)==int and lo<=hi<0 for lo,hi in values),'EVERY outward joint control strictly excludes')
                require(V.raw_hash(values)==c['coefficient_hash']and F(c['minimum_positive_vertex_weight'])>0,'every recomputed coefficient and positive physical stress weight bound')
        checks=[c for r in records for c in r['exact_checks']]
        require(len(checks)==cfg['receiving_stress_pieces']and sum(c['coefficient_count']for c in checks)==cfg['coefficient_checks'],'entire mathematical inventory')
        small=copy.deepcopy(records)
        for r in small:
            for c in r['exact_checks']:del c['coefficients']
        digest=hashlib.sha256((json.dumps(small,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
        require(digest==cfg['reference_stress_records_sha256'],'transparent migration retains EVERY previously verified physical stress record')
        upper=str(max(F(c['maximum_upper_coefficient'])for c in checks));weight=str(min(F(c['minimum_positive_vertex_weight'])for c in checks))
        require(upper==cfg['maximum_upper_coefficient']and weight==cfg['minimum_positive_weight'],'exact outward margins')
        lc=json.loads((where/'local_controls.json').read_text());sc=json.loads((where/'source_controls.json').read_text())
        require(lc['status']=='WHOLE_CLOSED_CELL_INDEPENDENT_AUTHOR_LOCAL_CONTROLS_PASSED'and lc['local_sha256']==sha(where/'local.json'),'same complete independent author local controls')
        require(sc['status']=='WHOLE_CLOSED_CELL_INDEPENDENT_SOURCE_AND_COVER_CONTROLS_PASSED'and sc['local_record_sha256']==sha(where/'local.json')and sc['local_controls_sha256']==sha(where/'local_controls.json'),'same complete independent physical/source cover controls')
        result[str(cell)]=dict(source_roots=108,source_leaves=len(records),source_midpoint_nodes=cfg['source_midpoint_nodes'],receiving_stress_pieces=len(checks),negative_joint_controls=len(checks)*60,maximum_upper_coefficient=upper,minimum_positive_weight=weight,full_coefficient_records_sha256=hashlib.sha256((json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest(),reference_stress_records_sha256=digest,local_sha256=sha(where/'local.json'),geometry_sha256=sha(where/'geometry.json'),local_controls_sha256=sha(where/'local_controls.json'),source_controls_sha256=sha(where/'source_controls.json'),literal_forest_sha256=cfg['expanded_forest_sha256'])
    record=dict(agent='six-rupert-1',role='researcher',status='FOUR_COMPLETE_CLOSED_RECEIVER_REGIONS_ALL_ORIGINAL_SOURCES_VERIFIED',cells=result,total_negative_joint_controls=sum(z['negative_joint_controls']for z in result.values()),fresh_named_geometry_sha256=sha(work/'named_geometry.json'),public_six_cell_dependency='LEMMA9604/0; source9d69be73ed1e121ed53701d6c21843f0fc7c4649',literal_union_cells=[14,28,13,11,20,34,19,18,16,33],scope='Every original proper Q and arbitrary physical translation/scale>=1 is classified on four entire closed receiving polygons; their literal union with cited9604 gives ten closed atlas cells and signed/projective proper-body images. Equality iff Q in actual G,b0,lambda1. Ordinary written bridge unformalized, independently unreviewed; global Rupert property OPEN.')
    raw=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if (HERE/'expected.json').exists():require(record==json.loads((HERE/'expected.json').read_text()),'entire compact expected proof record')
    if args.compare:require(raw==Path(args.compare).read_bytes(),'normal and optimized complete mathematical records agree')
    Path(args.output).write_bytes(raw);print(json.dumps(dict(status=record['status'],controls=record['total_negative_joint_controls'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',required=True);p.add_argument('--output',required=True);p.add_argument('--compare');main(p.parse_args())
