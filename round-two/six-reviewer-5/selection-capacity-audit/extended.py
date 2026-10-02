"""Independent semantic controls and optional upper71 append bridge.

Written after the first sealed core and credited peer chat1655. No private
category, catalog coefficient or proposed P35 assertion is imported.
"""
import json
import math
from itertools import combinations
from pathlib import Path
from literal import require, load_code, digest, canonical


def parse_primary(raw):
    lines = raw.decode().splitlines()
    require(len(lines) == 69 and len(set(lines)) == 69, 'distinct primary population')
    require(all(len(s) == 18 and set(s) <= {'0','1'} and s.count('1') == 5 for s in lines), 'binary length and weight')
    words = [frozenset(p for p,c in enumerate(s) if c == '1') for s in lines]
    require(all(len(a & b) <= 2 for a,b in combinations(words,2)), 'pair collision')
    return words


def reject(call, label):
    try: call()
    except ValueError: return label
    raise ValueError('semantic damage accepted: '+label)


def controls():
    raw = Path(__file__).with_name('primary69.txt').read_bytes(); lines = raw.decode().splitlines()
    parse_primary(raw)
    damaged = [lines[:-1],[lines[0]]+lines[2:]+[lines[0]],[lines[0]+'0']+lines[1:]]
    bad = list(lines); i = bad[0].index('1'); bad[0] = bad[0][:i]+'0'+bad[0][i+1:]; damaged.append(bad)
    names = ['missing word','duplicate word','wrong length','wrong weight']
    checks = [reject(lambda rows=rows:parse_primary(('\n'.join(rows)+'\n').encode()), name) for rows,name in zip(damaged,names)]
    # Distinct, correct-weight collision is rejected beyond byte-pin validation.
    bad = list(lines); first = set(p for p,c in enumerate(lines[0]) if c == '1')
    remove = min(first); add = next(p for p in range(18) if p not in first and ''.join('1' if q in (first-{remove})|{p} else '0' for q in range(18)) not in lines)
    bad[1] = ''.join('1' if q in (first-{remove})|{add} else '0' for q in range(18))
    checks.append(reject(lambda:parse_primary(('\n'.join(bad)+'\n').encode()), 'distinct correct-weight collision'))
    # True q1 unit pattern; its marked points are not high-isolated, but
    # a different high-isolated point still has its ordinary low friend.
    high = {0,1,2,3,4}; edges = [{0,1},{0,2},{1,2},{3,4}]; hubs = {3,4}
    q = sum(bool(e & hubs) for e in edges)
    require(q == 1, 'retained enlarged q1 two-hub positive control')
    checks.append(reject(lambda:require(q >= len(hubs), 'false q>=k catalog import'), 'false stronger hub charge'))
    checks.append(reject(lambda:require(all(not(e & hubs) for e in edges), 'false mark isolation'), 'q1 isolated-mark substitution'))
    all_edges = [{0,1},{0,2},{1,2},{1,3},{4,5}]
    require(not any(4 in e and bool((e-{4}) & high) for e in all_edges), 'isolated in deficient induced leave')
    require(any(4 in e for e in all_edges), 'ordinary low leave friend retained')
    checks.append(reject(lambda:require(not any(4 in e for e in all_edges), 'wrong full-leave isolation'), 'forbid ordinary low friend'))
    # Capacity guard rejects an ineligible incidence and accepts its exact
    # corrected budget; these are scalar logical controls, not packing hosts.
    def capacity(Z,M0,QM): require(4*Z <= 4*M0+3*QM, 'only actual allowed nonunit endpoints')
    capacity(1,1,0)
    checks.append(reject(lambda:capacity(1,0,1), 'four edges into capacity three'))
    checks.append(reject(lambda:require(8*(1+1) >= 4*5+8*0+4*(1-1)+0, 'wrong charged budget'), 'violated unified necessary inequality'))
    first = json.loads(Path(__file__).with_name('first-record.json').read_text())
    wrong = json.loads(canonical(first)); wrong['physical_rows']['coupled_frames'] -= 1
    checks.append(reject(lambda:require(canonical(first) == canonical(wrong), 'whole record mismatch'), 'missing coupled physical frame'))
    checks.append(reject(lambda:require(133+2*1+2*1 <= 4*34, 'wrong P34 boundary'), 'P34 simultaneous T1 and X1'))
    checks.append(reject(lambda:require(133+4*1 <= 4*34, 'wrong triangle boundary'), 'P34 positive tau'))
    checks.append(reject(lambda:require(76+2*1 <= 4*19, 'wrong four-hub equality'), 'P19 positive hub triple'))
    return {'semantic_damage_checks':len(checks),'rejected_labels':checks,
            'original_four_primary_damages_rejected':4,'enlarged_q1_positive_control':True,
            'ordinary_low_friend_of_induced_isolated_point_retained':True}


def append_bridge():
    words = load_code(Path(__file__).with_name('primary69.txt'))
    triples = {frozenset(t) for w in words for t in combinations(w,3)}
    records = []; zero = 0; member = 0
    for selected in combinations(range(18),5):
        H = frozenset(selected)
        T = sum(frozenset(t) in triples for t in combinations(selected,3))
        addable = H not in words and all(len(H & w) <= 2 for w in words)
        require(addable == (T == 0), 'literal five-hub append equivalence')
        zero += T == 0; member += H in words; records.append([selected,T,addable])
    # Explicit addable/nonaddable small families prevent a vacuous control.
    small = [frozenset(range(5))]
    for H,expected in [(frozenset(range(5,10)),True),(frozenset((0,1,2,5,6)),False),(small[0],False)]:
        T = sum(frozenset(t) <= small[0] for t in combinations(sorted(H),3))
        actual = H not in small and all(len(H & w) <= 2 for w in small)
        require(actual == expected == (T == 0), 'append small positive/negative/member control')
    boundary = json.loads(Path(__file__).with_name('first-record.json').read_text())['projected_necessary_inventories']['boundaries'][-1]['inventories']
    remaining = [r for r in boundary if r[1] >= 1]
    require(len(remaining) == 8 and all(r[1:4] == [1,0,0] for r in remaining), 'upper71 strengthened P34 necessary boundary')
    return {'literal_five_subsets':len(records),'primary_addable_controls':zero,'primary_member_controls':member,
            'whole_append_record_sha256':digest(records),'nonvacuous_small_controls':3,
            'P34_with_explicit_upper71_necessary_inventory_count':len(remaining),
            'P34_forced_T_X_tau':[1,0,0],'P35_claimed':False,
            'ordinary_append_bridge_credit':'six-code-1 private chat1655, independently derived after first core seal'}
