#!/usr/bin/env python3
"""Remove the last nontrivial-stabilizer rows from the exact h4191 interface."""
import argparse
import json
from pathlib import Path
from common import HERE, X, PAIRS, INPUT_SHA, inventory


def run(path,export=None):
    data = json.loads(Path(path).read_text())
    X.need(X.digest(data) == INPUT_SHA, 'pinned complete h4191 residual interface')
    fs,circle,monos,rowids,images = inventory()
    modes = {k:data[k] for k in ('remaining_exact','remaining_six')}
    selected = sorted(r for rows in modes.values() for r in rows if r[2] != 1)
    X.need(selected == PAIRS, 'all and only remaining nontrivial pair stabilizers')
    X.need(not [r for r in modes['remaining_exact'] if r[2] != 1],
           'all four rows were already in at-least-six mode')
    kept = {k:[r for r in rows if r[2] == 1] for k,rows in modes.items()}
    inherited = {tuple(p) for p in data['new_pair_exclusions']}
    X.need(not inherited.intersection(images), 'new exclusions do not reopen h4191 pairs')
    out = {'schema':'hn-radix-rotation-pair-frontier-v1',
           'source_frontier_sha256':INPUT_SHA, 'curve_inventory_sha256':X.digest(fs),
           'removed':selected, 'new_pair_exclusions':images,
           'reflection_and_rotation_pair_exclusions':sorted(inherited.union(images)),
           **kept,
           'mode_note':'Exact-five flags inherited from h4185 through h4191; no new pencil census or mode moves.'}
    result = {'verified':True, 'whole_pair_systems_removed':len(selected),
              'removed_conservative_allowance':sum(r[4] for r in selected),
              'new_expanded_pair_exclusions':len(images),
              'combined_reflection_rotation_exclusions':len(out['reflection_and_rotation_pair_exclusions']),
              'remaining_global_pairs':sum(map(len,kept.values())),
              'remaining_global_allowance':sum(r[4] for rows in kept.values() for r in rows),
              'inherited_exact_five_rows':len(kept['remaining_exact']),
              'inherited_exact_five_allowance':sum(r[4] for r in kept['remaining_exact']),
              'remaining_at_least_six_rows':len(kept['remaining_six']),
              'remaining_at_least_six_allowance':sum(r[4] for r in kept['remaining_six']),
              'every_remaining_pair_stabilizer_trivial':True,
              'new_mode_moves_computed':False, 'new_pencil_census_computed':False,
              'row_hashes':{k:X.digest(out[k]) for k in
                            ('removed','new_pair_exclusions','reflection_and_rotation_pair_exclusions',
                             'remaining_exact','remaining_six')},
              'export_canonical_sha256':X.digest(out), 'record_improvement':False}
    if export:
        with Path(export).open('x') as f:json.dump(out,f,sort_keys=True,separators=(',',':'));f.write('\n')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--frontier',type=Path,required=True)
    p.add_argument('--export-interface',type=Path);p.add_argument('--check-expected',action='store_true');a = p.parse_args()
    result = run(a.frontier,a.export_interface)
    if a.check_expected:X.need(result == json.loads((HERE/'FRONTIER_EFFECT.json').read_text()),'exact residual accounting')
    print(json.dumps(result,indent=2,sort_keys=True))
