"""Literal prior input only; no target executable or expected data imports."""
import itertools
import json
from pathlib import Path

FIELDS = ('e', 'k', 'q', 'eligible', 'h', 'c1', 'psi', 'mu',
          'sigma', 'I5', 'hub_weight')

def require(condition, message):
    if not condition:
        raise ValueError(message)

def reconstruct(stars):
    require(type(stars) is list and len(stars) == 23, '23 literal stars')
    raw, capped = [], []
    for sid, blocks in enumerate(stars):
        require(len(blocks) == 20, 'twenty blocks')
        owners = {}
        replication = [0] * 17
        family = set()
        for block in blocks:
            require(type(block) is list and len(block) == 4, 'quadruple')
            require(all(type(x) is int and 0 <= x < 17 for x in block), 'point')
            b = tuple(sorted(block))
            require(len(set(b)) == 4 and b not in family, 'distinct block')
            family.add(b)
            for x in b:
                replication[x] += 1
            for pair in itertools.combinations(b, 2):
                require(pair not in owners, 'repeated pair')
                owners[pair] = b
        deficit = [5 - r for r in replication]
        require(min(deficit) >= 0 and sum(deficit) == 5, 'deficit mass')
        leave = set(itertools.combinations(range(17), 2)) - set(owners)
        high = tuple(x for x in range(17) if deficit[x])
        hh = set(p for p in leave if all(x in high for x in p))
        require(len(leave) == 16 and len(hh) == len(high) - 1, 'leave mass')
        for x in range(17):
            require(sum(x in p for p in leave) == 1 + 3 * deficit[x], 'degree')
        require(all(any(x in high for x in p) for p in leave), 'no LOW-LOW')
        for size in range(len(high) + 1):
            for marked in itertools.combinations(high, size):
                hubs = set(marked)
                sat = set(high) - hubs
                q = sum(bool(hubs.intersection(p)) for p in hh)
                eligible = any(all(a not in p for p in hh) for a in hubs)
                h, k = len(high), size
                e = 5 - h
                c1 = sum(deficit[x] == 1 for x in sat)
                sigma = sum(deficit[x] - 1 for x in sat)
                psi = c1 if e == 0 and eligible else -c1 if e > 0 and not eligible else 0
                i5 = int(e == 0 and k == 5)
                mu = psi - 3 * (k - e - q - i5)
                weight = sum(deficit[x] for x in hubs)
                row = (e, k, q, eligible, h, c1, psi, mu, sigma, i5, weight)
                require(mu >= 0, 'corrected charge')
                entry = (sid, marked, row)
                raw.append(entry)
                if all(deficit[x] <= 2 for x in sat) and all(deficit[x] <= 3 for x in hubs):
                    capped.append(entry)
    return raw, capped, sorted(set(r for _, _, r in capped))

def load():
    return reconstruct(json.loads(Path(__file__).with_name('fixtures.json').read_text())['stars'])
