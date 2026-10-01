"""Solver-free reader for the all-motion P17 Hc=Hh=3 proof.

Replays the interior-integrality checker and prior exact pair propagator.
The published unique-second-prefix theorem remains an explicit premise.
"""
import argparse
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
from build import (HERE, ROOT, Tile, require, halo, load, candidates,
                   third_formula, compile_subset, audit_subset, RupChecker, dimacs)
from contact import check_patch
from reader import strict_rectangles


def reject(call):
    try:
        call()
    except ValueError:
        return 1
    raise ValueError('malformed control was accepted')


def lower_check(tile, records, corners):
    require(records and all(len(r) == 4 and all(type(x) is int for x in r)
                           and 0 <= r[0] <= 3 for r in records), 'bad lower pose')
    levels = [[tuple(r[1:]) for r in records if r[0] == k] for k in range(4)]
    require(levels[0] == [tile.root], 'bad lower root')
    old, stats = [], []
    for k in range(4):
        prefix = old+levels[k]
        if k:
            check_patch(tile, old, prefix, scale=1)
            require(strict_rectangles(tile, old, prefix), 'lower collar failed')
        pixels = set().union(*(tile.pixels(p, 1) for p in prefix))
        require(corners.disc(pixels), 'lower prefix is not a disc')
        stats.append(dict(level=k, copies=len(prefix), cells=len(pixels)))
        old = prefix
    return stats


def check(dependency_root):
    data = json.loads((HERE/'input.json').read_text())
    cert = json.loads((HERE/'certificate.json').read_text())
    for name, digest in json.loads((HERE/'dependencies.json').read_text()).items():
        actual = ROOT/name if name.startswith('round-two/six-heesch-1/') else dependency_root/name
        require(hashlib.sha256(actual.read_bytes()).hexdigest() == digest,
                'dependency byte pin changed: '+name)
    phase = load(HERE.parent/'p17-interior-integrality/check.py', 'p17_phase_reader')
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        phase.main()
    phase_result = json.loads(captured.getvalue())
    require(phase_result == json.loads((HERE.parent/'p17-interior-integrality/expected.json')
                                     .read_text()), 'phase replay changed')
    tile = Tile(data['cells'])
    require(data['cells'] == json.loads((HERE.parent/'p17-interior-integrality/input.json')
                                      .read_text())['cells'], 'P17 input changed')
    atlas = json.loads((dependency_root/'heesch_polyomino_four_corona_frontier/atlas.json')
                      .read_text())
    require(data['second_prefix'] == atlas['four_corona_second_prefixes'][2] and
            data['first_prefix'] == atlas['three_corona_first_prefixes'][8],
            'published frontier coordinates changed')
    corners = load(dependency_root/'heesch_polyomino_corner_obstruction/corners.py',
                   'p17_prior_corners')
    require(corners.variants(data['cells']) == tile.orientations,
            'orientation conventions disagree')
    pairs = json.loads((dependency_root/'heesch_polyomino_corner_obstruction/pairs.json')
                      .read_text())
    forbidden = set(map(tuple, pairs['forbidden_poses']))
    require(len(forbidden) == 237, 'prior library count changed')
    for o, x, y in sorted(forbidden):
        result = corners.propagate(data['cells'],
                    [(tile.orientations[tile.root[0]], (0, 0)),
                     (tile.orientations[o], (x, y))])
        require(result['status'] == 'contradiction', 'unproved prior pair exclusion')
    lower = lower_check(tile, data['known_three_corona_poses'], corners)
    source_lower = json.loads((dependency_root/
            'heesch_polyomino_euler_cnf/kaplan17_depth3.witness.json').read_text())['patch']
    reconstructed = sorted((r[0], tuple(sorted(tile.pixels(tuple(r[1:]), 1))))
                           for r in data['known_three_corona_poses'])
    require(reconstructed == sorted((r['level'], tuple(sorted(map(tuple, r['cells']))))
                                    for r in source_lower), 'lower provenance changed')
    motif = list(map(tuple, data['forbidden_three_copy_support']))
    motif_pixels = set().union(*(tile.pixels(p, 1) for p in motif))
    require(len(motif) == 3 and len(motif_pixels) == 51 and corners.disc(motif_pixels),
            'motif is not a three-copy disc')
    target = set(map(tuple, data['half_grid_target']))
    require(target <= halo(set().union(*(tile.pixels(p, 2) for p in motif))),
            'target is not demanded by a strict surround')
    mp, mc, mn = compile_subset(tile, motif, 2, target)
    audit_subset(tile, motif, 2, target, mp)
    motif_trace = (HERE/'three-copy.rup').read_text()
    require(hashlib.sha256(dimacs(mc, mn)).hexdigest() == cert['motif']['cnf_sha256'],
            'motif formula changed')
    motif_replay = RupChecker(mc, mn).verify(motif_trace)
    require(hashlib.sha256(motif_trace.encode()).hexdigest() ==
            cert['motif']['proof_sha256'], 'motif proof changed')
    fixed, pool, cnf, nv, metadata = third_formula(tile, data, pairs, dependency_root)
    target_integer, raw_pool = candidates(tile, fixed, 1)
    audit_subset(tile, fixed, 1, target_integer, raw_pool)
    require(metadata == cert['third']['metadata'], 'third metadata changed')
    require(hashlib.sha256(dimacs(cnf, nv)).hexdigest() == cert['third']['cnf_sha256'],
            'third formula changed')
    trace = (HERE/'third-cover.rup').read_text()
    third_replay = RupChecker(cnf, nv).verify(trace)
    require(hashlib.sha256(trace.encode()).hexdigest() == cert['third']['proof_sha256'],
            'third proof changed')
    controls = reject(lambda: lower_check(tile,
                    [r for r in data['known_three_corona_poses'] if r[0] < 3], corners))
    controls += reject(lambda: RupChecker(cnf, nv).verify('\n'.join(trace.splitlines()[:-1])+'\n'))
    controls += reject(lambda: RupChecker(mc[:-len(target)], mn).verify(motif_trace))
    positive_pair = tuple(data['first_prefix'][0])
    if positive_pair == tile.root:
        positive_pair = tuple(data['first_prefix'][1])
    typ = tile.relative_type(tile.root, positive_pair)
    def false_pair_exclusion():
        result = corners.propagate(data['cells'],
                    [(tile.orientations[tile.root[0]], (0, 0)),
                     (tile.orientations[typ[0]], (typ[1]//2, typ[2]//2))])
        require(result['status'] == 'contradiction', 'positive pair is not excluded')
    controls += reject(false_pair_exclusion)
    return dict(agent='six-heesch-1', role='researcher', seed_cells=17,
                Hc=3, Hh=3, motions='All Euclidean rigid motions and reflections',
                scope='Matches the reported grid value; no new shape or Heesch record.',
                lower_prefixes=lower, old_pair_exclusions_replayed=len(forbidden),
                raw_third_candidates=len(raw_pool), retained_third_candidates=len(pool),
                third_variables=nv, third_clauses=len(cnf),
                third_RUP_steps=third_replay['additions'],
                motif_copies=3, motif_target_pixels=len(target),
                motif_candidates=len(mp), motif_clauses=len(mc),
                motif_RUP_steps=motif_replay['additions'],
                rejected_controls=controls,
                phase_dependency_replayed=phase_result['claim'],
                unique_second_prefix='Published theorem 7887 is a mathematical premise.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dependency-root', type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(check(args.dependency_root.resolve()), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
