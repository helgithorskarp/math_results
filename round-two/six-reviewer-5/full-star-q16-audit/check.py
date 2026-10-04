"""Independent literal-coordinate audit of the public q16/k8 certificate.

Only input: the author's explicitly credited integer certificate, not a
program, expected record, numerical search, table, or representation decoder.
All matrix and basis calculations below are independent standard-library code.
"""
import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path


def require(p, label):
    if not p:
        raise ValueError(label)


def pack(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, dict):
        return {str(k): pack(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)):
        return [pack(x) for x in v]
    return v


def canonical(v):
    return (json.dumps(pack(v), sort_keys=True, separators=(',', ':'))+'\n').encode()


def carrier():
    d = {0}
    for size in (1, 2, 3):
        for a in itertools.combinations(range(19), size):
            b = sum(1 << i for i in a)
            if size < 3 or ((b & 7).bit_count() >= 2 and
                            not (b & 7 == 6 and b & 2040)):
                d.add(b)
    return sorted(d)


def orbit(b):
    return (b & 7, (b & 2040).bit_count(), (b & 522240).bit_count())


def image(a, v):
    return [sum(row[j]*x for j, x in v.items()) for row in a]


def dot(v, w):
    return sum(x*w.get(i, 0) for i, x in v.items())


def bilinear(v, av):
    return sum(x*av[i] for i, x in v.items())


def audit(cert, damage=None):
    require(cert['actual_agent'] == 'six-downset-3', 'author attribution')
    require((cert['q'], cert['k'], cert['actual_empty_N'],
             cert['maximum_star_s']) == (16, 8, 232, 52), 'domain metadata')
    D = cert['free_original_entry_denominator']
    require(D == 1024, 'entry denominator')
    full = carrier()
    require(len(full) == 232 and full[0] == 0, 'full carrier/empty')
    for b in full:
        a = b
        while a:
            require(a in full, 'downset submember')
            a = (a-1) & b
    proper = full[1:]
    index = {b: i for i, b in enumerate(proper)}
    n = len(proper)
    star = {i for i, b in enumerate(proper) if b & 1}
    anchor = index[1]
    sizes = [sum(bool(b & (1 << i)) for b in full) for i in range(19)]
    require(sizes == [52, 44, 44]+[21]*8+[22]*8, 'every original star')
    keys = [tuple(tuple(o) for o in k) for k in cert['free_original_entry_orbit_keys']]
    require(keys == sorted(set(keys)) and len(keys) == 143, 'complete key order')
    vals = cert['free_original_entry_numerators']
    require(len(vals) == 143 and all(type(x) is int for x in vals), 'entry values')
    entries = dict(zip(keys, vals))
    c = [[0]*n for _ in proper]
    used = set()
    for i, a in enumerate(proper):
        for j in range(i, n):
            b = proper[j]
            if i == j:
                v = 51*D
            elif a & b:
                v = -D
            elif anchor in (i, j):
                continue
            else:
                key = tuple(sorted((orbit(a), orbit(b))))
                require(key in entries, 'undecoded original pair')
                used.add(key)
                v = entries[key]
            c[i][j] = c[j][i] = v
    require(used == set(entries), 'all and only canonical original pair keys')
    for i in range(n):
        if i not in star:
            c[i][anchor] = c[anchor][i] = -sum(c[i][j] for j in star if j != anchor)
    if damage == 'anchor':
        i = next(i for i in range(n) if i not in star)
        c[i][anchor] += 1
        c[anchor][i] += 1
    if damage == 'intersection':
        i, j = next((i, j) for i in range(n) for j in range(i+1, n)
                    if proper[i] & proper[j])
        c[i][j] += 1
        c[j][i] += 1
    require(all(c[i][j] == c[j][i] for i in range(n) for j in range(n)), 'symmetry')
    require(all(c[i][j] == (51*D if i == j else -D)
                for i in range(n) for j in range(n) if proper[i] & proper[j]), 'support entries')
    require(all(sum(row[j] for j in star) == 0 for row in c), 'entire forced star kernel')
    u = [[D*(232*(i == j)-1)-c[i][j] for j in range(n)] for i in range(n)]
    rows = [sum(row) for row in c]
    l = [[D+sum(rows)]+[D-r for r in rows]]
    for i in range(n):
        l.append([D-rows[i]]+[D+c[i][j] for j in range(n)])
    cap = [[D*232*(i == j)-l[i][j] for j in range(232)] for i in range(232)]
    if damage == 'empty-loop':
        l[0][0] += 1
    usums = [sum(row) for row in u]
    for i in range(232):
        require(sum(l[i]) == 232*D and sum(cap[i]) == 0, 'all original row sums')
        for j in range(232):
            expected = (sum(usums) if i == j == 0 else -usums[j-1] if i == 0
                        else -usums[i-1] if j == 0 else u[i-1][j-1])
            require(cap[i][j] == expected, 'every actual-empty upper-lift entry')
            if full[i] & full[j]:
                require(l[i][j] == D*52*(i == j), 'every original H support entry')
    require(F(l[0][0]-52*D, 180*D) == F(37927, 92160), 'actual empty loop')
    center_star = [232*bool(b & 1)-52 for b in full]
    require(all(sum(x*y for x, y in zip(row, center_star)) == 0 for row in l),
            'all original centered-star images')
    # Full original entries under generators of both pool permutation groups.
    generator_positions = 0
    for pool in (list(range(3, 11)), list(range(11, 19))):
        for x, y in zip(pool, pool[1:]):
            def swap(b):
                return b ^ ((1 << x) | (1 << y)) if bool(b & (1 << x)) != bool(b & (1 << y)) else b
            perm = [index[swap(b)] for b in proper]
            for i in range(n):
                for j in range(n):
                    require(c[i][j] == c[perm[i]][perm[j]], 'all pool-generator original entries')
                    generator_positions += 1

    types = sorted({orbit(b) for b in proper})
    require(len(types) == 23, 'original member types')
    type_rows = {o: [i for i, b in enumerate(proper) if orbit(b) == o] for o in types}
    basis = []
    def add(sector, typ, copy, v):
        v = {i: x for i, x in v.items() if x}
        require(bool(v), 'nonzero original basis vector')
        basis.append((sector, typ, copy, v))
    for o in types:
        add('TT', o, 0, dict.fromkeys(type_rows[o], 1))
    standard_types = {}
    for name, pool in [('Z', range(3, 11)), ('W', range(11, 19))]:
        pool = list(pool)
        eligible = [o for o in types if any(
            bool(proper[i] & (1 << pool[0])) != bool(proper[i] & (1 << pool[1]))
            for i in type_rows[o])]
        standard_types[name] = eligible
        for j in range(1, 8):
            for o in eligible:
                v = {i: int(bool(proper[i] & (1 << pool[0])))-int(bool(proper[i] & (1 << pool[j])))
                     for i in type_rows[o]}
                add(name, o, j, v)
    for name, pool in [('ZZ', list(range(3, 11))), ('WW', list(range(11, 19)))]:
        pairs = list(itertools.combinations(range(1, 8), 2))
        free = [p for p in pairs if p != (1, 2)]
        for j, pair in enumerate(free):
            v = {index[(1 << pool[pair[0]]) | (1 << pool[pair[1]])]: 2,
                 index[(1 << pool[1]) | (1 << pool[2])]: -2}
            for t in range(1, 8):
                v[index[(1 << pool[0]) | (1 << pool[t])]] = 2*((t in (1, 2))-(t in pair))
            add(name, pair, j, v)
            require(v[index[(1 << pool[pair[0]]) | (1 << pool[pair[1]])]] == 2,
                    'unique free pair pivot')
            require(all(sum(x for i, x in v.items() if proper[i] & (1 << p)) == 0 for p in pool),
                    'every pair incidence equation')
    for i in range(4, 11):
        for j in range(12, 19):
            v = {index[(1 << a) | (1 << b)]: x*y
                 for a, x in [(3, 1), (i, -1)] for b, y in [(11, 1), (j, -1)]}
            add('ZW', (i, j), len(basis), v)
            require(v[index[(1 << i) | (1 << j)]] == 1, 'unique interior rectangle pivot')
    dims = {name: sum(b[0] == name for b in basis) for name in ('TT', 'Z', 'W', 'ZZ', 'WW', 'ZW')}
    require(dims == {'TT': 23, 'Z': 56, 'W': 63, 'ZZ': 20, 'WW': 20, 'ZW': 49}
            and len(basis) == n, 'complete original dimension')
    if damage == 'omit-basis':
        basis.pop()
    require(len(basis) == n, 'no omitted original direction')
    if damage == 'cross-sector':
        sector, typ, copy, v = basis[-1]
        v = dict(v)
        v[anchor] = 1
        basis[-1] = (sector, typ, copy, v)
    images = {'lower': [image(c, v) for _, _, _, v in basis],
              'upper': [image(u, v) for _, _, _, v in basis]}
    grams = {}
    for a in ('euclidean', 'lower', 'upper'):
        grams[a] = [[dot(v, w) if a == 'euclidean' else bilinear(v, images[a][j])
                     for j, (_, _, _, w) in enumerate(basis)] for _, _, _, v in basis]
    for i, (si, _, _, _) in enumerate(basis):
        for j, (sj, _, _, _) in enumerate(basis):
            for a in grams:
                require(grams[a][i][j] == grams[a][j][i], 'entire basis Gram symmetry')
                if si != sj:
                    require(grams[a][i][j] == 0, 'every original cross-sector entry')
    # Orthogonality, explicit coordinate pivots, and positive contrast Grams
    # prove full rank; no unverified representation-theory completeness remains.
    for i, (si, oi, ci, _) in enumerate(basis):
        for j, (sj, oj, cj, _) in enumerate(basis):
            if si == sj == 'TT':
                require(grams['euclidean'][i][j] == (len(type_rows[oi]) if i == j else 0),
                        'whole orbit metric')
            if si == sj and si in ('Z', 'W'):
                seed_i = next(k for k, b in enumerate(basis) if b[:3] == (si, oi, 1))
                seed_j = next(k for k, b in enumerate(basis) if b[:3] == (si, oj, 1))
                contrast = 2 if ci == cj else 1
                for a in grams:
                    require(2*grams[a][i][j] == contrast*grams[a][seed_i][seed_j],
                            'every standard-copy original Gram entry')
                if oi != oj:
                    require(grams['euclidean'][i][j] == 0, 'standard physical-type metric')

    sectors = cert['positive_sector_certificates']
    bounds = {}
    residuals = {}
    for name in ('TT', 'Z', 'W', 'ZZ', 'WW', 'ZW'):
        for a in ('lower', 'upper'):
            ids = [i for i, b in enumerate(basis) if b[0] == name]
            block_name = name+'_'+a
            item = sectors[block_name]
            if name in ('ZZ', 'WW', 'ZW'):
                k = ids[0]
                lam = F(grams[a][k][k], grams['euclidean'][k][k])
                for i in ids:
                    v = basis[i][3]
                    require(all(F(images[a][i][r]) == lam*v.get(r, 0) for r in range(n)),
                            'every original scalar-sector image')
                    for j in ids:
                        require(F(grams[a][i][j]) == lam*grams['euclidean'][i][j],
                                'every scalar-sector original Gram entry')
                require(F(item['scalar_gram_numerator'], item['scalar_gram_denominator']) == 4*lam/D,
                        'external scalar certificate matches original action')
                bounds[block_name] = lam/D
                continue
            if name in ('Z', 'W'):
                ids = [i for i in ids if basis[i][2] == 1]
            if name == 'TT' and a == 'lower':
                ids = [i for i in ids if basis[i][1] != (1, 0, 0)]
            g = [[grams[a][i][j] for j in ids] for i in ids]
            triangle = item['factor_lower_triangle_numerators']
            require(len(triangle) == len(ids) and all(len(row) == i+1 for i, row in enumerate(triangle)),
                    'full factor shape: '+block_name+' original '+str(len(ids))+' factor '+str(len(triangle)))
            Q = item['factor_denominator']
            require(Q == 2**32 and item['whole_residual_denominator'] == Q*Q,
                    'factor denominators')
            scale = Q*Q//D
            rem = [[g[i][j]*scale-sum(triangle[i][k]*triangle[j][k]
                    for k in range(min(i, j)+1)) for j in range(len(ids))] for i in range(len(ids))]
            margins = [row[i]-sum(abs(x) for j, x in enumerate(row) if j != i)
                       for i, row in enumerate(rem)]
            require(min(margins) == item['whole_residual_minimum_row_margin_numerator'] > 0,
                    'every exact diagonal-dominance residual')
            largest_norm = max(grams['euclidean'][i][i] for i in ids)
            delta = F(min(margins), Q*Q)
            bounds[block_name] = delta/largest_norm
            residuals[block_name] = {'dimension': len(ids), 'minimum': min(margins),
                                    'maximum_seed_norm_squared': largest_norm,
                                    'rows': margins}
    require(set(bounds) == set(sectors), 'all twelve endpoint blocks')
    require(min(bounds.values()) >= F(1, 128), 'both whole original endpoint margins')
    # All 231 literal images bind to the checked complete Gram decomposition.
    # Positive lower TT principal complement + Ch=0 gives precisely one kernel.

    disjoint = [(i, j) for i in range(n) for j in range(i+1, n) if not proper[i] & proper[j]]
    free = [(i, j) for i, j in disjoint if anchor not in (i, j)]
    nonstar = [i for i in range(n) if i not in star]
    m = {i: sum(j != anchor and not proper[i] & proper[j] for j in star) for i in nonstar}
    require(len(disjoint) == 20282 and len(nonstar) == 179 and len(free) == 20103,
            'entire real repair dimension')
    for i, j in free:
        r = {(i, j): 1, (j, i): 1}
        if i in star or j in star:
            a = j if i in star else i
            r[a, anchor] = r[anchor, a] = -1
        require(all(not proper[a] & proper[b] for a, b in r), 'all repair support entries')
        action = dict.fromkeys(range(n), 0)
        for (a, b), x in r.items():
            if b in star:
                action[a] += x
        require(all(x == 0 for x in action.values()), 'all repair kernel equations')
        require(r[i, j] == 1, 'all unique original-coordinate repair pivots')
    frob_squared = 2*(len(free)+sum(x*x for x in m.values()))
    K = math.isqrt(frob_squared)
    if K*K < frob_squared:
        K += 1
    require((K-1)**2 < frob_squared <= K*K, 'exact Frobenius integer enclosure')
    # all free coefficients +1 simultaneously attain this squared Frobenius bound
    saturated = [[0]*n for _ in proper]
    for i, j in free:
        saturated[i][j] = saturated[j][i] = 1
    for i in nonstar:
        saturated[i][anchor] = saturated[anchor][i] = -m[i]
    require(sum(x*x for row in saturated for x in row) == frob_squared,
            'sharp simultaneous Frobenius budget')
    require(all(sum(row[j] for j in star) == 0 for row in saturated),
            'saturated real-box corner kernel')
    epsilon = F(1, 256*K)
    old_epsilon = F(1, 512*20103)
    require(K*epsilon == F(1, 256) and epsilon > old_epsilon,
            'proved larger real-box radius')
    i = index[1 << 3]
    j = index[(1 << 4) | (1 << 5)]
    require((i, j) in free or (j, i) in free, 'separation entry has its own free coordinate')
    old_fixed_entry = F(16*(16-3), (16-1)*(16-2))-1
    require(old_fixed_entry == F(-1, 105), 'credited defining-entry arithmetic')
    separation = F(c[i][j], D)-old_fixed_entry
    require(F(c[i][j], D) == F(-583, 1024) and separation < 0,
            'actual original center separation')
    require(-separation-epsilon > F(1, 2), 'whole enlarged box remains separated')
    hashes = {'core_lower': hashlib.sha256(canonical(c)).hexdigest(),
              'core_upper': hashlib.sha256(canonical(u)).hexdigest(),
              'full_lower': hashlib.sha256(canonical(l)).hexdigest(),
              'full_upper': hashlib.sha256(canonical(cap)).hexdigest(),
              'basis': hashlib.sha256(canonical(basis)).hexdigest(),
              'whole_grams': hashlib.sha256(canonical(grams)).hexdigest(),
              'whole_images': hashlib.sha256(canonical(images)).hexdigest()}
    return {'domain': {'N': 232, 's': 52, 'proper': n, 'stars': sizes,
                       'member_orbits': types, 'free_edge_orbits': len(entries)},
            'literal_positions': {'proper_entries': n*n, 'full_lift_entries': 232**2,
                                  'endpoint_basis_images': 2*n*n,
                                  'complete_gram_entries': 3*n*n,
                                  'pool_generator_entries': generator_positions},
            'dimensions': dims, 'bounds': bounds, 'residuals': residuals,
            'actual_empty_M_diagonal': F(l[0][0]-52*D, 180*D),
            'full_repair': {'allowed_disjoint_edges': len(disjoint),
                            'independent_coordinates': len(free),
                            'nonstar_rows': len(nonstar),
                            'row_trade_counts': sorted(m.values()),
                            'sharp_Frobenius_squared': frob_squared, 'K': K,
                            'enlarged_box_radius': epsilon, 'old_box_radius': old_epsilon,
                            'radius_factor': epsilon/old_epsilon,
                            'retained_core_margin': F(1, 256),
                            'whole_box_entry_separation': -separation-epsilon},
            'rank_conclusions': {'lower': 231, 'upper': 231, 'unit_multiplicity': 1},
            'hashes': hashes}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--certificate', type=Path, default=Path(__file__).with_name('CERTIFICATE.json'))
    p.add_argument('--out', type=Path)
    p.add_argument('--damage', choices=['anchor', 'intersection', 'empty-loop', 'omit-basis', 'cross-sector'])
    a = p.parse_args()
    record = audit(json.loads(a.certificate.read_text()), a.damage)
    b = canonical(record)
    if a.out:
        a.out.write_bytes(b)
    else:
        print(b.decode(), end='')


if __name__ == '__main__':
    main()
