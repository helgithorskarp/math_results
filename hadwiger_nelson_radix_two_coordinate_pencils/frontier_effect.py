#!/usr/bin/env python3
"""Move pairs out of exact-five mode; never delete them from higher incidences."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import exact as X
import verify

HERE=Path(__file__).resolve().parent
SOURCE_SHA='1db1ecc86c993bbe22a83127b85c6d9467d385bdb7dba085193ad47308e1676a'


def run(interface,export=None):
    data=json.loads(Path(interface).read_text())
    X.need(X.digest(data)==SOURCE_SHA,'HN3 complete named mode/stabilizer interface')
    factors,patterns,quintets,keys,trace=verify.inventory()
    # Any two distinct directions determine a unique full affine pencil.
    # Thus a pair in one of these pencils cannot use a different exact-five cover.
    pairs={q for quintet in quintets for q in combinations(quintet,2)}
    modes=data['pair_modes']
    old=modes['exact_five_compatible']
    moved=[row for row in old if tuple(row[:2]) in pairs]
    # Independent criterion inside the imported exact-five mode: the two
    # nonparallel row normals have union of supports of size exactly two.
    raw_rows,_,_,_,rowids=verify.V.reconstruct_inventory()
    supports={c:{j for j,d in enumerate(r) if j and d!=(0,0)} for r,c in rowids.items()}
    by_support=[row for row in old if len(supports[row[0]]|supports[row[1]])==2]
    X.need(by_support==moved,'independent support criterion matches every moved pair')
    retained=[row for row in old if tuple(row[:2]) not in pairs]
    others=[row for name,rows in modes.items() if name!='exact_five_compatible' for row in rows]
    X.need(not any(tuple(row[:2]) in pairs for row in others),'all affected pairs were exact-five compatible')
    sharp=sum(row[3] for row in moved);allowance=sum(row[4] for row in moved)
    # Alternative accounting from row orders and the imported stabilizer masks.
    degrees=[max(i+j for i,j,c in f) for f in factors]
    for a,b,mask,bound,orb in moved:
        X.need(bound==degrees[a]*degrees[b]//2 and orb==bound//mask.bit_count(),'sharp pair-bound alignment')
    if export:
        with Path(export).open('x') as f:
            json.dump({'schema':'hn-radix-two-coordinate-pair-moves-v1','now_requires_at_least_six':moved},f,sort_keys=True,separators=(',',':'));f.write('\n')
    return {'verified':True,'new_forbidden_quintets':6912,'new_closed_realized_pencils':54,
            'remaining_exact_five_realized_pencils':5382-54,
            'remaining_h4171_quintet_survivors':132232896-6912,
            'previous_exact_five_pairs':len(old),'new_pairs_requiring_at_least_six':len(moved),
            'moved_pair_stabilizer_histogram':{str(h):n for h,n in sorted(Counter(row[2].bit_count() for row in moved).items())},
            'moved_product_surface_allowance':sharp,'moved_nonfour_orbit_allowance':allowance,
            'remaining_exact_five_pairs':len(retained),'remaining_exact_five_orbit_allowance':sum(r[4] for r in retained),
            'now_at_least_six_pairs':len(others)+len(moved),
            'now_at_least_six_orbit_allowance':sum(r[4] for r in others)+allowance,
            'whole_global_pair_systems_removed':0,'global_pair_systems':len(old)+len(others),
            'global_nonfour_orbit_allowance':sum(r[4] for r in old+others),
            'moved_pair_rows_sha256':X.digest(moved),'remaining_exact_five_rows_sha256':X.digest(retained),
            'record_improvement':False,'all_five_active_cases_closed':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--interface',type=Path,required=True)
    parser.add_argument('--export-moves',type=Path);parser.add_argument('--check-expected',action='store_true')
    args=parser.parse_args();result=run(args.interface,args.export_moves)
    if args.check_expected:X.need(result==json.loads((HERE/'FRONTIER_EFFECT.json').read_text()),'expected mode refinement')
    print(json.dumps(result,indent=2,sort_keys=True))
