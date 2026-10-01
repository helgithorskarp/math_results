"""Validate full coverage and freeze deterministic evidence, excluding timings."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
from bootstrap import ensure_runtime
ensure_runtime()
import maps4 as M
from carrier import STANDARD_G, check_code
from check58 import check
from check_coverage import verify

HERE = Path(__file__).resolve().parent


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def stable(value):
    if isinstance(value, dict):
        return {k: stable(v) for k, v in value.items()
                if k not in ('seconds', 'peak_RSS_kib', 'child_peak_RSS_kib', 'sanitized')}
    if isinstance(value, (list, tuple)):
        return [stable(v) for v in value]
    return value


def completion_cover(roots, color, native):
    indices = list(range(8))
    M.require(len(roots['roots']) == 8 and color['inventory_roots'] == 8 and
              color['requested_cases'] == indices and native['inventory_roots'] == 8 and
              native['cases'] == 8 and [r['root'] for r in color['records']] == indices and
              [r['root'] for r in native['records']] == indices, 'incomplete bound coverage')
    for i, (a, b) in enumerate(zip(color['records'], native['records'])):
        root = roots['roots'][i]
        M.require(a['fixture'] == b['fixture'] == root['fixture'] and
                  a['status'] == 'COMPLETE_MAXIMUM' and a['absence_claim'] is True and
                  b['status'] == 'COMPLETE_EXACT_UPPER_AND_LITERAL_LOWER' and
                  b['upper'] == a['residual_weight'] <= 22 and b['larger_cliques'] == 0 and
                  b['orbit_vertices'] == a['vertices'], 'incomplete or false bound')
        words = tuple(a['witness'])
        degrees = check_code(words, STANDARD_G)
        M.require(set(root['normalized']) <= set(words) and
                  len(words) == a['words'] == 36+a['residual_weight'] and
                  tuple(a['replications']) == degrees and degrees[:2] == (20, 20) and
                  sum(bool(w & 1) and bool(w & 2) for w in words) == 4,
                  'false completion witness')


def collect(work):
    work = Path(work)
    def read(path):
        return json.loads((work/path).read_text())
    carriers = [read(f'swapped-m4-full/fixture-{i:02d}.json') for i in range(23)]
    raw = read('swapped-m4-full/summary.json')
    roots = read('swapped-m4-roots.json')
    groups = read('swapped-full-groups.json')
    color = read('swapped-m4-completions/summary.json')
    native = read('swapped-m4-native/summary.json')
    controls = read('swapped-m4-controls.json')
    verify(roots, carriers)
    M.require(raw['eligible_mates'] == 71 and raw['raw_maps'] == 115020 and
              raw['valid_maps'] == roots['valid_maps'] == 26 and roots['rooted_cases'] == 8 and
              len(raw['fixtures']) == len(roots['fixtures']) == 23 and
              [r['fixture'] for r in raw['fixtures']] == list(range(23)) and
              groups['status'] == 'COMPLETE_ACTUAL_FULL_FIXTURE_GROUPS' and
              len(groups['groups']) == 23, 'incomplete carrier/group totals')
    completion_cover(roots, color, native)
    witness = json.loads((HERE/'WITNESS58.json').read_text())
    positive = check(witness)
    M.require(witness['words'] == color['records'][5]['witness'] and
              controls['status'] == 'COMPLETE_LAMBDA4_LITERAL_COVER_AND_CONTROLS' and
              encoded(controls['positive']) == encoded(positive) and
              len(controls['rejected_damages']) == 9 and color['small_weighted_controls'] == 1099 and
              native['native_small_cases'] == 6144, 'missing witness or damage controls')
    rejected = []
    def reject(name, fn):
        try:
            fn()
        except (ValueError, KeyError, IndexError):
            rejected.append(name)
        else:
            raise ValueError('damage accepted: '+name)
    bad = deepcopy(native); bad['records'].pop()
    reject('omitted-native-case', lambda: completion_cover(roots, color, bad))
    bad = deepcopy(color); bad['records'][0]['status'] = 'INCOMPLETE'
    reject('incomplete-producer', lambda: completion_cover(roots, bad, native))
    bad = deepcopy(native); bad['records'][0]['upper'] += 1
    reject('false-native-upper', lambda: completion_cover(roots, color, bad))
    manifest = json.loads((HERE/'RUNTIME.json').read_text())
    with tempfile.TemporaryDirectory(prefix='runtime-damage-', dir=work) as tmp:
        directory = Path(tmp)
        for item in manifest:
            dest = directory/item['path']; dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((HERE/'runtime'/item['path']).read_bytes())
        for item in manifest:
            dest = directory/item['path']; original = dest.read_bytes()
            dest.write_bytes(original+b'\nCORRUPTED\n')
            reject('changed-runtime:'+item['path'], lambda: ensure_runtime(directory))
            dest.write_bytes(original)
    return {
        'agent': 'six-code-2', 'role': 'researcher',
        'status': 'COMPLETE_SHARP58_EXCHANGED_SATURATED_PAIR_MULTIPLICITY4',
        'fixture_records_sha256': [hashlib.sha256((work/'swapped-m4-full'/f'fixture-{i:02d}.json').read_bytes()).hexdigest() for i in range(23)],
        'raw_summary': stable(raw), 'positive_cover_sha256': digest(stable(roots)),
        'full_groups_sha256': digest(stable(groups)),
        'root_fixtures': [r['fixture'] for r in roots['roots']],
        'root_maxima': [r['words'] for r in color['records']],
        'weighted_records': stable(color['records']), 'native_records': stable(native['records']),
        'weighted_controls': 1099, 'native_controls': 6144,
        'literal_controls': stable(controls), 'bound_and_runtime_damages': rejected,
        'runtime_manifest_sha256': hashlib.sha256((HERE/'RUNTIME.json').read_bytes()).hexdigest(),
        'literal_witness': positive,
        'scope': 'Only involution 2^8*1^2 exchanging two degree20 points with pair multiplicity4; generic23-star premise imported, ordinary bridges unformalized; historical priority unassessed.'}
