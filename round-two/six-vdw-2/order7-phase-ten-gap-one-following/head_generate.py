"""Twelve complete first-fourth6..11 models for the gap-one following lemma."""
import argparse
import json
from pathlib import Path
import time

from common import load_encoder, require, sha, endpoint_generator, pins
old = endpoint_generator()
neg, put = old.neg, old.put


PARAMETERS=[(ell,None,b) for ell in range(11,5,-1) for b in (0,1)]
def stem_for(ell,m,b):
    return f'third3-fourth-{ell}-fifth-{m or 0}-b-{b}'


def head_fixed(ell,m,background):
    require((ell,m,background) in PARAMETERS,'unsupported heterogeneous head')
    anchors={0,1,3,ell}
    if m is not None:anchors.add(m)
    last=ell if m is None else m
    fixed={i:1-background if i in anchors else background for i in range(last+1)}
    fixed[43]=background
    return fixed


def prefix(inputs, base, exact):
    require(exact in (5, 6), 'unsupported exact count')
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
    for ell,m,background in PARAMETERS:
        fixed = head_fixed(ell,m,background)
        free = [i for i in range(44) if i not in fixed]
        n = len(free)
        exact = 6 if m is None else 5
        last = ell if m is None else m
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
                and variables == (23+9*n if m is None else 29+8*n),
                'wrong heterogeneous exact-count dimension')
        core = field | color | phase | xor | counter
        density=set()
        selected=[neg(value) if background else value for value in phases]
        for origin in range(44):
            put(density,[selected[(origin-1)%44],neg(selected[origin]),
                         neg(selected[(origin+1)%44]),
                         *[selected[(origin+j)%44] for j in (2,3)]])
        require(len(density-core)>0,'new model adds no distinct THREE clauses')
        rows=sorted(core|density,key=lambda row:(len(row),row))+[(-1,)]
        stem=stem_for(ell,m,background)
        cnf = work/(stem+'.cnf')
        cnf.write_text(f'p cnf {variables} {len(rows)}\n' +
                       ''.join(' '.join(map(str, row))+' 0\n' for row in rows))
        records.append(dict(stem=stem,minimum_distance=1,background=background,
            third_selected_index=3,fourth_selected_index=ell,fifth_selected_index=m,
            selected_anchors=sorted(i for i,v in fixed.items() if v!=background),
            phase_K=34 if background else 10,free_phase_indices=free,
            variables=variables,clauses=len(rows),cnf_sha256=sha(cnf),
            free_selected_count=exact,selected_anchor_count=10-exact,
            root57_color_cut=True,adjacent_density_cut=True,
            density_lemma_graph=premise['density_graph'],
            density_lemma_source_commit=premise['density_source_commit'],
            density_clauses_after_substitution=len(density),new_density_clauses=len(density-core),
            fifth_anchor=m is not None,next_free_phase=last+1,
            proposed_third_within_two_cut=False,proposed_gap_one_following_cut=False,redundant_ancestor_cuts=False,
            no_adjacency_cut=False,conditional_successor_cut=False,
            selected_run_start=True,mathematical_exclusion=False))
    result = dict(status='GENERATED_NOT_AUDITED', agent='six-vdw-2', role='researcher',
                  records=records, producer_sha256=sha(Path(__file__)),
                  seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
