#!/usr/bin/env python3
"""Require every exact leaf, pinned inputs, expected signs and author controls."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
def require(b,s):
    if not b:raise ValueError(s)
def main(args):
    expected=json.loads((HERE/'expected.json').read_text());config=json.loads((HERE/'configuration.json').read_text());records=[]
    require(hashlib.sha256(Path(args.local).read_bytes()).hexdigest()==expected['local_whole_record_sha256'],'fresh complete local quadrilateral proof')
    for path in args.batches:
        batch=json.loads(Path(path).read_text())
        require(batch['status']=='DECLARED_EXACT_LEAF_RANGE_PASSED','batch must be complete within its declared guard')
        require(batch['forest_sha256']==expected['forest_sha256']and batch['geometry_sha256']==expected['geometry_sha256'],'same freshly checked geometry and complete source forest')
        require(batch['exact_cover_roots']==108 and batch['exact_midpoint_internal_nodes']==config['source_midpoint_count'] and batch['exact_cover_leaves']==config['source_leaf_count'],'same whole exact cover')
        require(batch['start']==len(records)and batch['completed_stop']==batch['requested_stop'],'consecutive declared complete exact batches')
        require(len(batch['exact_leaf_records'])==batch['completed_stop']-batch['start'],'whole declared record range')
        records.extend(batch['exact_leaf_records'])
    require([r['index']for r in records]==list(range(config['source_leaf_count'])),'every exact leaf occurs once, no gap or duplicate')
    require(all(r['kind']=='three_support_stress'and [c['receiver_triangle']for c in r['exact_checks']]==list(range(len(config['receiver_triangle_indices'])))for r in records),'every source leaf covers every receiver triangle')
    checks=[c for r in records for c in r['exact_checks']]
    require(all(c['coefficient_count']==60 and F(c['maximum_upper_coefficient'])<0 and F(c['minimum_positive_vertex_weight'])>0 for c in checks),'all tensor signs and affine weight signs strictly pass')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    summary=dict(leaves=len(records),midpoint_nodes=config['source_midpoint_count'],source_roots=108,coefficient_checks=sum(c['coefficient_count']for c in checks),canonical_leaf_records_sha256=hashlib.sha256(raw).hexdigest(),maximum_upper_coefficient=str(max(F(c['maximum_upper_coefficient'])for c in checks)),minimum_positive_weight=str(min(F(c['minimum_positive_vertex_weight'])for c in checks)))
    require(summary==expected['coefficient_summary'],'whole exact stream matches the compact expected mathematics')
    require(hashlib.sha256(Path(args.controls).read_bytes()).hexdigest()==expected['controls_sha256'],'whole independent author control record passes')
    result=dict(agent='six-rupert-1',role='researcher',status='COMPLETE_OUTER_SOURCE_COVER_EXACTLY_VERIFIED',**summary,geometry_sha256=expected['geometry_sha256'],forest_sha256=expected['forest_sha256'],controls_sha256=expected['controls_sha256'],local_whole_record_sha256=expected['local_whole_record_sha256'],local_dependency='Fresh whole closed quadrilateral34, two complete closed fan triangles and12 physical five-contact duals, Euclidean radius1/51; included local.py/local_certificate.json',scope='All proper source orientations classified on ENTIRE closed receiving quadrilateral34, both full fan triangles, all sides and vertices. Its literal union with cited9558 covers six closed receiving cells and both adjacent facet10/40 seams. Global Rupert property OPEN; author-checked, unformalized and independently unreviewed.')
    out=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    if args.compare:require(out==Path(args.compare).read_bytes(),'normal/optimized whole compact proof records match')
    Path(args.output).write_bytes(out);print(out.decode());print('whole_record_sha256',hashlib.sha256(out).hexdigest())
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('batches',nargs='+');p.add_argument('--controls',required=True);p.add_argument('--local',required=True);p.add_argument('--compare');p.add_argument('--output',required=True);main(p.parse_args())
