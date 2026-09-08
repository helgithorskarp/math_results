"""Definition-level audit, exact frozen-CNF support, and physical task cover."""
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def physical_variables():
    edges = [e for e in combinations(range(43), 2)
             if e[0] < 40 and not (e[0] // 4 == e[1] // 4)]
    need(len(edges) == 840, 'physical variable map')
    result = {edge: i + 2 for i, edge in enumerate(edges)}
    need({result[e] for e in [(3, 24), (3, 41), (3, 6), (3, 40), (3, 33)]} ==
         {139, 156, 121, 155, 148}, 'physical literal support')
    need([result[e] for e in [(3, 24), (3, 41), (3, 6), (3, 40), (3, 33)]] ==
         [139, 156, 121, 155, 148], 'physical literal labels')
    return result


def canonical_words():
    # An independent canonical algorithm: after a column permutation, sort
    # the four row values decreasingly instead of enumerating 24 row actions.
    answer = []
    for word in range(4096):
        rows = [(word >> (3 * r)) & 7 for r in range(4)]
        if any(all(row >> c & 1 for row in rows) for c in range(3)):
            continue
        orbit = []
        for columns in permutations(range(3)):
            values = [sum(((row >> c) & 1) << i
                          for i, c in enumerate(columns)) for row in rows]
            values.sort(reverse=True)
            orbit.append(sum(row << (3 * i) for i, row in enumerate(values)))
        if word == min(orbit):
            answer.append(word)
    need(len(answer) == 65, '65 canonical words')
    return answer


def structure():
    variables = physical_variables()
    core = [variables[r, c] for r in range(4) for c in (40, 41, 42)]
    words = canonical_words()
    need(json.loads((ROOT / 'CORE_WORDS.json').read_text()) ==
         {'words': words, 'variables': core}, 'canonical entry agreement')
    need({w >> 9 for w in words} == {0, 1, 3}, 'last core row forms')
    # The most significant bits of ordered columns are nonincreasing.
    for left in range(16):
        for right in range(left + 1):
            need(left >> 3 >= right >> 3, 'ordered column implication')
    patterns = [bits for bits in range(15)
                if all((bits >> i & 1) >= (bits >> (i + 1) & 1)
                       for i in range(3))]
    need(patterns == [0, 1, 3, 7], 'four ordered K4 contact patterns')
    # Whole-block order has these four-bit row words as its top nibble.
    # Therefore it orders their population counts, with every other edge free.
    count = 0
    maxima = {'d20-22-strong': -1, 'd22-20': -1,
              'd22-20-corezero': -1}
    for asc in combinations_with_replacement(range(4), 9):
        row = tuple(reversed(asc))
        for coreword in (0, 1, 3):
            degree = 3 + sum(row) + coreword.bit_count()
            count += 1
            if row[5] == 0 and not (coreword & 2):
                maxima['d20-22-strong'] = max(maxima['d20-22-strong'], degree)
            if row[0] <= 2 and row[7] <= 1:
                maxima['d22-20'] = max(maxima['d22-20'], degree)
            if row[0] <= 2 and not (coreword & 1):
                maxima['d22-20-corezero'] = max(maxima['d22-20-corezero'], degree)
    need(count == 660, 'exhaustive row audit')
    need(maxima == {'d20-22-strong': 19, 'd22-20': 21,
                    'd22-20-corezero': 21}, 'strict physical degree deficits')
    return {'canonical_words': 65, 'row_audit_cases': count,
            'maximum_degrees_in_excluded_cubes': maxima,
            'core_last_row_histogram': {str(i): sum(w >> 9 == i for w in words)
                                       for i in (0, 1, 3)}}


def read_cnf(path):
    lines = Path(path).read_text().splitlines()
    header = lines[0].split()
    need(len(header) == 4 and header[:2] == ['p', 'cnf'], 'core header')
    n, m = map(int, header[2:])
    need(n == 40351 and len(lines) == m + 1, 'core dimensions')
    rows = []
    for line in lines[1:]:
        data = list(map(int, line.split()))
        need(data and data[-1] == 0 and all(0 < abs(x) <= n for x in data[:-1]),
             'core clause syntax')
        c = tuple(sorted(data[:-1]))
        need(len(c) == len(set(c)) and not any(-x in c for x in c),
             'core clause normalization')
        rows.append(c)
    return rows


def support(branches):
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())
    result = []
    variables = physical_variables()
    core = [variables[r, c] for r in range(4) for c in (40, 41, 42)]
    allowed = set(canonical_words())
    forbidden = set()
    for word in range(4096):
        if any(all(word >> (3*r+c) & 1 for r in range(4)) for c in range(3)):
            continue
        if word not in allowed:
            forbidden.add(tuple(sorted(-v if word >> i & 1 else v
                                       for i, v in enumerate(core))))
    need(len(forbidden) == 3310, 'complete canonical rejection table')
    for branch in inputs['branches']:
        path = Path(branches) / (branch['branch'] + '.cnf')
        need(path.stat().st_size == branch['bytes'] and sha(path) == branch['sha256'],
             'frozen physical CNF hash: ' + branch['branch'])
        claims = [c for c in inputs['certificates'] if c['branch'] == branch['branch']]
        ids = set(i for c in claims for i in c['source_ids'] if i is not None)
        found = {}
        actual_forbidden = []
        admissibility = []
        with path.open() as stream:
            need(stream.readline() == 'p cnf 40351 1931146\n', 'frozen header')
            actual = 0
            for i, line in enumerate(stream, 1):
                actual = i
                if i in ids:
                    row = list(map(int, line.split()))
                    need(row[-1] == 0, 'source terminator')
                    found[i] = tuple(sorted(row[:-1]))
                if 1927831 <= i <= 1931140:
                    actual_forbidden.append(tuple(sorted(map(int, line.split()[:-1]))))
                if 3278 <= i <= 3280:
                    admissibility.append(tuple(sorted(map(int, line.split()[:-1]))))
        need(actual == 1931146 and set(found) == ids, 'source positions')
        need(len(actual_forbidden) == 3310 and set(actual_forbidden) == forbidden,
             'frozen formula canonical cover')
        need(admissibility == [tuple(sorted(-variables[r, c] for r in range(4)))
                               for c in (40, 41, 42)], 'three physical admissibility clauses')
        for c in claims:
            rows = read_cnf(ROOT / (c['id'] + '-core.cnf'))
            need(len(rows) == len(c['source_ids']), 'support length')
            hypotheses = []
            for row, source_id in zip(rows, c['source_ids']):
                if source_id is None:
                    hypotheses.append(row)
                else:
                    need(row == found[source_id], 'wrong physical support clause')
            need(sorted(hypotheses) == sorted([(-x,) for x in c['clause']]),
                 'exact two cube assumptions')
            result.append({'id': c['id'], 'core_clauses': len(rows),
                           'source_clauses': len(rows) - 2, 'cube_units': 2})
    return result


def tasks():
    variables = physical_variables()
    core = [variables[r, c] for r in range(4) for c in (40, 41, 42)]
    words = canonical_words()
    clauses = {'d20-22': [139, 156], 'd22-20': [121, 155]}
    out = []
    for branch, clause in clauses.items():
        pivot, core_literal = clause
        for index, word in enumerate(words):
            assignment = [v if word >> i & 1 else -v for i, v in enumerate(core)]
            for bit in (0, 1):
                cube = assignment + [pivot if bit else -pivot]
                closed = not bit and -core_literal in cube
                out.append({'id': f'{branch}-w{index:02d}-p{bit}', 'branch': branch,
                            'word': word, 'cube': cube,
                            'status': 'CERTIFIED_UNSAT' if closed else 'UNKNOWN',
                            'certificate': ('d20-22-strong' if branch == 'd20-22'
                                            else 'd22-20-corezero') if closed else None,
                            'forced_residual_literal': 148 if branch == 'd22-20'
                            and not bit and not closed else None})
    need(len(out) == 260 and len({t['id'] for t in out}) == 260, 'task partition')
    need(sum(t['status'] == 'CERTIFIED_UNSAT' for t in out) == 99, '99 exclusions')
    need(sum(t['forced_residual_literal'] is not None for t in out) == 29,
         '29 residual edge implications')
    return out


def task_summary(rows):
    return {branch: {'physical_tasks': sum(t['branch'] == branch for t in rows),
                     'certified_unsat': sum(t['branch'] == branch and
                        t['status'] == 'CERTIFIED_UNSAT' for t in rows),
                     'unknown': sum(t['branch'] == branch and
                        t['status'] == 'UNKNOWN' for t in rows)}
            for branch in ('d20-22', 'd22-20')}
