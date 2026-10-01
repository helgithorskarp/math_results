"""Reproduce the remaining depth-free ten-event B11 exclusions.

Author/executing agent: six-sorting-2, researcher. This small selection
adapter reuses hash-pinned public Boolean and independent audit kernels.
Verification modes do not import the generator or a SAT solver. Bulk
outputs are regenerated locally; a hash comparison alone is not a proof.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

H = Path(__file__).resolve().parent
BASE_NAME = 'sorting13_B11_additional_ten_event_exclusions'
FIELDS = ('last_pair', 'variables', 'clauses', 'cnf_sha256', 'raw_drat_sha256',
          'core_clauses', 'core_sha256', 'trimmed_drat_sha256', 'RUP_additions')
GEN_FIELDS = FIELDS[:5]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def pin_dependencies(repo):
    for item in read(H / 'dependencies.json')['pinned_files']:
        assert sha(repo / item['path']) == item['sha256'], item['path']


def imports(repo):
    sys.path.insert(0, str(repo / BASE_NAME))
    import audit_data
    import audit_encoding
    # The scalar algorithm is unchanged. Only the public record selector
    # is extended, through this explicit provenance callback.
    audit_data.provenance = lambda meta: provenance(repo, meta)
    return audit_data, audit_encoding


def record(repo, expected):
    parent = read(repo / 'sorting13_B11_ten_event_loop_postponement/certificate.json')
    item = next(r for r in parent['classes'] if r['code'] == expected['code'])
    assert item['obstruction'] is None and item['image_id'] == expected['image_id']
    image = parent['images9'][item['image_id']]
    assert len(image) == expected['rows']
    return dict(code=item['code'], partner=item['partner'], kind=item['kind'],
                canonical_events=item['events'], image9=image, image9_rows=len(image))


def provenance(repo, meta):
    pin_dependencies(repo)
    expected = next(r for r in read(H / 'certificate.json')['records']
                    if r['code'] == meta['record']['code'])
    assert meta['record'] == record(repo, expected)
    quotient = read(repo / 'sorting_networks/thirteen_extreme_multiset_quotient/certificate.json')
    entry = next(r for r in quotient['class_table'] if r[0] == expected['code'])
    assert entry[1] == 10 and entry[2] == expected['effective_orders']
    fixture = read(repo / 'sorting13_B11_ten_event_matching_dags/fixture.json')
    prefix = fixture['prefix22'] + [[a + 1, b + 1] for a, b in meta['record']['canonical_events']]
    assert len(prefix) == 32 and [list(g) for g in meta['prefix']] == prefix
    activity = read(repo / 'sorting13_B11_pruning_saturation_activity/certificate.json')
    roots = [(f['mode'], f['partner'], original)
             for f in activity['families'] if f['final_D'] == 9
             for original in f['original_representatives']]
    assert [(d['mode'], d['partner'], d['original']) for d in meta['domains']] == roots


def paths(expected, output):
    base = output / f"case{expected['image_id']:03d}.cnf"
    assert expected['method'] in ('whole', 'last_gate')
    leaves = [base] if expected['method'] == 'whole' else [
        output / f"case{expected['image_id']:03d}-last{i}.cnf" for i in range(8)]
    return base, leaves


def manifest_row(path, proof=False):
    meta = read(path.with_suffix('.metadata.json'))
    result = dict(last_pair=meta.get('last_pair'), variables=meta['variables'],
                  clauses=meta['clauses'], cnf_sha256=sha(path),
                  raw_drat_sha256=sha(path.with_suffix('.drat')))
    if proof:
        checked = read(path.with_suffix('.proof-check.json'))
        assert checked['status'] == 'PYTHON_RUP_CORE_AND_FULL_MEMBERSHIP_VERIFIED'
        for key in FIELDS[5:]:
            result[key] = checked[key]
    return result


def generate(repo, expected, output):
    # Solver dependencies are imported only in generation mode.
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '1'
    scalar, _ = imports(repo)
    spec = importlib.util.spec_from_file_location('pinned_generator', repo / BASE_NAME / 'build.py')
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    assert engine.pysat.__version__ == '1.8.dev24'
    instance = record(repo, expected)
    base, leaves = paths(expected, output)
    original = engine.Encoding(instance, 12, base)
    engine.add_suffix(original)
    assert original.metadata['cnf_sha256'] == expected['base_cnf_sha256']
    assert (original.top, original.count) == (expected['variables'], expected['base_clauses'])
    scalar.audit_data(original.metadata)
    if expected['method'] == 'last_gate':
        original.solver.delete()
    for i, path in enumerate(leaves):
        target = original if expected['method'] == 'whole' else engine.Encoding(instance, 12, path)
        if expected['method'] == 'last_gate':
            engine.add_suffix(target)
            assert target.metadata['cnf_sha256'] == expected['base_cnf_sha256']
            unit = target.choice[-1][engine.PAIRS.index((i, i + 1))]
            target.body = path.with_suffix('.body').open('a')
            target.add([unit])
            target.body.close()
            path.write_text(f'p cnf {target.top} {target.count}\n' + path.with_suffix('.body').read_text())
            target.metadata.update(clauses=target.count, partition_unit=unit, last_pair=[i, i + 1],
                                   base_cnf_sha256=expected['base_cnf_sha256'], cnf_sha256=sha(path))
            path.with_suffix('.metadata.json').write_text(json.dumps(target.metadata, separators=(',', ':')) + '\n')
        answer, seconds = target.limited(40, 30000)
        if answer is not False:
            target.solver.delete()
            raise RuntimeError(f'No exclusion reproduced: solver returned {answer!r}')
        path.with_suffix('.drat').write_text('\n'.join(target.solver.get_proof()) + '\n')
        target.solver.delete()
        print(json.dumps(dict(image_id=expected['image_id'], last_pair=target.metadata.get('last_pair'),
                              status='TRACE_GENERATED_CHECKS_PENDING', seconds=seconds)), flush=True)
    generated = [manifest_row(path) for path in leaves]
    assert digest(generated) == expected['generation_manifest_sha256']
    return dict(image_id=expected['image_id'], leaves=len(leaves), generation_manifest_sha256=digest(generated))


def positive(repo, expected, output):
    scalar, _ = imports(repo)
    spec = importlib.util.spec_from_file_location('pinned_generator', repo / BASE_NAME / 'build.py')
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    assert engine.pysat.__version__ == '1.8.dev24'
    word = engine.normalize([(j-1, j) for i in range(1, 9) for j in range(i, 0, -1)])
    target = engine.Encoding(record(repo, expected), 36, output / 'positive36.cnf', activity=False)
    engine.add_suffix(target)
    data = scalar.audit_data(target.metadata)
    answer, _ = target.limited(15, assumptions=target.fixed(word))
    assert answer is True, ('Positive control incomplete', answer)
    checked = scalar.check_model(target.metadata, word, target.solver.get_model(), target.path)
    target.solver.delete()
    return dict(data=data, model=checked)


def audit(repo, expected, output):
    scalar, clauses = imports(repo)
    base, leaves = paths(expected, output)
    meta = read(base.with_suffix('.metadata.json'))
    assert meta['budget'] == 12 and meta['activity'] is True
    assert sha(base) == expected['base_cnf_sha256'] == meta['cnf_sha256']
    data = scalar.audit_data(meta)
    checker = clauses.Audit(meta, base)
    coverage = checker.run()
    if expected['method'] == 'last_gate':
        pairs = [(a, b) for a in range(9) for b in range(a+1, 9)]
        actual = set(checker.clauses)
        terminal = meta['boundary'][-1]
        for flag in terminal:
            assert (-flag,) in actual
        for j, (a, b) in enumerate(pairs):
            if b > a+1:
                assert (-meta['choices'][-1][j], terminal[a], terminal[a+1]) in actual
        # The audited exactly-one block and these 28 prohibitions exhaust
        # all last choices. Each of the eight adjacent choices has a leaf.
        for i, path in enumerate(leaves):
            leaf = read(path.with_suffix('.metadata.json'))
            for key in ('budget', 'record', 'variables', 'choices', 'used', 'rows', 'swaps',
                        'prefix', 'caps', 'hit_flags', 'domains', 'activity', 'boundary'):
                assert leaf[key] == meta[key], key
            unit = meta['choices'][-1][pairs.index((i, i+1))]
            assert leaf['last_pair'] == [i, i+1] and leaf['partition_unit'] == unit
            assert leaf['clauses'] == meta['clauses']+1 and sha(path) == leaf['cnf_sha256']
            with base.open() as old, path.open() as new:
                assert new.readline() == f"p cnf {leaf['variables']} {leaf['clauses']}\n"
                assert old.readline() == f"p cnf {meta['variables']} {meta['clauses']}\n"
                for line in old:
                    assert new.readline() == line
                assert new.readline() == f'{unit} 0\n' and new.readline() == ''
        coverage = dict(coverage, exhaustive_last_gate_leaves=8, nonadjacent_last_choices_excluded=28)
    assert digest([manifest_row(p) for p in leaves]) == expected['generation_manifest_sha256']
    result = dict(image_id=expected['image_id'], status='SCALAR_ALL_BASE_CLAUSES_AND_ALL_LEAF_UNITS_AUDITED',
                  data=data, coverage=coverage)
    base.with_suffix('.coverage-audit.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def stop_replay(signum, frame):
    raise TimeoutError('Python RUP reached40s; no checked proof from this run')


def proof(repo, path, tool, rup):
    meta = read(path.with_suffix('.metadata.json'))
    assert sha(path) == meta['cnf_sha256']
    raw = path.with_suffix('.drat')
    command = [str(tool.resolve()), str(path), str(raw), '-c', str(path.with_suffix('.core.cnf')),
               '-l', str(path.with_suffix('.trimmed.drat')), '-L', str(path.with_suffix('.lrat')), '-t', '40']
    native = subprocess.run(command, capture_output=True, text=True, timeout=45)
    path.with_suffix('.native-check.log').write_text(native.stdout+native.stderr)
    assert native.returncode == 0 and 's VERIFIED' in native.stdout
    assert '0 RAT lemmas in core' in native.stdout
    corepath, proofpath = path.with_suffix('.core.cnf'), path.with_suffix('.trimmed.drat')
    n = count = None
    core = []
    with corepath.open() as stream:
        for line in stream:
            if line.startswith('c') or not line.strip():
                continue
            word = line.split()
            if word[0] == 'p':
                _, _, n, count = word
                n, count = int(n), int(count)
            else:
                values = list(map(int, word))
                assert values[-1] == 0
                core.append(tuple(sorted(set(values[:-1]))))
    assert n == meta['variables'] and len(core) == count
    needed = set(core)
    with path.open() as stream:
        for line in stream:
            if line.startswith(('p', 'c')):
                continue
            values = list(map(int, line.split()))
            assert values[-1] == 0
            needed.discard(tuple(sorted(set(values[:-1]))))
    assert not needed
    initially_unit_inconsistent = rup.WatchedRUP(n, core).entails_by_rup(())
    signal.signal(signal.SIGALRM, stop_replay)
    signal.alarm(40)
    try:
        additions, deletions = rup.replay(n, core, proofpath)
    finally:
        signal.alarm(0)
    result = dict(agent='six-sorting-2', role='researcher',
                  status='PYTHON_RUP_CORE_AND_FULL_MEMBERSHIP_VERIFIED',
                  core_clauses=count, core_sha256=sha(corepath), trimmed_drat_sha256=sha(proofpath),
                  RUP_additions=additions, proof_deletions=deletions, native_RAT_lemmas=0,
                  initially_unit_inconsistent=initially_unit_inconsistent,
                  checker_credit='six-sorting-1/graph7452/source5ad75ecb80164da04c921f1898cf62334668a027')
    path.with_suffix('.proof-check.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def frontier(repo):
    cert = read(H / 'certificate.json')
    parent = read(repo / 'sorting13_B11_ten_event_loop_postponement/certificate.json')
    matching = read(repo / 'sorting13_B11_ten_event_matching_dags/certificate.json')
    old = read(repo / BASE_NAME / 'certificate.json')
    first = read(repo / 'sorting13_B11_image61_depth_free_exclusion/certificate.json')
    previous = {r['code'] for r in old['records']} | {first['class_code']}
    new = {r['code'] for r in cert['coverage']}
    unresolved = {r['code'] for r in parent['classes'] if r['obstruction'] is None}
    assert previous.isdisjoint(new) and previous | new == unresolved
    proof_images = {r['image_id']: r for r in cert['records']}
    inherited_prefix_inputs = 0
    scalar, _ = imports(repo)
    fixture = read(repo / 'sorting13_B11_ten_event_matching_dags/fixture.json')
    for r in cert['coverage']:
        item = next(x for x in parent['classes'] if x['code'] == r['code'])
        assert item['image_id'] == r['image_id']
        assert r['proved_image_id'] in proof_images
        assert set(parent['images9'][r['proved_image_id']]) <= set(parent['images9'][r['image_id']])
        if r['code'] != proof_images[r['proved_image_id']]['code']:
            prefix = fixture['prefix22'] + [[a+1,b+1] for a,b in item['events']]
            projected = set()
            for original in range(8192):
                bits = [original >> i & 1 for i in range(13)]
                out = scalar.trace(bits, prefix)[-1]
                assert out[:2] == sorted(bits)[:2] and out[-2:] == sorted(bits)[-2:]
                projected.add(sum(out[j+2] << j for j in range(9)))
                inherited_prefix_inputs += 1
            assert projected == set(parent['images9'][r['image_id']])
    quotient = read(repo / 'sorting_networks/thirteen_extreme_multiset_quotient/certificate.json')
    table = {r[0]: (r[1], r[2]) for r in quotient['class_table']}
    assert all(r['effective_orders'] == table[r['code']][1] for r in cert['coverage'])
    first4 = set(matching['dropped_ten_class_codes'])
    inactive = {r['code'] for r in parent['classes'] if r['obstruction'] is not None}
    represented = {r['code'] for r in parent['classes']}
    all_ten = {code for code, (events, count) in table.items() if events == 10}
    assert len(parent['classes']) == 108 and all(table[r['code']][0] == 10 for r in parent['classes'])
    assert len(first4) == 27 and first4.isdisjoint(represented)
    assert len(inactive) == 18 and inactive.isdisjoint(previous | new)
    assert all_ten == first4 | inactive | previous | new
    assert len(all_ten) == 135
    assert len(unresolved) == 90 and len(previous) == 13 and len(new) == 77
    orders = sum(table[code][1] for code in new)
    assert orders == 432186
    assert sum(table[code][1] for code in all_ten) == 751950
    boundary = read(repo / 'sorting_networks/thirteen_class13_boundary_obstruction/certificate.json')
    repeated01 = set(parent['peer_repeated_exclusion_codes'])
    assert len(repeated01) == 18 and boundary['class_code'] not in repeated01
    all_eleven = {code for code, (events, count) in table.items() if events == 11}
    excluded_eleven = repeated01 | {boundary['class_code']}
    assert excluded_eleven <= all_eleven and len(excluded_eleven) == 19
    remaining_eleven = all_eleven - excluded_eleven
    def repeated(code):
        n = int(code)
        digits = []
        while n:
            digits.append(n % 4)
            n //= 4
        assert sum(digits) == 11 and max(digits) <= 2
        assert digits.count(2) <= 1
        return 2 in digits
    assert len(remaining_eleven) == 326
    assert sum(repeated(code) for code in remaining_eleven) == 29
    assert sum(not repeated(code) for code in remaining_eleven) == 297
    assert all(repeated(code) for code in excluded_eleven)
    assert sum(table[code][1] for code in remaining_eleven) == 2218605
    recent = read(repo / 'sorting_networks/thirteen_repeated23_reduction/certificate.json')
    extra = {r['class_code'] for r in recent['classes']
             if r['parent_index'] in recent['excluded_parent_indices']}
    assert recent['excluded_parent_indices'] == [34,149,237] and len(extra) == 3
    assert extra <= remaining_eleven and all(repeated(code) for code in extra)
    assert sum(table[code][1] for code in extra) == recent['excluded_effective_orders'] == 16155
    current_eleven = remaining_eleven - extra
    assert len(current_eleven) == 323 and sum(repeated(code) for code in current_eleven) == 26
    assert sum(table[code][1] for code in current_eleven) == 2202450
    transfer = cert['tail_transfer']
    tail = next(t for t in recent['remaining_tails']
                if t['parent_index'] == transfer['parent_index'] and t['image'] == transfer['local_image'])
    assert tail['class_code'] == transfer['class_code'] and tail['budget'] == transfer['budget'] == 11
    assert tail['rows9_sha256'] == transfer['rows9_sha256']
    proved = proof_images[transfer['proved_image_id']]
    assert proved['image_id'] == 2 and len(parent['images9'][2]) == 52
    assert tail['rows9'] == parent['images9'][2]
    prefix = fixture['prefix22'] + [[a+1,b+1] for a,b in tail['prefix_B11']]
    assert len(prefix) == 33
    projected = set()
    for original in range(8192):
        bits = [original >> i & 1 for i in range(13)]
        out = scalar.trace(bits, prefix)[-1]
        assert out[:2] == sorted(bits)[:2] and out[-2:] == sorted(bits)[-2:]
        projected.add(sum(out[j+2] << j for j in range(9)))
    assert projected == set(tail['rows9'])
    return dict(status='EXACT_CONDITIONAL_CLASS_INCIDENCE_AND_ARITHMETIC_VERIFIED',
                total_ten_classes=135, ten_effective_orders=751950,
                prior_first4_classes=27, prior_inactive_event_classes=18,
                new_classes=77, new_orders=orders, remaining_ten=0,
                remaining_conditional_classes=323,
                remaining_conditional_orders=2202450,
                remaining_eleven_distinct=297, remaining_eleven_repeated=26,
                relative_to8222_remaining_classes=403-len(new),
                peer8281_complete_class_exclusions=3, peer8281_effective_orders=16155,
                new_tail_transfer=dict(parent_index=155, local_image=0, proved_image=2,
                                      budget=11, proved_minimum=13, original_inputs_reconstructed=8192,
                                      peer_five_tail_frontier_reduced_to=4),
                inherited_prefix_inputs=inherited_prefix_inputs,
                trust='Arithmetic and image incidence assume the checked certificates and explicitly imported parent theorems')


def main():
    assert __debug__, 'Assertions are required'
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('generate', 'audit', 'proof', 'frontier'))
    parser.add_argument('--repository', type=Path, default=H.parent)
    parser.add_argument('--output', type=Path, default=H / 'generated')
    parser.add_argument('--image', type=int)
    parser.add_argument('--drat-trim', type=Path)
    args = parser.parse_args()
    repo = args.repository.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    pin_dependencies(repo)
    certificate = read(H / 'certificate.json')
    selected = [r for r in certificate['records'] if args.image is None or r['image_id'] == args.image]
    assert selected, 'Unlisted image'
    started = time.monotonic()
    results = []
    if args.mode == 'generate':
        control = positive(repo, selected[0], args.output)
        (args.output / 'positive-control.json').write_text(json.dumps(control, indent=2)+'\n')
        for expected in selected:
            result = generate(repo, expected, args.output)
            results.append(result)
    elif args.mode == 'audit':
        imports(repo)
        import controls
        base, _ = paths(selected[0], args.output)
        meta = read(base.with_suffix('.metadata.json'))
        controls_result = dict(semantics=controls.semantics(), structure=controls.structure(),
                               rejections=controls.rejections(meta, base))
        for expected in selected:
            result = audit(repo, expected, args.output)
            results.append(result)
            print(json.dumps(dict(image_id=result['image_id'], status=result['status'])), flush=True)
        (args.output / 'controls.json').write_text(json.dumps(controls_result, indent=2)+'\n')
    elif args.mode == 'proof':
        assert args.drat_trim is not None
        spec = importlib.util.spec_from_file_location('credited_peer_rup', repo / 'sorting13_maximum_preparation/watched_rup.py')
        rup = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rup)
        tiny_controls = rup.self_check()
        for expected in selected:
            _, leaves = paths(expected, args.output)
            assert digest([manifest_row(p) for p in leaves]) == expected['generation_manifest_sha256']
            checked = [proof(repo, path, args.drat_trim, rup) for path in leaves]
            manifest = [manifest_row(path, True) for path in leaves]
            assert digest(manifest) == expected['proof_manifest_sha256']
            assert sum(r['RUP_additions'] for r in checked) == expected['RUP_additions']
            assert sum(r['core_clauses'] for r in checked) == expected['core_clauses']
            result = dict(image_id=expected['image_id'], status='ALL_LEAF_PROOFS_CHECKED_AGGREGATE_MATCHED',
                          leaves=len(leaves), RUP_additions=expected['RUP_additions'], tiny_controls=tiny_controls)
            results.append(result)
            print(json.dumps(result), flush=True)
    else:
        results = [frontier(repo)]
    output = dict(agent='six-sorting-2', role='researcher', mode=args.mode, records=results,
                  seconds=time.monotonic()-started,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (args.output / f'{args.mode}-summary.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='records'}), flush=True)
    if args.mode == 'frontier':
        print(json.dumps(results[0]), flush=True)


if __name__ == '__main__':
    main()
