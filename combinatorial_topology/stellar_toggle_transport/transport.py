"""Exact stellar transport of face-lattice toggle words; Python 3.11+.

Vertices are bit positions, faces are nonnegative integer masks, and a complex
is a set of masks including 0. The new lattice top is implicit and is never a
face or move. No numerical packages or solver are used.
"""
from math import comb


def subfaces(face):
    ans = [0]
    while face:
        bit = face & -face
        ans += [x | bit for x in ans]
        face ^= bit
    return ans


def closure(facets):
    return {f for h in facets for f in subfaces(h)}


def mobius(complex_):
    if 0 not in complex_:
        raise ValueError("empty face missing")
    mu = {}
    for face in sorted(complex_, key=lambda x: (-x.bit_count(), x)):
        if not set(subfaces(face)) <= complex_:
            raise ValueError("not a simplicial complex")
        mu[face] = -1 - sum(v for h, v in mu.items() if face & h == face)
    return mu


def stellar(complex_, sigma, new_bit):
    vertices = 0
    for f in complex_:
        vertices |= f
    if not sigma or sigma not in complex_:
        raise ValueError("stellar face must be nonempty and present")
    if new_bit <= 0 or new_bit & (new_bit - 1) or vertices & new_bit:
        raise ValueError("new vertex must be a fresh single bit")
    result = {h for h in complex_ if h & sigma != sigma}
    for h in complex_:
        if h & sigma == sigma:
            for a in subfaces(sigma):
                if a != sigma:
                    result.add(new_bit | a | (h ^ sigma))
    return result


def clear_ideals(generators):
    """Clear their union when initially all on (formal move list)."""
    if not generators:
        return []
    old, last = generators[:-1], generators[-1]
    return (clear_ideals(old)
            + clear_ideals([h & last for h in old])[::-1] + [last])


def local_word(sigma, common):
    """Fill common * boundary(sigma); common is nonempty and disjoint."""
    if not sigma or not common or sigma & common:
        raise ValueError("invalid local simplex data")
    bits = [1 << i for i in range(sigma.bit_length()) if sigma >> i & 1]
    word = []
    for i, b in enumerate(bits):
        facet = common | (sigma ^ b)
        word += clear_ideals([facet ^ earlier for earlier in bits[:i]])
        word.append(facet)
    return word


def compile_word(complex_, word, sigma, new_bit):
    """Return (subdivision, new word, block endpoints).

    The supplied word is checked for legality and a winning final state.
    Endpoints pair each old move with its corresponding new move block.
    """
    new_complex = stellar(complex_, sigma, new_bit)
    mu = mobius(complex_)
    state, result, endpoints = set(), [], []
    for h in word:
        if h not in mu or not mu[h]:
            raise ValueError("old move is absent or has zero Mobius value")
        ideal = set(subfaces(h))
        if not (ideal <= state or ideal.isdisjoint(state)):
            raise ValueError("old ideal is not monochromatic")
        removing = ideal <= state
        if h & sigma != sigma:
            block = [h]
        else:
            block = local_word(sigma, new_bit | (h ^ sigma))
            if removing:
                block.reverse()
        result.extend(block)
        endpoints.append(len(result))
        state ^= ideal
    if state != complex_:
        raise ValueError("old word is not winning")
    return new_complex, result, endpoints


def barycentric_compile(complex_, word):
    """Descending stellar subdivisions, retaining old singleton labels.

    Return final complex/word and label map original nonempty face -> vertex.
    The singleton subdivisions, which would only relabel, are omitted.
    """
    current, result = set(complex_), list(word)
    labels = {h: h for h in complex_ if h.bit_count() == 1}
    next_bit = 1 << max(complex_).bit_length()
    for h in sorted(complex_, key=lambda x: (-x.bit_count(), x)):
        if h.bit_count() < 2:
            continue
        current, result, _ = compile_word(current, result, h, next_bit)
        labels[h] = next_bit
        next_bit <<= 1
    return current, result, labels


def ordered_bell(n):
    # Ordered partitions, classified by the nonempty first block.
    values = [1]
    for q in range(1, n + 1):
        values.append(sum(comb(q, j) * values[q-j]
                          for j in range(1, q + 1)))
    return values[n]
