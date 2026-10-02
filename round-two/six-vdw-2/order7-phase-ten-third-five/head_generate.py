"""Sixteen smaller fourth-selection models of the third-index6 class."""
import argparse
import json
from pathlib import Path
import time

from common import load_encoder, require, sha, endpoint_generator, pins
old = endpoint_generator()
neg, put = old.neg, old.put


def head_fixed(k, background):
    require(7 <= k <= 14, 'unsupported fourth selected index')
    fixed = {0: 1-background, 1: 1-background, 6: 1-background,
             k: 1-background, 43: background}
    for i in list(range(2, 6))+list(range(7, k)):
        fixed[i] = background
    require(sum(v != background for v in fixed.values()) == 4,
            'wrong four-selected head count')
    return fixed


def prefix(inputs, base):
    previous, rows, cursor = {0: True}, set(), base
    for i, value in enumerate(inputs, 1):
        current = {0: True}
        for threshold in range(1, min(i, 7)+1):
            cursor += 1
            a, b, z = previous.get(threshold, False), previous[threshold-1], cursor
            for row in ((neg(a), z), (neg(value), neg(b), z),
                        (a, value, -z), (a, b, -z)):
                put(rows, row)
            current[threshold] = z
        previous = current
    put(rows, [previous[6]])
    put(rows, [-previous[7]])
    return rows, cursor


def main(work):
    began = time.monotonic()
    require(not work.exists(), 'fresh work directory required')
    work.mkdir(parents=True)
    edges = load_encoder().field_edges()
    records = []
    premise = pins()
    for k in range(14, 6, -1):
        for background in (0, 1):
            fixed = head_fixed(k, background)
            free = [i for i in range(44) if i not in fixed]
            n = len(free)
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
                                         for i in free], 44+2*n)
            require(n == 42-k and variables == 23+9*n, 'wrong exact-six fourth-head dimension')
            core = field | color | phase | xor | counter
            density = set()
            selected = [neg(v) if background else v for v in phases]
            for i in range(44):
                put(density, [selected[(i-1) % 44], neg(selected[i]),
                              neg(selected[(i+1) % 44]),
                              *[selected[(i+j) % 44] for j in range(2, 7)]])
            require(len(density-core) > 0, 'changed proposal adds no density clauses')
            rows = sorted(core | density,
                          key=lambda row: (len(row), row)) + [(-1,)]
            stem = f'density-k6-fourth-{k}-b-{background}'
            cnf = work/(stem+'.cnf')
            cnf.write_text(f'p cnf {variables} {len(rows)}\n' +
                           ''.join(' '.join(map(str, row))+' 0\n' for row in rows))
            records.append(dict(stem=stem, minimum_distance=1, background=background,
                third_selected_index=6, fourth_selected_index=k, phase_K=34 if background else 10,
                free_phase_indices=free, variables=variables, clauses=len(rows),
                cnf_sha256=sha(cnf), free_selected_count=6, root57_color_cut=True,
                adjacent_density_cut=True, density_lemma_graph=premise['density_graph'],
                density_lemma_source_commit=premise['density_source_commit'],
                density_clauses_after_substitution=len(density),
                new_density_clauses=len(density-core),
                no_adjacency_cut=False, conditional_successor_cut=False,
                selected_run_start=True, next_phase_unfixed=True,
                mathematical_exclusion=False))
    result = dict(status='GENERATED_NOT_AUDITED', agent='six-vdw-2', role='researcher',
                  records=records, producer_sha256=sha(Path(__file__)),
                  seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
