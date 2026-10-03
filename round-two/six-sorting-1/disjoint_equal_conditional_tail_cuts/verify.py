"""Independent scalar reconstruction of each literal original-domain witness.

No packed producer/profile import. Numeric values, distinct HIGH ranks,
marked gate counts and whole-original identities are replayed from definitions.
Arbitrary finite-word monotonicity, conservation and leading-zero preservation
are proved by induction in PROOF.md; finite checks corroborate that argument.
"""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent
BASE = [[0,11],[1,7],[2,4],[3,5],[8,9],[10,12],[0,2],[3,6],[4,12],[5,7],
        [8,10],[0,8],[1,3],[2,5],[4,9],[6,11],[7,12],[0,1],[2,10],[4,8],
        [3,6],[9,11],[11,12],[3,4],[1,2],[1,3]]
ROUTES = [([[5,6],[7,10]],[1,2]), ([[5,6],[9,10]],[0,6]),
          ([[5,7],[6,10]],[1,2]), ([[5,9],[6,10]],[0,6]),
          ([[5,10],[6,7]],[1,2]), ([[5,10],[6,9]],[0,6])]


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def step(row, a, b):
    out = list(row)
    if out[a] > out[b]:
        out[a], out[b] = out[b], out[a]
    return out


def seed_rows(word, high):
    free = [i for i in range(13) if i not in high]
    rows, touches, active = [], set(), 0
    for x in range(2048):
        row = [0]*13
        row[high[0]], row[high[1]] = 2, 3
        for j, p in enumerate(free):
            row[p] = x >> j & 1
        hit = 0
        for t, (a, b) in enumerate(word):
            marked = row[a] > 1 or row[b] > 1
            hit |= int(marked) << t
            active |= int(not marked and row[a] > row[b]) << t
            row = step(row, a, b)
        touches.add(hit)
        rows.append(row)
    need(len(touches) == 1, 'Free-dependent original marked route')
    touch = next(iter(touches))
    identity = ((1 << len(word))-1) & ~(touch | active)
    return rows, free, touch, identity


def main():
    start = time.monotonic()
    f = json.loads((ROOT/'fixture.json').read_text())
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT/'work/proposal.json'
    proposal = json.loads(path.read_text())
    claimed = proposal['finite']
    need(digest(claimed) == proposal['finite_sha256'], 'Changed complete finite transport binding')
    need(f['ports'] == 13 and f['B23']+f['LOW_suffix'] == BASE and
         f['ordinary_HIGH_unit_ports'] == [5,6,7,9,10] and f['barrier_port'] == 11 and
         f['held_top_port'] == 12 and f['fixed_head_ports'] == [2,3,4] and
         f['imported_S11_lower_bound'] == 35 and f['total_comparator_ceiling'] == 44,
         'Wrong literal prefix or imported theorem fixture')
    need([(r['prior_HIGH_merges'], r['original_HIGH_inputs']) for r in f['routes']] == ROUTES,
         'Wrong six-route theorem fixture')
    need(len(claimed['route_records']) == 6, 'Missing or substituted actual route')
    expected_records = []
    samples = []
    moved_samples = seed_assignments = extended_assignments = 0
    for route_index, (branch, high) in enumerate(ROUTES):
        need(time.monotonic()-start < 45, 'Operational guard: incomplete scalar replay')
        record = claimed['route_records'][route_index]
        need(record['prior_HIGH_merges'] == branch and record['original_HIGH_inputs'] == high,
             'Wrong original HIGH witness or literal route')
        roots = sorted([branch[0][1], branch[1][1]])
        slack = next(p for p in [5,6,7,9,10] if p not in branch[0]+branch[1])
        dead = [p for p in range(2,12) if p not in roots+[slack,11]]
        word = BASE+branch
        rows, free, touch, identity = seed_rows(word, high)
        seed_assignments += 2048
        marks = [[p, rows[0][p]] for p in range(13) if rows[0][p] > 1]
        need(marks[-1] == [12,3] and marks[0] in [[q,2] for q in roots] and
             all([[p,row[p]] for p in range(13) if row[p] > 1] == marks for row in rows),
             'Actual original marked ranks differ')
        D, R = touch.bit_count(), identity.bit_count()
        need(D == 7 and R == 0 and record['actual_original_seed_D'] == D and
             record['actual_original_seed_R'] == R, 'False original seed D/R cost')
        need(all(row[slack] <= row[11] <= 1 for row in rows), 'Missing actual root/barrier relation')
        conditional = [x for x, row in enumerate(rows) if row[11] == 0]
        patterns = sorted({sum(rows[x][p] << j for j,p in enumerate(dead)) for x in conditional})
        greatest = 0
        for x in patterns:
            greatest |= x
        need(greatest in patterns and greatest.bit_count() == 2 and greatest & 7 == 0,
             'Actual conditional maximum lacks the claimed weight and leading zeros')
        need(record['complete_original_conditional_assignments'] == conditional,
             'Missing or substituted original conditional assignment')
        need(record['attained_conditional_maximum_mask'] == greatest and record['maximum_weight'] == 2,
             'False attained conditional maximum')
        need(record['fixed_head_ports'] == dead[:3] == [2,3,4], 'False fixed zero-head labels')
        for env in record['conservative_output_envelope']:
            v = env['output_mask']
            need(0 <= v < 64 and v.bit_count() == 2 and v & 7 == 0,
                 'False conservative output envelope')
            for b in env['bindings']:
                p = b['head_port']
                need(p in dead and not v >> dead.index(p) & 1,
                     'Actual nonzero output used as a zero head')
                r = max(p, slack)
                need(b['actual_head'] == sorted([p,slack]) and b['actual_head_root'] == r,
                     'Actual singleton head root was not routed')
                need(b['literal_balanced_tail'] == [roots,[r,11],[roots[-1],11]] and
                     b['identity_tail_index'] == 1 and b['additional_marked_tail_touches'] == 2,
                     'False literal tail or original identity position')
        envelope = []
        for v in range(64):
            if v.bit_count() != 2 or v & 7:
                continue
            zeros = [dead[j] for j in range(6) if not v >> j & 1]
            need(len(zeros) == 4 and all(p in zeros for p in [2,3,4]), 'Zero-head census differs')
            adaptive = min(p for p in zeros if p not in [2,3,4])
            bindings = [{'head_port':p, 'actual_head':sorted([p,slack]),
                         'actual_head_root':max(p,slack),
                         'literal_balanced_tail':[roots,[max(p,slack),11],[max(roots),11]],
                         'identity_tail_index':1, 'additional_marked_tail_touches':2} for p in zeros]
            envelope.append({'output_mask':v, 'zero_head_ports':zeros,
                             'adaptive_extra_head':adaptive, 'bindings':bindings})
        expected = {'prior_HIGH_merges':branch, 'literal_seed_sha256':digest(word),
                    'live_pair_roots':roots, 'slack_root':slack, 'dead_preparation_ports':dead,
                    'original_HIGH_inputs':high, 'original_HIGH_mask':sum(1 << p for p in high),
                    'original_free_input_ports':free, 'actual_seed_marked_ports_and_ranks':marks,
                    'actual_original_seed_D':D, 'actual_original_seed_R':R,
                    'actual_original_seed_touch_mask':touch, 'actual_original_seed_identity_mask':identity,
                    'full2048_original_seed_rows_sha256':digest(rows),
                    'full_original_slack_le_barrier':True,
                    'complete_original_conditional_assignments':conditional,
                    'complete_conditional_dead_patterns':patterns,
                    'attained_conditional_maximum_mask':greatest,
                    'maximum_original_witness_assignment':next(x for x in conditional
                        if sum(rows[x][p] << j for j,p in enumerate(dead)) == greatest),
                    'maximum_weight':2, 'fixed_head_ports':[2,3,4],
                    'conservative_output_envelope':envelope,
                    'minimum_excluded_head_count':4, 'certified_total_lower_bound':D+R+2+1+35}
        need(record == expected, 'Complete actual scalar route record differs')
        expected_records.append(expected)
        # Actual F instances exercise all output-envelope possibilities and
        # both orders of the disjoint first two tail gates. They corroborate
        # the written arbitrary-word proof, rather than bounding F's length.
        preparations = [[], [[dead[3],dead[5]]], [[dead[3],dead[4]],[dead[4],dead[5]]]]
        for prep in preparations:
            vrow = [(greatest >> j) & 1 for j in range(6)]
            for a,b in prep:
                vrow = step(vrow,dead.index(a),dead.index(b))
            zeros = [dead[j] for j in range(6) if vrow[j] == 0]
            for p in zeros:
                r = max(p,slack)
                first = [roots,[r,11]]
                for reverse in (False,True):
                    tail = (list(reversed(first)) if reverse else first)+[[roots[-1],11]]
                    extension = prep+[sorted([p,slack])]+tail
                    hits, active, finals = set(),0,[]
                    identity_position = len(prep)+1+(0 if reverse else 1)
                    for seed in rows:
                        row = list(seed);hit = 0
                        for t,(a,b) in enumerate(extension):
                            marked = row[a] > 1 or row[b] > 1
                            hit |= int(marked) << t
                            active |= int(not marked and row[a] > row[b]) << t
                            row = step(row,a,b)
                        hits.add(hit);finals.append(row)
                    need(len(hits) == 1, 'Actual sample has free-dependent marked route')
                    hit = next(iter(hits));ids = ((1 << len(extension))-1) & ~(hit | active)
                    need(hit.bit_count() == 2 and ids >> identity_position & 1 and
                         not hit >> identity_position & 1 and
                         all([[q,x] for q,x in enumerate(row) if x > 1] == [[11,2],[12,3]] for row in finals),
                         'Actual literal sample lacks its original unmarked identity and two passages')
                    samples.append({'route':route_index, 'preparation':prep, 'head':sorted([p,slack]),
                                    'tail':tail, 'extension_D':2, 'extension_identity_mask':ids,
                                    'full2048_final_rows_sha256':digest(finals)})
                    extended_assignments += 2048
                    moved_samples += int(p > slack)
    expected = {'literal_B23_LOW_sha256':digest(BASE), 'route_records':expected_records, 'total_routes':6,
                'fixed_head_tail_exclusions_per_preparation':18,
                'minimum_head_tail_exclusions_per_preparation_across_routes':24,
                'output_envelope_claimed_exactly_reachable':False,
                'arbitrary_preparation_length_allowed':True, 'suffix_depth_restricted':False,
                'other_balanced_tails_excluded':False, 'entire_six_routes_excluded':False,
                'global_size44_exclusion_claimed':False}
    need(claimed == expected, 'Outside claimed scope or complete finite fields differ')
    conservation = monotonicity = leading_zero = 0
    for a,b in combinations(range(6),2):
        images = []
        for x in range(64):
            row = step([(x >> j) & 1 for j in range(6)],a,b)
            out = sum(v << j for j,v in enumerate(row));images.append(out)
            need(out.bit_count() == x.bit_count(), 'Local comparator fails weight conservation')
            conservation += 1
            if x & 7 == 0:
                need(out & 7 == 0, 'Local standard comparator loses leading-zero prefix')
                leading_zero += 1
        for x in range(64):
            for y in range(64):
                if x & ~y == 0:
                    need(images[x] & ~images[y] == 0, 'Local comparator fails coordinatewise monotonicity')
                    monotonicity += 1
    finite = {'producer_finite_sha256':proposal['finite_sha256'], 'whole_producer_finite_matched':True,
              'complete_original_seed_assignments':seed_assignments,
              'literal_sample_count':len(samples), 'literal_sample_original_assignments':extended_assignments,
              'actual_moved_head_sample_count':moved_samples,
              'entire_literal_sample_records_sha256':digest(samples),
              'conservation_controls':conservation, 'monotonicity_controls':monotonicity,
              'leading_zero_controls':leading_zero, 'arbitrary_word_proof_claimed_by_induction':True,
              'preparation_catalogue_used':False, 'independent_person_review_claimed':False,
              'formalized':False}
    result = {'agent':'six-sorting-1', 'role':'researcher',
              'status':'SIX_ROUTE_ENTIRE_ORIGINAL_CUBES_AND_LITERAL_TAIL_BINDINGS_SCALAR_VERIFIED',
              'finite':finite, 'finite_sha256':digest(finite), 'seconds':time.monotonic()-start}
    if len(sys.argv) <= 1:
        suffix = '-O' if not __debug__ else ''
        (ROOT/('work/checked'+suffix+'.json')).write_text(json.dumps(result,indent=2)+'\n')
        (ROOT/('work/samples'+suffix+'.json')).write_text(json.dumps(samples,indent=2)+'\n')
    print(json.dumps({'finite':finite,'finite_sha256':result['finite_sha256'],'seconds':result['seconds']}),flush=True)


if __name__ == '__main__':
    main()
