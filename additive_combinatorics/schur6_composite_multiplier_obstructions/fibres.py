"""Exact finite fibre argument excluding an order-7 multiplier at modulus 539."""
import hashlib
import itertools
import json

P = 11
FULL = (1 << P) - 1
TRIPLES = [(x,y,(x+y)%7) for x in range(1,7) for y in range(x,7) if (x+y)%7]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def negative(a):
    return sum(1 << ((-i) % P) for i in range(P) if a >> i & 1)


def sumset(a, b):
    out = 0
    while a:
        low = a & -a
        i = low.bit_length() - 1
        out |= ((b << i) | (b >> (P-i))) & FULL
        a ^= low
    return out


def verify_sumset_inequality():
    # Independent translations put 0 in each nonempty subset. Commutativity
    # then permits unordered pairs of the 1024 odd bitmasks.
    checked = 0
    for a in range(1, FULL+1, 2):
        for b in range(a, FULL+1, 2):
            require(sumset(a,b).bit_count() >= min(P, a.bit_count()+b.bit_count()-1),
                    "sumset size inequality failed")
            checked += 1
    return checked


def pair_index(x):
    return min(x, 7-x) - 1


def size_profiles():
    possible = []
    for row in itertools.product(range(12), repeat=3):
        for x,y,z in TRIPLES:
            a,b,c = (row[pair_index(t)] for t in (x,y,z))
            if a and b and min(11,a+b-1)+c > 11:
                break
        else:
            possible.append(row)
    valid = set(possible)
    decompositions = []
    for i, a in enumerate(possible):
        for b in possible[i:]:
            c = tuple(11-a[j]-b[j] for j in range(3))
            if c >= b and c in valid:
                decompositions.append((a,b,c))
    return possible, decompositions


def valid_fibres(row):
    sets = {1:row[0], 2:row[1], 3:row[2],
            4:negative(row[2]), 5:negative(row[1]), 6:negative(row[0])}
    return all(not (sumset(sets[x],sets[y]) & sets[z]) for x,y,z in TRIPLES)


def subsets(size):
    return [sum(1 << x for x in chosen)
            for chosen in itertools.combinations(range(11), size)]


def classify_dense(sizes):
    # Doubling cycles the pair labels 1 -> 2 -> 3 -> 1. When consecutive
    # fibre sizes are 4, the target fibre is the complement of the sumset
    # (with a sign for 2*2=-3 and 2*3=-1). This is forced, not a pruning guess.
    source = next(i for i in range(3) if sizes[i] == sizes[(i+1)%3] == 4)
    target = (source+1) % 3
    other = 3-source-target
    out = []
    for a in subsets(4):
        summed = sumset(a,a)
        if summed.bit_count() != 7:
            continue
        b = FULL ^ summed
        if source in (1,2):
            b = negative(b)
        for c in subsets(sizes[other]):
            row = [0,0,0]
            row[source], row[target], row[other] = a,b,c
            if valid_fibres(row):
                out.append(tuple(row))
    return sorted(out)


def run():
    pairs = verify_sumset_inequality()
    possible, decompositions = size_profiles()
    dense = {sizes:classify_dense(sizes)
             for sizes in [(4,4,4),(3,4,4),(4,3,4),(4,4,3)]}
    require(all(not any(mask & 1 for mask in row) for row in dense[4,4,4]),
            "a (4,4,4) colour meets the zero-coordinate slice")
    # A proper three-colouring on the zero-coordinate copy of Z/7 minus 0
    # uses all three colours. Hence no colour can have profile (4,4,4).
    survivors = [rows for rows in decompositions if (4,4,4) not in rows]
    last = set(dense[4,4,3])
    covers = 0
    for a in dense[3,4,4]:
        for b in dense[4,3,4]:
            if any(x & y for x,y in zip(a,b)):
                continue
            c = tuple(FULL ^ (x | y) for x,y in zip(a,b))
            covers += c in last
    require(covers == 0, "balanced dense fibres form a partition")
    balanced = tuple(sorted(((3,4,4),(4,3,4),(4,4,3))))
    survivors = [rows for rows in survivors if rows != balanced]
    require(len(survivors) == 2 and all(max(row) >= 10 for rows in survivors for row in rows),
            "unexpected profile survives")
    catalog = json.dumps({str(k):v for k,v in dense.items()}, sort_keys=True, separators=(",",":"))
    return {"normalized_subset_pairs":pairs, "admissible_size_rows":len(possible),
            "size_decompositions":[[list(row) for row in rows] for rows in decompositions],
            "dense_fibre_counts":{str(k):len(v) for k,v in dense.items()},
            "dense_catalog_sha256":hashlib.sha256(catalog.encode()).hexdigest(),
            "balanced_covers":covers,
            "surviving_profiles":[[list(row) for row in rows] for rows in survivors]}
