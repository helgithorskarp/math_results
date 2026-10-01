"""Complete4096 root-word scan, set-based filters and point relabeling."""
import itertools
from blocks import PAIRS,graph


def local_graph(code):
    pairs = ((0,1),(0,2),(1,2))
    spec = dict(internal=[code>>i&1 for i in range(3)]+[0]*4,
                cross=[(code>>(3+3*pairs.index(pair)))&7 if pair[1]<3 else 0 for pair in PAIRS],
                joins=None)
    return [row & set(range(9)) for row in graph(spec)[:9]]


def encode(rows):
    internal = sum(int(3*i+1 in rows[3*i])<<i for i in range(3))
    masks = [sum(int(3*j+t in rows[3*i])<<t for t in range(3)) for i,j in ((0,1),(0,2),(1,2))]
    return internal+sum(mask<<(3+3*k) for k,mask in enumerate(masks))


def canonical(rows,inside):
    values = []
    for perm in itertools.permutations(range(3)):
        if inside and perm[0]!=0:
            continue
        for shifts in itertools.product(range(3),repeat=3):
            for unit in (1,2):
                relabel = {3*i+t:3*perm[i]+(unit*t+shifts[i])%3 for i in range(3) for t in range(3)}
                changed = [set() for _ in range(9)]
                for old,row in enumerate(rows):
                    changed[relabel[old]] = {relabel[v] for v in row}
                values.append(encode(changed))
    return min(values)


def enumerate_roots():
    records = {}
    for inside in (True,False):
        full = [9]*3+[10]*6 if inside else [10]*9
        initial = {}
        reduced = {}
        for code in range(4096):
            rows = local_graph(code)
            degrees = list(map(len,rows))
            edges = sum(degrees)//2
            if max(degrees)>3 or not (9 if inside else 12)<=edges<=12:
                continue
            sizes = [full[u]-1-degrees[u] for u in range(9)]
            caps = {(u,v):(2 if v in rows[u] else full[u]+full[v]-15)-len(rows[u]&rows[v])
                    for u,v in itertools.combinations(range(9),2)}
            if any(max(0,sizes[u]+sizes[v]-12)>cap for (u,v),cap in caps.items()):
                continue
            representative = canonical(rows,inside)
            initial.setdefault(str(representative),[]).append(code)
            valid = True
            for triple in itertools.combinations(range(9),3):
                total = sum(sizes[u] for u in triple)
                q,r = divmod(total,12)
                lower = 12*q*(q-1)//2+r*q
                upper = sum(caps[u,v] for u,v in itertools.combinations(triple,2))
                if lower>upper:
                    valid = False
                    break
            if valid:
                reduced.setdefault(str(representative),[]).append(code)
        records['inside' if inside else 'outside'] = dict(
            raw_survivors=sum(map(len,initial.values())),canonical_roots=len(initial),
            groups=initial,reduced_raw_survivors=sum(map(len,reduced.values())),
            reduced_canonical_roots=len(reduced),reduced_groups=reduced)
    return records
