"""Untrusted log/scaling generator; audit.py does not import this module."""
import argparse
import itertools
import json
from pathlib import Path
import time
from common import load_encoder, require, sha


def neg(value):
    return not value if isinstance(value, bool) else -value


def put(target, values):
    if any(value is True for value in values):
        return
    row = {value for value in values if value is not False}
    if not any(-value in row for value in row):
        target.add(tuple(sorted(row)))


def prefix_counter(inputs, base):
    previous = {0: True}
    rows = set()
    cursor = base
    for i, value in enumerate(inputs, 1):
        current = {0: True}
        for k in range(1, min(i, 6) + 1):
            cursor += 1
            a, b, z = previous.get(k, False), previous[k-1], cursor
            for row in ((neg(a), z), (neg(value), neg(b), z),
                        (a, value, -z), (a, b, -z)):
                put(rows, row)
            current[k] = z
        previous = current
    put(rows, [previous[5]])
    put(rows, [-previous[6]])
    return rows, cursor


def gap_profiles():
    rooted = [t for t in itertools.product((5, 6, 7), repeat=7) if sum(t) == 37]
    return sorted({min(t[j:] + t[:j] for j in range(7)) for t in rooted})


def fixed_neighborhood(distance, background):
    fixed = {0: 1-background, distance: 1-background}
    for anchor in (0, distance):
        for step in range(1, distance):
            for point in ((anchor + step) % 44, (anchor - step) % 44):
                require(point not in (0, distance), 'inconsistent neighborhood')
                fixed[point] = background
    fixed[43] = background
    return fixed


def write_model(work, stem, variables, groups, details):
    all_rows = set().union(*groups.values())
    rows = sorted(all_rows, key=lambda c: (len(c), c)) + [(-1,)]
    cnf = work / (stem + '.cnf')
    cnf.write_text(f'p cnf {variables} {len(rows)}\n' +
                   ''.join(' '.join(map(str, row)) + ' 0\n' for row in rows))
    return dict(stem=stem, variables=variables, clauses=len(rows),
                cnf_sha256=sha(cnf), groups={k: len(v) for k, v in groups.items()},
                **details)


def generate(work):
    require(not work.exists(), 'fresh external work directory required')
    work.mkdir(parents=True)
    start = time.monotonic()
    edges = load_encoder().field_edges()
    records = []
    for background in (0, 1):
        for case, gaps in enumerate(gap_profiles(), 1):
            positions = [0]
            for gap in gaps[:-1]:
                positions.append(positions[-1] + gap + 1)
            phases = [background ^ int(i in positions) for i in range(44)]
            colors = list(range(1, 45)) + [
                (i+1) * (-1 if phases[i] else 1) for i in range(44)]
            field, color = set(), set()
            for edge in edges:
                values = [colors[i] for i in edge]
                put(field, values)
                put(field, [-v for v in values])
            for i in range(88):
                values = [colors[(i+j) % 88] for j in range(7)]
                put(color, values)
                put(color, [-v for v in values])
            records.append(write_model(work, f'b-{background}-case-{case}', 44,
                dict(field=field, color=color), dict(background=background,
                phase_K=37 if background else 7, majority_gaps=list(gaps))))
    for distance in range(5, 0, -1):
        for background in (0, 1):
            fixed = fixed_neighborhood(distance, background)
            free = [i for i in range(44) if i not in fixed]
            n = len(free)
            index = {point: j for j, point in enumerate(free)}
            colors = list(range(1, 45)) + [
                (i+1)*(-1 if fixed[i] else 1) if i in fixed else 45+index[i]
                for i in range(44)]
            phases = [bool(fixed[i]) if i in fixed else 45+n+index[i]
                      for i in range(44)]
            field, color, phase, spacing, xor = (set() for _ in range(5))
            for edge in edges:
                values = [colors[i] for i in edge]
                put(field, values)
                put(field, [-v for v in values])
            for i in range(88):
                values = [colors[(i+j) % 88] for j in range(7)]
                put(color, values)
                put(color, [-v for v in values])
            for i in range(44):
                values = [phases[(i+j) % 44] for j in range(8)]
                put(phase, values)
                put(phase, [neg(v) for v in values])
                for step in range(1, distance):
                    values = [phases[i], phases[(i+step) % 44]]
                    put(spacing, values if background else [neg(v) for v in values])
            for i in free:
                a, b, s = i+1, 45+index[i], 45+n+index[i]
                xor.update(tuple(sorted(row)) for row in (
                    (a, b, -s), (a, -b, s), (-a, b, s), (-a, -b, -s)))
            counter, variables = prefix_counter([
                phases[i]*(-1 if background else 1) for i in free], 44+2*n)
            records.append(write_model(work, f'd-{distance}-b-{background}', variables,
                dict(field=field, color=color, phase=phase, spacing=spacing,
                     XOR=xor, counter=counter), dict(background=background,
                phase_K=37 if background else 7, minimum_distance=distance,
                free_phase_indices=free)))
    data = dict(status='GENERATED_NOT_AUDITED', agent='six-vdw-2', role='researcher',
                cases=records, seconds=time.monotonic()-start)
    (work / 'models.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(dict(status=data['status'], cases=len(records), seconds=data['seconds'])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    generate(parser.parse_args().work.absolute())
