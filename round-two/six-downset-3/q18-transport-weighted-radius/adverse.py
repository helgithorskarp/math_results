"""Designated semantic damage to NEW original transports and subset checks.

These are certificate rejection controls, not a source/cold delivery suite
or mathematical review. No original closed producer or factor is run.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import importlib.util
import json


def load(name):
    p = Path(__file__).with_name(name+'.py')
    spec = importlib.util.spec_from_file_location('adverse_'+name, p)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


TRANSPORT_GATES = {
    'domain': 'designated exact endpoint/floor domain',
    'types': 'whole exactly23 original transport recipe types',
    'targets': 'whole58 original subset-primal targets',
    'radius': 'ALL3906 original entry displacement bounds',
    'floor': 'ALL3906 original entry floor bounds',
    'row': 'ALL58 original transported row equations',
    'multiplicity': 'whole original3906 recipe position multiplicities',
    'column': 'ALL81 original individual transported column equations',
    'energy': 'whole original58 transported energy',
}
SUBSET_GATES = {
    'abc-fixed': 'NEW all9 fixed abc triple positions',
    'negative-fixed': 'NEW all351 fixed complement/triple positions',
    'J-column': 'NEW ALL9 individual J column sum39 identities',
    'J-support': 'NEW all1224 J pure positions and72 abc pure positions',
}


def run(suite, case, scratch):
    if suite == 'transport':
        mod = load('check_transport')
        record = json.loads(Path(__file__).with_name('TRANSPORT.json').read_bytes())
        ep = record['endpoint_certificates'][0]; e = F(ep['e']); recipe = ep['recipe_all23_types']
        eps = F(1, 100000)
        if case == 'domain': ep['tau'] = '1/255'
        elif case == 'types': recipe.pop()
        elif case == 'targets': ep['q'][0] = str(F(ep['q'][0])+eps)
        elif case == 'radius': recipe[0]['C_change'] = str(-220*e-eps)
        elif case == 'row': recipe[0]['C_change'] = str(F(recipe[0]['C_change'])+eps)
        elif case == 'multiplicity': recipe[0]['original_allowed_positions'] += 1
        elif case == 'energy': ep['exact_energy'] = str(F(ep['exact_energy'])+1)
        elif case == 'column':
            for cell in recipe:
                if cell['star_type'] == [3, 0, 0]:
                    adjustment = -eps if cell['bad_type'] == [0, 0, 2] else eps
                    cell['C_change'] = str(F(cell['C_change'])+adjustment)
        elif case == 'floor':
            S, B, label, A, _, _, _, D = mod.decode()
            candidates = []
            for cell in recipe:
                for i, s in enumerate(S):
                    for j, bad in enumerate(B):
                        if not s & bad and list(label[s]) == cell['star_type'] and list(label[bad]) == cell['bad_type']:
                            lower = F(1, 256)-1-F(A[i][j], D)
                            if -220*e < lower <= 220*e:
                                candidates.append((cell, lower)); break
                    if candidates: break
                if candidates: break
            if not candidates: raise ValueError('no chosen within-radius floor damage exists')
            cell, lower = candidates[0]
            cell['C_change'] = str((lower-220*e)/2)
        path = scratch/('damaged-transport-'+case+'.json')
        path.write_text(json.dumps(record,indent=2)+'\n')
        action = lambda: mod.check(path); expected = TRANSPORT_GATES[case]
    else:
        mod = load('subset_radius'); decoder = mod.decoder

        def damaged_decoder():
            S, B, label, A, values, P, N, D = decoder()
            abc = S.index(7); bc = next(j for j, bad in enumerate(B) if label[bad] == (6,0,1))
            if case == 'abc-fixed': A[abc][bc] += 1
            elif case == 'negative-fixed': A[N[0]][bc] += 1
            elif case == 'J-column': A[next(i for i in P if i != abc)][bc] += 1
            elif case == 'J-support': S[next(i for i in P if i != abc)] |= 8
            return S, B, label, A, values, P, N, D

        mod.decoder = damaged_decoder
        action = mod.check; expected = SUBSET_GATES[case]
    try:
        action()
    except ValueError as error:
        if str(error) != expected:
            raise ValueError('damage failed at wrong gate: '+str(error)) from error
        return {'suite': suite, 'case': case, 'designated_gate': expected,
                'rejected_exactly_at_designated_gate': True,
                'independent_review_or_source_delivery_claimed': False}
    raise ValueError('damaged certificate unexpectedly accepted')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--suite', choices=['transport','subset'], required=True)
    parser.add_argument('--case', required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args(); args.scratch.mkdir(parents=True,exist_ok=True)
    print(json.dumps(run(args.suite,args.case,args.scratch),indent=2))
