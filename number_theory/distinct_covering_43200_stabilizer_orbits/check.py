"""Standalone physical-coordinate verification of the declared stabilizers.

Python integers only. The written covering equivalence is in proof.md.
No search forest, solver, or private artifact is imported.
"""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
from time import monotonic
import orbits

N, Q = orbits.N, orbits.Q


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_partitions(mapping, trigger, shift, divisors):
    require(len(mapping) == N and len(set(mapping)) == N, 'Not a physical bijection')
    require(all(mapping[mapping[x]] == x for x in range(N)), 'Not an involution')
    for m in divisors:
        if m % trigger:
            require(shift % m == 0, 'An untriggered divisor does not divide the shift')
        else:
            # Each such class fixes the triggering leaf. The reference map
            # has a constant translation on that whole leaf; its phase map
            # is checked explicitly here. The written proof supplies this
            # constant-translation bridge, not an affine-only assumption.
            phase_map = [mapping[a] % m for a in range(m)]
            require(len(set(phase_map)) == m, 'A divisor phase map is not bijective')
            require(all(phase_map[phase_map[a]] == a for a in range(m)),
                    'A divisor phase map is not involutive')
    return len(divisors)


def controls():
    parent = [0,0,5,10,1,4,3,17,2,3,11,6,27,19]
    fixtures = [
        lambda: orbits.parent_ok(parent[:13]),
        lambda: orbits.parent_ok(parent[:5]+[16]+parent[6:]),
        lambda: orbits.parent_ok(parent[:5]+[False]+parent[6:]),
        lambda: orbits.quinary_map(N,3,4),
        lambda: orbits.quinary_map(N,3,8,fixed25=3),
        lambda: orbits.quinary_map(N,8,13,fixed_leaves=(3,8)),
        lambda: orbits.binary_rep(48,4),
        lambda: orbits.quinary_rep(True,3),
        lambda: orbits.pinned75_rep(75,3,33),
        lambda: orbits.binary_map(720)]
    rejected = 0
    for fixture in fixtures:
        try:
            fixture()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('An invalid stabilizer fixture was accepted')
    return rejected


def mathematics():
    start = monotonic()
    def cap():
        if monotonic()-start >= 20:
            raise RuntimeError('INCOMPLETE: unchanged20-second mathematical check cap')
    divisors = [m for m in range(1,N+1) if N % m == 0]
    require(len(divisors) == 84, 'Unexpected divisor family')
    binary_lookup = {(x % 675,x % 64):x for x in range(N)}
    quinary_lookup = {(x % 1728,x % 25):x for x in range(N)}
    require(len(binary_lookup) == len(quinary_lookup) == N, 'Physical CRT coordinates not bijective')

    binary_maps = {}
    binary_hash = sha256()
    partition_checks = 0
    for root in range(8):
        cap()
        reference = [binary_lookup[x % 675,
                     (x % 64+8) % 64 if x % 16 == root else
                     (x % 64-8) % 64 if x % 16 == root+8 else x % 64]
                     for x in range(N)]
        actual, actual_q = orbits.binary_map(N,root), orbits.binary_map(Q,root)
        require(actual == reference, 'Binary map differs pointwise from the CRT reference')
        require(all(actual_q[x % Q] == reference[x] % Q for x in range(N)),
                'Binary map does not commute with projection')
        partition_checks += check_partitions(reference,16,16200,divisors)
        for m in orbits.ANCHORS:
            if m == 16:
                require(all(reference[a] % m == a for a in range(m) if a % 8 != root),
                        'A pinned16 class is moved by an allowed generator')
            else:
                require(all(reference[x] % m == x % m for x in range(N)),
                        'A prescribed anchor partition is moved')
        require(all(reference[a] % 50 == a for a in range(50)), 'A binary generator moves a50 phase')
        binary_maps[root] = reference
        binary_hash.update(json.dumps([root,reference],separators=(',',':')).encode()+b'\n')
    binary_tables = [[orbits.binary_rep(a,fixed) for a in range(48)] for fixed in range(16)]
    for fixed,table in enumerate(binary_tables):
        require(len(set(table)) == 27,'Incorrect pinned binary subgroup count')
        for a,rep in enumerate(table):
            root = a % 8
            require(rep == a or (root != fixed % 8 and binary_maps[root][a] % 48 == rep),
                    'Missing binary phase transport')

    identity = list(range(N))
    cache = {}
    maps_hash = sha256()
    commutation_checks = 0
    for root in range(5):
        for j in range(5):
            for k in range(j+1,5):
                cap()
                u,v = root+5*j,root+5*k
                reference = [quinary_lookup[x % 1728,
                             v if x % 25 == u else u if x % 25 == v else x % 25]
                             for x in range(N)]
                actual = orbits.quinary_map(N,u,v)
                actual_q = orbits.quinary_map(Q,u,v)
                require(actual == reference, 'Quinary map differs pointwise from the CRT reference')
                require(all(actual_q[x % Q] == reference[x] % Q for x in range(N)),
                        'Quinary map does not commute with projection')
                partition_checks += check_partitions(reference,25,(reference[u]-u) % N,divisors)
                for binary in binary_maps.values():
                    require(all(binary[reference[x]] == reference[binary[x]] for x in range(N)),
                            'The binary and quinary maps do not commute')
                    commutation_checks += N
                cache[u,v] = reference
                maps_hash.update(json.dumps([u,v,reference],separators=(',',':')).encode()+b'\n')
    def tau(u,v):
        return identity if u == v else cache[tuple(sorted((u,v)))]

    product_hash = sha256()
    product_checks = 0
    orbit_rows = []
    for a in range(25):
        cap()
        quinary_representatives = sorted({orbits.quinary_rep(c,a) for c in range(50)})
        require(len(quinary_representatives) == 12, 'Incorrect single-pin quinary count')
        quinary_table = [orbits.quinary_rep(c,a) for c in range(50)]
        for fixed16 in range(16):
            cap()
            pairs = set()
            for b in range(48):
                br = binary_tables[fixed16][b]
                for c in range(50):
                    cr = quinary_table[c]
                    u,v = c % 25,cr % 25
                    require(u % 5 == v % 5 and (u == v or a not in (u,v)),
                            'A proposed quinary transport moves the fixed leaf')
                    mapping = tau(u,v)
                    image_b,image_c = mapping[b],mapping[c]
                    if br != b:
                        binary = binary_maps[b % 8]
                        image_b,image_c = binary[image_b],binary[image_c]
                        require(binary[fixed16] % 16 == fixed16,'The joint transporter moves the fixed16 class')
                    require(image_b % 48 == br and image_c % 50 == cr,
                            'A raw pair has no proposed physical transport')
                    require(mapping[a] == a, 'Known25 leaf is not fixed pointwise')
                    pairs.add((br,cr))
                    product_hash.update(bytes([fixed16,a,b,c,br,cr]))
                    product_checks += 1
            require(len(pairs) == 324, 'Incorrect declared product orbit count')
        orbit_rows.append([a,quinary_representatives])

    pinned_hash = sha256()
    pinned_cases,pinned_phase_checks = 0,0
    for a in range(25):
        cap()
        for b in range(50):
            reps = set()
            for c in range(75):
                rep = orbits.pinned75_rep(c,a,b)
                u,v = c % 25,rep % 25
                require(u % 5 == v % 5 and (u == v or not {a,b % 25}.intersection((u,v))),
                        'A75 transport moves a pinned leaf')
                mapping = tau(u,v)
                require(mapping[c] % 75 == rep and mapping[a] == a and mapping[b] == b,
                        'The75 representative or a parent class is wrong')
                reps.add(rep)
                pinned_phase_checks += 1
            require(len(reps) == (18 if a == b % 25 else 21), 'Incorrect two-pin75 orbit count')
            pinned_hash.update(json.dumps([a,b,sorted(reps)],separators=(',',':')).encode()+b'\n')
            pinned_cases += 1

    literal75_points = 0
    for c in range(75):
        cap()
        rep = orbits.pinned75_rep(c,3,33)
        mapping = tau(c % 25,rep % 25)
        points = set(range(c,N,75)) | set(range(3,N,25)) | set(range(33,N,50))
        for x in points:
            require((x % 75 != c or mapping[x] % 75 == rep)
                    and (x % 25 != 3 or mapping[x] == x)
                    and (x % 50 != 33 or mapping[x] == x),
                    'Full75 transport does not fix/transport its prescribed classes')
            literal75_points += 1
    cap()
    return {'actual_author':'six-covering-3','role':'researcher','N':N,'Q':Q,
            'divisor_partitions':84,'maps_checked':58,'divisor_compatibility_checks':partition_checks,
            'physical_map_comparisons':58*N,'pointwise_projection_checks':58*N,
            'commutation_point_checks':commutation_checks,'raw48_orbit_count':27,
            'known16_cases':16,'known25_cases':25,'raw50_orbit_count':12,'joint48_50_orbit_count':324,
            'raw_joint_pair_checks':product_checks,'known25_50_cases':pinned_cases,
            'raw75_phase_checks':pinned_phase_checks,'two_distinct_pins75_orbit_count':21,
            'coincident_pins75_orbit_count':18,'literal75_class_point_checks':literal75_points,
            'binary_reference_maps_sha256':binary_hash.hexdigest(),
            'quinary_reference_maps_sha256':maps_hash.hexdigest(),
            'joint_representatives_sha256':product_hash.hexdigest(),
            'pinned75_representatives_sha256':pinned_hash.hexdigest(),
            'orbit_rows_sha256':sha256(json.dumps(orbit_rows,separators=(',',':')).encode()).hexdigest(),
            'minimum_and_actualLCM_preserved_by_maps':True,'is_covering_witness':False,
            'is_period_exclusion':False,'numerical_bound_changed':False,'independent_review':False}


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--emit',action='store_true',help='Print freshly checked fields before comparison with expected.json')
    parser.add_argument('--controls',action='store_true')
    args = parser.parse_args()
    result = mathematics()
    if not args.emit:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        require(result == expected,'Exact expected fields or event hashes differ')
    print(json.dumps({'certificate':result,'controls_rejected':controls() if args.controls else 0,
                      'whole_mathematical_cap_seconds':20},indent=2))
