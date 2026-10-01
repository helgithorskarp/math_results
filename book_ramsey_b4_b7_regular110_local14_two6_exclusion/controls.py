"""Literal A--B counts and certificate controls; six-books-3, researcher.

Graph fixtures reuse, with attribution, the varied ten-regular controls
at source d00a13612475ea701786203b280200c11a105106, controls.py. This
program imports no local-core generator. The graph arithmetic is literal;
the certificate controls intentionally exercise the separate checker.
Control graphs may violate book caps; their arithmetic is still exact.
"""
from collections import Counter
from itertools import combinations, product
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import random
import urllib.request
import copy
import check

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def run():
    count = Counter()
    for number, steps in enumerate(combinations(range(1, 11), 5)):
        red = [{(i + sign * step) % 22 for sign in (-1, 1) for step in steps}
               for i in range(22)]
        rng = random.Random(970013 + number)
        for attempt in range(80):
            a, b, c, d = rng.sample(range(22), 4)
            if b in red[a] and d in red[c] and c not in red[a] and d not in red[b]:
                for u, v in ((a, b), (c, d)):
                    red[u].remove(v)
                    red[v].remove(u)
                for u, v in ((a, c), (b, d)):
                    red[u].add(v)
                    red[v].add(u)
                count['degree_preserving_switches'] += 1
        need(all(len(row) == 10 for row in red), 'Control not ten-regular')
        blue = [set(range(22)) - red[i] - {i} for i in range(22)]
        for v in (0, 1, 4, 9, 17):
            A, B = red[v], blue[v]
            h = {a: len(red[a] & A) for a in A}
            misses = {b: A - red[b] for b in B}
            need(sum(map(len, misses.values())) == sum(h.values()) + 20, 'Miss total')
            for b in B:
                Z = misses[b]
                z = len(Z)
                need(z == len(red[b] & B), 'Outside degree/miss identity')
                for a in A:
                    if b in red[a]:
                        t = len(red[a] & A & red[b])
                        X, Y = (red[a] & B) - {b}, red[b] & B
                        need(len(X) == 8 - h[a] and len(Y) == z, 'Red A--B column sizes')
                        need(X | Y <= B - {b}, 'Red union universe')
                        pages = len(red[a] & red[b])
                        need(pages == t + len(X & Y), 'Literal red pages split')
                        need(pages == t + 8 - h[a] + z - len(X | Y), 'Red union identity')
                        need(pages >= t + z - h[a] - 2, 'Red lower bound')
                        if pages <= 3:
                            need(z <= h[a] + 5 - t, 'Red necessary row filter')
                            count['red_cap_implications'] += 1
                        count['red_AB_identities'] += 1
                    else:
                        r = len(red[a] & Z)
                        local_pages = len(blue[a] & blue[b] & A)
                        need(local_pages == z - 1 - r, 'Blue A--B local-page identity')
                        pages = len(blue[a] & blue[b])
                        need(pages == local_pages + len(blue[a] & blue[b] & B), 'Blue page split')
                        need(pages >= z - 1 - r, 'Blue lower bound')
                        if pages <= 6:
                            need(r >= z - 7, 'Blue necessary row filter')
                            count['blue_cap_implications'] += 1
                        count['blue_AB_identities'] += 1
            count['regular_root_controls'] += 1

    expected=json.loads((HERE/'expected.json').read_text())
    certificate=json.loads((HERE/'negative_vectors.json').read_text())
    profiles=expected['profiles']
    mutations=[]
    def changed():return copy.deepcopy(certificate)
    c=changed();c['vectors'][0].pop();mutations.append(c)
    c=changed();c['vectors'][0][0]=True;mutations.append(c)
    c=changed();c['vectors'][0]=[0]*10;mutations.append(c)
    c=changed();c['vectors'][0]=[2*x for x in c['vectors'][0]];mutations.append(c)
    c=changed();c['profiles'][0]['vector_indices']=[len(c['vectors'])];mutations.append(c)
    c=changed();c['profiles'][0]['index']=100;mutations.append(c)
    for c in mutations:
        try:check.validate_certificate(c,profiles)
        except (RuntimeError,KeyError,ValueError):count['forged_certificates_rejected']+=1
        else:raise RuntimeError('Forged vector certificate accepted')
    records=json.loads((HERE/'gram_exceptions.json').read_text())['records']
    reference=records[0];profile=profiles[reference['profile_index']]
    _,neighbors=check.formula(profile['F_mask'],check.PAIRS[profile['intersection']])
    first=tuple(reference['first']);second=tuple(reference['second']);matrix=reference['matrix']
    bad=[]
    c=copy.deepcopy(reference);c['matrix'][0][0]+=1;bad.append(c)
    c=copy.deepcopy(reference);c['audit']['binary_rows'].pop();bad.append(c)
    c=copy.deepcopy(reference);c['audit']['entry_compatible_types'].pop();bad.append(c)
    c=copy.deepcopy(reference);c['audit']['rank']=4;bad.append(c)
    c=copy.deepcopy(reference);c['audit']['AB_neighbor_counts']=[1,0];bad.append(c)
    for c in bad:
        try:check.exception_check.audit(c,matrix,neighbors,first,second)
        except (RuntimeError,KeyError,ValueError):count['forged_certificates_rejected']+=1
        else:raise RuntimeError('Forged Gram obstruction accepted')
    rows=reference['audit']['binary_rows']
    for vector in certificate['vectors']:
        literal=sum(matrix[i][j]*vector[i]*vector[j] for i in range(10) for j in range(10))
        squares=sum(sum(vector[i] for i in row)**2 for row in rows)
        need(literal==squares and literal>=0,'Literal Gram form/squares control')
        need(check.is_negative(matrix,check.integer_form(vector))==(literal<0),'Encoded form control')
        count['positive_Gram_forms_checked']+=1
    need(count['forged_certificates_rejected']==11,'Forgery control coverage')
    return dict(sorted(count.items()))


def baseline():
    url = ('https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/'
           'tabu/constructions/R_B4_B7_construction_21vertices.txt')
    request = urllib.request.Request(url, headers={'User-Agent': 'six-books-3-math-research'})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
    # The primary file is one JSON adjacency array followed by search metadata.
    digits, end = json.JSONDecoder().raw_decode(data.decode().lstrip())
    need(isinstance(digits, list) and len(digits) == 21 and
         all(isinstance(row, list) and len(row) == 21 and
             all(type(x) is int and x in (0, 1) for x in row) for row in digits), 'Primary matrix shape')
    need(all(digits[i][i] == 0 for i in range(21)), 'Primary diagonal')
    red = [{j for j in range(21) if i != j and digits[i][j] == 0} for i in range(21)]
    need(all(i not in red[i] and all((j in red[i]) == (i in red[j]) for j in range(21)) for i in range(21)), 'Primary matrix not simple')
    blue = [set(range(21)) - red[i] - {i} for i in range(21)]
    need(sum(map(len, red)) // 2 == 93, 'Primary edge count')
    need(max(len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i]) == 3, 'Primary red cap')
    need(max(len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j in blue[i]) == 6, 'Primary blue cap')
    rows = ''.join(''.join(str(int(j in red[i])) for j in range(21)) + '\n' for i in range(21)).encode()
    fixture = HERE / 'baseline21.rows'
    need(rows == fixture.read_bytes(), 'Primary fixture bytes differ')
    result = {'source_url': url, 'source_sha256': hashlib.sha256(data).hexdigest(),
              'red_rows_sha256': hashlib.sha256(rows).hexdigest(), 'all441_entries_compared': True,
              'parser': 'First JSON adjacency array; following search metadata is not matrix data.',
              'red_edges': 93, 'max_red_blue_codegrees': [3, 6], 'known_baseline_not_new': True}
    return result


if __name__ == '__main__':
    print(json.dumps({'agent': 'six-books-3', 'role': 'researcher',
                      'controls': run(), 'baseline': baseline()}, sort_keys=True))
