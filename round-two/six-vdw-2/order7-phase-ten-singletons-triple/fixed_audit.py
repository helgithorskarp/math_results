"""Independent literal616-point audit and whole-CNF equivalence; no producer import."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import resource
import time
from common import COMMIT, REF, ROOT, SOURCE, pins, require, sha

PARAMETERS = [(gap, b) for gap in range(5) for b in (0, 1)]

def stem_for(gap, b):
    return f'length6-gap-{gap}-b-{b}'

def independently_fixed(gap, b):
    require((gap, b) in PARAMETERS, 'unsupported head')
    gaps = tuple(7-int(j == gap) for j in range(5))
    selected = [*range(6)] + [6+sum(gaps[:j])+j-1 for j in range(1, 5)]
    require(selected[-1]+gaps[-1]+1 == 44 and len(set(selected)) == 10,
            'incorrect actual positions')
    word = [1-b if j in selected else b for j in range(44)]
    return word, list(gaps), selected

def literal_field():
    require(all(617 % d for d in range(2, 25)), '617 is not prime')
    require(len({pow(3, e, 617) for e in range(616)}) == 616, '3 is not primitive')
    h = {pow(3, 88*j, 617) for j in range(7)}
    require(len(h) == 7 and {pow(3,44,617)*v % 617 for v in h} == {-v % 617 for v in h},
            'wrong H7 antipodal cosets')
    slots = {}
    for i in range(44):
        for side in (0, 1):
            for v in h:
                point = (-1 if side else 1)*pow(3,i,617)*v % 617
                require(point not in slots, 'overlapping actual cosets')
                slots[point] = (i, side)
    require(set(slots) == set(range(1,617)), 'missing actual field point')
    supports = set()
    kept = omitted = 0
    for a in range(617):
        for d in range(1,617):
            points = [(a+j*d) % 617 for j in range(7)]
            if 0 in points:
                omitted += 1
                continue
            kept += 1
            edge = tuple(sorted({slots[point] for point in points}))
            require(len({i % 2 for i,side in edge}) == 2, 'QR positive field control failed')
            supports.add(edge)
    require((kept,omitted,len(supports)) == (375760,4312,26488), 'incomplete literal AP census')
    return slots, supports

def semantic_rows(slots, supports, phase):
    def actual(point):
        index, side = slots[point]
        return (-1 if side and phase[index] else 1)*(index+1)
    def signed(index,side):
        return (-1 if side and phase[index] else 1)*(index+1)
    field,root3,root57 = set(),set(),set()
    def both(target,values):
        values = set(values)
        if not any(-value in values for value in values):
            target.add(tuple(sorted(values)))
            target.add(tuple(sorted(-value for value in values)))
    for edge in supports:
        both(field,[signed(index,side) for index,side in edge])
    for exponent in range(88):
        both(root3,[actual(pow(3,exponent-j,617)) for j in range(7)])
        point = pow(3,exponent,617)
        both(root57,[actual(point*pow(57,j,617) % 617) for j in range(8)])
    return field,root3,root57

def phase_checks(word,background):
    require(len(word) == 44 and all(type(x) is int and x in (0,1) for x in word),
            'invalid fixed phase domain')
    require(sum(x != background for x in word) == 10, 'not exactly TEN selected phases')
    checks = 0
    for i in range(44):
        require(len({word[(i+j) % 44] for j in range(8)}) == 2, 'phase8 fails')
        for width in (2,4):
            selected = [word[(i+j) % 44] != background for j in (-1,0,1,2,3,4)]
            true = (selected[0] or not selected[1] or not selected[2]
                    or (selected[3] if width == 2 else selected[4] or selected[5]))
            require(true, 'actual TWO/FOURTH4 implication fails')
            checks += 1
    return checks

def audit_case(record,cnf,slots,supports):
    gap,b = record['deficient_gap'],record['background']
    phase,gaps,selected = independently_fixed(gap,b)
    require(record['stem'] == stem_for(gap,b) and record['selected'] == selected
            and record['phases'] == phase and record['gaps'] == gaps
            and record['phase_K'] == sum(phase) and record['selected_phase_count'] == 10
            and record['variables'] == 44 and record['all_phases_fixed'] is True
            and record['phase_auxiliaries'] == record['counter_auxiliaries'] == record['color_auxiliaries'] == 0
            and record['only_global_y0_zero'] is True
            and record['actual_TWO_checked'] is True and record['actual_FOURTH4_checked'] is True
            and record['phase8_checked'] is True
            and all(record[name] is False for name in ('reflection_assumed','phase_exchange_assumed',
                'proposed_length6_exclusion_cut','proposed_no_adjacency_cut','unrelated_family_cut'))
            and record['premise_ref'] == REF and record['source_commit'] == COMMIT,
            'changed fixed-phase semantics or false theorem input')
    phase_truths = phase_checks(phase,b)
    field,root3,root57 = semantic_rows(slots,supports,phase)
    require([record['field_clauses'],record['root3_clauses'],record['root57_clauses']]
            == [len(field),len(root3),len(root57)], 'misstated substituted clause families')
    lines = cnf.read_text().splitlines()
    require(lines[0].split() == ['p','cnf','44',str(record['clauses'])], 'wrong original-color dimension')
    rows = []
    for line in lines[1:]:
        row = list(map(int,line.split()))
        require(row and row[-1] == 0 and all(1 <= abs(v) <= 44 for v in row[:-1]),
                'invalid DIMACS literal/domain')
        rows.append(tuple(sorted(row[:-1])))
    require(Counter(rows) == Counter(list(field|root3|root57)+[(-1,)])
            and len(rows) == record['clauses'] and sha(cnf) == record['cnf_sha256'],
            'entire literal-field substituted CNF differs')
    substitution_truths = 0
    for i in range(44):
        for lower in (0,1):
            upper = lower ^ phase[i]
            for side in (0,1):
                literal = (-1 if side and phase[i] else 1)*(i+1)
                require((lower ^ int(literal < 0)) == (upper if side else lower),
                        'exact actual upper/lower color substitution fails')
                substitution_truths += 1
    return dict(stem=record['stem'],variables=44,clauses=len(rows),cnf_sha256=sha(cnf),
                substituted_color_truths=substitution_truths,actual_phase_implications=phase_truths,
                field_clauses=len(field),root3_clauses=len(root3),root57_clauses=len(root57))

def cover_and_gauge_controls():
    tuples = list(itertools.product(range(1,8),repeat=5))
    feasible = [t for t in tuples if sum(t) == 34]
    require(len(tuples) == 16807 and len(feasible) == 5
            and set(feasible) == {tuple(7-int(j == k) for j in range(5)) for k in range(5)},
            'incomplete ordinary length6 gap cover')
    words = set()
    for gap,b in PARAMETERS:
        word,gaps,selected = independently_fixed(gap,b)
        for offset in range(44):
            rotated = tuple(word[(i-offset) % 44] for i in range(44))
            require(tuple(rotated[(i+offset) % 44] for i in range(44)) == tuple(word),
                    'rotation loses fixed-phase word')
            words.add((b,rotated))
    require(len(words) == 440, 'whole phase-word cover lost a unique length6 origin')
    gauge = 0
    for m in range(2,7):
        for bits in itertools.product((0,1),repeat=2*m):
            phase = [bits[i] ^ bits[i+m] for i in range(m)]
            for offset in range(2*m):
                values = [bits[(j+offset) % (2*m)] ^ bits[offset] for j in range(2*m)]
                require(values[0] == 0 and all(values[i+m] == values[i] ^ phase[(i+offset) % m]
                                             for i in range(m)), 'incomplete scalar/global gauge control')
                gauge += 1
    return len(tuples),len(feasible),len(words),gauge

def main(work):
    began = time.monotonic()
    pins()
    models = json.loads((work/'models.json').read_text())
    require(models['producer_sha256'] == sha(Path(__file__).with_name('fixed_generate.py')),
            'changed model producer')
    require([row['stem'] for row in models['records']] == [stem_for(*p) for p in PARAMETERS]
            and {p.name for p in work.glob('*.cnf')} == {stem_for(*p)+'.cnf' for p in PARAMETERS},
            'incomplete ten-head cover')
    slots,supports = literal_field()
    records = [audit_case(row,work/(row['stem']+'.cnf'),slots,supports) for row in models['records']]
    tuples,feasible,words,gauge = cover_and_gauge_controls()
    out = dict(agent='six-vdw-2',role='researcher',status='EXACT_H7_LENGTH6_FIXED10_DEFINITION_AUDIT',
               records=records,literal_APs=375760,removed_zero_APs=4312,signed_supports=26488,
               bounded_gap_tuples=tuples,feasible_gap_vectors=feasible,labeled_phase_words_both_values=words,
               signed_rotation_controls=gauge,lower_color_variables=44,
               phase_auxiliaries=0,counter_auxiliaries=0,
               synthetic_controls_do_not_prove_ordinary_coverage=True,
               proposed_length6_exclusion_cut=False,proposed_no_adjacency_cut=False,
               unrelated_family_cut=False,seconds=time.monotonic()-began,
               maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/('audit-normal.json' if __debug__ else 'audit-optimized.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work',required=True,type=Path)
    main(p.parse_args().work.absolute())
