#!/usr/bin/env python3
"""Self-contained exact finite certificate for the fourth degree-nine boundary coefficient.

Uniform analytic estimates and arbitrary-competitor completeness are ordinary
proof in PROOF.md. Local components use standard-library rational arithmetic;
no external source, numerical roots, solver or private data is loaded.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import runpy

BASE = Path(__file__).resolve().parent


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def component(name, **inputs):
    return runpy.run_path(str(BASE/name), init_globals={'QUIET': True, **inputs})


def build_record():
    candidate = component('candidate.py')
    generic = component('generic_eta4.py')
    spec = importlib.util.spec_from_file_location('fourth_higher_trace', BASE/'higher_trace.py')
    trace = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(trace)
    higher, directions = trace.build(candidate)
    # The family is given a freshly computed record, never expected.json.
    family = component('attaining_family.py', CANDIDATE_RECORD=candidate['record'])
    spec = importlib.util.spec_from_file_location('fourth_stability_family', BASE/'stability_family.py')
    split = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(split)
    stability, split_context = split.build(family)
    K, P = candidate['K'], candidate['P']
    lo, hi = map(F, candidate['record']['embedding_interval'])
    checks = 0

    def equal(a, b, label):
        nonlocal checks
        require(a == b, label)
        checks += 1

    equal(8*lo**3-6*lo-1 < 0 < 8*hi**3-6*hi-1 and 24*lo**2-6 > 0,
          True, 'isolating interval chooses cos(pi/9)')
    C4 = candidate['C4']
    displayed = K((F(340367352475,839808), F(808137564635,419904),
                   F(-1052841914857,419904)))
    equal(C4, displayed, 'displayed exact fourth boundary coefficient')
    bound = C4.interval(lo, hi)
    equal(F('-233.920855886') < bound[0] <= bound[1] < F('-233.920855885'),
          True, 'displayed rational fourth enclosure')
    for name in ['H', 'w3', 'w4']:
        equal(candidate[name].interval(lo,hi)[0] > 0, True, name+' strictly positive')
    equal(candidate['C3'].interval(lo,hi)[1] < 0, True, 'credited cubic coefficient negative')
    equal(C4.interval(lo,hi)[1] < 0, True, 'fourth coefficient negative')
    equal(family['record']['common_eta5_inward_repair'], 1000,
          'finite fifth inward correction')
    equal(candidate['C4'].record(), family['record']['objective_coefficients'][4][1],
          'finite dual optimum versus full-family fourth objective')
    rejected = []

    def reject(fn, label):
        nonlocal checks
        try:
            fn()
        except RuntimeError:
            checks += 1
            rejected.append(label)
            return
        raise RuntimeError('mathematical mutation not rejected: '+label)

    reject(lambda: require(candidate['cost'] + P.var(0)*P.var(6) == candidate['model'],
                           'injected mixed term'), 'nonzero imaginary-real cost coupling')
    reject(lambda: require(C4+1 == candidate['const']-F(3,4)*candidate['lin']**2,
                           'damaged exact fourth coefficient'), 'incorrect fourth-field coefficient')
    # Damage a genuine generic polynomial identity, using the separately
    # constructed partition route as the reference.
    gm = generic['m']
    reject(lambda: require(gm.padd(generic['p'], gm.ppow(generic['eps'],8))
                           == generic['partition_pol'], 'damaged fourth Newton jet'),
           'generic fourth primitive coefficient')
    reject(lambda: require(generic['a4'] == gm.padd(generic['a4'],
                          gm.pscale(gm.ppow(generic['hh'],8), F(1,128))),
                          'damaged one-point binomial coefficient'), 'eighth imaginary scalar moment')
    grad = directions['gradient_u'].copy()
    grad[0] += K(1)
    real = directions['real']
    reject(lambda: require(sum((b*a for a,b in zip(grad,real)),P()) == 0,
                           'damaged higher real gradient'), 'higher real tangent cancellation')
    grad_h = directions['gradient_h'].copy()
    grad_h[2] += K(1)
    tau = directions['tau']
    reject(lambda: require(sum((b*a for a,b in zip(grad_h,tau)),P()) == 0,
                           'damaged higher imaginary gradient'), 'higher imaginary tangent cancellation')
    fK, fZ = family['K'], family['Z']
    root = family['r'].copy()
    root[4] += fZ(1,q=family['omega'].q)
    reject(lambda: require(family['evaluate'](root) == [fZ(0,q=family['omega'].q)]*6,
                           'damaged fourth root coefficient'), 'complete original-root residual')
    radial = fK(family['record']['all_nine_root_branches'][3]['radial'][4])
    reject(lambda: require(radial.interval(lo,hi)[0] > 0,
                           'reversed fifth inward sign'), 'active fifth inward sign')
    reject(lambda: require(split_context['delta_pol'] ==
                           split_context['p'].kscale(split_context['target'], -1),
                           'reversed split-real fifth response'), 'split-real critical displacement sign')
    total = checks + candidate['record']['checks'] + generic['record']['checks']
    total += higher['checks'] + family['record']['checks']
    total += stability['checks']
    return {'agent':'six-sendov-3', 'role':'researcher',
            'status':'exact finite certificate; full ordinary analytic proof in PROOF.md',
            'exact_checks':total, 'mutations_rejected':rejected,
            'cost':candidate['record'], 'generic_fourth':generic['record'],
            'higher_trace':higher, 'attainment':family['record'],
            'sharp_next_profile_family':stability}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture',type=Path,default=BASE/'expected.json')
    parser.add_argument('--emit-fixture',action='store_true')
    args = parser.parse_args()
    fixture = None
    if not args.emit_fixture:
        require(args.fixture.is_file(), 'required fixture missing')
        try:
            fixture = json.loads(args.fixture.read_text())
        except (ValueError,OSError) as e:
            raise RuntimeError('required fixture malformed') from e
        require(isinstance(fixture,dict), 'required fixture must be an object')
    record = build_record()
    encoded = json.dumps(record,sort_keys=True,indent=2)+'\n'
    if args.emit_fixture:
        print(encoded,end='')
        return
    require(fixture == record, 'complete fixture differs')
    print('PASS: '+str(record['exact_checks'])+' exact checks; '
          +str(len(record['mutations_rejected']))+' mutations rejected; all nine root branches.')
    print('Complete record SHA256: '+sha256(encoded.encode()).hexdigest())


if __name__ == '__main__':
    main()
