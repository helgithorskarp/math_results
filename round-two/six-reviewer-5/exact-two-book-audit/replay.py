"""Independent exhaustive certificate replay, using only our MITM engine.

The original schema/serializer is credited mathematical input, inspected
after our independent 82-case first seal. No author executable is imported.
"""
import hashlib
import json
import math
import time
from domains import profiles, exceptions, initial
from propagate import compatible, close
from common import require


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def integer(value, lower, upper, message):
    require(type(value) is int and lower <= value <= upper, message)


CLAIM = 'No valid rootless9^4,10^18 graph has exactly two one-nine roots'


class Context:
    def __init__(self):
        self.profiles = profiles()
        self.exceptions = [exceptions(p)[0] for p in self.profiles]
        self.domains = {}

    def initial(self, index, exception):
        key = (index, tuple(exception))
        if key not in self.domains:
            self.domains[key] = initial(self.profiles[index], tuple(exception))
        return self.domains[key]


def coverage(packet, context, claim=CLAIM):
    require(type(packet) is dict and set(packet) == {'schema', 'claim', 'profiles'}, 'packet fields')
    require(type(packet['schema']) is int and packet['schema'] == 1, 'schema')
    require(packet['claim'] == claim, 'literal claim scope')
    require(type(packet['profiles']) is list and len(packet['profiles']) == 6, 'six profiles')
    for index, record in enumerate(packet['profiles']):
        require(type(record) is dict and set(record) == {'profile', 'types', 'cases'}, 'profile fields')
        for name in ['profile', 'types']:
            require(type(record[name]) is list and all(type(v) is int for v in record[name]), 'typed profile')
        require(record['profile'] == list(context.profiles[index]['rst']), 'all ordered labeled profiles')
        require(record['types'] == list(context.profiles[index]['types']), 'all actual incidence tags')
        require(type(record['cases']) is list and len(record['cases']) == len(context.exceptions[index]), 'all templates')
        for case, exception in zip(record['cases'], context.exceptions[index]):
            require(type(case) is dict and set(case) == {'exceptions', 'domain_sizes', 'domain_sha256',
                    'kind', 'empty_target', 'steps', 'deletions_sha256'}, 'case fields')
            require(type(case['exceptions']) is list and all(type(v) is int for v in case['exceptions']), 'typed exception')
            require(case['exceptions'] == list(exception), 'entire ordered template coverage')
            require(type(case['domain_sizes']) is list and len(case['domain_sizes']) == 18, 'eighteen domain sizes')
            for value in case['domain_sizes']: integer(value, 0, 24310, 'domain size')
            integer(case['empty_target'], 0, 17, 'empty target')
            require(type(case['kind']) is str and case['kind'] in ('empty', 'static', 'arc'), 'proof type')
            require(type(case['steps']) is list, 'steps')
            for step in case['steps']:
                require(type(step) is list and len(step) == 3, 'step shape')
                integer(step[0], 0, 17, 'step target'); integer(step[1], 0, 17, 'step other')
                integer(step[2], 1, 24310, 'positive deleted count')
                require(step[0] != step[1], 'self support')
            for name in ['domain_sha256', 'deletions_sha256']:
                require(type(case[name]) is str and len(case[name]) == 64 and
                        all(c in '0123456789abcdef' for c in case[name]), 'SHA256 field')


def case_replay(case, profile, rows, blue_caps=True):
    started = time.monotonic()
    require(case['domain_sizes'] == [len(row) for row in rows], 'complete initial sizes')
    require(case['domain_sha256'] == fingerprint(rows), 'whole regenerated initial domain fingerprint')
    current = [set(row) for row in rows]; deletions = []; tests = 0
    if case['kind'] == 'empty':
        require(not case['steps'] and not current[case['empty_target']], 'actual initial empty')
    else:
        require(all(current) and bool(case['steps']), 'nonempty original domains')
        for x, y, count in case['steps']:
            require(time.monotonic() - started < 45, 'INCOMPLETE fixed45-second replay guard')
            require(current[x] and current[y], 'step after contradiction')
            if case['kind'] == 'static': require(x == case['empty_target'], 'static target')
            gone = []; other = sorted(current[y])
            for sx in sorted(current[x]):
                supported = False
                for sy in other:
                    tests += 1
                    require(tests <= 20000000, 'INCOMPLETE fixed20-million replay guard')
                    if compatible(profile, x, sx, y, sy, blue_caps=blue_caps):
                        supported = True; break
                if not supported: gone.append(sx)
            require(len(gone) == count, 'ENTIRE unsupported set cardinality')
            current[x].difference_update(gone); deletions.append([x, y, gone])
        require(not current[case['empty_target']], 'actual final empty')
    require(case['deletions_sha256'] == fingerprint(deletions), 'whole ordered actual deletion fingerprint')
    return deletions


def audit(packet, context, blue_caps=True, claim=CLAIM):
    coverage(packet, context, claim)
    summary = {'profile_template_counts': [], 'templates': 0, 'empty': 0, 'static': 0,
               'arc': 0, 'deletion_batches': 0, 'deleted_stars': 0, 'raw_star_subsets': 0}
    full = []
    for index, record in enumerate(packet['profiles']):
        profile = context.profiles[index]; cases = []
        for case in record['cases']:
            rows = context.initial(index, case['exceptions'])
            gone = case_replay(case, profile, rows, blue_caps)
            cases.append({'exceptions': case['exceptions'], 'domains': rows, 'deletions': gone})
            summary['templates'] += 1; summary[case['kind']] += 1
            summary['deletion_batches'] += len(gone)
            summary['deleted_stars'] += sum(len(step[2]) for step in gone)
        full.append({'profile': record['profile'], 'cases': cases})
        summary['profile_template_counts'].append(len(cases))
        summary['raw_star_subsets'] += sum(math.comb(17, 10-t.bit_count()) for t in profile['types'])
    summary['certificate_canonical_sha256'] = fingerprint(packet)
    return summary, (canonical(full)+'\n').encode()


WEAKER_CLAIM = 'The independent-low two-triple exact-two sector is impossible without high-high blue caps'


def build_weaker(context):
    packet = {'schema': 1, 'claim': WEAKER_CLAIM, 'profiles': []}
    for index, profile in enumerate(context.profiles):
        cases = []
        for exception in context.exceptions[index]:
            rows = context.initial(index, exception)
            result = close(profile, rows, blue_caps=False)
            require(result['empty'], 'not a complete weaker exclusion')
            steps = result['batches']
            target = next(x for x, size in enumerate(result['remaining_sizes']) if size == 0)
            deleted = [[s['target'], s['other'], s['removed']] for s in steps]
            cases.append({'exceptions': list(exception), 'domain_sizes': [len(row) for row in rows],
                          'domain_sha256': fingerprint(rows), 'kind': 'empty' if result['initial_empty'] else 'arc',
                          'empty_target': target, 'steps': [[x, y, len(gone)] for x, y, gone in deleted],
                          'deletions_sha256': fingerprint(deleted)})
        packet['profiles'].append({'profile': list(profile['rst']), 'types': list(profile['types']), 'cases': cases})
    return packet
