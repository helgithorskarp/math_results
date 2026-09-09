#!/usr/bin/env python3
"""Return the complete reflection-pair exclusions to the pinned h4185 frontier."""
import argparse,json
from pathlib import Path
from collections import Counter
import geometry as G
import colour as C
X=C.X;HERE=Path(__file__).resolve().parent
SOURCE_SHA='5496087ac2e75104443c73022ec58bdcc71bb3bafb4605c79aed487fdd3f1da3'

def run(frontier,certificate,export=None):
    data=json.loads(Path(frontier).read_text());cert=json.loads(Path(certificate).read_text())
    X.need(X.digest(data)==SOURCE_SHA==cert['source_frontier_sha256'],'pinned complete h4185 input')
    modes={k:data[k] for k in ('remaining_exact','remaining_six')}
    selected=sorted(r for rows in modes.values() for r in rows if r[2]&56)
    X.need(selected==cert['pair_rows'],'complete named reflection-stabilizer stratum')
    factors,normalizations,polys,coeff,images=G.inventory(selected)
    X.need(X.digest(images)==cert['expanded_pair_exclusions_sha256'],'all symmetry-expanded exclusions')
    removed={k:[r for r in rows if r[2]&56] for k,rows in modes.items()}
    kept={k:[r for r in rows if not r[2]&56] for k,rows in modes.items()}
    rotation_only=[r for rows in kept.values() for r in rows if r[2].bit_count()>1]
    X.need(rotation_only==[[318,340,7,32,10],[318,341,7,32,10],[319,340,7,32,10],[319,341,7,32,10]],'four rotation-only systems explicitly retained')
    out={'schema':'hn-radix-reflection-pair-frontier-v1','curve_inventory_sha256':X.digest(factors),
         'removed':selected,'new_pair_exclusions':images,'remaining_exact':kept['remaining_exact'],'remaining_six':kept['remaining_six'],
         'mode_note':'Exact-five flags inherited from h4185; further pencil/lift viability propagation belongs to HN3.'}
    result={'verified':True,'previous_pair_systems':sum(map(len,modes.values())),
        'whole_pair_systems_removed':len(selected),'removed_exact_five_rows':len(removed['remaining_exact']),
        'removed_at_least_six_rows':len(removed['remaining_six']),
        'removed_exact_five_allowance':sum(r[4] for r in removed['remaining_exact']),
        'removed_at_least_six_allowance':sum(r[4] for r in removed['remaining_six']),
        'removed_total_allowance':sum(r[4] for r in selected),'new_D3_pair_exclusions':len(images),
        'remaining_global_pairs':sum(map(len,kept.values())),
        'remaining_global_allowance':sum(r[4] for rows in kept.values() for r in rows),
        'retained_previous_exact_five_rows':len(kept['remaining_exact']),
        'retained_previous_exact_five_allowance':sum(r[4] for r in kept['remaining_exact']),
        'remaining_at_least_six_rows':len(kept['remaining_six']),
        'remaining_at_least_six_allowance':sum(r[4] for r in kept['remaining_six']),
        'rotation_only_rows_retained':rotation_only,'new_mode_moves_computed':False,'new_pencil_census_computed':False,
        'row_hashes':{k:X.digest(out[k]) for k in ('removed','new_pair_exclusions','remaining_exact','remaining_six')},
        'export_canonical_sha256':X.digest(out),'record_improvement':False}
    if export:
        with Path(export).open('x') as f:json.dump(out,f,sort_keys=True,separators=(',',':'));f.write('\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--frontier',type=Path,required=True);p.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    p.add_argument('--export-interface',type=Path);p.add_argument('--check-expected',action='store_true');a=p.parse_args()
    result=run(a.frontier,a.certificate,a.export_interface)
    if a.check_expected:X.need(result==json.loads((HERE/'FRONTIER_EFFECT.json').read_text()),'expected frontier transformation')
    print(json.dumps(result,indent=2,sort_keys=True))
