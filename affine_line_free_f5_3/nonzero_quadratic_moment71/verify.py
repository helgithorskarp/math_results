#!/usr/bin/env python3
"""Regenerate every finite input to PROOF.md using only exact arithmetic."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import shlex
import subprocess
import tempfile

from model import (POINTS, determinant, dot, evaluation, information_set,
                   monomials, projective_points, require, structural_families)

HERE = Path(__file__).resolve().parent


def rejected(operation, message):
    try:
        operation()
    except RuntimeError:
        return
    raise RuntimeError(message)


def parse_census(output):
    lines = output.splitlines()
    require(bool(lines), 'empty census')
    footer = lines.pop().split()
    require(len(footer) == 3 and footer[0] == 'COMPLETE', 'missing completion')
    require(footer[1] == '14348907', 'incomplete enumeration')
    require(footer[2].isdigit() and int(footer[2]) == len(lines), 'retained count')
    require(all(len(w) == 31 and set(w) <= set('014') for w in lines), 'bad word')
    words = set(lines)
    require(len(words) == len(lines), 'duplicate word')
    return words


def reference_slice(chosen, inv, words):
    """Direct monomial evaluation, independent of the C++ meet-in-middle loop."""
    matrix = evaluation(4)
    direct = set()
    for first in (0, 1, 4):
        for tail in product((0, 1, 4), repeat=8):
            information = (first, 0, 0, 0, 0, 0, 0) + tail
            coefficients = tuple(dot(row, information) for row in inv)
            values = tuple(dot(row, coefficients) for row in matrix)
            if set(values) <= {0, 1, 4}:
                direct.add(''.join(map(str, values)))
    retained_slice = {w for w in words if all(w[chosen[i]] == '0' for i in range(1, 7))}
    require(direct == retained_slice, 'independent information slice disagrees')
    return {'tested': 3**9, 'retained': len(direct)}


def binary_audit(patterns):
    line = projective_points(2)
    image = {
        tuple(sum(c * pow(x, i, 5) * pow(y, 4-i, 5)
                  for i, c in enumerate(coefficients)) % 5 for x, y in line)
        for coefficients in product(range(5), repeat=5)
    }
    require(len(image) == 5**5 and all(sum(v) % 5 == 0 for v in image),
            'binary quartic image is the sum-zero hyperplane')
    require({v for v in image if set(v) <= {0, 1, 4}} == set(patterns),
            'binary pattern generation')
    return {'all_binary_forms': len(image), 'square_valued': len(patterns)}


def geometry_audit(words):
    conic = tuple(v for v in POINTS if dot(v, v) == 0)
    require(len(conic) == 6 and all(determinant(*triple) for triple in combinations(conic, 3)),
            'standard nonsingular six-point conic')
    h = {p: sum(dot(v, p) == 0 for v in conic) for p in POINTS}
    require(Counter(h.values()) == {0: 10, 1: 6, 2: 15}, 'conic incidence classes')
    tangents = [p for p in POINTS if h[p] == 1]
    require(all(sum(dot(v, p) == 0 for p in tangents) == 1 for v in conic),
            'one tangent radial line per conic plane')
    for x in product(range(5), repeat=3):
        incidence = sum(dot(v, x) == 0 for v in conic)
        for p in POINTS:
            on_line = x == (0, 0, 0) or any(
                x == tuple(t * z % 5 for z in p) for t in range(1, 5))
            if on_line:
                incidence += {0: 2, 1: 1, 2: 0}[h[p]]
        require(incidence == (32 if x == (0, 0, 0) else 2), 'conic counting identity')

    # Each five-subset has exactly one possible sixth point of an arc.
    for missing in conic:
        five = tuple(p for p in conic if p != missing)
        extensions = [p for p in POINTS if p not in five and
                      all(determinant(a, b, p) for a, b in combinations(five, 2))]
        require(extensions == [missing], 'five-arc conic completion')
    four = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1))
    require(all((x*y+x*z+3*y*z) % 5 == 0 for x, y, z in four), 'four-arc conic')
    # The polar matrix is twice the symmetric matrix, which is invertible in F_5.
    require(determinant((0, 1, 1), (1, 0, 3), (1, 3, 0)) != 0,
            'four-arc conic is nonsingular')

    collinear = 0
    for word in words:
        if word.count('0') == 21:
            fours = [POINTS[i] for i, v in enumerate(word) if v == '4']
            require(len(fours) == 5 and all(determinant(fours[0], fours[1], p) == 0
                                           for p in fours[2:]), '21-zero quartic four-locus')
            collinear += 1
    # Audit the projective field-sum identities on a spanning monomial family.
    for degree in (4, 8):
        matrix = evaluation(degree)
        require(all(sum(row[j] for row in matrix) % 5 == 0
                    for j in range(len(monomials(degree)))), 'projective power sum')
    return {'conic_normals': 6, 'radial_incidence_counts': [10, 6, 15],
            'pointwise_identity_checks': 125, 'five_arc_completions': 6,
            'quartics_with_collinear_four_locus': collinear}


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first, length-1):
                yield (first,) + rest


def profile_audit():
    table = Counter()
    for deficits in compositions(9, 5):
        sizes = tuple(16-v for v in deficits)
        if any(sum(sizes[t] * pow(t, k, 5) for t in range(5)) % 5 for k in (1, 2)):
            continue
        cubic = sum(sizes[t] * pow(t, 3, 5) for t in range(5)) % 5
        quartic = sum(sizes[t] * pow(t, 4, 5) for t in range(5)) % 5
        require(all(deficits[t] % 5 == (t**4+t*cubic+quartic) % 5 for t in range(5)),
                'indicator-polynomial moment formula')
        energy = sum(v*v for v in deficits)
        if cubic:
            require(quartic in (0, 1, 2, 3) and energy == 29-2*quartic
                    and deficits[0] == quartic, 'nonzero cubic profile')
        else:
            allowed = {0: {(5, 29), (0, 39)}, 1: {(1, 17)}, 4: {(9, 81), (4, 41)}}
            require(quartic in allowed and (deficits[0], energy) in allowed[quartic],
                    'zero cubic profile')
        table[(int(bool(cubic)), quartic, deficits[0], energy)] += 1
    require(sum(table.values()) == 27, 'complete centered zero-quadratic profile count')
    # Pure incidence identities: 155 planes, 31 through a point, 6 through a pair.
    count, first, second = 155, 31*71, 31*71+6*71*70
    energy = 256*count-32*first+second
    require(energy == 1269 and 31*16-6*71 == 70, 'global and central deficit sums')
    return {'centered_profiles': sum(table.values()),
            'table': [list(key)+[value] for key, value in sorted(table.items())],
            'global_deficit_square_sum': energy}


def statistics_audit(spectra):
    # T = 0: equations (E),(C), before using the conic inequality.
    zero_candidates = []
    for a, b, c in spectra:
        for f in range(min(6, c)+1):
            for g in range(a+1):
                for selected in (0, 1):
                    if (29*a+17*b+41*c+10*g+40*f == 1269 and
                            5*(a-g)+b+4*c+5*f == 70-25*selected):
                        zero_candidates.append([a, b, c, f, g, selected])
                        require(f+3*selected > 5 or (a == 21 and f > 2),
                                'unexcluded zero-cubic statistics')
    require(sorted(zero_candidates) == [[21, 5, 5, 4, 21, 1], [21, 5, 5, 5, 17, 0]],
            'zero-cubic reduction')

    # T != 0: enumerate small integer aggregates, not point configurations.
    nonzero_candidates, residue_survivors = [], []
    for d in range(15, 32):
        for a in range(32-d):
            for b in range(32-d-a):
                c = 31-d-a-b
                for f in range(min(5, c)+1):
                    for selected in (0, 1):
                        if f+3*selected > 5:
                            continue
                        for g in range(a+1):
                            twice_j = 29*a+17*b+41*c+29*d+10*g+40*f-1269
                            if twice_j % 2:
                                continue
                            j = twice_j//2
                            if not 0 <= j <= 3*d:
                                continue
                            if 5*(a-g)+b+4*c+j+5*f != 70-25*selected:
                                continue
                            candidate = [a, b, c, d, f, g, selected, j]
                            nonzero_candidates.append(candidate)
                            for n1 in range(d+1):
                                for n2 in range(d-n1+1):
                                    for n3 in range(d-n1-n2+1):
                                        if n1+2*n2+3*n3 != j or (b+16*c+n1+4*n2+9*n3) % 5:
                                            continue
                                        require(n2 == n3 == 0, 'remaining values must be squares')
                                        spectrum = (a+d-n1, b+n1, c)
                                        require(spectrum not in spectra, 'unexcluded nonzero-cubic spectrum')
                                        residue_survivors.append(list(spectrum))
    require(sorted(nonzero_candidates) == [
        [4, 0, 11, 16, 5, 4, 0, 1],
        [6, 0, 10, 15, 5, 5, 0, 0],
        [6, 0, 10, 15, 5, 6, 0, 5]], 'nonzero-cubic reduction')
    require(sorted(residue_survivors) == [[16, 5, 10], [21, 0, 10]], 'excluded quartic spectra')
    return {'zero_cubic_aggregate_candidates': sorted(zero_candidates),
            'nonzero_cubic_aggregate_candidates': sorted(nonzero_candidates),
            'absent_quartic_spectra': sorted(residue_survivors), 'unexcluded_cases': 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cxx', default='g++')
    parser.add_argument('--cxxflags', default='-O2')
    parser.add_argument('--expected', type=Path, default=HERE/'EXPECTED.json')
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    chosen, inv, generator = information_set()
    input_text = '\n'.join(' '.join(map(str, row)) for row in generator) + '\n'
    with tempfile.TemporaryDirectory(prefix='moment71-') as temp:
        binaries = {}
        for name in ('quartics', 'planar_cap'):
            target = str(Path(temp)/name)
            subprocess.run([args.cxx, '-std=c++20', *shlex.split(args.cxxflags),
                            str(HERE/(name+'.cpp')), '-o', target], check=True)
            binaries[name] = target
        planar = subprocess.run([binaries['planar_cap']], text=True, capture_output=True, check=True)
        require(planar.stdout.strip() == 'PLANAR_CAP16 1081575 0', 'planar census counters')
        census = subprocess.run([binaries['quartics']], input=input_text, text=True,
                                capture_output=True, check=True)
        words = parse_census(census.stdout)
        for malformed in ('', input_text+'0\n', input_text.replace('0', '8', 1)):
            control = subprocess.run([binaries['quartics']], input=malformed, text=True,
                                     capture_output=True)
            require(control.returncode in (2, 3, 4), 'malformed matrix accepted or crashed')
    squares, cones, binary_patterns = structural_families()
    require(words == squares | cones, 'complete census differs from explicit polynomial families')
    rejected(lambda: require(words - {'0'*31} == squares | cones, 'deleted zero form'),
             'deleted-form control was accepted')
    rejected(lambda: parse_census(census.stdout.rsplit('COMPLETE', 1)[0]),
             'missing completion control was accepted')
    rejected(lambda: parse_census(census.stdout.replace('14348907', '14348906')),
             'incomplete count control was accepted')
    spectra = Counter((w.count('0'), w.count('1'), w.count('4')) for w in words)
    result = {
        'planar_17_subsets': 1081575, 'planar_line_free_17_subsets': 0,
        'information_rows': list(chosen), 'information_words_tested': 3**15,
        'quartics': len(words), 'quadratic_squares': len(squares), 'binary_cones': len(cones),
        'family_intersection': len(squares & cones),
        'catalogue_sha256': sha256(('\n'.join(sorted(words))+'\n').encode()).hexdigest(),
        'value_spectra': [list(key)+[value] for key, value in sorted(spectra.items())],
        'reference_slice': reference_slice(chosen, inv, words),
        'binary_audit': binary_audit(binary_patterns),
        'geometry_audit': geometry_audit(words), 'profile_audit': profile_audit(),
        'statistics_audit': statistics_audit(spectra), 'negative_controls': 6,
    }
    if args.write_expected:
        args.expected.write_text(json.dumps(result, indent=2)+'\n')
    else:
        require(result == json.loads(args.expected.read_text()), 'expected summary mismatch')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
