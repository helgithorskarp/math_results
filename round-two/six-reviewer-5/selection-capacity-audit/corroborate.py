"""Post-seal adapter for the credited9299 record; no author code import.

The author's schema, ordering and metadata were read AFTER first-seal.json.
Mathematical quantities below are reconstructed from literal sets.
"""
import json
import math
from itertools import combinations, product
from pathlib import Path
from literal import require, load_code, digest, canonical
from capacity import constants


def charges():
    records = []; total = 0
    for h in range(1, 6):
        vertices = tuple(range(h)); pairs = tuple(combinations(vertices, 2))
        minima = [None]*(h+1)
        for edge_mask in range(1 << len(pairs)):
            if edge_mask.bit_count() != h-1: continue
            selected = [edge for i,edge in enumerate(pairs) if edge_mask >> i & 1]
            for k in range(h+1):
                for hub_tuple in combinations(vertices, k):
                    hubs = set(hub_tuple)
                    q = sum(bool(set(edge) & hubs) for edge in selected)
                    require(k == 0 or q >= k-1, 'independent projected q charge')
                    minima[k] = q if minima[k] is None else min(minima[k], q)
                    total += 1
        records.append({'h':h,'minima':minima})
    return {'all_enlarged_graph_and_hub_placements':total,'records':records,'classification_imported':False}


def weights():
    total = 0
    for h in range(1, 6):
        for values in product(range(1, 6), repeat=h):
            if sum(values) != 5: continue
            for k in range(h+1):
                for chosen in combinations(range(h), k):
                    hubs = set(chosen); e = sum(v-1 for v in values)
                    g = h-k; excess = sum(v-1 for i,v in enumerate(values) if i not in hubs)
                    require(e == 0 or g <= 3*e+excess, 'weighted endpoint capacity')
                    require(not(e and k == 0) or excess == e >= 1, 'unmarked endpoint excess')
                    require(not(e and k) or g <= 3, 'marked endpoint degree')
                    total += 1
    return {'all_ordered_positive_deficit_and_hub_placements':total,'exact_partition_weight':5}


def homogeneous(words):
    covered = {tuple(sorted(t)) for word in words for t in combinations(word, 3)}
    missing = [frozenset(t) for t in combinations(range(18),3) if t not in covered]
    degrees = {p:sum(p in w for w in words) for p in range(18)}
    pair = {t:sum(set(t) <= w for w in words) for t in combinations(range(18),2)}
    records = []; counts = {}
    for m in range(1,6):
        counts[m] = 0
        for hubs in combinations(range(18),m):
            H = frozenset(hubs)
            R = sum(degrees[p] for p in H)
            P = sum(v for t,v in pair.items() if set(t) <= H)
            T = sum(set(t) <= H for t in covered)
            A = sum(not(t & H) for t in missing)
            require(A == math.comb(18-m,3)-10*len(words)+6*R-3*P+T, 'independent original identity')
            require(R == sum(len(w & H) for w in words), 'literal word hub incidence')
            require(P == sum(math.comb(len(w & H),2) for w in words), 'literal word pair incidence')
            require(T == sum(math.comb(len(w & H),3) for w in words), 'literal word triple incidence')
            records.append([list(hubs),R,P,T,A]); counts[m] += 1
    return {'primary69_positive_control_only':True,'hub_subsets':len(records),
            'counts_by_size':counts,'whole_record_sha256':digest(records)}


def boundary(m,P):
    n,C,B = constants(m); W = C+2*P; budget = B+3*P
    before = []; after = []
    if budget >= 0:
        for T,tau,X,E in product(range(math.comb(m,3)+1),range(budget//2+1),range(min(4*n,budget)//2+1),range(min(4*n,budget)+1)):
            Q = budget-T-2*tau-E
            if Q < 0 or 2*X > E: continue
            if 8*E+11*Q < 4*W or 11*E+8*Q < 4*W+6*X: continue
            row = {'T':T,'X':X,'tau':tau,'E':E,'Q':Q,'Z_lower':W-2*(E+Q)+2*X}
            before.append(row)
            if E >= 4 or row['Z_lower'] <= 0: after.append(row)
    # Preserve the credited original record order only after reconstruction.
    key = lambda r:(r['T'],r['tau'],r['E'],r['X'])
    return {'m':m,'P':P,'necessary_arithmetic_before_unit_partner':sorted(before,key=key),
            'necessary_arithmetic_after_unit_partner':sorted(after,key=key),'actual_packings_enumerated':False}


def reconstruct(control_record):
    rows = []
    for m in range(1,6):
        n,C,B = constants(m); cut = 8*C-19*B
        rows.append({'m':m,'n':n,'W_constant':C,'B_constant':B,'cut_constant':cut,
                     'preliminary_P_lower':-(-cut//41),'final_P_lower':[None,3,8,19,34][m-1]})
    return {'actual_agent':'six-code-1','role':'researcher',
            'scope':'Exact arithmetic and definition-level validation of ordinary cuts; no packing census or formalized bridge.',
            'charge_graphs':charges(),'weighted_rows':weights(),'tables':rows,
            'boundary_cases':[boundary(m,p) for m,p in [(2,2),(3,7),(3,8),(4,18),(5,32),(5,33)]],
            'homogeneous_identity':homogeneous(load_code(Path(__file__).with_name('primary69.txt'))),
            'controls':control_record}


def compare(control_record):
    record = reconstruct(control_record)
    expected = json.loads(Path(__file__).with_name('author-record.json').read_text())
    require(canonical(record) == canonical(expected), 'every credited original record field independently matches')
    return {'every_original_field_equal':True,'canonical_original_record_sha256':digest(record),
            'author_schema_read_after_independent_first_seal':True,'author_module_imported':False}
