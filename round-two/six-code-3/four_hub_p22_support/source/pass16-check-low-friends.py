"""PRIVATE fresh inverse leave-friend marking oracle, no producer imports.

The outer marking order is heavy point first, then three light points.
Each low point's unique missing pair supplies its high friend, inversely
to the producer's high-point sets of low friends. Full marking bits and
every accepted high-subset/type count are compared after reconstruction.
This is algorithmic independence by the same author, not peer review.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

ROOT = Path('round-two/six-code-3')
SCRATCH = ROOT / 'scratch'
ALL = (1 << 17) - 1
FIELDS = ('e','k','q','eligible','h','g1_S','ss_excess','hub_weight','psi','margin','ss_hist')

def need(c, message):
    if not c:
        raise ValueError(message)

def key(row):
    return tuple(tuple(row[f]) if f == 'ss_hist' else row[f] for f in FIELDS)

def compile_one(words, fi):
    masks = []
    for q in words:
        need(len(q) == len(set(q)) == 4, 'quadruple cardinality')
        need(all(type(p) is int and 0 <= p < 17 for p in q), 'point domain')
        masks.append(sum(1 << p for p in q))
    need(len(masks) == len(set(masks)) == 20, 'twenty actual distinct blocks')
    rep = [sum((m >> p) & 1 for m in masks) for p in range(17)]
    delta = [5 - r for r in rep]
    need(min(delta) >= 0 and sum(delta) == 5, 'actual mass five')
    covered = [0] * 17
    for mask in masks:
        for p in range(17):
            if mask >> p & 1:
                rest = mask ^ (1 << p)
                need(not covered[p] & rest, 'pair owns at most one block')
                covered[p] |= rest
    missing = [ALL ^ (1 << p) ^ covered[p] for p in range(17)]
    high = [p for p in range(17) if delta[p]]
    low = [p for p in range(17) if not delta[p]]
    highmask = sum(1 << p for p in high)
    need(sum(m.bit_count() for m in missing) == 32, 'sixteen uncovered pairs')
    friend = {}
    for p in low:
        need(missing[p].bit_count() == 1, 'unique friend for each low point')
        f = missing[p].bit_length() - 1
        need(f in high, 'no low-low pair')
        friend[p] = f
    hh = [missing[p] & highmask for p in high]
    need(sum(m.bit_count() for m in hh) == 2 * (len(high) - 1), 'high forest edge count')
    rows = {}
    for k in range(len(high) + 1):
        for J in itertools.combinations(high, k):
            Jmask = sum(1 << p for p in J)
            hist = [sum(delta[p] == d for p in high if p not in J) for d in range(1,6)]
            e = 5 - len(high)
            q = sum(bool(((1 << p) | (1 << t)) & Jmask)
                    for p,t in itertools.combinations(high,2) if missing[p] >> t & 1)
            eligible = any(not (missing[p] & highmask) for p in J)
            sigma = sum(i * c for i,c in enumerate(hist))
            psi = hist[0] if e == 0 and eligible else -hist[0] if e and not eligible else 0
            rows[J] = dict(fixture=fi,hub_high=list(J),h=len(high),e=e,k=k,q=q,
                           eligible=eligible,g1_S=hist[0],ss_excess=sigma,
                           hub_weight=sum(delta[p] for p in J),psi=psi,
                           margin=psi-3*(k-e-q),ss_hist=hist)
    return delta, high, low, friend, rows

def main():
    start = time.monotonic()
    raw = (ROOT/'four_hub_p21_endpoint_cut/fixtures.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7','literal fixture pin')
    data = json.loads(raw)
    need(len(data['stars']) == 23, 'complete imported representative domain')
    compiled = [compile_one(words,fi) for fi,words in enumerate(data['stars'])]
    allrows = sorted([r for item in compiled for r in item[-1].values()],key=lambda r:(r['fixture'],r['hub_high']))
    types = sorted({key(r) for r in allrows if r['k'] <= 4})
    ids = {k:i for i,k in enumerate(types)}
    rank = {H:i for i,H in enumerate(itertools.combinations(range(17),4))}
    records = []
    marks = 0
    for fi,(delta,high,low,friend,rows) in enumerate(compiled):
        full_low = Counter(friend.values())
        membership = 0
        types_count = Counter()
        row_count = Counter()
        first_bad_id = 9520
        first_bad = None
        for heavy in range(17):
            for lights in itertools.combinations([p for p in range(17) if p != heavy],3):
                marks += 1
                need(marks <= 218960 and time.monotonic()-start <= 30, 'INCOMPLETE fixed marking guard; no mathematical absence')
                H = tuple(sorted((heavy,) + lights))
                original_id = 4 * rank[H] + H.index(heavy)
                J = tuple(p for p in high if p in H)
                row = rows[J]
                type_id = ids[key(row)]
                assigned_low = Counter(friend[p] for p in H if p in friend)
                bad = None
                for a in high:
                    L = full_low[a] - assigned_low[a]
                    defect = 2 if a == heavy else 1 if a in lights else 0
                    if L > 5 + 4*defect - delta[a]:
                        bad = dict(point=a,delta=delta[a],low_saturated_friends=L,
                                   global_point_defect=defect,hubs=list(H),heavy=heavy,
                                   hub_high=list(J),type_id=type_id)
                        break
                if bad:
                    if original_id < first_bad_id:
                        first_bad_id,first_bad = original_id,bad
                    continue
                membership |= 1 << original_id
                types_count[type_id] += 1
                row_count[J] += 1
        records.append(dict(fixture=fi,physical_marks=9520,accepted_marks=membership.bit_count(),
                            accepted_type_multiplicities=sorted(types_count.items()),
                            accepted_high_mark_multiplicities=[[list(J),c] for J,c in sorted(row_count.items())],
                            first_failure=first_bad,
                            accepted_membership_hex=membership.to_bytes(1190,'little').hex()))
    canon = lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
    first = json.loads((SCRATCH/'pass16-first-engine-low-friends.json').read_text())
    need(canon(records) == canon(first['records']), 'every membership bit and fixture aggregate differs')
    published = json.loads((ROOT/'four_hub_p21_endpoint_cut/expected.json').read_text())
    need(canon([dict(zip(FIELDS,k)) for k in types]) == canon(published['types']), 'all sixty projected basis rows')
    need(len(allrows) == 426, 'all actual high-subset baseline marks')
    need(hashlib.sha256(canon(allrows)).hexdigest() == '783bb3191fe37ee1e830b69062d2b465b3a9c4684c17a6359bc01ddbef64530f','all426 full row fields')
    result = dict(agent='six-code-3',role='researcher',status='PRIVATE_COMPLETE_TWO_ALGORITHM_MARKING_AGREEMENT',
                  physical_marks=marks,accepted_marks=sum(r['accepted_marks'] for r in records),
                  projected_types=sorted({i for r in records for i,c in r['accepted_type_multiplicities']}),
                  membership_vectors_sha256=hashlib.sha256(b''.join(bytes.fromhex(r['accepted_membership_hex']) for r in records)).hexdigest(),
                  whole_records_sha256=hashlib.sha256(canon(records)).hexdigest(),
                  all426_rows_matched=True,all60_types_matched=True,all218960_membership_bits_matched=True,
                  original_first_failure_witnesses_matched=True,elapsed_seconds=time.monotonic()-start,
                  new_pair_total_claim=None,independent_peer_review=False,ordinary_bridge_formalized=False,
                  method_credit_chat=1836)
    out = SCRATCH/'pass16-independent-low-friends.json'
    need(not out.exists(),'fresh independent output')
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__ == '__main__':
    main()
