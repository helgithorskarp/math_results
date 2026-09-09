#!/usr/bin/env python3
"""Count safe whole-system deletions in the pinned h4117 global interface."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)


def effect(frontier,quotient,four):
    curves=frontier['curves'];pairs=quotient['pair_system_representatives']
    require([c['id'] for c in curves]==list(range(2797)),'curve IDs')
    require(digest([c['polynomial'] for c in curves])=='85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9','h4105 curve catalog')
    require(digest(pairs)=='ab9d291e1b59a234712eb9ef95aaeb70654921351542b825afeee887b118ccd6','h4117 pair representatives')
    circle=frontier['circle_id']
    require(circle==342 and curves[circle]['polynomial']==[[0,0,-1],[0,2,3],[2,0,1]],'circle equation')
    degree=[max(i+j for i,j,a in c['polynomial']) for c in curves]
    removed=[e for e in pairs if circle in e];left=[e for e in pairs if circle not in e]
    allowance=lambda rows:sum(degree[a]*degree[b] for a,b in rows)
    require(len(pairs)==132130 and allowance(pairs)==7785424,'original interface')
    require(hashlib.sha256((json.dumps(four,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()=='76c806cdb5458bbc45e730f7dcd9e3231d6ffc6f4dc99c2013e0f19966c562eb','h4135 four-active interface')
    groups=four['pair_representatives']
    no_circle=groups['exact_four_no_circle'];with_circle=groups['exact_four_with_circle']
    require(len(no_circle)==2528 and len(with_circle)==26,'exact-four system counts')
    left_set=set(map(tuple,left));removed_set=set(map(tuple,removed))
    require(all(tuple(e) in left_set for e in no_circle) and all(tuple(e) in left_set|removed_set for e in with_circle),'exact-four subset interface')
    torus_explicit=sum(tuple(e) in removed_set for e in with_circle)
    require(torus_explicit==22,'torus-mode explicit-circle count')
    return {'verified':True, 'h4135_exact_four_global_systems_retained':len(no_circle),
            'h4135_exact_four_allowance_retained':allowance(no_circle),
            'h4135_torus_mode_systems_excluded_from_exact_four':len(with_circle),
            'h4135_torus_mode_whole_circle_systems_removed':torus_explicit,
            'h4135_torus_mode_retained_only_for_higher_incidence':len(with_circle)-torus_explicit,
            'other_retained_systems_require_at_least_five_curves':len(left)-len(no_circle),
            'higher_incidence_scope':'Parameters with at least five active curves can also occur on the exact-four-compatible systems; this is not a disjoint parameter partition','source_h4117_pair_orbits':len(pairs),'circle_curve_id':circle,
            'removed_circle_pair_orbits':len(removed),'removed_bezout_allowance':allowance(removed),
            'remaining_global_pair_orbit_representatives':len(left),
            'remaining_parameter_orbit_allowance':allowance(left),
            'remaining_pair_representatives_sha256':digest(left),
            'scope':'Only whole systems explicitly containing the circle are removed by this count. The theorem also excludes circle roots of all retained systems. No count of those roots is claimed.',
            'global_not_chamber_representatives':True,'record_improvement':False}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--frontier',type=Path,required=True);ap.add_argument('--quotient',type=Path,required=True);ap.add_argument('--four-interface',type=Path,required=True);ap.add_argument('--check-expected',action='store_true');a=ap.parse_args()
    r=effect(json.loads(a.frontier.read_text()),json.loads(a.quotient.read_text()),json.loads(a.four_interface.read_text()))
    if a.check_expected:require(r==json.loads(Path(__file__).with_name('FRONTIER_EFFECT.json').read_text()),'expected effect')
    print(json.dumps(r,sort_keys=True,indent=2))
if __name__=='__main__':main()
