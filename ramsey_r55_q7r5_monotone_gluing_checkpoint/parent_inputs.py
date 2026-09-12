"""Reconstruct every original input identity by literal core specialization.

The native projector emits the actual DIMACS bytes, chunk framed for hashing.
No solver is called and no original task is decided by this program.
"""

if not __debug__:
    raise RuntimeError('Run this research program without -O or -OO; its exact checks require assertions.')
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import struct
import subprocess
import sys
import time


def run(repo, cache, run_dir, projector):
    repo, cache, run_dir = map(Path, (repo, cache, run_dir))
    meta = json.loads((run_dir / 'INPUT.json').read_text())
    result_path = run_dir / 'ORIGINAL_INPUTS.json'
    if result_path.exists():
        raise ValueError('Refusing to overwrite a parent manifest')
    directory = repo / 'ramsey_r55_maximal_block_order'
    manifest = (directory / 'SHA256SUMS').read_bytes()
    if hashlib.sha256(manifest).hexdigest() != '452b38de607c4bfecd9f6addbf363b47b1400c8c63eaee954d68466648f534e6':
        raise ValueError('Changed ordered-parent manifest')
    for line in manifest.decode().splitlines():
        sha, name = line.split('  ', 1)
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != sha:
            raise ValueError('Changed ordered-parent source: ' + name)
    sys.path.insert(0, str(directory.resolve()))
    ordered = importlib.import_module('ordered')
    if Path(ordered.__file__).resolve().parent != directory.resolve():
        raise ValueError('Wrong ordered module')
    import model
    indices, cores = model.inputs(repo, cache)
    if meta['original_ids'] != [f'bo1-q7-r5-c{k:06d}' for k in indices]:
        raise ValueError('Wrong original family')
    rows = []
    for k in indices:
        name = f'bo1-q7-r5-c{k:06d}'
        task, plan, dims = ordered.build(name, cache, False)
        assert plan is None and dims['variables'] == 817
        assert all(task.fixed[e] == value for e, value in cores[k].items())
        bits = ''.join(str(task.fixed[i, j]) for i in range(28, 43) for j in range(i + 1, 43))
        rows.append(f"{k}\t{bits}\t{dims['clauses']}\n")
    core_file = run_dir / 'cores.tsv'
    with core_file.open('x') as f:
        f.writelines(rows)
    base_count = sum(meta['groups'][k] for k in ['constant', 'root', 'red5', 'blue5', 'red4', 'order'])
    started = time.monotonic()
    proc = subprocess.Popen([str(projector), str(run_dir / 'input.cnf'), str(base_count), str(core_file)], stdout=subprocess.PIPE)
    records = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        core, count = map(int, line.split())
        digest, size = hashlib.sha256(), 0
        while True:
            header = proc.stdout.read(4)
            if len(header) != 4:
                raise ValueError('Truncated native stream header')
            length = struct.unpack('<I', header)[0]
            if not length:
                break
            chunk = proc.stdout.read(length)
            if len(chunk) != length:
                raise ValueError('Truncated native stream data')
            digest.update(chunk)
            size += length
        records.append({'task': f'bo1-q7-r5-c{core:06d}', 'variables': 817, 'clauses': count, 'bytes': size, 'sha256': digest.hexdigest()})
        print(records[-1], flush=True)
    if proc.wait() != 0 or [r['task'] for r in records] != meta['original_ids']:
        raise ValueError('Incomplete exact original stream')
    expected = json.loads((Path(__file__).resolve().parent / 'ORIGINAL_INPUTS.json').read_text())
    if records != expected['records']:
        raise ValueError('Original bytes differ from recorded inputs')
    result = {'status': 'ALL_122_EXACT_ORIGINAL_INPUT_IDENTITIES', 'records': records, 'seconds': time.monotonic() - started, 'base_clauses': base_count, 'core4_matches_pinned_physical_parent': True}
    with result_path.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--cache', required=True)
    p.add_argument('--run', required=True)
    p.add_argument('--projector', required=True)
    args = p.parse_args()
    result = run(args.repo, args.cache, args.run, args.projector)
    print(result['status'])
