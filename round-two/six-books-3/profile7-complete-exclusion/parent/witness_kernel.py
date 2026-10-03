"""Exact indexed support with BOTH-endpoint COLOR/parity deficit caps.

Whole pair masks use binary bit-plane cardinality with proved zero-carry skipping. Every
index insertion, bit-plane Boolean operation, support query, and DP update
is charged to the unchanged2M work guard. At most40s inside the45s child.
"""
import time

LIMIT = 2000000
class Limit(Exception):
    pass

def bits(word):
    while word:
        bit = word & -word
        yield bit.bit_length()-1
        word ^= bit

def require(ok,message):
    if not ok:
        raise ValueError(message)


def accumulate(words,star,band,bxor):
    """Exact binary addition; a zero carry leaves all higher planes unchanged."""
    planes=[0,0,0,0]
    for z in bits(star):
        carry=words[z]
        for j in range(3):
            if not carry:
                break
            nxt=band(planes[j],carry)
            planes[j]=bxor(planes[j],carry)
            carry=nxt
        if carry:
            planes[3]=bxor(planes[3],carry)
    return planes


def kernel(types,columns,initial,limit=LIMIT,deadline=None):
    require(type(limit) is int and 0 < limit <= LIMIT, 'Work guard may not increase')
    pool = [tuple(row) for row in initial]
    require(len(pool) == len(types) == len(columns) == 18 and all(pool), 'Wrong indexed scope')
    active = [(1<<len(row))-1 for row in pool]
    all_words = list(active)
    low_masks = [sum(1<<x for x,t in enumerate(types) if t & (1<<i)) for i in range(4)]
    slacks = [[(c >> (2*i)) & 3 for i in range(4)] for c in columns]
    budgets = [2+2*t.bit_count()-sum(s) for t,s in zip(types,slacks)]
    parities = [sum(s[i] for i in bits(t)) % 2 for t,s in zip(types,slacks)]
    require(all(b >= 0 for b in budgets), 'Negative matrix endpoint budget')
    red_upper = [b-((b-p) % 2) for b,p in zip(budgets,parities)]
    blue_upper = [b-p for b,p in zip(budgets,parities)]
    indices = {}
    cache = {}
    steps = []
    work = 0
    started = time.monotonic()
    if deadline is None:
        deadline = started+40
    cursor = None

    def tick():
        nonlocal work
        if work >= limit or time.monotonic() >= deadline:
            raise Limit
        work += 1

    def band(a,b):
        tick(); return a & b

    def bor(a,b):
        tick(); return a | b

    def bxor(a,b):
        tick(); return a ^ b

    def index(y):
        if y not in indices:
            words = [0]*18
            for j,star in enumerate(pool[y]):
                for z in bits(star):
                    words[z] = bor(words[z],1<<j)
            indices[y] = words
        return indices[y]

    def supports(x,sx,y):
        key = (x,sx,y)
        if key not in cache:
            words = index(y)
            edge = bool(sx & (1<<y))
            shared = types[x] & types[y]
            cap = (3 if edge else 6)-shared.bit_count()
            upper = red_upper if edge else blue_upper
            lower = max(0,cap-min(upper[x],upper[y]))
            if cap < lower:
                cache[key] = 0
            else:
                # Add one membership bit-vector at a time to four binary
                # planes. Each candidate's count is its exact intersection
                # size; stars have at most9 high neighbors, hence no carry
                # beyond the fourth plane can occur.
                planes = accumulate(words,sx,band,bxor)
                mask = 0
                for count in range(lower,cap+1):
                    eq = all_words[y]
                    for j,plane in enumerate(planes):
                        chosen = plane if count & (1<<j) else bxor(all_words[y],plane)
                        eq = band(eq,chosen)
                    mask = bor(mask,eq)
                reciprocal = words[x] if edge else bxor(all_words[y],words[x])
                mask = band(mask,reciprocal)
                if edge:
                    forbidden = 0
                    for i in bits(shared):
                        forbidden |= sx & low_masks[i]
                    for z in bits(forbidden):
                        mask = band(mask,bxor(all_words[y],words[z]))
                cache[key] = mask
        return band(cache[key],active[y])

    def avoids(z,common):
        words = index(z)
        forbidden = 0
        for w in bits(common):
            forbidden = bor(forbidden,words[w])
        return band(active[z],bxor(all_words[z],forbidden))

    return dict(pool=pool,active=active,types=types,columns=columns,budgets=budgets,
                parities=parities,red_upper=red_upper,blue_upper=blue_upper,
                supports=supports,avoids=avoids,tick=tick,
                band=band,work=lambda:work,limit=limit)
