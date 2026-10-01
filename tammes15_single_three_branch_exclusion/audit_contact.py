"""Separate contact-case raw-label/unoriented-cell/signed-dual audit.
No production schema/predicate/forcing imports; same researcher.
"""
from pathlib import Path
from collections import Counter
import hashlib, importlib.util, json
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'tammes15_ordinary_five_four_one_exclusion/audit.py'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != 'f9d4ebbab1316f68e4dffdec8375ad158203c3cf2fd0627d90da68dee019eabb':
    raise RuntimeError('Published8180 auditor changed')
loader = importlib.util.spec_from_file_location('published8180_auditor', SOURCE)
a = importlib.util.module_from_spec(loader)
loader.loader.exec_module(a)
old_check = a.check
def check(labels, spec, use_orientability=True):
    return len(set(labels)) <= 15 and old_check(labels, spec, use_orientability)
a.check = check
ANCHORS = ('F', 'U', 'X', 'R', 'S', 'Z', 'B', 'C')
BASE = (('F', 'R', 'X'), ('F', 'S', 'R'), ('F', 'Z', 'S'),
        ('F', 'U', 'C', 'Z'), ('F', 'X', 'B', 'U'), ('U', 'B', 'Y', 'C'),
        ('R', 'S', 'K', 'L'), ('R', 'L', 'P', 'X'), ('S', 'Z', 'Q', 'K'))
ROLES = {
    'X1Z1': (('E',), ('X', 'Z', 'B', 'C', 'E')),
    'X1Z2': (('E', 'G'), ('X', 'B', 'C', 'E', 'G')),
    'X2Z1': (('E', 'G'), ('Z', 'B', 'C', 'E', 'G')),
}
def specification(case):
    extra, ones = ROLES[case]
    originals = ANCHORS + extra
    names, words = originals + ('Y', 'L', 'K', 'P', 'Q'), BASE
    if 'X' in ones:
        names += ('AX',)
        words += (('X', 'P', 'AX', 'B'),)
    else:
        words += (('X', 'P', 'B'),)
    if 'Z' in ones:
        names += ('AZ',)
        words += (('Z', 'C', 'AZ', 'Q'),)
    else:
        words += (('Z', 'C', 'Q'),)
    number = {n: i for i, n in enumerate(names)}
    return {'case': case, 'names': names, 'words': words,
            'faces': tuple(tuple(number[n] for n in w) for w in words),
            'mode': 'full', 'maxima': {0: 3},
            'exact': {0: 3, 1: 0, **{number[n]: 1 for n in ones}},
            'distinct': (), 'initial': tuple(range(len(originals))),
            'contact_edges': ((0, 1), (1, 6), (1, 7))}
def ordinary_stars(labels, spec):
    positions = {n: i for i, n in enumerate(spec['names'])}
    roles = {n: a.actual_role(labels, spec, labels[positions[n]]) for n in ('L', 'K')}
    names, words = (), ()
    for n in ('L', 'K'):
        if roles[n] not in (0, 1, 2):
            raise RuntimeError('Passing original has unclassified role')
        if roles[n] != 2:
            continue
        h = 'H' + n
        names += (h,)
        if n == 'L':
            words += (('L', 'K', h), ('L', h, 'P'))
        else:
            words += (('K', 'Q', h), ('K', h, 'L'))
    return roles, a.append_words(spec, names, words)

def run(data):
    if hashlib.sha256(data).hexdigest() != '5830ff7e4a34562a18dfb1acc0d421992328040e9698d469e1df6c5ce29c6c37':
        raise RuntimeError('Regenerated component trace changed')
    trace = json.loads(data)
    stream = iter(trace)
    counts = Counter()
    controls = {}
    def record(stage, spec, initial=None):
        entry = next(stream)
        wanted = entry['spec']
        if entry['stage'] != stage or entry['initial'] != (list(initial) if initial else None):
            raise RuntimeError('Original-face cover schedule differs')
        if list(spec['names']) != wanted['names'] or not a.same_words(spec['words'], wanted['words']):
            raise RuntimeError('Independent original face words differ')
        if {spec['names'][i]: t for i, t in spec['exact'].items()} != wanted['exact']:
            raise RuntimeError('Independent exact roles differ')
        if set(spec['contact_edges']) != set(map(tuple, wanted['contact_edges'])):
            raise RuntimeError('Actual U contacts differ')
        states, raw, boundaries = a.cover(spec, entry['cover'], spec['initial'] if initial is None else initial)
        counts[stage] += 1
        counts['raw_label_assignments'] += raw
        counts['entrywise_compared_boundaries'] += boundaries
        return states
    def recurse(labels, spec, depth=0):
        if depth > 12:
            raise RuntimeError('INCOMPLETE: fixed12forcingdepth')
        if a.new_U_offenders(labels, spec):
            counts['one_T_U_cuts'] += 1
            return
        forced = a.last_face(labels, spec)
        if forced is None:
            raise RuntimeError('A terminal partial/closed map survives independent audit')
        for p in record('forced_last_face', forced[3], labels):
            recurse(p, forced[3], depth + 1)
    reference = None
    for case in ROLES:
        spec = specification(case)
        if not check(spec['initial'], spec):
            raise RuntimeError('Positive three-T F-star rejected')
        wrong = dict(spec, exact=dict(spec['exact'], **{}), maxima={})
        wrong['exact'][0] = 4
        if check(spec['initial'], wrong):
            raise RuntimeError('Wrong four-T F-role accepted')
        controls[case] = {'F_three_T_positive': True, 'F_four_T_negative': True}
        if case == 'X1Z1':
            reference = trace[0]
        states = record('original_face', spec)
        for labels in states:
            if a.new_U_offenders(labels, spec):
                counts['early_one_T_U_cuts'] += 1
                continue
            roles, full = ordinary_stars(labels, spec)
            for p in record('ordinary_strip_stars', full, labels):
                recurse(p, full)
    if next(stream, None) is not None or sum(counts[x] for x in ('original_face','ordinary_strip_stars','forced_last_face')) != len(trace):
        raise RuntimeError('Unconsumed cover or cover-count mismatch')
    spec = specification('X1Z1')
    states1, raw1, b1 = a.cover(spec, reference['cover'], spec['initial'], 1)
    states2, raw2, b2 = a.cover(spec, reference['cover'], spec['initial'], 2)
    if states1 != states2 or len(states1) != 7:
        raise RuntimeError('Nontrivial one/two-position raw-block reference differs')
    return {'agent': 'six-tammes-1', 'role': 'researcher',
            'status': 'SEPARATE_SAME_AUTHOR_ALL_BRANCH_BOUNDARIES_MATCH_NO_TERMINAL',
            'counts': dict(sorted(counts.items())), 'controls': {**controls, **a.controls()},
            'raw_block_reference': [{'width':1,'raw_tuples':raw1,'boundaries':b1},
                                    {'width':2,'raw_tuples':raw2,'boundaries':b2}],
            'production_trace_sha256': hashlib.sha256(data).hexdigest(),
            'scope': 'Unformalized original-face reduction and imported7912 collar remain written bridges; independent mathematical review pending.'}
