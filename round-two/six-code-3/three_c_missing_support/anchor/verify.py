"""Definition-level witness checker and whole-domain comparator; imports no producer."""
import argparse
import copy
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

START = time.monotonic()
STATES = 0


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def check_record(rec):
    tick()
    cells = [(r, c) for r in range(4) for c in range(4) if r != c]
    colors = rec['colors']
    require(len(colors) == 12 and all(type(x) is int and 0 <= x < 4 for x in colors), 'color domain')
    classes = rec['classes']
    require(len(classes) == 3 and all(len(cls) == 4 for cls in classes), 'three classes, four triples each')
    require(classes[0] == [[k for k, p in enumerate(cells) if p[0] == r] for r in range(4)] and
            classes[1] == [[k for k, p in enumerate(cells) if p[1] == c] for c in range(4)], 'retained first two classes')
    for cls in classes:
        require(all(len(t) == 3 and t == sorted(set(t)) for t in cls) and
                sorted(p for t in cls for p in t) == list(range(12)), 'every physical parallel class partitions U')
    for a, b in itertools.combinations(range(3), 2):
        require(all(len(set(x) & set(y)) <= 1 for x in classes[a] for y in classes[b]), 'cross-class literal incidence')
    require(classes[2] == [[p for p in range(12) if colors[p] == a] for a in range(4)], 'entire color-to-triple bridge')
    for r in range(4):
        row = [colors[p] for p, cell in enumerate(cells) if cell[0] == r]
        require(sorted(row) == [x for x in range(4) if x != r], 'specified row-missing normalization')
    missing = []
    for c in range(4):
        column = [colors[p] for p, cell in enumerate(cells) if cell[1] == c]
        require(len(set(column)) == 3, 'column injectivity')
        missing.append(next(x for x in range(4) if x not in column))
    require(rec['column_missing'] == missing and sorted(missing) == list(range(4)), 'entire column permutation')
    anchor = [[1, 2, 3, 4, 5]]
    for cls, pair in zip(classes, [[1, 2], [1, 3], [2, 3]]):
        anchor += [sorted(pair + [p + 6 for p in triple]) for triple in cls]
    require(rec['anchor'] == anchor, 'entire thirteen-word anchor reconstruction')
    require(all(len(set(w)) == 5 and all(1 <= p < 18 for p in w) for w in anchor) and
            len(set(tuple(w) for w in anchor)) == 13, 'point domain and word uniqueness')
    require(all(len(set(x) & set(y)) <= 2 for x, y in itertools.combinations(anchor, 2)), 'physical intersection-two')
    for pair in [{1, 2}, {1, 3}, {2, 3}]:
        tails = [set(w) - pair for w in anchor if pair <= set(w)]
        require(len(tails) == 5 and sorted(p for t in tails for p in t) ==
                [p for p in range(1, 18) if p not in pair], 'exact C-pair multiplicity and all completing points')


def cycle_type(permutation):
    remaining = set(range(4))
    lengths = []
    while remaining:
        current = min(remaining)
        length = 0
        while current in remaining:
            remaining.remove(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return ','.join(str(x) for x in sorted(lengths))


def verify_domain(math):
    records = math['records']
    require(math['domain'] == 1296 and len(math['coverage']) == 1296, 'whole 1296-bit domain')
    require(records == sorted(records, key=lambda r: r['colors']) and
            len({tuple(r['colors']) for r in records}) == len(records), 'ordered whole positive records')
    positives = {tuple(r['colors']) for r in records}
    cells = [(r, c) for r in range(4) for c in range(4) if r != c]
    choices = [list(itertools.permutations([s for s in range(4) if s != r])) for r in range(4)]
    for index, rows in enumerate(itertools.product(*choices)):
        tick()
        colors = tuple(x for row in rows for x in row)
        valid = all(len({colors[p] for p, cell in enumerate(cells) if cell[1] == c}) == 3 for c in range(4))
        require(math['coverage'][index] == str(int(valid)) and (colors in positives) == valid,
                'every bit and every physical accepted system')
    for rec in records:
        check_record(rec)
    require(math['baseline'] in records, 'positive baseline retained as whole record')
    return Counter(cycle_type(r['column_missing']) for r in records)


def reject_record(rec, name):
    try:
        check_record(rec)
    except (ValueError, IndexError, KeyError):
        return name
    raise ValueError('semantic damage was accepted: ' + name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--literal', type=Path, required=True)
    ap.add_argument('--dual', type=Path, required=True)
    ap.add_argument('--expected', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    left, right = [json.loads(p.read_text()) for p in [args.literal, args.dual]]
    expected = json.loads(args.expected.read_text())
    require(left['mathematics'] == right['mathematics'], 'all mathematics fields, not aggregate counts')
    math = left['mathematics']
    common = hashlib.sha256(json.dumps(math, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    require(left['common_math_sha256'] == right['common_math_sha256'] == common, 'whole common mathematics hash')
    require(math['baseline']['colors'] == expected['baseline_colors'], 'frozen classical baseline')
    hist = verify_domain(math)
    rejections = []
    rec = math['baseline']
    for name, damage in [('color outside domain', lambda r: r['colors'].__setitem__(0, 4)),
                         ('lost physical triple', lambda r: r['classes'][2].pop()),
                         ('duplicated physical point', lambda r: r['classes'][2][0].__setitem__(0, r['classes'][2][0][1])),
                         ('false column matching', lambda r: r['column_missing'].__setitem__(0, 1)),
                         ('heavy0 in anchor', lambda r: r['anchor'][0].__setitem__(0, 0)),
                         ('lost whole anchor word', lambda r: r['anchor'].pop())]:
        corrupted = copy.deepcopy(rec)
        damage(corrupted)
        rejections.append(reject_record(corrupted, name))
    lost = copy.deepcopy(math)
    lost['records'].pop()
    try:
        verify_domain(lost)
    except ValueError:
        rejections.append('lost whole accepted system')
    else:
        raise ValueError('lost accepted system survived complete coverage comparison')
    incorrect = copy.deepcopy(math)
    incorrect['coverage'] = ('1' if math['coverage'][0] == '0' else '0') + math['coverage'][1:]
    try:
        verify_domain(incorrect)
    except ValueError:
        rejections.append('false complete-domain bit')
    else:
        raise ValueError('corrupted coverage bit survived')
    non_identity = [r for r in math['records'] if r['column_missing'] != list(range(4))]
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_WHOLE_ANCHOR_CLASSIFICATION_CHECK',
                  cases=1296, accepted=len(math['records']), column_missing_cycle_histogram=dict(sorted(hist.items())),
                  non_identity_column_matching=len(non_identity),
                  non_identity_control=non_identity[0] if non_identity else None,
                  common_math_sha256=common, all_physical_records_and_domain_bits_checked=True,
                  semantic_rejections=rejections, states=STATES, guard_states=500000, guard_seconds=20,
                  ordinary_bridge_formalized=False, independent_person_review=False,
                  unrestricted_packing_completion_claimed=False)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
