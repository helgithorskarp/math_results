"""Separate scalar-set replay of every proposed original reserved identity.

No packed producer/profile imports. Uses the already full2048-input checked
ORIGINAL seed domains; complete64-row representatives are replayed separately.
Only positive records are exclusions, and all other prep functions stay open.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time

from controls import operations_allow

ROOT = Path(__file__).resolve().parent
PILOT = ROOT
WORK = ROOT/'work'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def gate(value, a, b):
    return value ^ (1 << a) ^ (1 << b) if (value >> a & 1) > (value >> b & 1) else value


def main():
    operations_allow()
    started = time.monotonic()
    deadline = started+45
    file = Path(sys.argv[1]) if len(sys.argv)>1 else WORK/'reserve-preparation-classifications.json'
    proposal = json.loads(file.read_text())
    rows = proposal['classifications']
    need(digest(rows) == proposal['finite']['classification_sha256'] and
         digest(proposal['finite']) == proposal['finite_sha256'], 'Changed classification transport binding')
    manifest = json.loads((ROOT/'work/preparation-bindings.json').read_text())
    for name in ('branch03.json', 'cuts03.json'):
        pin = next(r['sha256'] for r in manifest['generated_evidence'] if r['path'] == 'work/'+name)
        need(hashlib.sha256((PILOT/'work'/name).read_bytes()).hexdigest() == pin,
             'Previously full-graph checked preparation input changed')
    p = json.loads((PILOT/'work/branch03.json').read_text())
    cuts = json.loads((PILOT/'work/cuts03.json').read_text())
    n = json.loads((WORK/'reserve-seed-checked.json').read_text())
    o = json.loads((WORK/'reserve-seed-checked-O.json').read_text())
    need(n['finite'] == o['finite'] and digest(n['finite']) == n['finite_sha256'] ==
         o['finite_sha256'] == proposal['finite']['scalar_seed_reserve_finite_sha256'] and
         digest(n['activity_domains']) == n['finite']['whole_original_activity_domains_sha256'],
         'Complete actual original reserve/domain binding differs')
    originals = {r['original_HIGH_mask']: r for r in n['activity_domains']}
    records = [r['original_record'] for r in originals.values()]
    classes = {}
    for r in records:
        classes[r[3]] = max(classes.get(r[3], 0), r[4])
    dead = [2, 3, 4, 5, 8, 9]
    indices = {p: i for i, p in enumerate(dead)}
    need(len(rows) == len(cuts['retained_function_ids']) and
         [r['function_id'] for r in rows] == cuts['retained_function_ids'] and
         [r['retained_offset'] for r in rows] == list(range(len(rows))),
         'Incomplete original retained-function classification')
    replay, census, metrics, negatives, open_offsets = [], Counter(), Counter(), [], []
    for offset, item in enumerate(rows):
        if offset % 128 == 0:
            operations_allow()
            need(time.monotonic() < deadline, 'Incomplete45s scalar reserve-negative replay')
        f = p['functions'][item['function_id']]
        word = f['shortest_word']
        need(item['preparation_word_sha256'] == digest(word) and
             item['full_function_sha256'] == digest(f['full_six_variable_columns']),
             'Wrong literal complete function/preparation word')
        witness = item['witness']
        if witness is None:
            need(item['status'] == 'NO_RESERVED_IDENTITY_FOUND_PRESERVED_OPEN',
                 'An unresolved case is mislabeled negative')
            open_offsets.append(offset)
            census['unresolved_preparation_functions_preserved_open'] += 1
            continue
        need(item['status'] == 'ORIGINAL_HIGH_RESERVED_IDENTITY_PROPOSAL', 'Unrecognized negative type')
        need(all(0 <= a < b < 13 and a in indices and b in indices for a, b in word),
             'Nonstandard or live-port preparation comparator')
        truth = list(range(64))
        for a, b in word:
            truth = [gate(value, indices[a], indices[b]) for value in truth]
            metrics['full64_preparation_gate_evaluations'] += 64
        columns = [sum((value >> j & 1) << i for i, value in enumerate(truth)) for j in range(6)]
        need(columns == f['full_six_variable_columns'], 'Literal preparation is not its complete64-row function')
        original = witness['original_HIGH_mask']
        need(original in originals, 'Unknown ORIGINAL HIGH clamp')
        domain = originals[original]
        seed = domain['original_record']
        E, h = classes[seed[3]], 9-classes[seed[3]]
        need(seed == witness['original_seed_record'] and seed[4]+seed[5]+h == 9 and
             E == witness['current_HIGH_class_maximum_E'] and h == witness['reserved_marked_touches'],
             'Reported future CLASS maximum or marked-touch reserve differs')
        mask = domain['dead_projected_image_mask']
        need(mask == witness['original_activity_image_mask'], 'Wrong whole ORIGINAL activity image')
        values = {i for i in range(64) if mask >> i & 1}
        t = witness['first_reported_preparation_identity_index']
        need(isinstance(t, int) and 0 <= t < len(word) and
             word[t] == witness['identity_comparator'], 'Reported identity comparator is not in the literal word')
        identities = 0
        for index, (a, b) in enumerate(word[:t+1]):
            ia, ib = indices[a], indices[b]
            inactive = all((value >> ia & 1) <= (value >> ib & 1) for value in values)
            identities += int(inactive)
            metrics['selected_original_projected_assignments'] += len(values)
            if index == t:
                need(inactive, 'Chosen ORIGINAL is active at the reported identity gate')
            values = {gate(value, ia, ib) for value in values}
        need(identities >= 1 and witness['certified_total_cost_lower_bound'] == 45 and
             seed[4]+seed[5]+1+h+35 == 45, 'Actual original future pruning does not force45')
        replay.append([offset, item['function_id'], original, t, E, h, digest(sorted(values)), identities])
        negatives.append(offset)
        census['original_reserved_identity_preparations_excluded'] += 1
    need(len(negatives)+len(open_offsets) == len(rows) and
         open_offsets == proposal['finite']['remaining_retained_offsets'], 'Expected complete negative/open census differs')
    finite = {'branch_index': 3, 'HIGH_word': [[5, 6], [9, 10]],
              'retained_preparation_domain': [0, len(rows)],
              'producer_reserve_classification_finite_sha256': proposal['finite_sha256'],
              'complete_classification_sha256': proposal['finite']['classification_sha256'],
              'scalar_seed_reserve_finite_sha256': n['finite_sha256'],
              'census': dict(census), 'scalar_metrics': dict(metrics),
              'actual_original_identity_replay_sha256': digest(replay),
              'excluded_retained_offsets_sha256': digest(negatives),
              'remaining_retained_offsets_sha256': digest(open_offsets),
              'all_original_lower_bounds_at_least45': True,
              'whole_route_exclusion_claimed': False}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'ALL_FRESH_ORIGINAL_HIGH_RESERVED_IDENTITY_PREPARATIONS_SCALAR_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-started,
              'external_person_review_claimed': False,
              'scope': 'Only supplied positive complete preparation functions; every sufficient miss stays open before other proofs.'}
    if len(sys.argv)==1:
        suffix = '-O' if not __debug__ else ''
        (WORK/('reserve-preparations-checked'+suffix+'.json')).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
