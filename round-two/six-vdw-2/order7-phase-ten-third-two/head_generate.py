"""Twenty-two ordinary fifth/sixth heads for the remaining third-three class."""
import argparse
import json
from pathlib import Path
import time

from common import load_encoder, require, sha, endpoint_generator, pins
old = endpoint_generator()
neg, put = old.neg, old.put


PARAMETERS = [(5,m,None,b) for m in range(13,5,-1) for b in (0,1)]
PARAMETERS += [(4,6,q,b) for q in (8,7) for b in (0,1)]
PARAMETERS += [(4,5,None,b) for b in (0,1)]


def stem_for(w,m,q,b):
    return f'third3-next22-fourth-{w}-fifth-{m}-sixth-{q or 0}-b-{b}'


def head_fixed(w,m,q,background):
    require((w,m,q,background) in PARAMETERS,'unsupported heterogeneous head')
    anchors={0,1,3,w,m}
    if q is not None:anchors.add(q)
    last=m if q is None else q
    fixed={i:(1-background if i in anchors else background) for i in range(last+1)}
    fixed[43]=background
    require(sum(v!=background for v in fixed.values())==len(anchors),'wrong selected head count')
    return fixed


def prefix(inputs, base, exact):
    require(exact in (4, 5), 'unsupported exact count')
    levels = exact+1
    previous, rows, cursor = {0: True}, set(), base
    for i, value in enumerate(inputs, 1):
        current = {0: True}
        for threshold in range(1, min(i, levels)+1):
            cursor += 1
            a, b, z = previous.get(threshold, False), previous[threshold-1], cursor
            for row in ((neg(a), z), (neg(value), neg(b), z),
                        (a, value, -z), (a, b, -z)):
                put(rows, row)
            current[threshold] = z
        previous = current
    put(rows, [previous[exact]])
    put(rows, [-previous[levels]])
    return rows, cursor


def main(work):
    began = time.monotonic()
    require(not work.exists(), 'fresh work directory required')
    work.mkdir(parents=True)
    edges = load_encoder().field_edges()
    records = []
    premise = pins()
    for w,m,q,background in PARAMETERS:
        fixed = head_fixed(w,m,q,background)
        free = [i for i in range(44) if i not in fixed]
        n = len(free)
        exact = 4 if q is not None else 5
        last = m if q is None else q
        index = {i: j for j, i in enumerate(free)}
        colors = list(range(1, 45)) + [
            (i+1)*(-1 if fixed[i] else 1) if i in fixed else 45+index[i]
            for i in range(44)]
        phases = [bool(fixed[i]) if i in fixed else 45+n+index[i]
                  for i in range(44)]
        field, color, phase, xor = (set() for _ in range(4))
        for edge in edges:
            values = [colors[i] for i in edge]
            put(field, values)
            put(field, [-v for v in values])
        for i in range(88):
            values = [colors[(i+j) % 88] for j in range(7)]
            put(color, values)
            put(color, [-v for v in values])
            values = [colors[(i+19*j) % 88] for j in range(8)]
            put(color, values)
            put(color, [-v for v in values])
        for i in range(44):
            values = [phases[(i+j) % 44] for j in range(8)]
            put(phase, values)
            put(phase, [neg(v) for v in values])
        for i in free:
            a, b, s = i+1, 45+index[i], 45+n+index[i]
            xor.update(tuple(sorted(row)) for row in
                       ((a, b, -s), (a, -b, s), (-a, b, s), (-a, -b, -s)))
        counter, variables = prefix([phases[i]*(-1 if background else 1)
                                     for i in free], 44+2*n, exact)
        require(n == 42-last
                and variables == (34+7*n if q is not None else 29+8*n),
                'wrong heterogeneous exact-count dimension')
        core = field | color | phase | xor | counter
        density, pair = set(), set()
        selected = [neg(value) if background else value for value in phases]
        for i in range(44):
            put(density, [selected[(i-1) % 44], neg(selected[i]),
                          neg(selected[(i+1) % 44]),
                          *[selected[(i+j) % 44] for j in (2,3)]])
            put(pair, [selected[(i-1) % 44], neg(selected[i]),
                       neg(selected[(i+1) % 44]),
                       *[selected[(i+j) % 44] for j in (2,4,5)]])
        require(len(density-core) > 0 and len(pair-(core | density)) > 0,
                'changed model adds no distinct THREE or FOLLOWING_ONE clauses')
        rows = sorted(core | density | pair, key=lambda row: (len(row), row)) + [(-1,)]
        stem = stem_for(w,m,q,background)
        cnf = work/(stem+'.cnf')
        cnf.write_text(f'p cnf {variables} {len(rows)}\n' +
                       ''.join(' '.join(map(str, row))+' 0\n' for row in rows))
        records.append(dict(stem=stem, minimum_distance=1, background=background,
            third_selected_index=3, fourth_selected_index=w, fifth_selected_index=m,
            sixth_selected_index=q, selected_anchors=sorted(i for i,v in fixed.items() if v!=background),
            phase_K=34 if background else 10, free_phase_indices=free,
            variables=variables, clauses=len(rows), cnf_sha256=sha(cnf),
            free_selected_count=exact, selected_anchor_count=10-exact,
            root57_color_cut=True, adjacent_density_cut=True, gap_one_following_cut=True,
            density_lemma_graph=premise['premises']['third3']['graph'],
            density_lemma_source_commit=premise['premises']['third3']['source_commit'],
            following_lemma_graph=premise['premises']['gap1-following']['graph'],
            following_lemma_source_commit=premise['premises']['gap1-following']['source_commit'],
            density_clauses_after_substitution=len(density),
            new_density_clauses=len(density-core),
            pair_clauses_after_substitution=len(pair),
            new_pair_clauses=len(pair-(core | density)),
            extra_sixth_anchor=q is not None, next_free_phase=last+1,
            proposed_third_within_two_cut=False, redundant_ancestor_cuts=False,
            no_adjacency_cut=False, conditional_successor_cut=False,
            selected_run_start=True, mathematical_exclusion=False))
    result = dict(status='GENERATED_NOT_AUDITED', agent='six-vdw-2', role='researcher',
                  records=records, producer_sha256=sha(Path(__file__)),
                  seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
