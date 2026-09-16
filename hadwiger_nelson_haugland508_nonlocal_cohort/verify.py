"""Positive certificate checker; no solver or producer imports."""
from pathlib import Path
import argparse
import importlib.util
import json
from hashlib import sha256
from collections import deque
import model as m

def max_capped_ball(adj):
    maximum = 0
    for root in range(m.N):
        seen = {root}; layer = {root}; last = 1
        while layer:
            new = set().union(*(adj[v] for v in layer))-seen
            seen.update(new)
            if len(seen)>508:
                break
            last = len(seen); layer = new
        maximum = max(maximum,last)
    return maximum

def geometry(supports, source_edges):
    path = m.HERE.parent/'hadwiger_nelson_haugland2131_strict_edges/independent_check.py'
    m.require(sha256(path.read_bytes()).hexdigest()=='5e7f356bb66237a7f8f46ac01ca4a29a3bc23fc382296ec476fd09d6cdde8916','pinned geometry code')
    spec = importlib.util.spec_from_file_location('haugland_exact_geometry',path)
    g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
    payload = json.loads((m.HERE.parent/'hadwiger_nelson_haugland2131_exact_reproduction/graph.json').read_text())
    sqrt3,vectors = g.field_constants()
    g1 = g.build_g1(payload['paths'],sqrt3,vectors)
    g2 = g.build_g2(g1,sqrt3)
    g3 = g.build_g3(g2,sqrt3)
    m.require((len(g1),len(g2),len(g3))==(740,1066,2131),'physical source counts')
    m.require(len(set(g3))==2131,'distinct parent coordinates')
    m.require(g.coordinate_hash(g3,True)=='fcdcba9dee3c2e0ea6044e17cb5f32bc9c989b8155d8c377863d41d357f72cab','coordinate stream')
    # Left half lies in Q(zeta84); every noncommon right point has a sqrt5 part.
    m.require(all(x[1]==g.ZERO and y[1]==g.ZERO for x,y in g3[:1066]),'left base field')
    m.require(all(x[1]!=g.ZERO or y[1]!=g.ZERO for x,y in g3[1066:]),'right outside base field')
    union = sorted(set().union(*map(set,supports)))
    points = [g3[v] for v in union]
    specializations = [dict(prime=2521,zeta_image=1397,sqrt5_image=643),dict(prime=2689,zeta_image=2025,sqrt5_image=172)]
    for pars in specializations:
        g.check_specialization(pars)
    summary,edges = g.certify('cohort union',points,specializations,True)
    actual = [(union[u],union[v]) for u,v in edges]
    m.require(actual==m.induced(union,source_edges),'complete all-pairs induced union edges')
    return {'union_vertices':len(union),'union_all_pairs':summary['pairs_checked'],
        'union_unit_edges':len(actual),'union_coordinate_sha256':summary['coordinate_sha256'],
        'union_global_edge_sha256':m.digest_edges(actual),
        'all_left_base_field_all_right_nonbase':True,
        'support_coordinate_sha256':[g.coordinate_hash([g3[v] for v in vs],True) for vs in supports]}

def verify(cert, with_geometry=False):
    m.require(cert['version']==1 and cert['graph_sha256']==m.GRAPH_SHA,'certificate source')
    m.require(cert['source_strict_edge_sha256']==m.EDGE_SHA,'certificate edge source')
    records = cert['records']
    m.require([(r['seed'],r['orientation']) for r in records]==[(s,o) for s in range(8) for o in (0,1)],'complete fixed cohort')
    edges,adj = m.load()
    parent_cert = json.loads((m.HERE.parent/'hadwiger_nelson_haugland2131_exact_reproduction/certificate.json').read_text())
    five = ''.join(map(str,parent_cert['five_colouring']))
    m.check_word(list(range(m.N)),edges,five,5)
    supports=[];sizes=[];word_stream=sha256();point_stream=sha256();min_degrees=[]
    for row in records:
        # No heap, incremental degree state, or producer support is trusted.
        vs = m.support_reference(row['seed'],row['orientation'],adj)
        ie = m.induced(vs,edges)
        m.require(len(vs)==row['order']==508,'order')
        m.require(m.PINS <= set(vs),'all five connecting anchors')
        m.require(row['vertex_sha256']==m.digest_labels(vs),'support hash')
        m.require(row['size']==len(ie) and row['edge_sha256']==m.digest_edges(ie),'complete edge hash')
        m.require((303,1368) in ie and (435,1500) in ie,'both cross edges retained')
        m.require(len(m.components(vs,adj))==1,'connected complete support')
        m.check_word(vs,ie,row['four_word'],4)
        m.check_word(vs,ie,''.join(five[v] for v in vs),5)
        supports.append(vs);sizes.append(len(ie))
        min_degrees.append(min(len(adj[v]&set(vs)) for v in vs))
        word_stream.update((row['four_word']+'\n').encode())
        point_stream.update((row['vertex_sha256']+'\n').encode())
    m.require(len({tuple(v) for v in supports})==16,'distinct supports')
    maximum = max_capped_ball(adj)
    m.require(maximum==507,'largest capped metric ball')
    result={'status':'VERIFIED_FIXED_NONLOCAL_COHORT_FOUR_COLOURABLE',
        'cases':16,'distinct_supports':16,'vertices_each':508,
        'unit_edge_counts':sizes,'minimum_degrees':min_degrees,
        'all_connected':True,'both_cross_edges_present_each':True,
        'maximum_host_metric_ball_order_through508':maximum,
        'no_support_contained_in_target_sized_metric_ball':True,
        'all_four_words_checked':True,'all_parent_five_restrictions_checked':True,
        'four_word_stream_sha256':word_stream.hexdigest(),
        'support_hash_stream_sha256':point_stream.hexdigest(),
        'record_candidate':False,'all_parent_subsets_classified':False}
    if with_geometry:
        result['geometry']=geometry(supports,edges)
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--geometry',action='store_true');args=ap.parse_args()
    result=verify(json.loads((m.HERE/'certificate.json').read_text()),args.geometry)
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
