"""Independent actual-point definitions, entire signed CNFs and ordinary phase cover.

No producer or compressed field-edge generator is imported here.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time
from common import COMMIT, REF, ROOT, pins, require, sha

def stem_for(index, background):
    return f'eleven-run7-gap-{index:02d}-b-{background}'

def gap_cover():
    # Place the two missing background positions among five length-seven gaps.
    deficits = [(tuple(2 if j == a else 0 for j in range(5))) for a in range(5)]
    deficits += [tuple(int(j in (a, b)) for j in range(5)) for a in range(5) for b in range(a+1, 5)]
    gaps = sorted(tuple(7-v for v in row) for row in deficits)
    require(len(set(gaps)) == 15 and all(sum(g) == 33 and 1 <= min(g) <= max(g) <= 7 for g in gaps), 'literal deficit cover differs')
    return gaps

def phase_for(gaps, background):
    selected = set(range(7)); cursor = 7
    for gap in gaps[:-1]:
        cursor += gap; selected.add(cursor); cursor += 1
    require(cursor + gaps[-1] == 44, 'cyclic endpoint differs')
    return [int((i in selected) != bool(background)) for i in range(44)]

def cyclic_runs(bits, value):
    starts = [i for i in range(len(bits)) if bits[i] == value and bits[(i-1) % len(bits)] != value]
    lengths = []
    for start in starts:
        length = 0
        while length < len(bits) and bits[(start+length) % len(bits)] == value:
            length += 1
        lengths.append(length)
    return starts, lengths

def literal_field():
    require(all(617 % divisor for divisor in range(2, 25)), '617 not prime')
    require(len({pow(3, exponent, 617) for exponent in range(616)}) == 616, '3 not primitive')
    subgroup = {pow(3, 88*j, 617) for j in range(7)}
    require(len(subgroup) == 7 and {pow(3, 44, 617)*h % 617 for h in subgroup} == {-h % 617 for h in subgroup}, 'antipodal H7 differs')
    require(pow(3, 19, 617) == 57, 'root57 quotient direction differs')
    slots = {}
    for lower in range(44):
        for side in (0, 1):
            for h in subgroup:
                point = (-1 if side else 1)*pow(3, lower, 617)*h % 617
                require(point not in slots, 'overlapping actual cosets')
                slots[point] = lower, side
    require(set(slots) == set(range(1, 617)), 'actual616-point partition incomplete')
    supports = set(); removed = kept = 0
    for start in range(617):
        for step in range(1, 617):
            points = [(start+j*step) % 617 for j in range(7)]
            if 0 in points:
                removed += 1; continue
            kept += 1
            edge = tuple(sorted({slots[x] for x in points}))
            require(len({i % 2 for i, side in edge}) == 2, 'independent quadratic-residue control differs')
            supports.add(edge)
    require((kept, removed, len(supports)) == (375760, 4312, 26488), 'whole actual AP census differs')
    return slots, supports

def semantic_rows(slots, supports, phase):
    def signed(point):
        i, side = slots[point]
        return (i+1)*(-1 if side and phase[i] else 1)
    def add_both(target, values):
        values = set(values)
        if values.isdisjoint({-v for v in values}):
            target.add(tuple(sorted(values))); target.add(tuple(sorted(-v for v in values)))
    field, color = set(), set()
    for edge in supports:
        add_both(field, [(i+1)*(-1 if side and phase[i] else 1) for i, side in edge])
    for end in range(88):
        add_both(color, [signed(pow(3, end-j, 617)) for j in range(7)])
        start = pow(3, end, 617)
        add_both(color, [signed(start*pow(57, j, 617) % 617) for j in range(8)])
    require(all(any(phase[(end-j) % 44] == wanted for j in range(8))
                for end in range(44) for wanted in (0, 1)), 'actual complete fixed phase8 fails')
    return field, color

def read_cnf(path):
    lines = path.read_text().splitlines()
    require(lines and len(lines[0].split()) == 4 and lines[0].split()[:2] == ['p', 'cnf'], 'invalid DIMACS header')
    variables, count = map(int, lines[0].split()[2:])
    require(variables == 44 and count >= 0 and len(lines) == count+1, 'DIMACS dimensions differ')
    rows = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        require(values and values[-1] == 0 and 0 not in values[:-1]
                and all(1 <= abs(v) <= 44 for v in values[:-1]), 'invalid signed DIMACS row')
        rows.append(tuple(sorted(values[:-1])))
    return rows

def audit_case(record, cnf, slots, supports, cache=None):
    index, background = record['gap_index'], record['background']
    require(isinstance(index, int) and not isinstance(index, bool) and 0 <= index < 15
            and type(background) is int and background in (0, 1), 'unsupported case identity')
    gaps = gap_cover()[index]; phase = phase_for(gaps, background)
    starts, selected_runs = cyclic_runs(phase, 1-background)
    _, background_runs = cyclic_runs(phase, background)
    require(starts[0] == 0 and selected_runs == [7, 1, 1, 1, 1]
            and background_runs == list(gaps) and phase[7] == phase[43] == background, 'independent cyclic runs differ')
    if cache is None:
        field, color = semantic_rows(slots, supports, phase)
    else:
        field, color = cache
    expected = dict(stem=stem_for(index, background), gap_index=index, background=background, background_gaps=list(gaps),
        phase=phase, phase_K=sum(phase), minority_count=11, normalized_minority_run=list(range(7)),
        minority_run_lengths=[7, 1, 1, 1, 1], background_run_count=5,
        unique_longest_minority_run=True, maximum_minority_run=7, maximum_background_run=7,
        phase_variables=0, lower_orientation_variables=44, independent_lower_colors_before_palette_gauge=44,
        variables=44, clauses=len(field | color)+1, cnf_sha256=sha(cnf), physical_field_clauses=len(field),
        universal_color_clauses=len(color), new_universal_color_clauses=len(color-field),
        only_global_y0_zero=True, gauge_clauses=[[-1]], root3_color_cut=True, root57_color_cut=True,
        nonconstant_phase8_checked=True, phase8_residual_clauses=0,
        isolated_eleven_gap4_rule_used=False, exact_TEN_rules_used=False,
        prior_adjacent_rule_used_as_numerical_cut=False, proposed_run7_exclusion_used=False,
        unrelated_family_cut=False, unpublished_exclusion_used_as_input=False,
        prior_adjacent_ref=REF, source_commit=COMMIT, mathematical_exclusion=False)
    require(record == expected, 'ENTIRE definition/phase/cut/gauge/identity record differs')
    require(Counter(read_cnf(cnf)) == Counter(list(field | color) + [(-1,)]), 'ENTIRE independent signed field/window/gauge multiset differs')
    return expected

def ordinary_cover_controls(slots):
    gaps = gap_cover(); normalized = [phase_for(g, 0) for g in gaps]
    discovered = set()
    examined = 0
    # Independent literal placement of every remaining four minority positions.
    for other in itertools.combinations(range(8, 43), 4):
        examined += 1
        selected = list(range(7)) + list(other)
        distances = [(selected[(j+1) % 11]-selected[j]) % 44 for j in range(11)]
        if max(distances) > 8:
            continue
        bits = [int(i in selected) for i in range(44)]
        starts, lengths = cyclic_runs(bits, 1)
        require(starts[0] == 0 and lengths == [7, 1, 1, 1, 1], '33 background bits failed to force four singleton runs')
        require(all(len({bits[(end-j) % 44] for j in range(8)}) == 2 for end in range(44)), 'literal phase8 wrap differs')
        discovered.add(tuple(bits))
    require(examined == 52360 and discovered == {tuple(w) for w in normalized}, 'all literal normalized phase placements not covered')
    all_gap_vectors = [g for g in itertools.product(range(1, 8), repeat=5) if sum(g) == 33]
    require(all_gap_vectors == gaps, 'full16807 gap-tuple reconstruction differs')
    stream = b''; scalar_checks = 0
    for bits in normalized:
        for background in (0, 1):
            phase = [v ^ background for v in bits]; stream += (''.join(map(str, phase))+'\n').encode()
            rotations = {tuple(phase[r:]+phase[:r]) for r in range(44)}
            require(len(rotations) == 44, 'unique longest run rotation cover failed')
            # Compare actual scalar maps as expressions in 44 unconstrained lower colors.
            # Each pair (variable index, constant) means x_index XOR constant.
            for shift in range(44):
                new_phase = phase[shift:] + phase[:shift]
                lower = [((i+shift) % 44, phase[(i+shift) % 44] if i+shift >= 44 else 0) for i in range(44)]
                for point, (i, side) in slots.items():
                    j, old_side = slots[point*pow(3, shift, 617) % 617]
                    require((lower[i][0], lower[i][1] ^ (new_phase[i] if side else 0))
                            == (j, phase[j] if old_side else 0), 'literal symbolic scalar transport differs')
                    scalar_checks += 1
    rotations = {tuple(w[r:]+w[:r]) for w in normalized for r in range(44)}
    require(len(rotations) == 660, 'incomplete labeled phase rotation cover')
    # Upper substitution and the sole global palette gauge preserve the phase exactly.
    truth_rows = 0
    for low, phase, palette in itertools.product((0, 1), repeat=3):
        high = low ^ phase
        require((low ^ high) == phase and ((low ^ palette) ^ (high ^ palette)) == phase, 'XOR/palette truth differs')
        truth_rows += 1
    return dict(ordered_gap_vectors=15, gap_tuples_examined=16807, literal_four_position_placements=examined,
                normalized_phase_words_per_background=15, labeled_phase_words_per_background=660,
                total_heads=30, independent_actual_scalar_expression_checks=scalar_checks,
                independent_lower_colors_before_palette_gauge=44, XOR_palette_truth_rows=truth_rows,
                phase_stream_sha256=hashlib.sha256(stream).hexdigest(), necessary_phases_are_field_colorings=False)

def validate_cover(produced):
    expected_cases = [(i, b) for i in range(15) for b in (0, 1)]
    require(set(produced) == {'agent', 'role', 'status', 'producer_sha256', 'total_heads', 'records', 'seconds'}
            and produced['agent'] == 'six-vdw-2' and produced['role'] == 'researcher'
            and produced['status'] == 'GENERATED_NOT_AUDITED' and produced['total_heads'] == 30
            and produced['producer_sha256'] == sha(ROOT / 'generate.py')
            and [(r['gap_index'], r['background']) for r in produced['records']] == expected_cases,
            'incomplete30-head whole producer coverage')
    hashes = {r['cnf_sha256'] for r in produced['records']}
    require(len(hashes) == 30 and not hashes.intersection(pins()['frozen_prior_cnfs']), 'duplicate/frozen native coverage')

def audit_work(work, batch=None, controls=False):
    began = time.monotonic(); pins()
    produced = json.loads((work / 'models.json').read_text()); validate_cover(produced)
    slots, supports = literal_field()
    records = []
    if not controls:
        require(type(batch) is int and 0 <= batch < 5, 'preselected disjoint six-head audit batch required')
        records = [audit_case(record, work / (record['stem'] + '.cnf'), slots, supports)
                   for record in produced['records'][6*batch:6*batch+6]]
    control_record = ordinary_cover_controls(slots) if controls else None
    result = dict(agent='six-vdw-2', role='researcher', status='INDEPENDENT_DEFINITIONS_CHECKED',
        literal_field_points=616, literal_kept_APs=375760, omitted_zero_APs=4312,
        distinct_physical_supports=26488, bounded_batch=batch, records=records,
        ordinary_cover_controls=control_record, mathematical_exclusion=False,
        seconds=time.monotonic()-began, maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    mode = 'optimized' if not __debug__ else 'normal'
    name = f'audit-{mode}-controls.json' if controls else f'audit-{mode}-batch-{batch}.json'
    (work / name).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'records'}), flush=True)

def witness(work, stem):
    pins(); records = json.loads((work / 'models.json').read_text())['records']
    selected = [r for r in records if r['stem'] == stem]; require(len(selected) == 1, 'witness case missing')
    record = selected[0]; cnf = work / (stem+'.cnf'); slots, supports = literal_field()
    audit_case(record, cnf, slots, supports)
    bits = json.loads(cnf.with_suffix('.model.json').read_text())
    require(len(bits) == 44 and all(type(v) is int and v in (0, 1) for v in bits) and bits[0] == 0, 'candidate44-color domain/gauge differs')
    require(all(any(bits[abs(v)-1] == int(v > 0) for v in row) for row in read_cnf(cnf)), 'candidate whole signed model fails')
    actual = {point: bits[i] ^ (record['phase'][i] if side else 0) for point, (i, side) in slots.items()}
    for point in range(1, 617):
        require(all(actual[point*pow(3, 88*j, 617) % 617] == actual[point] for j in range(7)), 'candidate H7 invariance fails')
    checked = 0
    for start in range(617):
        for step in range(1, 617):
            points = [(start+j*step) % 617 for j in range(7)]
            if 0 in points:
                continue
            require(len({actual[x] for x in points}) == 2, 'candidate actual monochromatic AP7')
            checked += 1
    require(checked == 375760, 'witness literal AP coverage incomplete')
    result = dict(status='INDEPENDENT_ACTUAL_FIELD_WITNESS', stem=stem, lower_colors=bits,
                  actual616_colors=[actual[x] for x in range(1, 617)], checked_APs=checked,
                  interval3704_witness=False, global_W_bound=False, mathematical_exclusion=False)
    (work / (stem+'.witness.json')).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'actual616_colors'}), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--batch', type=int); parser.add_argument('--controls', action='store_true')
    parser.add_argument('--witness'); args = parser.parse_args()
    if args.witness:
        witness(args.work.absolute(), args.witness)
    else:
        audit_work(args.work.absolute(), args.batch, args.controls)
