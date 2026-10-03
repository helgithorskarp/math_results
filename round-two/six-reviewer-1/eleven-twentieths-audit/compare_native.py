"""OPTIONAL data-only whole comparison; executes only the sealed reviewer code."""
import hashlib
import json
from pathlib import Path
import sys
from arithmetic import F, require
from check import run


def compare(data):
    own = run()
    require(data['late_native_corroboration_NOT_primary'] is True, 'late trust marker')
    whole = data['whole']; vectors = data['all393_complete_native_vectors']
    require(own['mass_floor']['coefficients'] == whole['mass_coefficients'] and
            own['mass_floor']['integral'] == whole['mass_integral'], 'entire mass polynomial/integral')
    from check import newton_constants
    require([str(c) for c in newton_constants()] == whole['newton_constants'],
            'all Newton constants, independent partition computation')
    require(len(whole['polar_cells']) == len(own['polar']) == 57 and
            len(whole['origin_leaves']) == len(own['origin']) == 48 and len(vectors) == 393,
            'entire finite/vector census')
    require(whole['cover'] == json.loads(Path(__file__).with_name('PLAN.json').read_text()),
            'entire defining closed cover')
    cursor = 0
    def vector(expected, reported_hash):
        nonlocal cursor
        actual = vectors[cursor]; cursor += 1
        require(actual == expected, 'entire native/reviewer vector '+str(cursor))
        canonical = json.dumps(actual, sort_keys=True, separators=(',', ':')).encode()
        require(hashlib.sha256(canonical).hexdigest() == reported_hash, 'native vector fingerprint consistency')
    for primary, native in zip(own['polar'], whole['polar_cells']):
        require({k: primary[k] for k in ['k', 'L', 'U', 'P', 'd', 'integral']} ==
                {k: native[k] for k in ['k', 'L', 'U', 'P', 'd', 'integral']},
                'every full polar cell input/ceiling/integral')
        vector(primary['coefficients'], native['all21_coefficients_sha256'])
    for primary, native in zip(own['origin'], whole['origin_leaves']):
        mapping = {'path': 'path', 'box': 'box', 's': 'smax', 'S': 'Smax', 'ds': 'dmean',
                   'db': 'dbeta', 'dS': 'dS', 'beta': 'beta', 'Q': 'odd_root',
                   'D': 'D', 'R': 'R', 'bound': 'score'}
        require(all(primary[a] == native[b] for a, b in mapping.items()),
                'entire origin leaf inputs/envelopes/diagonal/remainder')
        require(len(native['terms']) == 7, 'native all centered terms')
        for term, other in zip(primary['terms'], native['terms']):
            require(term['l'] == other['l'] and term['term'] == other['integral'],
                    'every weighted entire origin integral')
            weighted = [str(F(x)*F(term['weight'])) for x in term['coefficients']]
            vector(weighted, other['coefficients_sha256'])
    require(cursor == len(vectors), 'no native vector omitted')
    return dict(agent='six-reviewer-1', role='independent mathematical reviewer',
                late_native_corroboration_NOT_primary=True, native_code_imported=False,
                full_native_input=data, full_independent_output=own,
                all393_entire_vectors_equal=True, all57_polar48_origin_fields_equal=True,
                full_closed_topology_equal=True, every_rational_integral_equal=True)


if __name__ == '__main__':
    print(json.dumps(compare(json.loads(Path(sys.argv[1]).read_text())),
                     sort_keys=True, separators=(',', ':')))
