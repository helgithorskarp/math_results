"""Fresh (2,3) then third-gap 2..8 models, both selected phase values."""
import argparse
import json
from pathlib import Path
import time

from common import load_encoder, require, sha, endpoint_generator
old = endpoint_generator()
neg, put = old.neg, old.put


def head_fixed(k, background):
    require(7 <= k <= 13, 'unsupported fourth selected index')
    fixed = {0: 1-background, 2: 1-background, 5: 1-background, k: 1-background}
    for i in (43, 1, 3, 4, 6, k+1):
        fixed[i] = background
    for i in range(6, k):
        fixed[i] = background
    require(sum(v != background for v in fixed.values()) == 4,
            'wrong selected head count')
    return fixed


def prefix(inputs, base):
    previous = {0: True}
    rows, cursor = set(), base
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
    for k in range(13, 6, -1):
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
            field, color, phase, spacing, xor, successor = (set() for _ in range(6))
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
                values = [phases[i], phases[(i+1) % 44]]
                put(spacing, values if background else [neg(v) for v in values])
                selected = [neg(phases[(i+d) % 44]) if background
                            else phases[(i+d) % 44] for d in (0, 2, 4, 5)]
                put(successor, [neg(selected[0]), neg(selected[1]), selected[2], selected[3]])
            for i in free:
                a, b, s = i+1, 45+index[i], 45+n+index[i]
                xor.update(tuple(sorted(row)) for row in
                           ((a, b, -s), (a, -b, s), (-a, b, s), (-a, -b, -s)))
            counter, variables = prefix([phases[i]*(-1 if background else 1)
                                         for i in free], 44+2*n)
            require(n == 41-k and variables == 23+9*n, 'wrong exact-six head dimension')
            rows = sorted(field | color | phase | spacing | xor | counter | successor,
                          key=lambda row: (len(row), row)) + [(-1,)]
            stem = f'gap-2-3-next-{k}-b-{background}'
            cnf = work/(stem+'.cnf')
            cnf.write_text(f'p cnf {variables} {len(rows)}\n' +
                           ''.join(' '.join(map(str, row))+' 0\n' for row in rows))
            records.append(dict(stem=stem, minimum_distance=2, background=background,
                fourth_selected_index=k, third_gap=k-5, phase_K=34 if background else 10,
                free_phase_indices=free, variables=variables, clauses=len(rows),
                cnf_sha256=sha(cnf), free_selected_count=6, root57_color_cut=True,
                successor_cut=True, successor_shift_count=44,
                successor_clauses=len(successor), mathematical_exclusion=False))
    result = dict(status='GENERATED_NOT_AUDITED', agent='six-vdw-2', role='researcher',
                  records=records, producer_sha256=sha(Path(__file__)),
                  seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
