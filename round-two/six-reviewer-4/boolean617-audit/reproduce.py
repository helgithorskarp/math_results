"""Serial source-only audit, full normal/O outputs, fixed 30s child guards."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
from field import P, cover, need

def digest(data):
    return hashlib.sha256(data).hexdigest()

def reproduce(work):
    source = Path(__file__).resolve().parent
    work.mkdir(exist_ok=False)
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    jobs = []
    def child(mode, script, arguments, output):
        command = [sys.executable]+(['-O'] if mode == 'optimized' else [])+[str(source/script)]+arguments
        start = time.monotonic()
        completed = subprocess.run(command, env=env, capture_output=True, timeout=30)
        jobs.append({'mode': mode, 'script': script, 'arguments': arguments,
                     'seconds': time.monotonic()-start, 'returncode': completed.returncode,
                     'stdout_sha256': digest(completed.stdout), 'stderr': completed.stderr.decode()})
        (work/'jobs.json').write_text(json.dumps(jobs, indent=2)+'\n')
        need(completed.returncode == 0, 'mathematical child failure: '+completed.stderr.decode())
        json.loads(completed.stdout)
        output.write_bytes(completed.stdout)
        return json.loads(completed.stdout)
    finals = []
    inventories = []
    for mode in ('normal', 'optimized'):
        directory = work/mode
        directory.mkdir()
        foundation = child(mode, 'basics.py', ['foundation'], directory/'foundation.json')
        controls = child(mode, 'basics.py', ['controls'], directory/'controls.json')
        seed = child(mode, 'basics.py', ['seed'], directory/'seed.json')
        core_records = []
        for index, row in enumerate(cover()):
            path = directory/('core-'+str(row[0])+'.json')
            record = child(mode, 'core.py', ['generate', str(row[0])], path)
            child(mode, 'core.py', ['validate', str(path)], directory/('core-check-'+str(row[0])+'.json'))
            core_records.append(record)
            if index % 20 == 0:
                print(mode, 'core geometries', index+1, flush=True)
        merged = directory/'core-merged.json'
        merged.write_text(json.dumps(core_records, sort_keys=True)+'\n')
        raw = child(mode, 'core.py', ['raw', str(merged)], directory/'raw.json')
        total_units = total_third_roots = 0
        for lower in range(0, P, 16):
            upper = min(P, lower+16)
            path = directory/('units-'+str(lower)+'.json')
            child(mode, 'interval.py', ['batch', str(lower)+':'+str(upper)], path)
            check = child(mode, 'interval.py', ['check_batch', str(path)+':'+str(lower)+':'+str(upper)], directory/('units-check-'+str(lower)+'.json'))
            total_units += check['verified_integer_units']
            total_third_roots += check['third_roots']
            if lower % 128 == 0:
                print(mode, 'physical third roots', total_third_roots, flush=True)
        need(total_third_roots == 615 and total_units == 12915, 'physical whole domain')
        need(raw['raw_nonprojection_states'] == 76875, 'raw whole truth domain')
        need(seed['integer_APs_checked'] == 1140833, 'entire seed AP domain')
        result = {'actual_agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
                  'target': 'LEMMA9842', 'status': 'fresh finite premises and ordinary defining reductions checked; native comparison separate',
                  'foundation': foundation, 'controls': controls, 'seed': seed, 'raw': raw,
                  'canonical_nonprojection_states': sum(len(r['witnesses']) for r in core_records),
                  'canonical_positive_pairs_tested': sum(r['candidate_pairs_tested'] for r in core_records),
                  'physical_third_roots': total_third_roots, 'physical_projection_cases': 3*total_third_roots,
                  'physical_unit_APs': total_units, 'fixed_integer_supports': 6*total_units,
                  'constant_core_min_free_columns': 89}
        final = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
        (directory/'RESULT.json').write_bytes(final)
        finals.append(final)
        inventories.append({p.name: digest(p.read_bytes()) for p in directory.iterdir() if p.is_file()})
    need(finals[0] == finals[1], 'whole normal/optimized final record disagreement')
    need(inventories[0] == inventories[1], 'whole normal/optimized witness/check inventory disagreement')
    (work/'RESULT.json').write_bytes(finals[0])
    receipt = {'mathematical_children': len(jobs), 'child_guard_seconds': 30,
               'whole_file_pairs_equal': len(inventories[0]), 'total_child_seconds': sum(j['seconds'] for j in jobs),
               'max_child_seconds': max(j['seconds'] for j in jobs),
               'max_child_RSS_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'result_sha256': digest(finals[0]), 'inventory': inventories[0]}
    (work/'RECEIPT.json').write_text(json.dumps(receipt, sort_keys=True, indent=2)+'\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'inventory'}, sort_keys=True), flush=True)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    reproduce(args.work)
