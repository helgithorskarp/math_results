#!/usr/bin/env python3
"""Cold exact reproduction. Generated data remain outside the source bundle.

Actual author six-code-2, researcher. Paired programs are same-author
validation, not an independent mathematical review or formal proof.
"""
from collections import Counter
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import argparse
import json
import os
import resource
import subprocess
import time

import census
import color
import common as C
import dependencies
import joint
import point_maps
import reference as R


def graph_file(path, adjacency):
    lines = [str(len(adjacency))]
    for row in adjacency:
        neighbors = tuple(C.bits(row))
        lines.append(' '.join(map(str, (len(neighbors),) + neighbors)))
    path.write_text('\n'.join(lines) + '\n')


def native(executable, work, name, adjacency, target, cap=30000000, expected='COMPLETE'):
    input_path, output_path = work / (name + '.graph'), work / (name + '.maxima')
    graph_file(input_path, adjacency)
    run = subprocess.run([str(executable), str(input_path), str(output_path), str(cap), '30', str(target)],
                         capture_output=True, text=True, timeout=40)
    (work / (name + '.native.log')).write_text(run.stdout + run.stderr)
    C.require(run.stdout.startswith(expected + ' ') and
              run.returncode == (0 if expected == 'COMPLETE' else 2),
              'INCOMPLETE or incorrect native status: ' + name + ': ' + run.stdout + run.stderr)
    if expected != 'COMPLETE':
        return (), 0
    cliques = tuple(sorted(tuple(map(int, line.split())) for line in output_path.read_text().splitlines()))
    C.require(len(set(cliques)) == len(cliques), 'native duplicate cliques')
    for q in cliques:
        C.require(len(q) == len(set(q)) == target and tuple(sorted(q)) == q and
                  all(0 <= v < len(adjacency) for v in q) and
                  all(adjacency[v] >> w & 1 for v, w in combinations(q, 2)), 'native invalid clique')
    return cliques, int(run.stdout.split()[2])


def compile_native(work, sanitizers):
    output = work / 'pivot'
    command = ['g++', '-std=c++20', '-Wall', '-Wextra', '-Werror', '-O1' if sanitizers else '-O2']
    if sanitizers:
        command += ['-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-fno-pie', '-no-pie']
    run = subprocess.run(command + [str(C.HERE / 'pivot.cpp'), '-o', str(output)],
                         capture_output=True, text=True, timeout=60)
    (work / 'compiler.log').write_text(run.stdout + run.stderr)
    C.require(run.returncode == 0, 'native compilation failed')
    return output


def census_all(work):
    data, literal = C.model(), R.literal_model()
    C.require(data == literal, 'carrier differs entrywise')
    group, other_group = C.anchor_group(data), R.literal_group(literal)
    C.require(group == other_group, 'anchor maps differ entrywise')
    cases, other_cases = C.cases(data, group), R.literal_cases(literal, other_group)
    C.require(cases == other_cases, 'deficit cases differ entrywise')
    roots, records, profile = [], [], Counter()
    for i, case in enumerate(cases):
        if case['direct']:
            records.append(dict(case=i, direct=True, orbit_size=case['orbit_size'], count=0))
            continue
        covers, n1, optional, configs = census.solve(data, case)
        other, n2 = R.literal_solve(other_cases[i])
        C.require(tuple(covers) == other, 'covers differ entrywise at case ' + str(i))
        for cover in covers:
            Q = tuple(sorted(data['anchors'] + tuple(case['columns'][j] for j in cover)))
            C.check_star(Q, tuple(5 - d for d in case['deficit']) + (5, 5))
            roots.append((i, cover, Q))
            profile[tuple(sorted((d for d in case['deficit'] if d), reverse=True))] += 1
        records.append(dict(case=i, direct=False, orbit_size=case['orbit_size'], count=len(covers),
                            covers_sha256=C.digest(covers), primary_nodes=n1, reference_nodes=n2,
                            optional_rows=optional, optional_configurations=configs))
    (work / 'rooted-packings.json').write_bytes(C.encoded(roots))
    C.require(len(cases) == 108 and len(roots) == 352, 'unexpected complete census size')
    print('census COMPLETE 108 cases 352 packings, entrywise matched', flush=True)
    return roots, dict(raw_deficit_assignments=3060, cases=len(cases),
                      packings=len(roots), records=records, packings_sha256=C.digest(roots),
                      profile_counts=[dict(deficit_profile=k, count=v) for k, v in sorted(profile.items())])


def cover_by_fixtures(roots, fixtures, groups, work):
    records = []
    for i, (_, _, Q) in enumerate(roots):
        for j, fixture in enumerate(fixtures):
            maps, _ = point_maps.point_maps(Q, fixture, stop_after_first=True)
            if maps:
                R.check_point_map(Q, fixture, maps[0])
                records.append(dict(root=i, fixture=j, point_map=maps[0]))
                break
        else:
            raise ValueError('root packing not positively covered by fixtures')
    for Q, group in zip(fixtures, groups):
        C.check_star(Q)
        R.check_group(Q, group)
        if any(sum(v in q for q in Q) == 4 for v in range(17)):
            generated, _ = point_maps.point_maps(Q, Q)
            C.require(tuple(sorted(generated)) == group, 'fixture maps differ from regenerated maps')
    (work / 'positive-point-maps.json').write_bytes(C.encoded(records))
    print('fixture cover COMPLETE 352 actual positive point maps', flush=True)
    return dict(fixtures=len(fixtures), positive_maps=len(records), maps_sha256=C.digest(records),
                group_orders=[len(g) for g in groups])


def completions(fixtures, groups, executable, work):
    table, all_pairs = [], []
    for j, (Q, group) in enumerate(zip(fixtures, groups)):
        mates = tuple(v for v in range(17) if sum(v in q for q in Q) == 4)
        for mate in mates:
            C.require(joint.maps_for_mate(Q, mate) == R.literal_involutions(Q, mate),
                      '324 involutions differ entrywise')
        valid, literal = joint.valid_pairs(Q), R.literal_valid(Q)
        C.require(valid == literal, 'valid mate/involution anchors differ entrywise')
        representatives = joint.pair_quotient(valid, group) if valid else []
        for k, item in enumerate(representatives):
            mate, mapping, anchor = item['mate'], item['mapping'], item['anchor']
            rows, adjacency = joint.residual(anchor, mapping, mate)
            other_rows, other_adj = R.literal_residual(anchor, mapping, mate)
            C.require(rows == other_rows and adjacency == other_adj, 'residual vertices or edges differ')
            maximum, maxima, nodes = color.maximum_cliques(adjacency)
            native_maxima, native_nodes = native(executable, work, f'class-{j:02}-{k:02}', adjacency, maximum)
            C.require(maxima == native_maxima, 'maximum families differ entrywise')
            C.require(maximum <= 13 and maxima, 'unexpected maximum')
            code = tuple(sorted(set(anchor) | {b for i in maxima[0] for b in
                                              (rows[i], C.image_word(rows[i], mapping))}))
            R.check_code(dict(center=17, involution=mapping, words=[C.points(b) for b in code]),
                         expected_size=36 + 2 * maximum)
            table.append(dict(star_fixture=j, pair_case=k, mate=mate, orbit_size=len(item['orbit']),
                              vertices=len(rows), edges=sum(a.bit_count() for a in adjacency) // 2,
                              graph_sha256=C.digest(dict(vertices=rows, adjacency=adjacency)),
                              maximum_orbits=maximum, maximum_words=36 + 2 * maximum,
                              maximum_families=len(maxima), maxima_sha256=C.digest(maxima),
                              coloring_nodes=nodes, native_pivot_nodes=native_nodes))
            print('joint COMPLETE', j, k, 'max_words', 36 + 2 * maximum, flush=True)
        all_pairs.append(dict(fixture=j, mates=len(mates), all_involutions=324 * len(mates),
                              valid_pairs=len(valid), representative_pairs=len(representatives),
                              valid_sha256=C.digest([(m, g, a) for (m, g), a in sorted(valid.items())])))
    C.require(len(table) == 25 and max(t['maximum_words'] for t in table) == 62,
              'complete joint census size or sharp maximum differs')
    return dict(pair_records=all_pairs, joint_cases=len(table), maximum_words=62, table=table)


def controls(executable, work, fixtures, witness):
    controls = []

    def rejected(name, callback, exception=ValueError):
        try:
            callback()
        except exception:
            controls.append(name)
        else:
            raise ValueError('negative control accepted: ' + name)

    high = tuple(range(5))
    def synthetic(columns, mandatory):
        used = set(v for q in columns for v in q)
        return dict(columns=columns, mandatory=mandatory, high=high, already_high=0,
                    covered_high_budget=6, quota=tuple(int(v in used) for v in range(15)))
    data = dict(eligible=tuple(combinations(range(15), 2)))
    for name, case in [('optional-only-row', synthetic(((0, 1, 2, 3),), ())),
                       ('mixed-optional-positive', synthetic(((0, 1, 2, 5), (3, 4, 6, 7)), ((6, 7),)))]:
        first, *_ = census.solve(data, case)
        second, _ = R.literal_solve(case)
        C.require(tuple(first) == second == (tuple(range(len(case['columns']))),), 'optional control failed')
        controls.append(name)
    case = synthetic(((0, 1, 2, 3),), ())
    rejected('primary-guard', lambda: census.solve(data, case, nodes=0), C.Incomplete)
    rejected('literal-guard', lambda: R.literal_solve(case, nodes=0), C.Incomplete)
    bad = deepcopy(witness)
    bad['words'][1] = bad['words'][0]
    rejected('duplicate-witness-word', lambda: R.check_code(bad))
    bad = deepcopy(witness)
    bad['involution'][0] = 0
    rejected('broken-involution', lambda: R.check_code(bad))
    rejected('duplicate-star-quadruple', lambda: C.check_star(fixtures[0][:-1] + (fixtures[0][0],)))
    complete4 = tuple(((1 << 4) - 1) ^ (1 << v) for v in range(4))
    cliques, _ = native(executable, work, 'control-K4', complete4, 4)
    C.require(cliques == ((0, 1, 2, 3),), 'positive native control failed')
    controls.append('native-positive-K4')
    complete5 = tuple(((1 << 5) - 1) ^ (1 << v) for v in range(5))
    native(executable, work, 'control-K5', complete5, 4, expected='LARGER_CLIQUE')
    controls.append('native-larger-clique')
    native(executable, work, 'control-guard', complete4, 4, cap=1, expected='INCOMPLETE')
    controls.append('native-guard')
    path = work / 'control-asymmetric.graph'
    graph_file(path, (2, 0, 0))
    run = subprocess.run([str(executable), str(path), str(work / 'bad.maxima'), '100', '1', '1'],
                         capture_output=True, text=True, timeout=5)
    C.require(run.returncode == 2 and 'ERROR asymmetric graph' in run.stderr, 'asymmetry control failed')
    controls.append('native-asymmetric-input')
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=C.HERE.parents[2])
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--sanitizers', action='store_true')
    parser.add_argument('--record-expected', action='store_true')
    args = parser.parse_args()
    repository, work = args.repository.resolve(), args.work.resolve()
    C.require(work != C.HERE and C.HERE not in work.parents, 'work must be outside source bundle')
    C.require(not work.exists(), 'work directory must be new')
    work.mkdir(parents=True)
    for key in C.THREADS:
        os.environ[key] = '1'
    if args.sanitizers:
        os.environ['ASAN_OPTIONS'] = 'detect_leaks=1:halt_on_error=1'
        os.environ['UBSAN_OPTIONS'] = 'halt_on_error=1:print_stacktrace=1'
    started = time.monotonic()
    executable = compile_native(work, args.sanitizers)
    fixtures_record = json.loads((C.HERE / 'fixtures.json').read_text())
    fixtures = tuple(tuple(tuple(q) for q in Q) for Q in fixtures_record['stars'])
    groups = tuple(tuple(tuple(p) for p in group) for group in fixtures_record['groups'])
    C.require(len(fixtures) == len(groups) == 23, 'fixture arrays have incorrect lengths')
    witness = json.loads((C.HERE / 'witness.json').read_text())
    R.check_code(witness)
    roots, census_record = census_all(work)
    cover_record = cover_by_fixtures(roots, fixtures, groups, work)
    joint_record = completions(fixtures, groups, executable, work)
    control_record = controls(executable, work, fixtures, witness)
    dependency_record = dependencies.replay(repository, work)
    stable = dict(agent='six-code-2', role='researcher', status='COMPLETE',
                  statement='free-involution saturated-star maximum62; full free-involution upper68',
                  census=census_record, fixture_cover=cover_record, completions=joint_record,
                  controls=control_record, dependencies=dependency_record,
                  witness_sha256=C.digest(witness), upper_bound=68,
                  possible_size68_replications=[18, 18] + [19] * 16)
    raw = C.encoded(stable)
    (work / 'result.json').write_bytes(raw)
    if args.record_expected:
        (C.HERE / 'expected.json').write_bytes(raw)
    else:
        C.require(raw == (C.HERE / 'expected.json').read_bytes(), 'complete stable record differs')
    metrics = dict(status='COMPLETE', seconds=time.monotonic() - started,
                   own_peak_RSS_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   child_peak_RSS_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   optimized_python=bool(__import__('sys').flags.optimize), sanitizers=args.sanitizers)
    (work / 'metrics.json').write_bytes(C.encoded(metrics))
    print(json.dumps(metrics, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
