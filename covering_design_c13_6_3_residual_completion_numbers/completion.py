"""Lift local compatibility and exhaust regular ten-block completions."""

from hashlib import sha256
from itertools import combinations

from local import require


def validate_through(rows):
    require(len(rows) == len(set(rows)) == 12, 'through-family size or duplicate')
    require(all(type(row) is int and 0 <= row < 4096 and row.bit_count() == 5 for row in rows),
            'through-row domain')
    require(all(sum(row >> p & 1 for row in rows) == 5 for p in range(12)),
            'through point degree')
    require(all(1 <= sum(row & pair == pair for row in rows) <= 2
                for pair in (sum(1 << p for p in pair) for pair in combinations(range(12), 2))),
            'through pair multiplicity')
    require(all((left & right).bit_count() <= 2 for left, right in combinations(rows, 2)),
            'through row intersection')


def validate_completion(rows, blocks):
    require(len(blocks) == len(set(blocks)), 'duplicate residual block')
    require(all(type(b) is int and 0 <= b < 4096 and b.bit_count() == 6 for b in blocks),
            'residual block domain')
    require(all(any(row & triple == triple for row in rows + blocks)
                for triple in (sum(1 << p for p in t) for t in combinations(range(12), 3))),
            'missed triple in completion')
    require(all(sum(block >> p & 1 for block in blocks) >= 5 for p in range(12)),
            'residual point degree below the proved lower bound')


def compatibility_graph(rows, local_columns, allowed, compatible):
    maps = []
    for point in range(12):
        through = [row for row in rows if row >> point & 1]
        columns = {q: sum(1 << i for i, row in enumerate(through) if row >> q & 1)
                   for q in range(12) if q != point}
        singles = sorted(c.bit_length() - 1 for c in columns.values() if c.bit_count() == 1)
        require(len(singles) == len(set(singles)) == 2, 'local singleton normalization')
        order = singles + [i for i in range(5) if i not in singles]
        normalized = {q: sum(1 << i for i, old in enumerate(order) if c >> old & 1)
                      for q, c in columns.items()}
        require(set(normalized.values()) == set(local_columns), 'local columns are not K5-e')
        maps.append({q: local_columns.index(c) for q, c in normalized.items()})

    candidates = []
    residues = {}
    for subset in combinations(range(12), 6):
        block = sum(1 << p for p in subset)
        local = {p: sum(1 << maps[p][q] for q in subset if q != p) for p in subset}
        if all(mask in allowed for mask in local.values()):
            candidates.append(block)
            residues[block] = local
    adjacency = [0] * len(candidates)
    for i, left in enumerate(candidates):
        for j in range(i + 1, len(candidates)):
            right = candidates[j]
            if all(tuple(sorted((residues[left][p], residues[right][p]))) in compatible
                   for p in range(12) if (left & right) >> p & 1):
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
    digest = sha256(''.join(f'{row:x}\n' for row in adjacency).encode()).hexdigest()
    summary = dict(vertices=len(candidates), edges=sum(row.bit_count() for row in adjacency) // 2,
                   adjacency_sha256=digest)
    return candidates, adjacency, summary


def regular_completion(rows, blocks, adjacency):
    """Decide existence of a ten-block completion; no time or node cutoff."""
    index = {block: i for i, block in enumerate(blocks)}
    triples = [sum(1 << p for p in t) for t in combinations(range(12), 3)
               if not any(all(row >> p & 1 for p in t) for row in rows)]
    coverage = [sum(1 << i for i, t in enumerate(triples) if block & t == t) for block in blocks]
    point_vertices = [sum(1 << i for i, b in enumerate(blocks) if b >> p & 1) for p in range(12)]
    triple_vertices = [sum(1 << i for i, b in enumerate(blocks) if b & t == t) for t in triples]
    degrees = [0] * 12
    nodes = tails = 0

    def expand(vertices, path, missing):
        nonlocal nodes, tails
        nodes += 1
        remaining_slots = 10 - len(path)
        for p in range(12):
            if degrees[p] == 5:
                vertices &= ~point_vertices[p]
            if (degrees[p] > 5 or degrees[p] + remaining_slots < 5
                    or (vertices & point_vertices[p]).bit_count() < 5 - degrees[p]):
                return None
        if vertices.bit_count() < remaining_slots:
            return None

        if remaining_slots == 2:
            tails += 1
            twice = sum(1 << p for p in range(12) if degrees[p] == 3)
            once = sum(1 << p for p in range(12) if degrees[p] == 4)
            choices = vertices
            while choices:
                bit = choices & -choices
                i = bit.bit_length() - 1
                choices ^= bit
                block = blocks[i]
                if block & twice != twice or block & ~(twice | once):
                    continue
                partner = twice | (once ^ (block & once))
                j = index.get(partner)
                if (j is not None and j != i and (vertices & adjacency[i]) >> j & 1
                        and not missing & ~(coverage[i] | coverage[j])):
                    return path + [i, j]
            return None

        uncovered = missing
        while uncovered:
            bit = uncovered & -uncovered
            t = bit.bit_length() - 1
            uncovered ^= bit
            if not vertices & triple_vertices[t]:
                return None

        # Greedy independent color classes upper-bound any candidate clique.
        uncolored = vertices
        order = []
        bounds = []
        color = 0
        while uncolored:
            color += 1
            independent = uncolored
            while independent:
                bit = independent & -independent
                v = bit.bit_length() - 1
                order.append(v)
                bounds.append(color)
                uncolored ^= bit
                independent ^= bit
                independent &= ~adjacency[v]
        for position in range(len(order) - 1, -1, -1):
            if len(path) + bounds[position] < 10:
                return None
            v = order[position]
            block = blocks[v]
            for p in range(12):
                degrees[p] += block >> p & 1
            result = expand(vertices & adjacency[v], path + [v], missing & ~coverage[v])
            for p in range(12):
                degrees[p] -= block >> p & 1
            if result is not None:
                return result
            vertices ^= 1 << v
        return None

    result = expand((1 << len(blocks)) - 1, [], (1 << len(triples)) - 1)
    witness = None if result is None else [blocks[i] for i in result]
    if witness is not None:
        validate_completion(rows, witness)
    return witness, dict(search_states=nodes, two_block_tails=tails)
