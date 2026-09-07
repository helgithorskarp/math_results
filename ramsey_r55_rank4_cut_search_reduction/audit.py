#!/usr/bin/env python3
"""Exact counting identities, physical controls and a feasible core witness."""
import copy
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path

import extract
import family
import verify


def require(condition, message):
    if not condition:
        raise ValueError(message)


def spanning(m, r, nonzero=False):
    d = [1] + [0] * r
    for _ in range(m):
        e = [0] * (r + 1)
        for k, value in enumerate(d):
            e[k] += value * ((1 << k) - int(nonzero))
            if k < r:
                e[k + 1] += value * ((1 << r) - (1 << k))
        d = e
    return d[r]


def gaussian(r, k):
    return math.prod((1 << r) - (1 << i) for i in range(k)) // math.prod((1 << k) - (1 << i) for i in range(k))


def mobius_nonzero(m, r):
    return sum(gaussian(r, k) * (-1) ** (r - k) * (1 << ((r-k)*(r-k-1)//2)) * ((1 << k)-1)**m
               for k in range(r + 1))


def onto(m, q):
    d = [1] + [0] * q
    for _ in range(m):
        e = [0] * (q + 1)
        for k in range(q + 1):
            e[k] += k * d[k]
            if k < q:
                e[k + 1] += (q - k) * d[k]
        d = e
    return d[q]


def dense_rank(matrix):
    a = [row[:] for row in matrix]
    k = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(k, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        for i in range(len(a)):
            if i != k and a[i][j]:
                a[i] = [(x + y) % 2 for x, y in zip(a[i], a[k])]
        k += 1
    return k


def count_audit():
    for m in range(1, 24):
        for r in range(5):
            require(spanning(m, r) == math.prod((1 << m)-(1 << i) for i in range(r)), 'full-rank count')
            require(spanning(m, r, True) == mobius_nonzero(m, r), 'nonzero Mobius count')
    enumerated = removed_small = 0
    for m in range(1, 5):
        for n in range(1, 5):
            counts = [0] * (min(m, n) + 1)
            zeros = counts[:]
            for word in range(1 << (m*n)):
                rows = [(word >> (n*i)) & ((1 << n)-1) for i in range(m)]
                r = family.rank(rows)
                counts[r] += 1
                has_col_zero = any(not any(row >> j & 1 for row in rows) for j in range(n))
                if 0 in rows and has_col_zero:
                    zeros[r] += 1
                    require(family.rank([x ^ ((1 << n)-1) for x in rows]) == r+1, 'complement rank')
                    removed_small += 1
                enumerated += 1
            for r in range(min(m, n) + 1):
                gl = spanning(r, r)
                require(counts[r] * gl == spanning(m, r) * spanning(n, r), 'physical rank count')
                require(zeros[r] * gl == (spanning(m,r)-spanning(m,r,True)) * (spanning(n,r)-spanning(n,r,True)), 'physical zero count')
    # Explicitly compare every full-rank factor fiber in dimension two.
    fibers = {}
    for u in itertools.product(range(4), repeat=3):
        if family.rank(u) != 2:
            continue
        for v in itertools.product(range(4), repeat=4):
            if family.rank(v) != 2:
                continue
            word = tuple(sum(((x & y).bit_count() % 2) << j for j, y in enumerate(v)) for x in u)
            fibers[word] = fibers.get(word, 0) + 1
    require(set(fibers.values()) == {6}, 'free basis-action fibers')
    gl = spanning(4, 4)
    total = spanning(20, 4) * spanning(23, 4) // gl
    excluded = (spanning(20,4)-spanning(20,4,True)) * (spanning(23,4)-spanning(23,4,True)) // gl
    for m in (20, 23):
        require(onto(m,16) == sum((-1)**j * math.comb(16,j) * (16-j)**m for j in range(17)), 'onto count')
    full_support = onto(20,16) * onto(23,16) // gl
    require(full_support <= excluded and 56 * total < 100 * excluded < 57 * total, 'material reduction')
    return {'all_rank4_cross_matrices': total, 'excluded_rank4_cross_matrices': excluded,
            'remaining_cross_matrices_before_other_constraints': total-excluded,
            'excluded_fraction': str(Fraction(excluded, total)),
            'full_support_cross_matrices_excluded': full_support,
            'internal_free_pairs': 443, 'basis_fiber_size': gl,
            'small_matrices_checked': enumerated, 'small_zero_pair_matrices': removed_small,
            'rank2_physical_fibers_checked': len(fibers)}


def dense_graph(n, text):
    word = int(text, 16)
    require(word.bit_length() <= n*(n-1)//2, 'dense graph padding')
    mat = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            mat[i][j] = mat[j][i] = word % 2
            word //= 2
    return mat


def core_audit():
    obj = json.loads(Path(__file__).with_name('core32.json').read_text())
    require(obj['n'] == 32 and len(obj['red_hex']) == 124, 'core dimensions')
    mat = dense_graph(32, obj['red_hex'])
    checked = 0
    for q in itertools.combinations(range(32), 5):
        colors = {mat[u][v] for u, v in itertools.combinations(q, 2)}
        require(len(colors) == 2, 'core monochromatic five')
        checked += 1
    for c in (0, 1):
        adj = [sum((mat[u][v] == c) << v for v in range(32) if u != v) for u in range(32)]
        require(extract.clique(adj, (1 << 32)-1, 5) is None, 'independent core clique search')
    for u in range(16):
        for v in range(16):
            require(mat[u][16+v] == (u & v).bit_count() % 2, 'dot table')
    cross = [row[16:] for row in mat[:16]]
    require(dense_rank(cross) == 4 and dense_rank([[1-x for x in row] for row in cross]) == 5, 'core cut ranks')
    require(sum(mat[0]) >= 14 and sum(mat[16]) >= 11, 'necessary core degrees')
    return {'order': 32, 'literal_fives_checked': checked, 'red_fives': 0, 'blue_fives': 0,
            'core_zero_vertex_red_degrees': [sum(mat[0]), sum(mat[16])],
            'sha256': hashlib.sha256(Path(__file__).with_name('core32.json').read_bytes()).hexdigest(),
            'is_43_vertex_target': False}


def controls():
    stream = hashlib.sha256()
    cases = pairs = high = low = 0
    stored = None
    for seed in range(12):
        bits = int.from_bytes(hashlib.sha512(str(seed).encode()).digest(), 'little') & ((1 << 443)-1)
        # One half has high degree at its zero representative in even fixtures.
        if seed % 2 == 0:
            bits |= (1 << 19)-1
        params = {'left': list(range(16)) + [1+seed%15]*4,
                  'right': list(range(16)) + [1+(seed+3)%15]*7,
                  'internal_hex': format(bits, '0111x')}
        obj = family.generate(params)
        require(family.filter_status(params) == 'EXCLUDED_ZERO_TYPES', 'full-support filter')
        mat = dense_graph(43, obj['red_hex'])
        # Independent materialization of every cross edge and every internal bit.
        internal = int(params['internal_hex'], 16)
        for u in range(43):
            for v in range(u+1,43):
                if u < 20 <= v:
                    x, y = params['left'][u], params['right'][v-20]
                    bit = sum(((x >> k)&1)*((y >> k)&1) for k in range(4)) % 2
                else:
                    bit = internal % 2
                    internal //= 2
                require(mat[u][v] == bit, 'physical generator bit')
                pairs += 1
        require(internal == 0, 'internal decoding length')
        for comp, reverse_cut, shift in itertools.product((0,1), (0,1), (0,7)):
            perm = [(v+shift)%43 for v in range(43)]
            moved = [[0]*43 for _ in range(43)]
            for u in range(43):
                for v in range(u+1,43):
                    moved[perm[u]][perm[v]] = moved[perm[v]][perm[u]] = mat[u][v] ^ comp
            word = sum(moved[u][v] << i for i,(u,v) in enumerate(itertools.combinations(range(43),2)))
            cut = sorted(perm[u] for u in (range(20,43) if reverse_cut else range(20)))
            inp = {'n':43,'red_hex':format(word,'0226x'),'cut':cut,'color':1-comp}
            cert = extract.extract(inp)
            verify.verify(inp, cert)
            high += cert['route'] == 'mixed_eighteen'
            low += cert['route'] == 'low_degree_twenty_five'
            stream.update(json.dumps([inp,cert],sort_keys=True).encode())
            cases += 1
        stored = obj, extract.extract(obj)
    # Both filter survivors and rank-deficient inputs have distinct outcomes.
    for side in ('left','right'):
        params = {'left':list(range(16))+[1]*4,'right':list(range(16))+[1]*7,'internal_hex':'0'*111}
        params[side] = [1 if v == 0 else v for v in params[side]]
        require(family.filter_status(params) == 'SURVIVES_ZERO_TYPE_FILTER', 'surviving branch')
        require(extract.extract(family.generate(params))['status'] == 'OUTSIDE_ZERO_PAIR_FAMILY', 'outside extractor')
    obj, cert = stored
    bad_inputs = []
    for key, value in [('n',True),('red_hex','f'*226),('cut',[]),('cut',[0,0]),('cut',[True]),('color',True)]:
        bad = copy.deepcopy(obj);bad[key]=value;bad_inputs.append(bad)
    for bad in bad_inputs:
        for fn in (lambda:extract.extract(bad), lambda:verify.verify(bad,cert)):
            try:fn()
            except ValueError:pass
            else:raise ValueError('accepted malformed input')
    corruptions = []
    for key, value in [('status','UNKNOWN'),('input_sha256','0'*64),('five',[0]*5),('five_color',1-cert['five_color']),('zero_pair',[0,1]),('route','invented')]:
        bad = copy.deepcopy(cert);bad[key]=value;corruptions.append(bad)
    for bad in corruptions:
        try:verify.verify(obj,bad)
        except ValueError:pass
        else:raise ValueError('accepted corrupted certificate')
    require(high > 0 and low > 0, 'both extraction branches')
    return {'physical_certificates_checked':cases,'generator_pairs_checked':pairs,
            'mixed_eighteen_cases':high,'low_degree_cases':low,'surviving_filter_controls':2,
            'malformed_inputs_rejected_by_both_parsers':len(bad_inputs),
            'corrupt_certificates_rejected':len(corruptions),'physical_stream_sha256':stream.hexdigest()}


def run():
    return {'status':'VERIFIED_RANK4_CUT_SEARCH_REDUCTION','counting':count_audit(),
            'physical_controls':controls(),'core_witness':core_audit(),
            'full_support_43_family_excluded':True,'remaining_rank4_family_decided':False,
            'ramsey_graph_found':False,'ramsey_bound_improved':False}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
