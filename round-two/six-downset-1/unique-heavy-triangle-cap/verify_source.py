"""Verify source provenance and recorded evidence, without replaying mathematics.

six-downset-1 / researcher. Standard library only; explicit checks survive -O.
The publication commit supplies the external anchor for SHA256SUMS.
"""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
PRIVATE_MANIFEST_SHA = '06329d122d2890d3d9ad98998cdb3b016847275d9da518ca6bf5ace659547057'
EXPECTED_SHA = '23c5aac7367f4148fba504a14ed7bc51be1aba71f346f2b7540e1d284caaf005'
VERBATIM = ('geometry.py', 'reader.py', 'adverse.py', 'reproduce.py',
            'EXPECTED.json', 'VALIDATION.json')
EDITORIAL = ('PROOF.md', 'SCALAR-BOUNDS.md', 'README.md')
PUBLIC_FILES = set(VERBATIM + EDITORIAL + (
    'PROVENANCE.json', 'DEPENDENCIES.json', 'verify_source.py', '.gitignore',
    'SHA256SUMS'))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def binding(raw):
    return dict(bytes=len(raw), sha256=sha256(raw).hexdigest())


def main():
    require({p.name for p in HERE.iterdir() if p.is_file()} == PUBLIC_FILES,
            'exact publication file census')
    manifest = {}
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ')
        require(name in PUBLIC_FILES - {'SHA256SUMS'} and name not in manifest,
                'unique declared public manifest names')
        require(len(digest) == 64 and all(c in '0123456789abcdef' for c in digest),
                'canonical public SHA256')
        manifest[name] = digest
        require(sha256((HERE / name).read_bytes()).hexdigest() == digest,
                'whole current public bytes: ' + name)
    require(set(manifest) == PUBLIC_FILES - {'SHA256SUMS'},
            'complete publication manifest')

    provenance = json.loads((HERE / 'PROVENANCE.json').read_text())
    raw_seal = provenance['sealed_private_manifest_utf8'].encode('utf-8')
    require(sha256(raw_seal).hexdigest() == PRIVATE_MANIFEST_SHA,
            'whole original private seal')
    require(provenance['sealed_private_manifest_sha256'] == PRIVATE_MANIFEST_SHA,
            'private seal attribution')
    sealed = json.loads(raw_seal)
    original = sealed['complete_files']
    require(set(original) == set(VERBATIM + EDITORIAL)
            and sealed['complete_files_bytes'] == 97277
            and sum(row['bytes'] for row in original.values()) == 97277,
            'complete nine-file original seal')
    require(provenance['verbatim_files'] == list(VERBATIM)
            and set(provenance['editorial_replacements']) == set(EDITORIAL),
            'complete source transformation classes')
    for name in VERBATIM:
        require(binding((HERE / name).read_bytes()) == original[name],
                'byte-identical paid source/evidence: ' + name)
    for name in EDITORIAL:
        text = (HERE / name).read_text()
        for change in reversed(provenance['editorial_replacements'][name]):
            require(set(change) == {'old', 'new'} and change['old'] and change['new'],
                    'explicit reversible editorial substitution')
            require(text.count(change['new']) == 1,
                    'unique inverse editorial substitution: ' + name)
            text = text.replace(change['new'], change['old'], 1)
        require(binding(text.encode('utf-8')) == original[name],
                'whole reconstructed sealed mathematical document: ' + name)

    recorded = json.loads((HERE / 'VALIDATION.json').read_text())
    require(set(recorded['source_manifest']) == set(VERBATIM[:4] + EDITORIAL),
            'complete historical seven-file math source binding')
    for name, row in recorded['source_manifest'].items():
        require(row == original[name], 'historical source binding: ' + name)
    expected_raw = (HERE / 'EXPECTED.json').read_bytes()
    require(binding(expected_raw) == dict(bytes=25928, sha256=EXPECTED_SHA)
            and recorded['whole_mathematics_bytes'] == len(expected_raw)
            and recorded['whole_mathematics_sha256'] == EXPECTED_SHA,
            'whole recorded mathematical evidence, not a selected digest')
    expected = json.loads(expected_raw)
    controls = [('asymmetric', [4, 3, 2]), ('minimum-light', [5, 2, 2]),
                ('four-baseline', [3, 2, 2, 2])]
    require(set(expected) == {name for name, _ in controls} | {'adverse'},
            'complete historical mathematical control census')
    cases = []
    for name, counts in controls:
        math = expected[name]['whole_math']
        require(math['n'] == 4 and math['counts'] == counts and math['N'] == 70,
                'original bounded control: ' + name)
        require(math['physical_dimension'] == 67
                and math['seed_lower_rank'] == 68 and math['seed_upper_rank'] == 69
                and math['all_original_actual_lift_positions'] == 4900,
                'recorded original ranks and full lifted coverage: ' + name)
        require(math['formalized'] is False and math['independent_review'] is False,
                'recorded proof trust boundary: ' + name)
        cases.append(dict(n=4, counts=counts, N=70))
    require(recorded['cases'] == cases
            and recorded['actual_math_children'] == 21
            and recorded['all_children_exit_zero'] is True
            and recorded['lanes'] == ['normal', 'optimized', 'cold']
            and recorded['whole_lane_comparisons'] == 2,
            'complete historical paid lane record')
    adverse = expected['adverse']
    require(adverse['rejection_count'] == len(adverse['rejections']) == 39
            and all(row['result'] == 'REJECTED' for row in adverse['rejections'])
            and recorded['semantic_rejections_per_lane'] == 39
            and recorded['controls_are_not_infinite_enumeration'] is True
            and recorded['large_original_constructed'] is False,
            'whole semantic adverse record and enumeration boundary')
    require(recorded['formalized'] is False and recorded['independent_review'] is False,
            'no independent or formal verdict from byte verification')
    deps = json.loads((HERE / 'DEPENDENCIES.json').read_text())
    require(deps['agent'] == 'six-downset-1' and deps['role'] == 'researcher'
            and deps['verbatim_utilities'] == [] and deps['priority_claim'] is False
            and deps['globally_resolves_H'] is False
            and deps['adopted_peer_carrier_bounds'] == [], 'explicit predecessor scope')
    require([p['height'] for p in deps['predecessors']] ==
            [9361, 10111, 10160, 10270, 10282, 10294, 10310, 10316],
            'complete committed predecessor credits')
    for name in VERBATIM[:4] + ('verify_source.py',):
        compile((HERE / name).read_text(), name, 'exec')
    print(json.dumps(dict(agent='six-downset-1', role='researcher',
        status='COMPLETE PUBLIC SOURCE/PROVENANCE INTEGRITY ONLY',
        publication_files=len(PUBLIC_FILES), whole_current_byte_checks=len(manifest),
        verbatim_paid_files=len(VERBATIM), recovered_sealed_documents=len(EDITORIAL),
        private_manifest_sha256=PRIVATE_MANIFEST_SHA,
        whole_mathematical_record_bytes=len(expected_raw),
        whole_mathematical_record_sha256=EXPECTED_SHA,
        historical_math_children=21, historical_semantic_rejections=117,
        mathematics_replayed=False, independent_review=False, formalized=False),
        sort_keys=True))


if __name__ == '__main__':
    main()
