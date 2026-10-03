"""Source-only complete explicit profile7 proof, with serial guarded children.

Normal and optimized modes regenerate every required proposal. In optimized
mode the root-cut checkers inspect the SAME normal input bytes, after every
new optimized proposal has been compared byte for byte. Parent packets have
only elapsed seconds removed before literal checking; all mathematical and
scope fields, including the actual packet hash, remain in the whole records.
"""
import argparse
import datetime
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESIDUAL = [19, 28, 31]
CLOSED = [t for t in range(32) if t not in RESIDUAL]
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')
ROOT_DAMAGE_CASES = ('remove-valid-row', 'insert-invalid-row', 'boolean-row-word',
                     'false-unsupported-pair', 'fabricated-complete-cut')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_bytes(encoded(value) + b'\n')


def without_elapsed(value):
    if isinstance(value, dict):
        return {k:without_elapsed(v) for k,v in value.items() if k != 'seconds'}
    if isinstance(value, list):
        return [without_elapsed(v) for v in value]
    return value


def portable_mathematics(value):
    # These are actual certificate-byte provenance, not domain membership,
    # coverage or rejection data. They remain in FULL_MATHEMATICS.json and
    # must match normal/O. A fresh absolute work path changes the FIXED
    # packet's source filenames and hence these enclosing provenance hashes.
    omit = {'seconds', 'packet_sha256', 'fixed_packet_sha256',
            'original_fixed_packet_sha256', 'actual_damaged_sha256'}
    if isinstance(value, dict):
        return {k:portable_mathematics(v) for k,v in value.items() if k not in omit}
    if isinstance(value, list):
        return [portable_mathematics(v) for v in value]
    return value


def source_seal():
    paths = sorted(ROOT.rglob('*.py')) + [ROOT / 'parent/primary21.txt']
    require(all('__pycache__' not in p.parts for p in paths), 'Cache in source domain')
    return [dict(path=str(p.relative_to(ROOT)), bytes=len(p.read_bytes()),
                 sha256=sha(p.read_bytes())) for p in paths]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--mode', choices=('normal', 'optimized'), required=True)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    work = args.work.resolve()
    require(work != ROOT and ROOT not in work.parents,
            'Generated work must be outside the public source directory')
    current = work / args.mode
    basis = work / 'normal'
    current.mkdir(parents=True, exist_ok=True)
    for name in ('parent', 'cut', 'receipts'):
        (current / name).mkdir(exist_ok=True)
    seal = source_seal()
    meta_path = current / 'RUN.json'
    if meta_path.exists():
        old = json.loads(meta_path.read_bytes())
        require(args.resume and old['source_files'] == seal
                and old['mode'] == args.mode, 'Existing work or changed source; use a fresh path')
    else:
        require(not args.resume, 'No run exists to resume')
        dump(meta_path, dict(agent='six-books-3', role='researcher', mode=args.mode,
            source_files=seal, source_seal_sha256=sha(encoded(seal)),
            created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            python=sys.version, child_seconds_guard=45,
            inner_work_guard=2000000, inner_seconds_guard=40, native_threads=1))
    if args.mode == 'optimized':
        require((basis / 'RESULT.json').is_file(), 'Complete normal mode must exist first')
        require(json.loads((basis / 'RUN.json').read_bytes())['source_files'] == seal,
                'Normal mode belongs to different source bytes')
    env = dict(os.environ)
    for name in THREADS:
        env[name] = '1'
    env.pop('PYTHONPATH', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONHASHSEED'] = '0'
    calls = []
    products = []

    def operational_pause():
        # Optional campaign-only guard. No private host path is a mathematical
        # input or required for ordinary standalone reproduction.
        state = env.get('BOOKS_CAMPAIGN_STATE')
        if state:
            require(not any((Path(state) / name).exists() for name in
                ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json')),
                'Operations pause: preserve completed work, no mathematical verdict')

    def job(label, program, *arguments):
        operational_pause()
        command = [sys.executable]
        if args.mode == 'optimized':
            command.append('-O')
        command.extend([str(ROOT / program), *map(str, arguments)])
        receipt = current / 'receipts' / (label + '.json')
        output = current / 'receipts' / (label + '.stdout')
        error = current / 'receipts' / (label + '.stderr')
        if args.resume and receipt.exists():
            row = json.loads(receipt.read_bytes())
            require(row['command'] == command and row['status'] == 'CHILD_COMPLETED'
                    and row['exit_code'] == 0 and sha(output.read_bytes()) == row['stdout_sha256'],
                    'Saved child not complete/bound; do not infer an exclusion')
        else:
            started = time.monotonic()
            try:
                child = subprocess.run(command, env=env, capture_output=True, timeout=45)
                out, err, code = child.stdout, child.stderr, child.returncode
                status = 'CHILD_COMPLETED' if code == 0 else 'CHILD_FAILED_NO_VERDICT'
            except subprocess.TimeoutExpired as exc:
                out, err, code = exc.stdout or b'', exc.stderr or b'', None
                status = 'OPERATIONAL_LIMIT_NO_VERDICT'
            output.write_bytes(out)
            error.write_bytes(err)
            row = dict(label=label, command=command, status=status, exit_code=code,
                seconds=time.monotonic()-started, stdout_bytes=len(out),
                stdout_sha256=sha(out), guard_seconds=45,
                peak_children_rss_so_far_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                native_threads=1, mathematical_children=1)
            dump(receipt, row)
        calls.append(row)
        dump(current / 'PROGRESS.json', dict(mode=args.mode, complete_children=len(calls),
            last_label=label, last_status=row['status'], whole_profile_excluded=False))
        require(row['status'] == 'CHILD_COMPLETED' and row['exit_code'] == 0,
                'Child failed or stopped; preserve receipts, no mathematical verdict: ' + label)
        return without_elapsed(json.loads(output.read_bytes()))

    def bind_product(path):
        relative = path.relative_to(current)
        data = path.read_bytes()
        if args.mode == 'optimized':
            require(data == (basis / relative).read_bytes(),
                    'Entire regenerated normal/optimized data differs: ' + str(relative))
        products.append(dict(path=str(relative), bytes=len(data), sha256=sha(data)))

    inventory = job('parent-inventory', 'parent/compare_inventory.py')
    require(inventory['matrices'] == 32
            and inventory['whole_inventory_sha256'] ==
            'd4854ad9e4cd8dc1a88742bcb1809536193c1ecd05a109438acc6f94202b216d',
            'Entire original matrix/star domain differs')
    transport = job('parent-transport', 'parent/transport.py')
    require(transport['residual_orbit'] == RESIDUAL
            and RESIDUAL in transport['orbits'] and transport['matrices'] == 32,
            'Required physical residual orbit not completely transported')
    parent_records = []
    for template in CLOSED:
        packet = current / 'parent' / ('certificate' + str(template) + '.json')
        checked = current / 'parent' / ('checked' + str(template) + '.json')
        job('parent-producer-' + str(template), 'parent/generate.py',
            '--template', template, '--out', packet)
        # Protocol-only normalization precedes literal checking. Do not omit
        # a cut, status, rule, scope, pending operation or domain size.
        dump(packet, without_elapsed(json.loads(packet.read_bytes())))
        bind_product(packet)
        job('parent-literal-' + str(template), 'parent/check.py',
            '--packet', packet, '--out', checked)
        record = without_elapsed(json.loads(checked.read_bytes()))
        dump(checked, record)
        bind_product(checked)
        require(record['template'] == template and record['claim_template_excluded']
                and record['empty_targets'] and record['pending'] is None
                and record['status'] == 'FULL_PAIR_DELETION_EXCLUSION_CHECKED',
                'Original parent case not fully literally excluded')
        parent_records.append(record)
        print('Closed parent case', template, 'literal cuts', record['checked_stars'], flush=True)
    parent_controls = job('parent-controls', 'parent/controls.py',
        '--packet', current / 'parent/certificate0.json')
    require(len(parent_controls['certificate_controls']['damages_detected']) == 15
            and parent_controls['primary_baseline']['whole_spines'] == 210,
            'Parent semantic controls/baseline incomplete')

    cut = current / 'cut'
    bound = cut if args.mode == 'normal' else basis / 'cut'
    rows = cut / 'CUT_ROWS-normal.jsonl'
    columns = cut / 'COLUMN_CERT-normal.jsonl'
    pair0 = cut / 'PAIR-0-25.json'
    pair1 = cut / 'PAIR-25-2850.json'
    fixed = cut / 'FIXED-normal.json'
    complete = cut / 'COMPLETE-normal.json'
    root_records = {}
    root_records['rows'] = job('cut-rows', 'root_cut/cut_rows.py', '--out', rows)
    bind_product(rows)
    root_records['literal_rows'] = job('cut-literal-rows', 'root_cut/check_rows.py',
        '--records', bound / rows.name)
    root_records['columns'] = job('cut-columns', 'root_cut/column_bounds.py',
        '--records', bound / rows.name, '--out', columns)
    bind_product(columns)
    root_records['pair0'] = job('cut-pair0', 'root_cut/pair_cover.py',
        '--records', bound / rows.name, '--columns', bound / columns.name,
        '--start', 0, '--stop', 25, '--out', pair0)
    bind_product(pair0)
    root_records['pair1'] = job('cut-pair1', 'root_cut/pair_cover.py',
        '--records', bound / rows.name, '--columns', bound / columns.name,
        '--start', 25, '--stop', 2850, '--out', pair1)
    bind_product(pair1)
    root_records['literal_filters'] = job('cut-literal-filters', 'root_cut/check_filters.py',
        '--records', bound / rows.name, '--columns', bound / columns.name,
        '--packets', bound / pair0.name, bound / pair1.name, '--fixed-out', fixed)
    bind_product(fixed)
    root_records['complete'] = job('cut-complete', 'root_cut/cut_complete.py',
        '--fixed', bound / fixed.name, '--out', complete)
    bind_product(complete)
    root_records['literal_complete'] = job('cut-literal-complete', 'root_cut/check_complete.py',
        '--fixed', bound / fixed.name, '--proposed', bound / complete.name)
    root_controls = [job('cut-control-' + case, 'root_cut/controls.py',
                         '--root', bound, '--case', case) for case in ROOT_DAMAGE_CASES]
    filters = root_records['literal_filters']
    require(filters['original_graphs'] == 50400 and filters['empty_row_exclusions'] == 47492
            and filters['column_bound_exclusions'] == 58
            and filters['literal_pair_empty_exclusions'] == 2849
            and filters['remaining_graph_indices'] == [25642]
            and root_records['complete']['complete']
            and root_records['literal_complete']['complete']
            and root_records['complete']['physical_cut_matrices'] == 0
            and root_records['literal_complete']['physical_cut_matrices'] == 0
            and len(root_controls) == 5
            and all(r['status'] == 'ACTUAL_SEMANTIC_DAMAGE_REJECTED' for r in root_controls),
            'Root cut cover, complete last matrix domain or controls incomplete')
    require([r['template'] for r in parent_records] == CLOSED
            and sorted(CLOSED + RESIDUAL) == list(range(32)),
            'Canonical deficit coverage incomplete')
    full = dict(inventory=inventory, transport=transport, parent_records=parent_records,
                parent_controls=parent_controls, root_records=root_records, root_controls=root_controls)
    full_bytes = encoded(full)
    portable_bytes = encoded(portable_mathematics(full))
    if args.mode == 'optimized':
        require(full_bytes == (basis / 'FULL_MATHEMATICS.json').read_bytes(),
                'Whole normal/O mathematical records differ, including actual provenance')
    (current / 'FULL_MATHEMATICS.json').write_bytes(full_bytes)
    (current / 'PORTABLE_MATHEMATICS.json').write_bytes(portable_bytes)
    dump(current / 'PRODUCTS.json', products)
    require(source_seal() == seal, 'Source bytes changed during computation')
    result = dict(agent='six-books-3', role='researcher',
        status='COMPLETE_SOURCE_ONLY_EXPLICIT_PROFILE7_EXCLUSION',
        counts=inventory['counts'], ordinary_order=22, independent_degree9_lows=4,
        degree10_highs=18, no_high_type0=True, ordinary_page_caps=[3,6],
        canonical_matrices=32, complete_literal_parent_cases=29,
        parent_literal_deletions=sum(r['checked_stars'] for r in parent_records),
        residual_low_label_orbit=RESIDUAL,
        original_marked_neighborhoods=50400,
        root_cover=[47492,58,2849,1], final_cut_matrices=0,
        parent_semantic_damages=15, root_semantic_damages=5,
        parent_positive_prefixes=2, ordinary_bridges_formalized=False,
        independent_person_review=False, whole_explicit_profile_excluded=True,
        global_Ramsey_bound_claimed=False,
        full_mathematical_bytes=len(full_bytes), full_mathematical_sha256=sha(full_bytes),
        portable_mathematical_bytes=len(portable_bytes), portable_mathematical_sha256=sha(portable_bytes),
        source_seal_sha256=sha(encoded(seal)), bounded_complete_children=len(calls),
        native_threads=1, mathematical_children=1, child_seconds_guard=45,
        inner_work_guard=2000000, inner_seconds_guard=40,
        maximum_child_rss_kib=max(r['peak_children_rss_so_far_kib'] for r in calls),
        all_regenerated_products=len(products),
        whole_normal_O_records_compared=args.mode == 'optimized')
    dump(current / 'RESULT.json', result)
    dump(current / 'PROGRESS.json', dict(mode=args.mode, complete_children=len(calls),
        last_status='COMPLETE', whole_explicit_profile_excluded=True,
        global_Ramsey_bound_claimed=False))
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
