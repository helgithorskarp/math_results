"""List-colouring infeasibility tables for connected point sets of size 2, 3, 4.
T_k[shape, idx] = True iff the list-colouring instance (k points, internal edges given by the shape bit-vector over
the pairs in itertools.combinations(range(k), 2) order, free-colour masks packed 4 bits per point into idx) has NO
proper colouring.  Built by vectorised enumeration over all 4^k colour tuples (exhaustive, no solver)."""
import itertools
import numpy as np


def build(k):
    pairs = list(itertools.combinations(range(k), 2))
    shapes = list(itertools.product((0, 1), repeat=len(pairs)))
    M = 16 ** k
    idx = np.arange(M, dtype=np.int64)
    masks = [(idx >> (4 * i)) & 15 for i in range(k)]
    tuples = np.array(list(itertools.product(range(4), repeat=k)), dtype=np.int64)     # (4^k, k)
    allowed = np.zeros((len(tuples), M), dtype=bool)
    for t, cols in enumerate(tuples):
        a = np.ones(M, dtype=bool)
        for i in range(k):
            a &= ((masks[i] >> int(cols[i])) & 1).astype(bool)
        allowed[t] = a
    T = np.zeros((len(shapes), M), dtype=bool)
    for si, s in enumerate(shapes):
        proper = np.ones(len(tuples), dtype=bool)
        for (i, j), bit in zip(pairs, s):
            if bit:
                proper &= tuples[:, i] != tuples[:, j]
        feas = allowed[proper].any(axis=0)
        T[si] = ~feas
    return T, {s: i for i, s in enumerate(shapes)}, pairs


if __name__ == '__main__':
    import time
    t0 = time.time()
    for k in (2, 3, 4):
        T, S, P = build(k)
        print(k, T.shape, int(T.sum()), f'{time.time()-t0:.1f}s')
    T2, S2, _ = build(2)
    assert T2[S2[(1,)], 1 | (1 << 4)] and not T2[S2[(1,)], 1 | (2 << 4)] and T2[S2[(0,)], 0 | (15 << 4)] and not T2[S2[(0,)], 1 | (1 << 4)]
    print('sanity ok')
