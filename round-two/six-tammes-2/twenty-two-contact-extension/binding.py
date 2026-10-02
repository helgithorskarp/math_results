"""Bind unchanged historical arithmetic modules to pinned public source.

Actual author: six-tammes-2, researcher. Runtime copies and generated states
belong in a caller-selected scratch directory, never in this source packet.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
NATIVE_THREADS = (
    'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
    'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS',
)
for name in NATIVE_THREADS:
    os.environ[name] = '1'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def manifest():
    return json.loads((HERE / 'INPUTS.json').read_text())


def materialize(work):
    """Copy only named, byte-checked source files into the old path layout.

    These are small executable sources and the public frame proof required
    by its existing dependency loader. No witness table is an input.
    """
    work = Path(work).resolve()
    if work == REPOSITORY or work == HERE or HERE in work.parents:
        raise ValueError('select a separate scratch directory')
    runtime = work / 'binding'
    data = manifest()
    for item in data['source_files']:
        source = (HERE if item['origin'] == 'packet' else REPOSITORY) / item['source']
        payload = source.read_bytes()
        if sha(payload) != item['sha256']:
            raise ValueError('source pin mismatch: ' + item['source'])
        target = runtime / item['target']
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink():
            raise ValueError('runtime source may not be a symlink')
        if target.exists():
            if target.read_bytes() != payload:
                raise ValueError('existing runtime source differs: ' + str(target))
        else:
            target.write_bytes(payload)
    return runtime, data


def load(work):
    runtime, data = materialize(work)
    path = runtime / 'scratch/g22-cap-replay-delta-v2.py'
    spec = importlib.util.spec_from_file_location('g22_frozen_delta', path)
    delta = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(delta)
    # The historical loaders also pin the unchanged reader, model and
    # imported frame kernel. The manifest pins their full public inputs.
    return delta, runtime, data


def write_json(path, obj, compact=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, separators=(',', ':')) if compact else json.dumps(obj, indent=2)
    temporary = path.with_name(path.name + '.temporary')
    temporary.write_text(text + '\n')
    temporary.replace(path)


NODE_FIELDS = ('cell', 'remaining', 'proofs', 'bounded_inherited', 'bounded',
               'split', 'children', 'prune', 'complete')


def canonical(state):
    """Exclude timings, paths and search counters, retain every proof entry."""
    obj = dict(nodes=[{key: node[key] for key in NODE_FIELDS if key in node}
                      for node in state['nodes']], stack=state['stack'])
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()
