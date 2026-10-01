"""Literal-field semantic audit. Does not import the model generator or solver."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import importlib.util
import itertools
import json
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'order7-geometric-cut'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slots():
    pins = json.loads((HERE/'SOURCE_PINS.json').read_text())
    require(sha(BASE/'sign_audit.py') == pins['files']['sign_audit.py'], 'changed literal coset source')
    spec = importlib.util.spec_from_file_location('committed_literal_cosets', BASE/'sign_audit.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    return helper.orientations()


def independent_cases():
    # Distribute four indistinguishable deficit units to six gap slots.
    # This differs from the generator's six nested bounded coordinates.
    rooted = set()
    for places in itertools.combinations_with_replacement(range(6), 4):
        rooted.add(tuple(places.count(i) for i in range(6)))
    canonical = sorted({min(t[j:]+t[:j] for j in range(6)) for t in rooted})
    require(len(rooted) == 126 and len(canonical) == 22, 'independent composition cover failed')
    profiles = []
    for t in canonical:
        p = [0]
        for value in t[:5]:
            p.append(p[-1]+8-value)
        require(p[-1]+8-t[5] == 44, 'independent cyclic sum failed')
        profiles.append(tuple(p))
    all_patterns = set()
    orbit_sizes = []
    for p in profiles:
        orbit = {tuple(sorted((i+s)%44 for i in p)) for s in range(44)}
        require(not orbit&all_patterns, 'two gap classes share a phase pattern')
        all_patterns |= orbit
        orbit_sizes.append(len(orbit))
    require(len(all_patterns) == 924 and Counter(orbit_sizes) == Counter({44:20, 22:2}),
            'independent rotation orbit coverage failed')
    for p in all_patterns:
        t = tuple(7-((p[(j+1)%6]-p[j])%44-1) for j in range(6))
        require(all(0 <= v <= 4 for v in t) and sum(t) == 4, 'invalid six-exception gap')
        canonical_t = min(t[j:]+t[:j] for j in range(6))
        shift_index = next(j for j in range(6) if t[j:]+t[:j] == canonical_t)
        rotated = tuple(sorted((i-p[shift_index])%44 for i in p))
        require(rotated == profiles[canonical.index(canonical_t)], 'gap normalization lost a profile')
    cases = [{'stem':f'arc-b{b}', 'kind':'arc', 'background':b,
              'width':36, 'variables':79} for b in (0, 1)]
    for b in (0, 1):
        for j,p in enumerate(profiles, 1):
            cases.append({'stem':f'boundary-b{b}-{j:02d}', 'kind':'boundary',
                          'background':b, 'variables':44, 'case':j,
                          'deficit':list(canonical[j-1]), 'exception_positions':list(p)})
    return cases, {'rooted_deficits':126, 'gap_orbits':22,
                   'phase_patterns_per_background':924, 'gap_orbit_sizes':orbit_sizes,
                   'gap_normalizations_checked':924,
                   'labeled_words_per_boundary':924*2**44}


def normalization_controls():
    checked = 0
    for half in range(2, 7):
        for word in itertools.product((0, 1), repeat=2*half):
            phase = [word[i]^word[i+half] for i in range(half)]
            for b in (0, 1):
                exceptional = [i for i in range(half) if phase[i] != b]
                if not exceptional:
                    continue
                for width in range(1, half):
                    covers = [s for s in range(half)
                              if all((i-s)%half < width for i in exceptional)]
                    if not covers:
                        continue
                    anchor = min(exceptional, key=lambda i:(i-covers[0])%half)
                    rotated = [word[(i+anchor)%(2*half)]^word[anchor]
                               for i in range(2*half)]
                    normalized = [rotated[i]^rotated[i+half] for i in range(half)]
                    require(rotated[0] == 0 and normalized[0] == 1-b, 'arc anchor failed')
                    require(all(normalized[i] == b for i in range(width, half)), 'arc cover failed')
                    decoded = list(rotated[:half])
                    for i in range(half):
                        decoded.append(rotated[i+half] if 0 < i < width else
                                       rotated[i]^(1-b if i == 0 else b))
                    require(decoded == rotated, 'orientation lost by the partial signed model')
                    checked += 1
    require(checked == 24224, 'incomplete small normalization controls')
    return checked


def read_cnf(path, variables):
    rows = path.read_text().splitlines()
    require(bool(rows), 'empty CNF')
    h = rows[0].split()
    require(len(h) == 4 and h[:3] == ['p', 'cnf', str(variables)], 'wrong DIMACS header')
    require(int(h[3]) >= 0 and len(rows) == int(h[3])+1, 'wrong DIMACS count')
    clauses = []
    for row in rows[1:]:
        values = list(map(int, row.split()))
        require(bool(values) and values[-1] == 0 and
                all(1 <= abs(v) <= variables for v in values[:-1]), 'invalid DIMACS literal')
        clauses.append(tuple(sorted(values[:-1])))
    return clauses


def signed_literal(rec, i, side):
    if not side:
        return i+1
    if rec['kind'] == 'boundary':
        opposed = (i in rec['exception_positions']) != bool(rec['background'])
        return -(i+1) if opposed else i+1
    if i == 0:
        return -1 if rec['background'] == 0 else 1
    if i < 36:
        return 44+i
    return -(i+1) if rec['background'] else i+1


def audit(work):
    began = time.monotonic()
    cases, coverage = independent_cases()
    actual_slots = slots()
    signatures = set()
    squares = {x*x%617 for x in range(1, 617)}
    retained = removed = 0
    for a in range(617):
        for d in range(1, 617):
            terms = [(a+j*d)%617 for j in range(7)]
            if 0 in terms:
                removed += 1
                continue
            retained += 1
            signatures.add(tuple(sorted({actual_slots[x] for x in terms})))
            for flip in (0, 1):
                require(len({int(x in squares)^flip for x in terms}) == 2, 'literal QR control failed')
    require((retained, removed, len(signatures)) == (375760, 4312, 26488), 'field AP census wrong')
    records = []
    for rec in cases:
        expected = set()
        for sig in signatures:
            signed = {signed_literal(rec,i,side) for i,side in sig}
            if any(-v in signed for v in signed):
                continue
            expected.add(tuple(sorted(signed)))
            expected.add(tuple(sorted(-v for v in signed)))
        cnf = work/(rec['stem']+'.cnf')
        actual = read_cnf(cnf, rec['variables'])
        require(Counter(actual) == Counter(list(expected)+[(-1,)]), 'complete semantic CNF mismatch: '+rec['stem'])
        records.append(dict(rec, clauses=len(actual), cnf_sha256=sha(cnf)))
    return {'status':'ALL_46_MODELS_EXACTLY_DEFINITION_AUDITED', 'records':records,
            'retained_APs':retained, 'zero_APs_removed':removed,
            'actual_signed_supports':len(signatures), 'QR_controls':2,
            'small_arc_normalizations':normalization_controls(), 'coverage':coverage,
            'seconds':time.monotonic()-began}


def check_candidate(rec, bits):
    require(len(bits) == rec['variables'] and all(v in (0, 1) for v in bits), 'invalid candidate domain')
    colors = {}
    for x,(i,side) in slots().items():
        literal = signed_literal(rec,i,side)
        colors[x] = bits[abs(literal)-1]^int(literal < 0)
    require(all(colors[x] == colors[x*pow(3,88,617)%617] for x in colors), 'candidate violates H invariance')
    retained = removed = 0
    for a in range(617):
        for d in range(1, 617):
            terms = [(a+j*d)%617 for j in range(7)]
            if 0 in terms:
                removed += 1
                continue
            require(len({colors[x] for x in terms}) == 2, f'candidate has a monochromatic AP {a},{d}')
            retained += 1
    squares = {x*x%617 for x in range(1,617)}
    require(not any(all(colors[x] == (int(x in squares)^flip) for x in colors)
                    for flip in (0,1)), 'candidate is ordinary QR')
    require((retained,removed) == (375760,4312), 'candidate AP check incomplete')
    return {'status':'INDEPENDENT_LITERAL_NONQR_H7_FIELD_WITNESS_VERIFIED',
            'retained_APs':retained, 'zero_APs_removed':removed,
            'colors':[colors[x] for x in range(1,617)], 'global_W_bound':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('work', type=Path)
    print(json.dumps(audit(parser.parse_args().work), sort_keys=True))
