"""Bind the completed mathematical partition and full paired scalar products."""
import hashlib
import json
from pathlib import Path

from run_preparations import need
from run_witnesses import source_fingerprint
from run_extended import extension_fingerprint
from run_nested import nested_fingerprint

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def canonical(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def source_rows():
    rows = []
    for parent in (ROOT, ROOT/'prior'):
        for path in parent.iterdir():
            if (not path.is_file() or path.name in ('SOURCE-MANIFEST.json','certificate.json','VALIDATION.json')
                    or path.suffix not in ('.py','.json','.md') and path.name != '.gitignore'):
                continue
            data = path.read_bytes()
            rows.append({'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(data).hexdigest(),
                         'bytes': len(data)})
    return sorted(rows, key=lambda row:row['path'])


def checked(name):
    obj = json.loads((WORK/name).read_text())
    plain = hashlib.sha256(json.dumps(obj['finite'], separators=(',', ':')).encode()).hexdigest()
    need(obj['finite_sha256'] in (plain, canonical(obj['finite'])), 'Invalid saved finite record: '+name)
    return obj


def verify_and_seal():
    whole = checked('whole-result.json')
    need(whole['finite']['all_preparations_partitioned_and_excluded'] and
         whole['finite']['conditional_route_only'] and
         not whole['finite']['global_size44_exclusion_claimed'], 'False final scope/partition')
    need(whole['finite']['source_computation_sha256'] == source_fingerprint(), 'Changed mathematical source')
    controls = []
    for name in ('semantic-controls-complete.json','extended-semantic-controls-complete.json',
                 'nested-semantic-controls-complete.json'):
        record = checked(name)
        finite = record['finite']
        need(finite['all_original_inputs_unchanged'] and finite['all_transport_hashes_repaired'] and
             not finite['operational_failure_counted_as_math_rejection'], 'False semantic-control evidence')
        need(all(r['returncode'] != 0 and r['transport_hashes_repaired']
                 for r in finite['all_rejections']), 'Unrejected semantic damage')
        controls.append({'file':name, 'finite':finite, 'finite_sha256':record['finite_sha256']})
    need(sum(r['finite']['damage_types'] for r in controls) == 18 and
         sum(r['finite']['actual_math_children'] for r in controls) == 36, 'Incomplete semantic damage cover')
    products = {}
    for path in sorted(WORK.glob('*-O.json')):
        normal = path.with_name(path.name[:-7]+'.json')
        if not normal.exists():
            continue
        a, b = json.loads(normal.read_text()), json.loads(path.read_text())
        if 'finite' not in a:
            continue
        need(a['finite'] == b['finite'], 'Full scalar normal/O mathematical product differs: '+normal.name)
        products[normal.name] = canonical(a['finite'])
    need(len(products) == 49, 'One complete paired scalar product is missing')
    # Expected records are opened only after the entire current mathematical
    # partition, literal originals, witnesses and semantic rejections passed.
    expected = json.loads((ROOT/'EXPECTED.json').read_text())
    need(whole['finite'] == expected['whole_finite'] and
         whole['finite_sha256'] == expected['whole_finite_sha256'], 'Full expected partition differs')
    need(controls == expected['semantic_controls'], 'Full actual semantic rejection products differ')
    need(products == expected['paired_scalar_finite_products'], 'Full expected scalar product map differs')
    nested = checked('nested-phase-complete.json')
    need(nested['finite']['nested_source_sha256'] == nested_fingerprint(), 'Changed nested source')
    for interval in whole['finite']['intervals']:
        extension = interval['extension']
        if extension is not None:
            first,last = interval['new_reserve_open_function_interval']
            actual = checked(f'extended-phase-complete-{first:05}-{last:05}.json')
            need(actual['finite']['extension_source_sha256'] == extension_fingerprint(), 'Changed extension source')
    manifest = (ROOT/'SOURCE-MANIFEST.json').read_bytes()
    need(source_rows() == json.loads(manifest)['files'], 'Final source seal differs')
    finite = {
        'schema': 'complete-disjoint-high-56-910-conditional-exclusion-v1',
        'whole_original_partition': whole['finite'],
        'whole_original_partition_finite_sha256': whole['finite_sha256'],
        'paired_entire_scalar_products': products,
        'nested_phase': nested['finite'],
        'whole_ordered_function_transfer': checked('transfer-checked.json')['finite'],
        'semantic_controls': controls,
        'source_manifest_sha256': hashlib.sha256(manifest).hexdigest(),
        'complete_source_only_expected_products_match': True,
        'actual_preparation_length_bounded': False,
        'suffix_depth_bounded': False,
        'external_person_review_claimed': False,
        'global_size44_exclusion_claimed': False}
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'COMPLETE_SCOPED_SOURCE_ONLY_ORIGINAL_CERTIFICATE_AND_SEMANTIC_CONTROLS',
              'finite':finite, 'finite_sha256':canonical(finite)}
    (WORK/'certificate-candidate.json').write_text(json.dumps(result, indent=2)+'\n')
    if (ROOT/'certificate.json').exists():
        previous = json.loads((ROOT/'certificate.json').read_text())
        need(previous['finite'] == finite and previous['finite_sha256'] == result['finite_sha256'],
             'Entire published certificate differs from actual fresh mathematical reproduction')
    return result


if __name__ == '__main__':
    print(json.dumps(verify_and_seal()))
