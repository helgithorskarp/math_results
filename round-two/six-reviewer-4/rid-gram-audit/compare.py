"""Optional partial author-record comparison; no author executable import."""
import argparse
from copy import deepcopy
from fractions import Fraction
import json,re
from pathlib import Path
import check as audit
HERE=Path(__file__).resolve().parent

def compare(native,own,b):
    count=0
    def rational(x):
        audit.require(type(x) is str,'rational string');f=Fraction(x);return b.q(f.numerator,f.denominator)
    def nf(x):
        audit.require(type(x) is list and len(x)==2,'native phi field');return rational(x[0])+b.P*rational(x[1])
    def of(x):
        audit.require(type(x) is str,'own field string');m=re.fullmatch(r'\(([^)]+)\)\+\(([^)]+)\)sqrt5',x)
        return rational(m[1])+rational(m[2])*(2*b.P-1) if m else rational(x)
    def eq(x,y,why):
        nonlocal count
        audit.require(x==y,why);count+=1
    def vec(x,y,why):
        audit.require(len(x)==len(y)==3,why+' dimension')
        for a,c in zip(x,y,strict=True):eq(nf(a),of(c),why)
    p=own['physical_construction'];P,Z=b.P,b.Z
    V=[b.as_fields(v,2) for v in b.originals()]
    # Published original indexing is sorted by the full rational coefficient key
    # in a+b*phi; derive that key from this reviewer's a+b*sqrt5 representation.
    def phi_key(v):return tuple((Fraction(x.a-x.b,x.d),Fraction(2*x.b,x.d)) for x in v)
    V.sort(key=phi_key)
    vec(native['raw_receiver'],p['receiver_raw'],'literal receiver')
    vec(native['raw_source_normal'],p['source_normal_raw'],'actual source normal')
    for nk,ok in [('receiver_norm_squared','receiver_norm_squared'),('physical_receiving_area_squared','area_target_squared'),('actual_filter_squared_directional_width','receiving_width_filter_squared'),('physical_minimum_receiving_width_squared','width_target_squared'),('physical_minimum_source_width_squared','width_source_squared')]:eq(nf(native[nk]),of(p[ok]),nk)
    for x,y in zip(native['proper_rotation'],p['source_rotation'],strict=True):vec(x,y,'proper rotation')
    r=tuple(of(x) for x in p['receiver_raw']);R=tuple(tuple(of(x) for x in row) for row in p['source_rotation']);RV=[b.act(R,v) for v in V]
    rawgap=nf(native['physical_area_raw_gap']);require_area=of(p['area_source_squared'])
    # Both physical areas have common sqrt(N). Their positive raw gap squared
    # and product give the exact raw difference without introducing radicals.
    target_raw=nf(native['physical_receiving_area_squared'])*of(p['receiver_norm_squared'])
    eq((target_raw+rawgap*rawgap-require_area*of(p['receiver_norm_squared']))**2,4*target_raw*rawgap*rawgap,'squared raw area gap identity')
    audit.require(rawgap>0 and rawgap*rawgap<target_raw,'positive difference branch of raw area gap')
    for nk,ok in [('pair_source_squared_norms','s'),('pair_target_squared_norms','t')]:
        audit.require(len(native[nk])==2,'pair inventory')
        for x,y in zip(native[nk],p['gram'][ok],strict=True):eq(nf(x),of(y),nk)
    eq(nf(native['oriented_Gram']),of(p['gram']['H']),'signed Gram');eq(nf(native['Gram_unsquared_L0']),of(p['gram']['D']),'unsquared branch')
    eq(sorted(nf(x) for x in native['same_original_E_support_margins']),sorted(of(x) for x in p['all_four_actual_equatorial_margins']),'all actual E margins')
    audit.require(len(native['receiving_hull_cycle'])==len(native['source_hull_cycle'])==16,'native cycle inventory')
    for key,ok in [('receiving_hull_cycle','target_cycle_originals'),('source_hull_cycle','source_cycle_originals')]:
        indices=native[key];audit.require(all(type(i) is int and 0<=i<60 for i in indices) and len(set(indices))==16,'all distinct literal original indices')
        eq({V[i] for i in indices},{tuple(of(x) for x in v) for v in p[ok]},'all sixteen '+key+' originals')
    own_edges={tuple(of(x) for x in e['from_original']):e for e in p['all16_receiving_edge_records']}
    records=native['full_edge_records'];audit.require(len(records)==16,'all16 edge records')
    seen=set()
    for record in records:
        i,j=record['receiving_edge'];audit.require(type(i) is type(j) is int and 0<=i<60 and 0<=j<60,'literal edge indices')
        a,c=V[i],V[j];audit.require((a,c) not in seen,'duplicate edge record');seen.add((a,c))
        edge=own_edges[a];eq(c,tuple(of(x) for x in edge['to_original']),'same directed physical edge')
        normal=b.fcross(b.sub(c,a),r);h=b.fdot(normal,a);audit.require(h>0,'outward native edge orientation')
        scale=b.absolute(next(x for x in normal if x!=0));excess=nf(record['excess']);eq(excess/scale,of(edge['maximum_source_excess']),'all16 exact normalized excesses')
        k=record['source_maximizer'];audit.require(type(k) is int and 0<=k<60,'maximizer index')
        eq(b.fdot(normal,RV[k])-h,excess,'each supplied full original maximizer attains')
        audit.require(type(record['violates']) is bool and record['violates']==(excess>0),'strict edge violation flag')
    audit.require(len(seen)==16 and native['violating_receiving_edges']==10 and native['full_receiving_original_edge_comparisons']==960,'full edge coverage counters')
    audit.require(len(native['actual_shortest_transport_rows'])==2,'both actual transported rows')
    for j,row in enumerate(native['actual_shortest_transport_rows']):
        audit.require(type(row['axis']) is int and row['axis']==j,'row axis')
        endpoints=p['actual_rows'][j]['endpoints'];vec(row['target_original'],endpoints[0]['target_support_originals'][0],'both literal row supporters')
        eq(nf(row['minimum_source_margin']),min(of(e['minimum_source_margin']) for e in endpoints),'both exact row margin minima')
        audit.require(row['source_endpoint_comparisons']==row['target_endpoint_comparisons']==120,'whole row inventory')
    audit.require(native['circle_controls']['classification_sha256']==own['circle']['two_pair_decisions_sha256'],'all2304 original control decisions fingerprint')
    audit.require(type(native['all_proper_W_union_P_memberships']) is int and native['all_proper_W_union_P_memberships']==0,'all proper W/P memberships')
    return {'exact_field_or_inventory_comparisons':count,'all16_edge_endpoints_excesses_and_actual_maximizers_match':True,'both_full_shadow_vertex_inventories_match':True,'physical_area_widths_rows_and_Gram_match':True,'all2304_circle_control_decisions_fingerprint_match':True,'trust':'Partial decoded mathematical-entry comparison, separate from complete independent record and complete native replay; author executable never imported.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('native',type=Path);p.add_argument('--controls',action='store_true');args=p.parse_args()
    native=json.loads(args.native.read_text());own=json.loads((HERE/'expected.json').read_text());b,pin=audit.geometry();result=compare(native,own,b)
    if args.controls:
        cases=[]
        def damage(name,fn):
            d=deepcopy(native);fn(d);cases.append((name,d))
        damage('missing_full_edge',lambda d:d['full_edge_records'].pop())
        damage('duplicate_full_edge',lambda d:d['full_edge_records'].__setitem__(1,deepcopy(d['full_edge_records'][0])))
        damage('wrong_actual_maximizer',lambda d:d['full_edge_records'][0].__setitem__('source_maximizer',0))
        damage('changed_physical_width',lambda d:d.__setitem__('physical_minimum_source_width_squared',['0','0']))
        damage('unsigned_Gram',lambda d:d.__setitem__('oriented_Gram',['0','0']))
        damage('boolean_original_index',lambda d:d['source_hull_cycle'].__setitem__(0,True))
        damage('false_row_margin',lambda d:d['actual_shortest_transport_rows'][0].__setitem__('minimum_source_margin',['0','0']))
        damage('changed_circle_fingerprint',lambda d:d['circle_controls'].__setitem__('classification_sha256','0'*64))
        rejected=[]
        for name,d in cases:
            try:compare(d,own,b)
            except (ValueError,KeyError,TypeError,IndexError):rejected.append(name)
            else:raise ValueError('damaged native input accepted:'+name)
        result['damaged_inputs_rejected']=rejected
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
