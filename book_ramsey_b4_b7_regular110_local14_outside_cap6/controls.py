"""Literal A--B counts and size-eight controls; six-books-3, researcher.

Graph fixtures reuse, with attribution, the varied ten-regular controls
at source d00a13612475ea701786203b280200c11a105106, controls.py. This
program imports neither local-core generator nor any campaign checker.
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

    # This abstract pair census checks the universal set-complement bridge.
    # It neither chooses F nor asserts a host extension.
    C = set(range(2, 10))
    L = {0, 1}
    choices = list(combinations(C, 2))
    for first, second in product(choices, repeat=2):
        pairs = [set(first), set(second)]
        common = len(pairs[0] & pairs[1])
        survivors = []
        for Z in map(set, combinations(range(10), 8)):
            possible = all(not (low in Z and pairs[low] & Z) for low in range(2))
            possible = possible and not (L <= Z and 2 - common < 1)
            if possible:
                survivors.append(Z)
            count['abstract_size8_rows'] += 1
        need(survivors == [C], 'Size-eight low-point bridge failed')
        need(6 + 8 - 10 == 4 and 4 > 3, 'Forced red-spine contradiction')
        count['abstract_low_pair_systems'] += 1
        count['size8_all_cubic_forced'] += 1
    subsets=list(map(set,combinations(range(10),4)))
    for first in subsets:
        for second in subsets:
            joint=len(first&second)
            unmissed=len(set(range(10))-first-second)
            need(unmissed==2+joint and (unmissed>=3)==(joint>=1), 'Double-low unmiss identity')
            count['double_low_four_subset_pairs']+=1
    expected=json.loads((HERE/'expected.json').read_text())
    certificate=json.loads((HERE/'negative_vectors.json').read_text())
    for kind in ('zero','short','boolean','nonprimitive','duplicate','bad_index','bad_profile','missing_profile'):
        fake=copy.deepcopy(certificate)
        active=next(p for p in fake['profiles'] if p['vector_indices'])
        if kind=='zero':fake['vectors'][0]=[0]*10
        elif kind=='short':fake['vectors'][0].pop()
        elif kind=='boolean':fake['vectors'][0][0]=True
        elif kind=='nonprimitive':fake['vectors'][0]=[2*x for x in fake['vectors'][0]]
        elif kind=='duplicate':fake['vectors'].append(fake['vectors'][0][:])
        elif kind=='bad_index':active['vector_indices'][0]=len(fake['vectors'])
        elif kind=='bad_profile':active['index']=-1
        else:fake['profiles'].pop()
        try:check.validate_certificate(fake,expected['profiles'])
        except RuntimeError:count['forged_certificates_rejected']+=1
        else:raise RuntimeError('Accepted invalid certificate: '+kind)
    control=json.loads((HERE/'gram_control.json').read_text())
    four_rows=list(map(set,control['four_rows']))
    need(len(four_rows)==9 and all(len(row)==4 for row in four_rows),'Positive Gram row shape')
    literal=[[sum(i in row and j in row for row in four_rows) for j in range(10)] for i in range(10)]
    need(literal==control['residual_matrix'],'Literal positive binary Gram differs')
    echelon=[[Fraction(int(i in row)) for i in range(10)] for row in four_rows]
    rank=0
    for column in range(10):
        pivot=next((i for i in range(rank,len(echelon)) if echelon[i][column]),None)
        if pivot is None:continue
        echelon[rank],echelon[pivot]=echelon[pivot],echelon[rank]
        for i in range(rank+1,len(echelon)):
            factor=echelon[i][column]/echelon[rank][column]
            echelon[i]=[a-factor*b for a,b in zip(echelon[i],echelon[rank])]
        rank+=1
    need(rank==control['rank']==5,'Positive binary Gram exact rank')
    matrix,_=check.formula(control['F_mask'],tuple(map(tuple,control['pairs'])))
    first,second=set(control['first']),set(control['second'])
    rebuilt=[[matrix[i][j]-int(i in first and j in first)-int(i in second and j in second)
              for j in range(10)] for i in range(10)]
    incident=[0]*10
    for i,j,w in control['slack_weights']:
        rebuilt[i][j]-=w;rebuilt[j][i]-=w;incident[i]+=w;incident[j]+=w
    need(rebuilt==literal,'Uncut residual reconstruction differs')
    all_rows=[first,second]+four_rows
    need([sum(i in row for row in all_rows) for i in range(10)]==[4,4]+[5]*8,'Positive miss-column totals')
    need(sum(0 in row and 1 in row for row in all_rows)==0,'Positive control joint-low count')
    r=len(set(control['pairs'][0])&set(control['pairs'][1]))
    LL=next(w for i,j,w in control['slack_weights'] if (i,j)==(0,1))
    need(LL>1-r,'Positive Gram control should fail double-low cut')
    need(not any(check.is_negative(literal,check.integer_form(v)) for v in certificate['vectors']),
         'An exact positive binary Gram has a negative form')
    count['positive_binary_Gram_entries']+=100
    count['positive_Gram_forms_checked']+=len(certificate['vectors'])
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
