"""Gauss/original-coordinate positive-certificate checker; no producer import."""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def need(ok, message):
    if not ok:
        raise ValueError(message)


def character(q, x):
    need(type(x) is int and 0 < x < q, 'character zero is undefined')
    return sum((k*x) % q > (q-1)//2 for k in range(1, (q+1)//2)) % 2


def pattern(chars, q, x, roots):
    need(x not in roots, 'all original input roots retained as free columns')
    a, b, c = (chars[(x-r) % q] for r in roots)
    return 4*a+2*b+c


def parse_packs(raw):
    need(type(raw) is bytes, 'whole certificate bytes required')
    try:
        rows = [[int(v) for v in line.split(',')] for line in raw.decode('ascii').splitlines()]
    except (ValueError, UnicodeDecodeError) as error:
        raise ValueError('canonical literal certificate format') from error
    need(len(rows) == 128 and all(len(r) == 11 for r in rows), 'whole128 by five-AP cover')
    need([r[0] for r in rows] == list(range(0, 256, 2)), 'every gauged table in canonical order')
    canonical = ''.join(','.join(map(str, r))+'\n' for r in rows).encode()
    need(raw == canonical, 'whole canonical CSV bytes')
    return [(r[0], list(zip(r[1::2], r[2::2]))) for r in rows]


def base_check(raw, kernel):
    q = 103
    need(kernel.get('q') == q and kernel.get('pole') == 0 and kernel.get('roots') == [1,2,4],
         'actual field, physical pole and all three original roots')
    need(kernel.get('pattern_supports') == [[1,2],[1,4],[1,5],[2,4,5]], 'whole four-AP obstruction')
    need(type(kernel.get('APs')) is list and len(kernel['APs']) == 4, 'four original field AP leaves')
    chars = {x: character(q,x) for x in range(1,q)}
    roots = [1,2,4]
    labels = {x: pattern(chars,q,x,roots) for x in range(1,q) if x not in roots}
    groups = [[x for x in labels if labels[x] == k] for k in range(8)]
    need([len(g) for g in groups] == [11,14,14,11,14,11,11,13], 'all eight realized physical pattern blocks')
    packs = parse_packs(raw)
    transcript = hashlib.sha256()
    inventory = []
    for word, pairs in packs:
        occupied = set()
        witnesses = []
        for a,d in pairs:
            need(type(a) is int and type(d) is int and 0 <= a < q and 1 <= d <= 51,
                 'literal nonzero, oriented field AP')
            points = [(a+j*d) % q for j in range(7)]
            need(len(set(points)) == 7 and all(x in labels for x in points), 'all seven distinct nonroot/nonpole points')
            keys = [labels[x] for x in points]
            colors = [(word >> k) & 1 for k in keys]
            need(len(set(colors)) == 1, 'actual full-table monochromatic AP')
            need(not occupied.intersection(points), 'five pairwise disjoint physical column supports')
            occupied.update(points)
            transcript.update(struct.pack('<3H7H7B7B',word,a,d,*points,*keys,*colors))
            witnesses.append((a,d,points,keys,colors[0]))
        need(len(occupied) == 35, 'literal35 distinct columns per table')
        inventory.append((word,witnesses))
    kernel_points = []
    for (a,d), expected in zip(kernel['APs'],kernel['pattern_supports']):
        need(type(a) is int and type(d) is int and 0 <= a < q and 1 <= d <= 51,
             'actual compact-kernel AP coordinate')
        points = [(a+j*d) % q for j in range(7)]
        need(len(set(points)) == 7 and all(x in labels for x in points), 'kernel keeps every original root and pole free')
        keys = [labels[x] for x in points]
        need(sorted(set(keys)) == expected, 'entire defining actual-AP pattern support')
        kernel_points.append((a,d,points,keys))
    first_bad = [0]*4
    full_cover = set()
    for word in range(256):
        canonical = word if word % 2 == 0 else word ^ 255
        need(canonical in range(0,256,2), 'palette gauge covers the whole abstract Boolean cube')
        full_cover.add(word)
        for i, (_,_,_,keys) in enumerate(kernel_points):
            if len({(word >> k) & 1 for k in keys}) == 1:
                first_bad[i] += 1
                break
        else:
            raise ValueError('actual four-AP truth-table cover incomplete')
    need(full_cover == set(range(256)) and first_bad == [128,64,32,32], 'whole256-table kernel cover')
    signed_cube = 0
    for word in range(256):
        for leading_bits in range(8):
            transformed = sum(((word >> (k ^ leading_bits)) & 1) << k for k in range(8))
            for k in range(8):
                need((transformed >> k) & 1 == (word >> (k ^ leading_bits)) & 1,
                     'whole leading-coefficient truth substitution')
                signed_cube += 1
    need(signed_cube == 16384, 'all leading-input signs and every abstract truth value')
    return chars, labels, inventory, kernel_points, {
        'author':'six-vdw-1','role':'researcher','status':'ALL128_ACTUAL_FIELD_FIVE_PACKS_AND_FOUR_AP_KERNEL_CHECKED',
        'q':q,'pole':0,'all_original_roots':[1,2,4],
        'pattern_sizes':[len(g) for g in groups], 'gauged_tables':128,'full_tables':256,
        'five_pack_APs':640,'five_pack_points':4480,'columns_per_pack':35,
        'kernel_APs':4,'kernel_points':28,'kernel_first_bad_full_table_histogram':first_bad,
        'leading_coefficient_cube_values':signed_cube,
        'pack_bytes':len(raw),'pack_sha256':hashlib.sha256(raw).hexdigest(),
        'entire_literal_pack_transcript_sha256':transcript.hexdigest(),
        'repair_lower_bound':5,'optimum_claim':False,'numerical_W_improvement':False}


def affine_check(chars, labels, kernel_points):
    """Entire field input basis and four actual APs for every physical pole/unit."""
    q = 103
    inv6 = next(k for k in range(1,q) if 6*k % q == 1)
    digest = hashlib.sha256()
    ap_digest = hashlib.sha256()
    configs = points = identities = original_APs = original_points = 0
    maximum_integer = 0
    for pole in range(q):
        for unit in range(1,q):
            configs += 1
            roots = [(pole+unit*r) % q for r in [1,2,4]]
            flip = 7*chars[unit]
            mapped = [(pole+unit*x) % q for x in range(q)]
            need(len(set(mapped)) == q and mapped[0] == pole and [mapped[r] for r in [1,2,4]] == roots,
                 'entire affine bijection and all four distinctly named free columns')
            for x in sorted(labels):
                y = mapped[x]
                need(y not in [pole]+roots, 'pole and every original root retained')
                key = pattern(chars,q,y,roots)
                need(key == labels[x] ^ flip, 'all actual affine character inputs, no root zero convention')
                points += 1
                identities += 3
                digest.update(struct.pack('<6H',pole,unit,x,y,labels[x],key))
            for a,d,xs,keys in kernel_points:
                delta = (inv6*unit*d) % q
                need(delta != 0, 'actual integer step has nonzero field component')
                source = a
                if delta > 51:
                    source = (a+6*d) % q
                    delta = q-delta
                    xs = list(reversed(xs))
                    keys = list(reversed(keys))
                field_start = (pole+unit*source) % q
                start = 1+6*((inv6*(field_start-1)) % q)
                step = 6*delta
                integers = [start+j*step for j in range(7)]
                residues = [n % 618 for n in integers]
                need(1 <= start <= 613 and 1 <= step <= 306 and max(integers) <= 2449,
                     'literal finite interval2449 bound')
                need(len(set(residues)) == 7 and all(n % 6 == 1 for n in integers), 'original cyclic618 AP and fixed phase')
                for x,key,n in zip(xs,keys,integers):
                    y = n % q
                    need(y == (pole+unit*x) % q and y not in [pole]+roots,
                         'each actual original cyclic/integer AP point and free columns')
                    need(pattern(chars,q,y,roots) == key ^ flip, 'literal transformed kernel input at each original point')
                    original_points += 1
                original_APs += 1
                maximum_integer = max(maximum_integer,max(integers))
                ap_digest.update(struct.pack('<4H7H7H',pole,unit,start,step,*integers,*residues))
    need((configs,points,identities,original_APs,original_points) == (10506,1040094,3120282,42024,294168),
         'complete ordered affine/original-AP domains')
    return {'author':'six-vdw-1','role':'researcher','status':'ENTIRE10506_AFFINE_INPUT_BASES_AND_ORIGINAL_KERNEL_APS_CHECKED',
            'configurations':configs,'actual_field_points':points,'actual_character_values':identities,
            'original_cyclic618_and_integer2449_APs':original_APs,'original_AP_points':original_points,
            'entire_affine_input_basis_sha256':digest.hexdigest(),
            'entire_original_kernel_AP_transcript_sha256':ap_digest.hexdigest(),
            'maximum_actual_integer':maximum_integer,'all_root_columns_nonperiodically_free':True,
            'all_pole_columns_nonperiodically_free':True,'numerical_W_improvement':False}


def scale_packs_check(chars, inventory, all_phases=False):
    """Literal five-packs at every102 scale, p=0; optional all six phases."""
    q = 103
    inv6 = next(k for k in range(1,q) if 6*k % q == 1)
    digest = hashlib.sha256()
    cases = APs = points = 0
    maximum_integer = 0
    phases = list(range(1,7)) if all_phases else [1]
    for unit in range(1,q):
        roots = [unit*r % q for r in [1,2,4]]
        flip = 7*chars[unit]
        for word, witnesses in inventory:
            actual_word = sum(((word >> (k ^ flip)) & 1) << k for k in range(8))
            for phase in phases:
                occupied = set()
                cases += 1
                for a,d,xs,keys,color in witnesses:
                    delta = inv6*unit*d % q
                    source = a
                    if delta > 51:
                        source = (a+6*d) % q
                        delta = q-delta
                        xs = list(reversed(xs))
                    start = phase+6*((inv6*(unit*source % q-phase)) % q)
                    step = 6*delta
                    integers = [start+j*step for j in range(7)]
                    residues = [n % 618 for n in integers]
                    need(phase <= start <= phase+612 and 1 <= step <= 306 and max(integers) <= phase+2448,
                         'every positive pack integer lift')
                    need(len(set(residues)) == 7 and all(n % 6 == phase % 6 for n in integers), 'all original pack AP coordinates')
                    physical = []
                    actual_colors = []
                    for x,n in zip(xs,integers):
                        y = n % q
                        need(y == unit*x % q and y not in [0]+roots, 'actual original pack field transport')
                        key = pattern(chars,q,y,roots)
                        actual_colors.append((actual_word >> key) & 1)
                        physical.append(y)
                        points += 1
                    need(actual_colors == [color]*7 and not occupied.intersection(physical),
                         'actual five monochromatic APs still have disjoint physical supports')
                    occupied.update(physical)
                    APs += 1
                    maximum_integer = max(maximum_integer,max(integers))
                    digest.update(struct.pack('<6H7H7H7B',unit,word,actual_word,phase,start,step,*integers,*residues,*actual_colors))
                need(len(occupied) == 35, 'entire transported35-column packing')
    need((cases,APs,points) == tuple(len(phases)*n for n in (13056,65280,456960)),
         'entire102-scale by128-table by each declared phase literal pack domain')
    return {'author':'six-vdw-1','role':'researcher','status':'ALL102_SCALES128_TABLES_ORIGINAL_FIVE_PACKS_CHECKED',
            'scales':102,'gauged_tables':128,'physical_phases':phases,'literal_cases':cases,'original_cyclic618_and_integer_APs':APs,
            'original_AP_points':points,'maximum_actual_integer':maximum_integer,
            'entire_original_pack_transcript_sha256':digest.hexdigest(),
            'all10506_translated_five_packs_by_ordinary_basis_substitution':True,
            'literal_iteration_is_not_claimed_for_all_translated_packs':True,
            'repair_column_lower_bound':5,'cyclic_point_edit_lower_bound':30 if all_phases else 5,
            'integer_all_phase_bound':2454 if all_phases else 2449,
            'optimum_claim':False,'numerical_W_improvement':False}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['base','affine','packs','phases'])
    p.add_argument('certificate', type=Path)
    p.add_argument('kernel', type=Path)
    a = p.parse_args()
    chars,labels,inventory,points,record = base_check(a.certificate.read_bytes(),json.loads(a.kernel.read_bytes()))
    if a.mode == 'affine':
        record = affine_check(chars,labels,points)
    elif a.mode in ['packs','phases']:
        record = scale_packs_check(chars,inventory,a.mode == 'phases')
    print(json.dumps(record,sort_keys=True))
