#!/usr/bin/env python3
"""Regenerate the complete quartic cover and check every integer contradiction."""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random
import shlex
import subprocess
import tempfile

from field import (POINTS, dot, evaluation, information_set, monomials,
                   projective_points, require)
import quadratic
from model import (AFFINE, ALLOWED, FORMS, check_certificate,
                   feasible_memberships, geometry, partition,
                   profile_deficits, quadratic_values, signature)

HERE = Path(__file__).resolve().parent


def rejected(function, message):
    try:
        function()
    except RuntimeError:
        return
    raise RuntimeError(message)


def digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def build(directory, cxx='g++', flags='-O2'):
    result = {}
    for name in ('quartics','planar_cap'):
        target = str(Path(directory)/name)
        subprocess.run([cxx,'-std=c++20','-Wall','-Wextra','-Wpedantic',
                        *shlex.split(flags),str(HERE/(name+'.cpp')),'-o',target],check=True)
        result[name] = target
    return result


def parse_census(output, qvalues):
    lines = output.splitlines()
    require(bool(lines), 'empty census')
    footer = lines.pop().split()
    require(len(footer) == 3 and footer[0] == 'COMPLETE', 'completion marker')
    require(footer[1] == '14348907' and footer[2].isdigit() and int(footer[2]) == len(lines),
            'complete census counters')
    require(all(len(w) == 31 and set(w) <= set('01234') and
                all(int(u) in ALLOWED[q] for u,q in zip(w,qvalues)) for w in lines),
            'allowed quartic evaluation words')
    words = set(lines)
    require(len(words) == len(lines), 'duplicate retained word')
    return words


def reference_slice(qvalues, chosen, inverse, words):
    """Direct monomial evaluation of a 3^8 information-word slice."""
    matrix = evaluation(4)
    bases = [ALLOWED[qvalues[i]] for i in chosen]
    prefix = tuple(base[0] for base in bases[:7])
    retained = set()
    for tail in product(*bases[7:]):
        coefficients = tuple(dot(row,prefix+tail) for row in inverse)
        values = tuple(dot(row,coefficients) for row in matrix)
        if all(u in ALLOWED[q] for u,q in zip(values,qvalues)):
            retained.add(''.join(map(str,values)))
    actual = {w for w in words if all(int(w[chosen[i]]) == prefix[i] for i in range(7))}
    require(retained == actual, 'direct monomial reference slice')
    return len(retained)


def collect_cases(binary):
    chosen, inverse, generator = information_set()
    all_cases, summaries, zero_words = [], {}, None
    for name,diagonal in FORMS.items():
        qvalues = quadratic_values(diagonal)
        source = [' '.join(map(str,row)) for row in generator]
        source.extend(' '.join(str(int(u in ALLOWED[q])) for u in range(5)) for q in qvalues)
        source.extend(' '.join(map(str,ALLOWED[qvalues[i]])) for i in chosen)
        text = '\n'.join(source)+'\n'
        run = subprocess.run([binary],input=text,text=True,capture_output=True,check=True)
        words = parse_census(run.stdout,qvalues)
        if name == 'zero':
            zero_words = words
        if name == 'rank1_nonsquare':
            translated = {''.join(str((int(u)+2*q*q) % 5) for u,q in zip(w,qvalues))
                          for w in words}
            require(translated == zero_words, 'quadratic-translation catalogue identity')
        multiplicities = Counter(signature(qvalues,w) for w in words)
        memberships = {key:feasible_memberships(key) for key in multiplicities}
        candidates = {w for w in words if memberships[signature(qvalues,w)]}
        orbits = partition(diagonal,candidates,memberships,chosen,inverse)
        for i,orbit in enumerate(orbits):
            for epsilon in orbit['epsilon']:
                all_cases.append({'form':name,'orbit':i,'epsilon':epsilon,
                                  'representative':orbit['representative'],'orbit_size':orbit['size']})
        summaries[name] = {
            'quartic_information_words':3**15, 'retained_quartics':len(words),
            'quartic_catalogue_sha256':sha256(('\n'.join(sorted(words))+'\n').encode()).hexdigest(),
            'histogram_types':len(multiplicities), 'aggregate_candidates':len(candidates),
            'subgroup_orbits':len(orbits), 'orbits':orbits,
            'direct_reference_words':3**8,
            'direct_reference_retained':reference_slice(qvalues,chosen,inverse,words),
        }
        # Native input and completion controls run once; all seven domains
        # are fully enumerated and directly sampled above.
        if name == 'zero':
            for bad in ('',text+'0\n',text.replace('0','8',1)):
                control = subprocess.run([binary],input=bad,text=True,capture_output=True)
                require(control.returncode in range(2,9), 'invalid native input accepted or crashed')
            rejected(lambda:parse_census(run.stdout.rsplit('COMPLETE',1)[0],qvalues),
                     'incomplete census accepted')
            rejected(lambda:parse_census(run.stdout.replace('14348907','14348906'),qvalues),
                     'incomplete counter accepted')
    return summaries, all_cases


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first,length-1):
                yield (first,)+tail


def audit_profiles():
    direct = set()
    tested = 0
    for deficits in compositions(9,5):
        tested += 1
        sizes = tuple(16-d for d in deficits)
        moments = tuple(sum(sizes[t]*t**k for t in range(5)) % 5 for k in (1,2,3,4))
        if moments[0] == moments[2] == 0:
            direct.add((moments[1],moments[3],deficits))
    formula = {(q,u,d) for q in range(5) for u in ALLOWED[q] for d in profile_deficits(q,u)}
    require(direct == formula and tested == 715 and len(direct) == 39,
            'independent complete profile generation')
    for q in range(5):
        allowed = tuple(u for u in range(5)
                        if sum((t**4+q*t*t+u) % 5 for t in range(5)) in (4,9))
        require(allowed == ALLOWED[q], 'complete local quartic value triples')
    for a,b in ((1,4),(2,3)):
        for u in ALLOWED[a]:
            require({(sum(x*x for x in d),d[0]) for d in profile_deficits(a,u)} ==
                    {(sum(x*x for x in d),d[0]) for d in profile_deficits(b,u)},
                    'profile statistics invariant under normal rescaling')
    return {'compositions':tested, 'zero_cubic_profiles':len(direct)}


def audit_incidence(incidence):
    stars,lines,pencils = incidence
    plane_points = tuple(tuple(p for p in AFFINE if dot(v,p) == t)
                         for v in POINTS for t in range(5))
    require(len(stars) == 125 and all(len(s) == 31 for s in stars), 'point stars')
    require(all(len(p) == 25 for p in plane_points), 'plane sizes')
    require(Counter(h for star in stars for h in star) == Counter({i:25 for i in range(155)}),
            'point-plane incidences')
    rng = random.Random(2026092604)
    samples = [set(AFFINE[:71]), set(rng.sample(AFFINE,71)), set(rng.sample(AFFINE,71))]
    for selected in samples:
        sizes = [sum(p in selected for p in plane) for plane in plane_points]
        deficits = [16-m for m in sizes]
        require(sum(sizes) == 2201 and sum(m*m for m in sizes) == 32021 and
                sum(d*d for d in deficits) == 1269, 'independent incidence energy control')
        for point,star in zip(AFFINE,stars):
            require(sum(deficits[h] for h in star) == 70-25*int(point in selected),
                    'point-star inversion control')
        for line,pencil in zip(lines,pencils):
            require(sum(deficits[h] for h in pencil) == 25-5*sum(p in selected for p in line),
                    'line-pencil inversion control')
        # These arbitrary 71-sets are not asserted to be line-free. They test
        # the general centered indicator-polynomial identity independently.
        mu = tuple(sum(p[i] for p in selected) % 5 for i in range(3))
        centered = {tuple((p[i]-mu[i]) % 5 for i in range(3)) for p in selected}
        for v in POINTS:
            projections = [dot(v,p) for p in centered]
            q,t,u = (sum(x**k for x in projections) % 5 for k in (2,3,4))
            for b in range(5):
                require((16-projections.count(b)) % 5 == (b**4+q*b*b+t*b+u) % 5,
                        'centered indicator-polynomial identity')
    # A definition-level positive line-free control of size 64.
    grid = set(product(range(4),repeat=3))
    require(all(sum(p in grid for p in line) <= 4 for line in lines), 'hypercube line-free control')
    require(all(sum(p in grid for p in plane) <= 16 for plane in plane_points), 'hypercube plane control')
    return {'points':125,'lines':len(lines),'planes':155,'arbitrary_71_set_controls':len(samples),
            'line_free_control_size':len(grid)}


def validate_cover(certificates, cases):
    fields = ('form','orbit','epsilon','representative','orbit_size')
    actual = [tuple(row[k] for k in fields) for row in certificates]
    expected = [tuple(row[k] for k in fields) for row in cases]
    require(actual == expected and len(set(actual)) == len(actual), 'complete certificate-case cover')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cxx',default='g++')
    parser.add_argument('--cxxflags',default='-O2')
    parser.add_argument('--certificates',type=Path,default=HERE/'certificates.json')
    parser.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--write-expected',action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='cubic71-') as temp:
        binaries = build(temp,args.cxx,args.cxxflags)
        planar = subprocess.run([binaries['planar_cap']],text=True,capture_output=True,check=True)
        require(planar.stdout.strip() == 'PLANAR_CAP16 1081575 0', 'complete planar cap census')
        summaries,cases = collect_cases(binaries['quartics'])
    incidence = geometry()
    data = json.loads(args.certificates.read_text())
    require(data['format'] == 'nonzero-cubic-farkas-v1', 'certificate format')
    certificates = data['cases']
    validate_cover(certificates,cases)
    checked = [check_certificate(row,FORMS[row['form']],incidence) for row in certificates]
    rejected(lambda:validate_cover(certificates[:-1],cases), 'missing-case control accepted')
    damaged = deepcopy(certificates[0])
    damaged['inequality_multipliers'][0][1] = -1
    rejected(lambda:check_certificate(damaged,FORMS[damaged['form']],incidence),
             'negative inequality-multiplier control accepted')
    damaged = deepcopy(certificates[0])
    damaged['contradiction'] += 1
    rejected(lambda:check_certificate(damaged,FORMS[damaged['form']],incidence),
             'incorrect contradiction control accepted')
    result = {
        'status':'NONZERO_CUBIC_MOMENT71_VERIFIED',
        'planar_17_subsets':1081575, 'line_free_planar_17_subsets':0,
        'quadratic_congruence_audit':quadratic.audit(),
        'profiles':audit_profiles(), 'incidence':audit_incidence(incidence),
        'forms':summaries, 'complete_information_words':sum(r['quartic_information_words'] for r in summaries.values()),
        'retained_quartics':sum(r['retained_quartics'] for r in summaries.values()),
        'rank1_nonsquare_translation_catalogue_equal':True,
        'aggregate_candidates':sum(r['aggregate_candidates'] for r in summaries.values()),
        'subgroup_orbits':sum(r['subgroup_orbits'] for r in summaries.values()),
        'certificate_cases':len(cases),'case_cover_sha256':digest(cases),
        'certificates_sha256':sha256(args.certificates.read_bytes()).hexdigest(),
        'certificate_column_checks':sum(r['variables'] for r in checked),
        'nonzero_multipliers':sum(r['nonzero_multipliers'] for r in checked),
        'smallest_strict_contradiction':min(-r['rhs'] for r in checked),
        'largest_multiplier':max(abs(v) for r in certificates for key in
                                  ('inequality_multipliers','equality_multipliers') for i,v in r[key]),
        'negative_controls':8, 'unexcluded_cases':0,
    }
    if args.write_expected:
        args.expected.write_text(json.dumps(result,indent=2)+'\n')
    else:
        require(result == json.loads(args.expected.read_text()), 'expected result mismatch')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
