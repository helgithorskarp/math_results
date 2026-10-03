"""Bounded positive set-packing search. Failure establishes no nonexistence."""
import argparse, hashlib, json
from pathlib import Path
from field import Q, candidates, gauss, require

def pack(records):
    # Literal sets and increasing candidate tuples, rather than native bit-mask greedy.
    visits = 0
    def search(indices, chosen, occupied):
        nonlocal visits
        visits += 1
        require(visits <= 100000, 'INCOMPLETE positive search node guard')
        if len(chosen) == 5:
            return chosen
        if len(indices) < 5-len(chosen):
            return None
        for offset, i in enumerate(indices):
            rec = records[i]
            rest = [j for j in indices[offset+1:] if not rec[2].intersection(records[j][2])]
            answer = search(rest, chosen+[rec], occupied.union(rec[2]))
            if answer is not None:
                return answer
        return None
    answer = search(list(range(len(records))), [], frozenset())
    require(answer is not None, 'INCOMPLETE positive search; no achieved pack')
    return answer, visits

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--lo', type=int, required=True)
    ap.add_argument('--hi', type=int, required=True); ap.add_argument('--output', required=True)
    args = ap.parse_args(); require(1 <= args.lo < args.hi <= Q, 'scale partition')
    base = candidates()
    normalized = {}
    for word in range(0, 256, 2):
        normalized[word] = [r for r in base if len({(word >> k)&1 for k in r[3]}) == 1]
    rows = []; max_visits = 0
    for scale in range(args.lo, args.hi):
        flip = 7*gauss(scale)
        for word in range(0, 256, 2):
            pulled = sum(((word >> (k^flip))&1) << k for k in range(8))
            if pulled&1: pulled ^= 255
            physical = []
            for a, d, points, pattern in normalized[pulled]:
                start, step = scale*a%Q, scale*d%Q
                if step > 51: start, step = (start+6*step)%Q, Q-step
                if step > 50: continue
                support = frozenset(scale*x%Q for x in points)
                physical.append((start, step, support, pattern))
            # Dispersion ordering is fixed, nonrandom and independent of native order.
            physical.sort(key=lambda r:(max(r[2])-min(r[2]), r[1], r[0]))
            chosen, visits = pack(physical); max_visits = max(max_visits, visits)
            rows.append([scale, word, *[v for r in chosen for v in r[:2]]])
    raw = ''.join(','.join(map(str,r))+'\n' for r in rows).encode()
    Path(args.output).write_bytes(raw)
    print(json.dumps({'lo':args.lo,'hi':args.hi,'cases':len(rows),'bytes':len(raw),
                      'sha256':hashlib.sha256(raw).hexdigest(),'max_search_nodes':max_visits},sort_keys=True))

if __name__ == '__main__': main()
