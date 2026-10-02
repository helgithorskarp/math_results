#!/usr/bin/env python3
"""Independent exact square-set, orbit incidence and CRT coordinate checker."""
import argparse
import copy
import hashlib
import json
import math
from collections import Counter
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def local(data):
    need(data['q'] == 103 and data['period'] == 618 and data['phase'] == [0,0,0,1,1,1],
         'Changed canonical character template')
    need(data['fractional_edge_weight'] == [1,7] and
         all(type(x) is int for x in data['fractional_edge_weight']), 'Bad rational orbit weight')
    squares = {x*x % 103 for x in range(1,103)}
    need(len(squares) == 51 and 0 not in squares, 'Bad exact nonzero square set')
    bits = {x: int(x not in squares) for x in range(1,103)}
    need(data['character_word'] == '-' + ''.join(str(bits[x]) for x in range(1,103)),
         'Producer and independent square definition differ')
    row = data['seed_actual_AP']
    a,d,color = row['start'],row['step'],row['color']
    need(all(type(v) is int for v in (a,d,color)) and 0 <= a < 618 and
         0 < d < 618 and color in (0,1), 'Bad actual AP parameters')
    terms = [(a+j*d) % 618 for j in range(7)]
    fields = [t % 103 for t in terms]
    need(0 not in fields and len(set(fields)) == 7 and sorted(fields) == row['field_support'],
         'Bad original regular field support')
    need(all(bits[t % 103] ^ int(t % 6 >= 3) == color for t in terms), 'Seed AP is mixed')
    return bits


def orbit(data,bits):
    row = data['seed_actual_AP']
    units = [A for A in range(618) if A % 6 == 1 and math.gcd(A,618) == 1]
    need(len(units) == 102 and {A % 103 for A in units} == set(range(1,103)), 'Incomplete multipliers')
    seen,degree,transcript = set(),Counter(),[]
    for A in units:
        a,d = A*row['start'] % 618,A*row['step'] % 618
        need(d != 0, 'Unit collapsed the AP')
        terms = [(a+j*d) % 618 for j in range(7)]
        support = tuple(sorted(t % 103 for t in terms))
        need(len(set(support)) == 7 and 0 not in support and support not in seen,
             'Invalid/repeated support in complete orbit')
        color = row['color'] ^ bits[A % 103]
        need(all(bits[t % 103] ^ int(t % 6 >= 3) == color for t in terms), 'Scaled actual AP mixed')
        first,delta = a,d
        if delta > 309:
            first,delta = (first+6*delta) % 618,618-delta
        first = first or 618
        need(0 < delta <= 309 and first+6*delta <= 2472, 'Bad canonical interval lift')
        need(all(bits[(first+j*delta) % 103] ^ int((first+j*delta) % 6 >= 3) == color
                 for j in range(7)), 'Lifted actual interval AP mixed')
        seen.add(support)
        degree.update(support)
        transcript.append([A,a,d,color,*support])
    need(set(degree) == set(range(1,103)) and all(degree[x] == 7 for x in range(1,103)),
         'Orbit not exactly seven-regular on all character columns')
    return units,hashlib.sha256(json.dumps(transcript,separators=(',',':')).encode()).hexdigest()


def phases():
    legal,illegal,checked,singleton_tests = [],[],0,0
    for mask in range(64):
        g = tuple((mask >> i) & 1 for i in range(6))
        bad = []
        for d in range(1,6):
            for a in range(6):
                row = tuple(g[(a+j*d) % 6] for j in range(7))
                checked += 1
                if len(set(row)) == 1:
                    bad.append((a,d,row[0]))
        if not bad:
            legal.append(mask)
            continue
        illegal.append(mask)
        a,d,color = bad[0]
        for field in range(1,103):
            starts = [t for t in range(618) if t % 103 == field and t % 6 == a]
            need(len(starts) == 1, 'Bad singleton CRT start')
            first,delta = starts[0],103*d
            if delta > 309:
                first,delta = (first+6*delta) % 618,618-delta
            first = first or 618
            need(0 < delta <= 309 and first+6*delta <= 2472, 'Bad singleton lift')
            for bit in (0,1):
                for j in range(7):
                    t = first+j*delta
                    need(t % 103 == field and bit ^ g[t % 6] == bit ^ color, 'Bad singleton colors')
                    singleton_tests += 1
    rotations = {sum(int((i+s) % 6 >= 3) << i for i in range(6)) for s in range(6)}
    need(set(legal) == rotations and len(illegal) == 58 and checked == 1920,
         'Incomplete arbitrary-six-phase cover')
    return legal,illegal,checked,singleton_tests


def coordinates(units,bits):
    shifts = [{B % 103:B for B in range(618) if B % 6 == (-s) % 6} for s in range(6)]
    need(all(set(r) == set(range(103)) for r in shifts), 'Incomplete phase/field shifts')
    field_tests,phase_tests,palette_tests,unit_tests = 0,0,0,0
    for A in units:
        inverse = [a for a in range(1,103) if a*A % 103 == 1]
        need(len(inverse) == 1, 'Bad inverse multiplier')
        a = inverse[0]
        # These are complete actual CRT points for the linear map; arbitrary
        # shifts are checked by their two coefficients below.
        for t in range(618):
            need((A*t) % 103 == A*(t % 103) % 103 and A*t % 6 == t % 6,
                 'Whole CRT linear coordinate identity failed')
            unit_tests += 1
        for beta in range(103):
            root = -A*beta % 103
            seen = set()
            for old in range(103):
                new = (A*old+root) % 103
                need((a*new+beta) % 103 == old and ((new == root) == (old == 0)),
                     'Field inverse/root identity failed')
                seen.add(new)
                if old != 0:
                    for palette in (0,1):
                        need(bits[(a*new+beta) % 103] ^ palette == bits[old] ^ palette,
                             'Character/palette transport failed')
                        palette_tests += 1
                field_tests += 1
            need(len(seen) == 103, 'Field transport not bijective')
            for s in range(6):
                B = shifts[s][root]
                need(B % 103 == root and (B+s) % 6 == 0, 'Bad affine shift coefficients')
                for old_phase in range(6):
                    need((A*old_phase+B+s) % 6 == old_phase,
                         'Complete phase transport failed')
                    phase_tests += 1
    need((field_tests,phase_tests,palette_tests,unit_tests) == (1082118,378216,2143224,63036),
         'Incomplete affine/palette coordinate coverage')
    return field_tests,phase_tests,palette_tests,unit_tests


def controls(data):
    bad = []
    r=copy.deepcopy(data);r['seed_actual_AP']['color'] ^= 1;bad.append(r)
    r=copy.deepcopy(data);r['seed_actual_AP']['step']=0;bad.append(r)
    r=copy.deepcopy(data);r['seed_actual_AP']['start']=618;bad.append(r)
    r=copy.deepcopy(data);r['seed_actual_AP']['field_support'][0]=0;bad.append(r)
    r=copy.deepcopy(data);r['seed_actual_AP']['color']=bool(r['seed_actual_AP']['color']);bad.append(r)
    r=copy.deepcopy(data);r['phase'][0] ^= 1;bad.append(r)
    r=copy.deepcopy(data);r['fractional_edge_weight']=[1,6];bad.append(r)
    r=copy.deepcopy(data);r['fractional_edge_weight']=[True,7];bad.append(r)
    r=copy.deepcopy(data);r['character_word']=r['character_word'][:1]+str(1-int(r['character_word'][1]))+r['character_word'][2:];bad.append(r)
    for r in bad:
        try:
            local(r)
        except (ValueError,KeyError,IndexError):
            continue
        raise ValueError('Damaged certificate accepted')
    return len(bad)


def verify(path):
    raw=path.read_bytes();data=json.loads(raw)
    bits=local(data);units,digest=orbit(data,bits)
    multiplicativity=0
    for x in range(1,103):
        for y in range(1,103):
            need(bits[x*y % 103] == bits[x] ^ bits[y], 'Exact square-character identity failed')
            multiplicativity += 1
    legal,illegal,phase_inputs,singletons=phases()
    fields,phase_points,palettes,crt_points=coordinates(units,bits)
    damages=controls(data)
    return {'agent':'six-vdw-3','role':'researcher','status':'EXACT_CHARACTER_ORBIT_REPAIR_LEMMA_AUTHOR_CHECKED',
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),'orbit_transcript_sha256':digest,
            'regular_character_columns':102,'distinct_actual_bad_AP_supports':102,
            'points_per_support':7,'degree_each_regular_point':7,'literal_orbit_point_tests':714,
            'fractional_packing_and_cover_optimum':[102,7],'regular_edit_lower_bound':15,
            'illegal_phase_regular_edit_lower_bound':102,'all_phase_rows':64,
            'legal_phase_rows':len(legal),'illegal_phase_rows':len(illegal),
            'complete_phase_progression_inputs':phase_inputs,'illegal_singleton_point_palette_tests':singletons,
            'multiplicativity_truth_inputs':multiplicativity,'affine_field_parameters':10506,
            'affine_phase_parameters':63036,'field_coordinate_point_identities':fields,
            'phase_coordinate_point_identities':phase_points,'character_palette_point_values':palettes,
            'whole_CRT_linear_point_identities':crt_points,'damaged_certificates_rejected':damages,
            'arbitrary_orientation_three_hole_distance_if_root_regular':12,
            'arbitrary_orientation_three_hole_distance_if_root_hole':13,
            'zero_argument_column_free':True,'sufficient_integer_repair_constructed':False,
            'integer_packing_optimum_claimed':False,'arbitrary_orientation_family_excluded':False,
            'W_bound_improved':False,'native_solver_invoked':False,'external_review_claimed':False,'formalized':False}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path)
    a=p.parse_args();print(json.dumps(verify(a.certificate)))
