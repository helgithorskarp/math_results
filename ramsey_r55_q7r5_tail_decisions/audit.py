"""Independent matrix / truth-table audit. Does not import the encoder."""
import hashlib
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path

def require(test, message):
    if not test:
        raise ValueError(message)

def matrix(line):
    require(len(line) == 19 and line[0] == 'N', 'Core order/length')
    digits = [ord(c) - 63 for c in line[1:]]
    require(all(0 <= x < 64 for x in digits), 'Core alphabet')
    payload = 0
    for digit in digits:
        payload = 64 * payload + digit
    require(payload % 8 == 0, 'Padding')
    a = [[-1] * 23 for _ in range(23)]
    for j in range(1, 15):
        for i in range(j):
            a[i][j] = a[j][i] = (payload >> (107 - (j * (j - 1) // 2 + i))) & 1
    for start in (15, 19):
        for i, j in combinations(range(start, start + 4), 2):
            a[i][j] = a[j][i] = 0
    for vertices in combinations(range(15), 4):
        colors = {a[i][j] for i, j in combinations(vertices, 2)}
        require(colors == {0, 1}, 'Core is not Ramsey(4,4;15)')
    return a

def variable_matrix(a):
    v = [[0] * 23 for _ in range(23)]
    nextvar = 0
    for i in range(23):
        for j in range(i + 1, 23):
            if a[i][j] == -1:
                nextvar += 1
                v[i][j] = v[j][i] = nextvar
    require(nextvar == 136, 'Physical variable count')
    return v

def parse(raw):
    lines = raw.decode('ascii').splitlines()
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ['p', 'cnf'], 'Header')
    nv, nc = map(int, header[2:])
    require(nv == 279 and nc == len(lines) - 1, 'Dimensions')
    rows = []
    for line in lines[1:]:
        words = list(map(int, line.split()))
        require(words and words[-1] == 0 and all(0 < abs(x) <= nv for x in words[:-1]), 'Literal syntax')
        row = words[:-1]
        require(len(set(row)) == len(row) and not any(-x in row for x in row), 'Duplicate or tautological clause')
        rows.append(row)
    return rows

def holds(rows, assignment):
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in row) for row in rows)

def check_order(rows, v):
    words = []
    for start in (15, 19):
        for u in range(start, start + 3):
            words.append(([v[i][u] for i in reversed(range(15))],
                          [v[i][u + 1] for i in reversed(range(15))]))
    words.append(([v[i][u] for u in (18, 17, 16, 15) for i in reversed(range(15))],
                  [v[i][u] for u in (22, 21, 20, 19) for i in reversed(range(15))]))
    offset = 0
    aux = 137
    tables = 0
    for left, right in words:
        prefix = None
        for bit, (x, y) in enumerate(zip(left, right)):
            last = bit == len(left) - 1
            size = 1 if last else (5 if prefix is None else 6)
            part = rows[offset:offset + size]
            require(len(part) == size, 'Missing comparator gate')
            scope = [x, y] + ([] if prefix is None else [prefix]) + ([] if last else [aux])
            require(all(abs(lit) in scope for row in part for lit in row), 'Comparator scope')
            for bits in product((False, True), repeat=len(scope)):
                values = dict(zip(scope, bits))
                p = True if prefix is None else values[prefix]
                wanted = (not p or values[x] <= values[y])
                if not last:
                    wanted = wanted and values[aux] == (p and values[x] == values[y])
                require(holds(part, values) == wanted, 'Comparator truth table')
                tables += 1
            offset += size
            if not last:
                prefix = aux
                aux += 1
    require(offset == len(rows) == 858 and aux == 280, 'Comparator termination')
    return tables

def formula(line, raw):
    a = matrix(line)
    v = variable_matrix(a)
    expected = []
    counts = []
    for size, color in ((4, 1), (5, 0)):
        count = 0
        for vertices in combinations(range(23), size):
            satisfied = False
            literals = []
            for i, j in combinations(vertices, 2):
                if a[i][j] == -1:
                    literals.append(v[i][j] * (1 - 2 * color))
                elif a[i][j] != color:
                    satisfied = True
                    break
            if not satisfied:
                require(literals, 'A fixed forbidden set')
                expected.append(literals)
                count += 1
        counts.append(count)
    actual = parse(raw)
    require(actual[:len(expected)] == expected, 'Physical literal stream mismatch')
    tables = check_order(actual[len(expected):], v)
    e = sum(a[i][j] for i, j in combinations(range(15), 2))
    t = sum(all(a[i][j] for i, j in combinations(s, 2)) for s in combinations(range(15), 3))
    u = sum(not any(a[i][j] for i, j in combinations(s, 2)) for s in combinations(range(15), 3))
    require(counts == [16 * e + 8 * t, comb(8, 5) + 15 * comb(8, 4) + (105 - e) * comb(8, 3) + u * comb(8, 2)], 'Independent polynomial count')
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'clauses': len(actual),
            'red_four': counts[0], 'blue_five': counts[1], 'gate_truth_assignments': tables}

def witness(line, word):
    require(type(word) is str and len(word) == 136 and set(word) <= {'0', '1'}, 'Witness length/alphabet')
    a = matrix(line)
    k = 0
    for i in range(23):
        for j in range(i + 1, 23):
            if a[i][j] == -1:
                a[i][j] = a[j][i] = int(word[k])
                k += 1
    for size, color in ((4, 1), (5, 0)):
        for s in combinations(range(23), size):
            require(not all(a[i][j] == color for i, j in combinations(s, 2)), 'Forbidden set in witness')
    return {'vertices': 23, 'edges': sum(a[i][j] for i, j in combinations(range(23), 2)),
            'red_K4': 0, 'blue_K5': 0, 'physical43_status': 'UNKNOWN'}
