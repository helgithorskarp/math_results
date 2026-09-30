#!/usr/bin/env python3
"""Regenerate all small inputs and build the two unchanged exact kernels."""
from itertools import combinations, product
import json
import subprocess
import helpers as p
import mixed_carrier as c


def checked_group(template):
    group = p.m.automorphisms(template['star'])
    domain = {tuple(g) for g in group}
    first = {frozenset(p.points(w | (1 << 17))) for w in template['star']}
    for g in group:
        if sorted(g) != list(range(18)) or tuple(g[:3]) != (0, 1, 2) or g[17] != 17:
            raise RuntimeError('invalid group permutation')
        if {frozenset(g[z] for z in word) for word in first} != first:
            raise RuntimeError('group does not preserve first star')
    if tuple(range(18)) not in domain or any(tuple(a[b[z]] for z in range(18)) not in domain
                                             for a, b in product(group, repeat=2)):
        raise RuntimeError('group is not closed')
    return group


def p3_control(shape, template, baseline, group):
    triples = baseline['common_triples']
    union = sorted(set().union(*(set(q) for q in triples)))
    domain = set()
    for q in combinations(union, 3):
        leaves, _ = c.carrier_independent(triples, q)
        domain.update(leaves)
    if len(domain) != 270:
        raise RuntimeError('wrong p3 control domain')
    seen = set()
    representatives = []
    for leave in sorted(domain):
        if leave in seen:
            continue
        orbit = {p.edge_image(leave, g) for g in group}
        if not orbit <= domain or orbit & seen:
            raise RuntimeError('invalid p3 control orbit')
        seen.update(orbit)
        representatives.append(leave)
    if seen != domain or len(representatives) != [55, 46, 71][shape]:
        raise RuntimeError('p3 control coverage differs')
    pairs = list(combinations(range(1, 17), 2))
    index = {edge: i for i, edge in enumerate(pairs)}
    common = set().union(*(set(combinations(t, 2)) for t in triples))
    masks = baseline['candidate_quadruples']
    lines = [f'120 {len(masks)} 6']
    lines.extend(str(w) + ' ' + ' '.join(str(index[e]) for e in combinations(p.points(w), 2))
                 for w in sorted(masks))
    lines.append(str(len(representatives)))
    for i, leave in enumerate(representatives):
        missing = sorted(index[e] for e in set(leave) | common)
        if len(missing) != 18:
            raise RuntimeError('wrong p3 excluded-pair count')
        lines.append(f'{i} 18 ' + ' '.join(map(str, missing)))
    inp = p.WORK / f'p3_s{shape}.input'
    out = p.WORK / f'p3_s{shape}.jsonl'
    inp.write_text('\n'.join(lines) + '\n')
    result = subprocess.run([str(p.WORK / 'bitset'), str(inp), str(out)],
                            capture_output=True, text=True, timeout=60)
    if result.returncode or result.stderr:
        raise RuntimeError('INCOMPLETE p3 control: ' + result.stderr)
    records = [json.loads(s) for s in out.read_text().splitlines()]
    if [r['index'] for r in records] != list(range(len(representatives))):
        raise RuntimeError('p3 control case order differs')
    for leave, record in zip(representatives, records):
        for cover in record['covers']:
            p.validate_second(template, triples, cover, leave)


def main():
    p.WORK.mkdir(parents=True, exist_ok=True)
    templates = json.loads((p.SOURCE / 'expected.json').read_text())['templates']
    p.write('first_star_templates.json', templates)
    p.write('baseline69.json', p.historical_baseline())
    for source, target in [(p.SOURCE / 'bitset.cpp', p.WORK / 'bitset'),
                           (p.BASE / 'dlx.cpp', p.WORK / 'dlx')]:
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic',
                        str(source), '-o', str(target)], check=True)
    cases = []
    for shape, template in enumerate(templates):
        common = sorted(p.points(w & ~1) for w in template['star'] if w & 1)
        first = [frozenset(p.points(w | (1 << 17))) for w in template['star']]
        masks = [sum(1 << z for z in q) for q in combinations(range(1, 17), 4)
                 if all(len((frozenset(q) | {0}) & word) <= 2 for word in first)]
        if len(common) != 3 or len(set().union(*map(set, common))) != 9 or len(masks) != [489, 483, 477][shape]:
            raise RuntimeError('mixed candidate carrier differs')
        baseline = dict(shape=shape, common_triples=common, candidate_quadruples=masks,
                        candidate_sha256=p.digest(masks))
        cases.append(baseline)
        group = checked_group(template)
        reps = [q for q in combinations(range(1, 17), 3)
                if q == min(tuple(sorted(g[z] for z in q)) for g in group)]
        if len(group) != [6, 6, 4][shape] or len(reps) != [110, 110, 161][shape]:
            raise RuntimeError('mixed C orbit domain differs')
        p.write(f'c_orbits_s{shape}.json', dict(groups=group, c_reps=reps))
        p3_control(shape, template, baseline, group)
    p.write('mixed_row_baseline.json', dict(cases=cases))
    print(json.dumps(dict(status='PREPARED', historical_words=69, shapes=[0, 2],
                          candidate_counts=[len(q['candidate_quadruples']) for q in cases],
                          p3_control_fibers=172, work=str(p.WORK)), sort_keys=True))


if __name__ == '__main__':
    main()
