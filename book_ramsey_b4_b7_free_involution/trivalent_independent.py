"""Actual author six-books-2, researcher. No other generator imports.
Binary edge decisions, exact constraint propagation, literal22-point pages.
Main records are untrusted comparison data and never drive enumeration.
"""
import argparse
from pathlib import Path
from itertools import combinations
from collections import Counter
from hashlib import sha256
import json
import resource
import time

PAIRS = tuple(combinations(range(11), 2))
INDEX = {e: i for i, e in enumerate(PAIRS)}
UNIVERSE = (1 << 55) - 1
INCIDENT = [sum(1 << k for k, e in enumerate(PAIRS) if i in e) for i in range(11)]
ALL22 = (1 << 22) - 1

def edge_mask(edges):
    return sum(1 << INDEX[tuple(sorted(e))] for e in edges)

def enumerate_binary(wanted, included, excluded, clauses):
    def visit(yes, no):
        while True:
            previous = yes, no
            if yes & no:
                return
            for i in range(11):
                if yes & no:
                    return
                need = wanted[i] - (yes & INCIDENT[i]).bit_count()
                choices = (UNIVERSE ^ (yes | no)) & INCIDENT[i]
                count = choices.bit_count()
                if need < 0 or need > count:
                    return
                if need == 0:
                    no |= choices
                elif need == count:
                    yes |= choices
            for clause in clauses:
                if yes & clause:
                    continue
                choices = clause & ~no
                if choices == 0:
                    return
                if choices.bit_count() == 1:
                    yes |= choices
            if (yes, no) == previous:
                break
        if yes & no:
            return
        if all((yes & INCIDENT[i]).bit_count() == wanted[i] for i in range(11)):
            yield yes
            return
        undecided = UNIVERSE ^ (yes | no)
        active = [i for i in range(11) if (yes & INCIDENT[i]).bit_count() < wanted[i]]
        vertex = min(active, key=lambda i: (undecided & INCIDENT[i]).bit_count())
        choice = undecided & INCIDENT[vertex]
        bit = choice & -choice
        yield from visit(yes | bit, no)
        yield from visit(yes, no | bit)
    yield from visit(included, excluded)

def literal_obstruction(red_mask, blue_mask):
    rows = [0] * 22
    r_pairs, d_pairs, m_pairs = [], [], []
    for k, (i, j) in enumerate(PAIRS):
        if (red_mask >> k) & 1:
            for a in [0, 1]:
                rows[2 * i + a] |= 3 << (2 * j)
                rows[2 * j + a] |= 3 << (2 * i)
            r_pairs.append((i, j))
        elif (blue_mask >> k) & 1:
            d_pairs.append((i, j))
        else:
            rows[2 * i] |= 1 << (2 * j)
            rows[2 * i + 1] |= 1 << (2 * j + 1)
            rows[2 * j] |= 1 << (2 * i)
            rows[2 * j + 1] |= 1 << (2 * i + 1)
            m_pairs.append((i, j))
    if any(row.bit_count() != 10 for row in rows):
        raise RuntimeError('literal graph is not regular')
    blue_rows = [ALL22 ^ (1 << v) ^ row for v, row in enumerate(rows)]
    for pairs, label, cap in [(r_pairs, 'R', 6), (d_pairs, 'D', 12), (m_pairs, 'M', 9)]:
        for i, j in pairs:
            if label == 'R':
                pages = (rows[2 * i] & rows[2 * j]).bit_count() + (rows[2 * i] & rows[2 * j + 1]).bit_count()
            elif label == 'D':
                pages = (blue_rows[2 * i] & blue_rows[2 * j]).bit_count() + (blue_rows[2 * i] & blue_rows[2 * j + 1]).bit_count()
            else:
                pages = (rows[2 * i] & rows[2 * j]).bit_count() + (blue_rows[2 * i] & blue_rows[2 * j + 1]).bit_count()
            if pages > cap:
                return [label, i, j, pages]
    return None


def degree_controls():
    # Independent brute-force definitions on all 1024 simple five-point graphs.
    pairs=tuple(combinations(range(5),2));by_degree={}
    for word in range(1024):
        selected={e for i,e in enumerate(pairs) if (word>>i)&1}
        degrees=tuple(sum(v in e for e in selected) for v in range(5))
        if max(degrees)<=2:by_degree.setdefault(degrees,set()).add(edge_mask(selected))
    checks=0
    for target in __import__('itertools').product(range(3),repeat=5):
        obtained=set(enumerate_binary(list(target)+[0]*6,0,0,[]))
        if obtained!=by_degree.get(target,set()):raise RuntimeError('five-point exact degree control mismatch')
        checks+=1
    target=[2]*5+[0]*6;clause=edge_mask({(0,2),(1,3)})
    obtained=set(enumerate_binary(target,0,0,[clause]))
    expected={m for m in by_degree[(2,)*5] if m&clause}
    if obtained!=expected:raise RuntimeError('positive local cover control mismatch')
    return {'five_point_binary_graph_words':1024,'exact_degree_vectors':checks,'local_cover_positive_graphs':len(obtained),'entrywise_degree_and_cover_controls':True}

def run(main_records):
    records,summaries=[],[];expected={}
    for line in main_records.read_text().splitlines():
        row=json.loads(line)
        if not isinstance(row,list) or len(row)!=3 or not isinstance(row[0],str) or type(row[1]) is not int or (row[0],row[1]) in expected:raise RuntimeError('malformed/duplicate main record')
        expected[(row[0],row[1])]=row[2]
    R8={tuple(sorted((i,(i+1)%8))) for i in range(8)}|{(8,9),(9,10)}
    for label in [1, 2, 3, 4, (11,), (5, 6)]:
        clauses = []
        if type(label) is int:
            red = R8
            wanted = [2] * 8 + [1, 2, 1]
            fixed = edge_mask({(8, 10), (0, 9), (label, 9)})
            no = edge_mask(red) | ((INCIDENT[8] | INCIDENT[10] | INCIDENT[9]) & ~fixed)
        else:
            red, first = set(), 0
            for length in label:
                red.update(tuple(sorted((first + i, first + (i + 1) % length))) for i in range(length))
                first += length
            wanted, fixed, no = [2] * 11, 0, edge_mask(red)
            nr = [set() for _ in range(11)]
            for i, j in red:
                nr[i].add(j); nr[j].add(i)
            for i, j in sorted(red):
                a = next(iter(nr[i] - {j}))
                b = next(iter(nr[j] - {i}))
                clauses.append(edge_mask({tuple(sorted((a, j))), tuple(sorted((i, b)))}))
        seen, counts = set(), Counter()
        for mask in enumerate_binary(wanted, fixed, no, clauses):
            if mask in seen:
                raise RuntimeError('duplicate independently generated D')
            seen.add(mask)
            key = ('C8:'+str(label), mask) if type(label) is int else ('C11' if label==(11,) else 'C5+C6', mask)
            failure = literal_obstruction(edge_mask(red), mask)
            if key not in expected or expected.pop(key) != failure:
                raise RuntimeError('independent domain/first literal obstruction mismatch')
            if failure is None:
                raise RuntimeError('necessary independent survivor')
            counts[failure[0]] += 1
            records.append([key[0], mask, failure])
        row = {'case': 'C8:'+str(label) if type(label) is int else 'C11' if label==(11,) else 'C5+C6', 'D_completions': len(seen), 'first_failure_counts': dict(counts)}
        summaries.append(row)

    if expected:raise RuntimeError('unmatched main domain records')
    records.sort(key=lambda r:(r[0],r[1]))
    encoded=''.join(json.dumps(r,separators=(',',':'))+'\n' for r in records)
    return {'agent':'six-books-2','role':'researcher','complete':True,'profiles':summaries,'literal_regular_lifts':len(records),'survivors':0,'canonical_records_sha256':sha256(encoded.encode()).hexdigest(),'all_records_match_entrywise':True,'binary_degree_controls':degree_controls(),'threads':1,'local_jobs':1,'author_independence_not_peer_review':True}

def main():
    parser=argparse.ArgumentParser(description='Independent binary edge propagation and literal Book pages')
    parser.add_argument('--main-records',type=Path,required=True);parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('trivalent_expected.json'))
    args=parser.parse_args();result=run(args.main_records)
    if not args.emit and result!=json.loads(args.expected.read_text())['independent']:raise RuntimeError('independent fixture mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
