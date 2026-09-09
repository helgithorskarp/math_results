#!/usr/bin/env python3
"""Check complete algebraic coverage and all colour-bad physical edge exclusions."""
import argparse,json,time
from pathlib import Path
from collections import Counter
import geometry as G
import colour as C
X=C.X;HERE=Path(__file__).resolve().parent

def run(path):
    cert=json.loads(Path(path).read_text());X.need(cert['schema']=='hn-radix-reflection-pair-stratum-v1','certificate schema')
    data=G.compile(cert['pair_rows'])
    for name,key in [('component_inventory_sha256','components'),('cover_sha256','coverage'),('normalizations_sha256','normalizations'),('expanded_pair_exclusions_sha256','physical_pair_exclusions')]:
        X.need(cert[name]==X.digest(data[key]),'independent '+key+' inventory')
    X.need(data['curve_inventory_sha256']==cert['curve_inventory_sha256'],'original curve IDs')
    words=cert['colour_word_indices'];prime=cert['prime']
    X.need(type(prime)is int and X.is_prime(prime),'proof modulus is prime')
    X.need(len(words)==len(data['components']) and all(type(k)is int and 0<=k<81 for k in words),'complete explicit colouring words')
    bad=C.inventory()
    for component,k in zip(data['components'],words):C.check(component,{'prime':prime,'colour':k},bad)
    degrees=Counter(len(q)-1 for q,T,R in data['components'])
    return {'verified':True,'pair_systems':len(cert['pair_rows']),'conservative_pair_orbit_allowance_removed':sum(row[4] for row in cert['pair_rows']),
            'D3_expanded_pair_exclusions':len(data['physical_pair_exclusions']),'real_coefficient_norm_curves':data['real_coefficient_curves'],
            'algebraic_chart_records':len(words),'chart_degree_histogram':{str(k):v for k,v in sorted(degrees.items())},
            'pair_chart_incidence_slots':sum(len(ids) for pair,ids in data['coverage']),
            'colour_word_histogram':{str(k):v for k,v in sorted(Counter(words).items())},
            'eliminant_inventory_sha256':data['eliminants_sha256'],'fibre_degree_histogram':data['fibre_degree_histogram'],
            'all_physical_members_of_named_stratum_chromatic_number':3,'maximum_physical_order':243,
            'complete_A5_architecture_closed':False,'record_improvement':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--check-expected',action='store_true');a=p.parse_args()
    result=run(a.certificate)
    if a.check_expected:X.need(result==json.loads((HERE/'EXPECTED.json').read_text()),'expected stratum closure')
    print(json.dumps(result,indent=2,sort_keys=True))
