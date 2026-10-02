"""Literal-set catalog producer. All finite point roles are explicit."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

PIN = 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'
POINTS = frozenset(range(17))
def require(test, message):
    if not test:
        raise ValueError(message)
def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def compile_star(blocks, fi):
    Q = frozenset(frozenset(q) for q in blocks)
    require(len(Q) == len(blocks) == 20, 'twenty distinct quadruples required')
    require(all(len(q) == 4 and q <= POINTS for q in Q), 'invalid quadruple')
    rho = Counter(p for q in Q for p in q)
    owners = Counter(t for q in Q for t in itertools.combinations(sorted(q), 2))
    require(all(count == 1 for count in owners.values()), 'repeated point pair')
    delta = {p: 5-rho[p] for p in POINTS}
    require(min(delta.values()) >= 0 and sum(delta.values()) == 5, 'invalid deficits')
    high = frozenset(p for p in POINTS if delta[p])
    leave = frozenset(t for t in itertools.combinations(range(17), 2) if t not in owners)
    require(len(leave) == 16, 'sixteen leave edges required')
    low = POINTS-high
    require(all(sum(p in t for t in leave) == 1 for p in low), 'low leave degree')
    require(all(not set(t) <= low for t in leave), 'universal low-low prohibition')
    HH = frozenset(t for t in leave if set(t) <= high)
    require(len(HH) == len(high)-1, 'high leave count')
    isolated = frozenset(p for p in high if all(p not in t for t in HH))
    return dict(fixture=fi, delta=delta, high=high, HH=HH, isolated=isolated)

def rows_from_data(data):
    require(len(data['stars']) == len(data['groups']) == 23, 'complete23-star input required')
    rows = []
    for fi, blocks in enumerate(data['stars']):
        s = compile_star(blocks, fi)
        high = tuple(sorted(s['high']))
        for bits in range(1 << len(high)):
            B = frozenset(p for j,p in enumerate(high) if bits >> j & 1)
            h, k = len(high), len(B)
            e = 5-h
            q = sum(bool(set(t) & B) for t in s['HH'])
            eligible = bool(s['isolated'] & B)
            g1 = sum(s['delta'][p] == 1 for p in s['high']-B)
            sigma = sum(s['delta'][p]-1 for p in s['high']-B)
            w = sum(s['delta'][p] for p in B)
            require(e == w-k+sigma, 'weighted/support identity')
            psi = g1 if e == 0 and eligible else -g1 if e and not eligible else 0
            rows.append(dict(fixture=fi, hub_high=sorted(B), h=h, e=e, k=k, q=q,
                eligible=eligible, g1_S=g1, ss_excess=sigma, hub_weight=w,
                psi=psi, margin=psi-3*(k-e-q)))
    return sorted(rows, key=lambda r:(r['fixture'],r['hub_high']))

def summary(rows):
    within = [r for r in rows if r['k'] <= 4]
    require(all(r['margin'] >= 0 for r in within), 'within-scope row inequality fails')
    outside = [r for r in rows if r['k'] == 5]
    return dict(status='PASS_ALL_LITERAL_ROWS_WITH_K_LE_FOUR', total_rows=len(rows),
        within_scope_rows=len(within), row_records_sha256=digest(rows),
        within_scope_sha256=digest(within), minimum_margin=min(r['margin'] for r in within),
        outside_scope_actual_failures=outside,
        fixture_populations=[sum(r['fixture'] == fi for r in rows) for fi in range(23)])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixtures',type=Path,default=Path(__file__).with_name('fixtures.json'))
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args()
    raw=args.fixtures.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PIN, 'credited input bytes differ')
    rows=rows_from_data(json.loads(raw))
    result=dict(rows=rows, summary=summary(rows))
    args.work.mkdir(parents=True,exist_ok=True)
    (args.work/'catalog.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result['summary'],sort_keys=True))
if __name__=='__main__':
    main()
