"""Literal-field and gate-truth auditor; imports neither generator nor log helpers."""
import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path
import resource
import time
from common import HERE, pins, require, sha


def literal_field():
    require(all(617 % d for d in range(2, 25)), 'field must be prime')
    require(len({pow(3, e, 617) for e in range(616)}) == 616, 'root not primitive')
    subgroup = {pow(3, 88*j, 617) for j in range(7)}
    require(len(subgroup) == 7 and {pow(3, 44, 617)*h % 617 for h in subgroup}
            == {-h % 617 for h in subgroup}, 'wrong antipodal cosets')
    slots = {}
    for i in range(44):
        for h in subgroup:
            for side in (0, 1):
                point = pow(3, i, 617)*h*(-1 if side else 1) % 617
                require(point not in slots, 'overlapping literal cosets')
                slots[point] = i, side
    require(set(slots) == set(range(1, 617)), 'incomplete literal partition')
    supports = set()
    retained = removed = 0
    for a in range(617):
        for difference in range(1, 617):
            points = [(a+j*difference) % 617 for j in range(7)]
            if 0 in points:
                removed += 1
            else:
                retained += 1
                supports.add(tuple(sorted({slots[p] for p in points})))
    require((retained, removed, len(supports)) == (375760, 4312, 26488),
            'wrong literal AP census')
    # Actual QR colors of signed cosets are i modulo2, since -1 is square.
    require(all(len({i % 2 for i, side in edge}) == 2 for edge in supports),
            'positive QR control failed')
    return slots, supports


def packing_cover():
    rooted = []
    for extras in itertools.combinations_with_replacement(range(7), 2):
        rooted.append(tuple(5+extras.count(j) for j in range(7)))
    canonical = sorted({min(t[j:]+t[:j] for j in range(7)) for t in rooted})
    require(len(rooted) == 28 and len(canonical) == 4, 'incomplete packing cover')
    labeled = set()
    for gaps in rooted:
        points = [sum(gaps[:j])+j for j in range(7)]
        require(points[-1]+gaps[-1]+1 == 44, 'wrong cyclic length')
        labeled.update(tuple(sorted((v+r) % 44 for v in points)) for r in range(44))
    require(len(labeled) == 176, 'wrong labeled packing cover')
    for points in labeled:
        gaps = tuple((points[(j+1) % 7]-points[j]) % 44-1 for j in range(7))
        require(sum(gaps) == 37 and min(gaps) >= 5, 'wrong packing word')
        require(any(gaps[j:]+gaps[:j] in canonical for j in range(7)),
                'missing packing anchor')
    return canonical


def independent_fixed(distance, background):
    result = {}
    for i in range(44):
        if i in (0, distance):
            result[i] = 1-background
        elif i == 43 or any(min((i-a) % 44, (a-i) % 44) < distance
                            for a in (0, distance)):
            result[i] = background
    return result


def simplified(target, values):
    if any(v is True for v in values):
        return
    values = {v for v in values if v is not False}
    if not any(-v in values for v in values):
        target.add(tuple(sorted(values)))


def expected_clauses(slots, supports, fixed, distance=None):
    free = [i for i in range(44) if i not in fixed]
    n = len(free)
    upper = {i: 45+j for j, i in enumerate(free)}
    phase_vars = {i: 45+n+j for j, i in enumerate(free)}

    def signed(i, side):
        if not side:
            return i+1
        return (i+1)*(-1 if fixed[i] else 1) if i in fixed else upper[i]

    field, color, phase, spacing, xor = (set() for _ in range(5))
    for edge in supports:
        values = {signed(i, side) for i, side in edge}
        if not any(-v in values for v in values):
            field.add(tuple(sorted(values)))
            field.add(tuple(sorted(-v for v in values)))
    for end in range(88):
        values = {signed(*slots[pow(3, end-j, 617)]) for j in range(7)}
        if not any(-v in values for v in values):
            color.add(tuple(sorted(values)))
            color.add(tuple(sorted(-v for v in values)))
    if distance is not None:
        background = fixed[43]
        for end in range(44):
            indices = [slots[pow(3, end-j, 617)][0] for j in range(8)]
            for wanted in (0, 1):
                if not any(i in fixed and fixed[i] == wanted for i in indices):
                    phase.add(tuple(sorted(phase_vars[i]*(1 if wanted else -1)
                                           for i in indices if i not in fixed)))
        for i, j in itertools.combinations(range(44), 2):
            if min((i-j) % 44, (j-i) % 44) < distance:
                if not any(v in fixed and fixed[v] == background for v in (i, j)):
                    spacing.add(tuple(sorted(phase_vars[v]*(1 if background else -1)
                                             for v in (i, j) if v not in fixed)))
        for i in free:
            names = i+1, upper[i], phase_vars[i]
            for bits in itertools.product((0, 1), repeat=3):
                if bits[2] != bits[0] ^ bits[1]:
                    xor.add(tuple(sorted(-v if bit else v for v, bit in zip(names, bits))))
    return set().union(field, color, phase, spacing, xor), n


def audit_counter(rows, n, background):
    base = 44+2*n
    cells = {(i, k): base+(i*(i-1)//2 if i <= 6 else 6*(i-1)-15)+k
             for i in range(1, n+1) for k in range(1, min(i, 6)+1)}
    end = base+6*n-15
    require(set(cells.values()) == set(range(base+1, end+1)), 'missing counter cells')
    units = {(cells[n, 5],), (-cells[n, 6],)}
    require({row for row in rows if len(row) == 1} == units, 'wrong exact-five units')
    accounted = set(units)
    truth_rows = 0
    for (i, k), output in cells.items():
        a = cells.get((i-1, k), False)
        b = True if k == 1 else cells[i-1, k-1]
        x = (44+n+i)*(-1 if background else 1)
        local = {row for row in rows if len(row) > 1
                 and max(abs(v) for v in row) == output}
        domain = {abs(v) for v in (a, b, x, output) if not isinstance(v, bool)}
        require(local and all(set(map(abs, row)) <= domain for row in local),
                'missing gate or foreign gate input')
        for bits in itertools.product((0, 1), repeat=len(domain)):
            assignment = dict(zip(sorted(domain), bits))
            def value(v):
                return v if isinstance(v, bool) else assignment[abs(v)] ^ int(v < 0)
            relation = bool(assignment[output]) == bool(value(a) or (value(x) and value(b)))
            require(all(any(value(v) for v in row) for row in local) == relation,
                    'gate truth relation is incorrect')
            truth_rows += 1
        accounted.update(local)
    require(accounted == rows, 'unaccounted counter clause')
    return end, truth_rows


def controls():
    anchors = signed_rotations = thresholds = exact = 0
    for m in range(4, 13):
        for bits in itertools.product((0, 1), repeat=m):
            for background in (0, 1):
                positions = [i for i in range(m) if bits[i] != background]
                if not 2 <= len(positions) < m:
                    continue
                gaps = [(positions[(i+1) % len(positions)]-positions[i]) % m
                        for i in range(len(positions))]
                d = min(gaps)
                if d > 5:
                    continue
                anchor = (next(i for i in positions if bits[(i-1) % m] == background
                               and bits[(i+1) % m] != background) if d == 1
                          else positions[gaps.index(d)])
                word = [bits[(i+anchor) % m] for i in range(m)]
                require(word[0] == word[d] == 1-background and word[-1] == background,
                        'anchor lost a phase word')
                require(all(word[(a+r) % m] == background for a in (0, d)
                            for r in range(1-d, d) if r), 'forced neighborhood invalid')
                anchors += 1
    for m in range(2, 7):
        for bits in itertools.product((0, 1), repeat=2*m):
            phase = [bits[i] ^ bits[i+m] for i in range(m)]
            for r in range(2*m):
                rotated = [bits[(i+r) % (2*m)] ^ bits[r] for i in range(2*m)]
                require(rotated[0] == 0 and all(rotated[i+m] ==
                        rotated[i] ^ phase[(i+r) % m] for i in range(m)),
                        'signed rotation lost color orientations')
                signed_rotations += 1
    for m in range(1, 10):
        for bits in itertools.product((0, 1), repeat=m):
            for flip in (0, 1):
                cells = {}
                for i, bit in enumerate(bits, 1):
                    for k in range(1, min(i, 6)+1):
                        a = cells.get((i-1, k), False)
                        b = True if k == 1 else cells[i-1, k-1]
                        cells[i, k] = bool(a or ((bit ^ flip) and b))
                        require(cells[i, k] == (sum(x ^ flip for x in bits[:i]) >= k),
                                'tiny prefix threshold failed')
                        thresholds += 1
                require((cells.get((m, 5), False) and not cells.get((m, 6), False)) ==
                        (sum(x ^ flip for x in bits) == 5), 'tiny exact-five failed')
                exact += 1
    return dict(tiny_anchor_controls=anchors, signed_rotation_controls=signed_rotations,
                tiny_threshold_cells=thresholds, tiny_exact_counts=exact)


def audit(work):
    start = time.monotonic()
    pins()
    slots, supports = literal_field()
    profiles = packing_cover()
    expected = []
    for background in (0, 1):
        for case, gaps in enumerate(profiles, 1):
            points = {sum(gaps[:j])+j for j in range(7)}
            fixed = {i: background ^ int(i in points) for i in range(44)}
            expected.append((f'b-{background}-case-{case}', fixed, None, background, gaps))
    for distance in range(5, 0, -1):
        for background in (0, 1):
            expected.append((f'd-{distance}-b-{background}',
                             independent_fixed(distance, background), distance, background, None))
    metadata = json.loads((work / 'models.json').read_text())['cases']
    require([row['stem'] for row in metadata] == [row[0] for row in expected],
            'incomplete or duplicated endpoint cover')
    require({p.name for p in work.glob('*.cnf')} == {row[0]+'.cnf' for row in expected},
            'missing or unexpected endpoint CNF')
    checked = []
    for (stem, fixed, distance, background, gaps), record in zip(expected, metadata):
        cnf = work / (stem+'.cnf')
        lines = cnf.read_text().splitlines()
        header = lines[0].split()
        require(len(header) == 4 and header[:2] == ['p', 'cnf'], 'bad DIMACS header')
        variables, count = map(int, header[2:])
        rows = []
        for line in lines[1:]:
            values = list(map(int, line.split()))
            require(values and values[-1] == 0 and all(1 <= abs(v) <= variables
                    for v in values[:-1]), 'bad DIMACS row')
            rows.append(tuple(sorted(values[:-1])))
        semantic, n = expected_clauses(slots, supports, fixed, distance)
        truth_rows = 0
        if distance is None:
            require(variables == 44 and record['majority_gaps'] == list(gaps),
                    'wrong packing case')
        else:
            require(n == {1: 41, 2: 39, 3: 36, 4: 33, 5: 30}[distance], 'wrong neighborhood')
            require(record['minimum_distance'] == distance and record['free_phase_indices'] ==
                    [i for i in range(44) if i not in fixed], 'wrong branch coordinates')
            counter_rows = {row for row in rows if any(abs(v) > 44+2*n for v in row)}
            end, truth_rows = audit_counter(counter_rows, n, background)
            require(variables == end == 29+8*n, 'wrong counter dimension')
            semantic.update(counter_rows)
        require(Counter(rows) == Counter(list(semantic)+[(-1,)]) and count == len(rows),
                'entire literal-field clause multiset differs')
        require(record['background'] == background and record['phase_K'] == (37 if background else 7)
                and record['variables'] == variables and record['clauses'] == count
                and record['cnf_sha256'] == sha(cnf), 'incorrect model metadata')
        checked.append(dict(stem=stem, variables=variables, clauses=count,
            cnf_sha256=sha(cnf), counter_truth_rows=truth_rows,
            phase_inputs_before_cuts=math.comb(n, 5) if distance else 1))
    extra = controls()
    result = dict(status='EXACT_ENDPOINT_DEFINITION_AUDIT', agent='six-vdw-2', role='researcher',
        cases=checked, literal_APs=375760, removed_zero_APs=4312, signed_supports=26488,
        rooted_packing_profiles=28, packing_orbits=4, packing_phase_words_per_endpoint=176,
        seconds=time.monotonic()-start, maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        **extra)
    (work / ('audit-optimized.json' if not __debug__ else 'audit-normal.json')).write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    audit(parser.parse_args().work.absolute())
