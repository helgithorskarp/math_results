"""Check every physical tail clause against the pinned actual h3873 emitter."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import audit
import encode

HERE = Path(__file__).resolve().parent

def run(parent_root, cache):
    root = Path(parent_root).resolve()
    specs = json.loads((HERE / 'INPUTS.json').read_text())['parents']
    for row in specs:
        directory = root / row['directory']
        raw = (directory / 'SHA256SUMS').read_bytes()
        audit.require(hashlib.sha256(raw).hexdigest() == row['manifest_sha256'], 'Parent manifest')
        for line in raw.decode().splitlines():
            sha, name = line.split('  ', 1)
            audit.require(hashlib.sha256((directory / name).read_bytes()).hexdigest() == sha, 'Parent source changed')
    path = root / 'ramsey_r55_global_maximal_packing'
    sys.path.insert(0, str(path))
    spec = importlib.util.spec_from_file_location('_q7r5_parent_family', path / 'family.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    audit.require(Path(module.catalog.__file__).resolve().parent == path, 'Wrong parent catalog module')
    lines = encode.catalog(Path(cache) / 'r44_15.g6')
    embedding = list(range(28, 43)) + list(range(20, 28))
    count = 0
    for i, line in enumerate(lines):
        task = module.Task(f'mp1-q7-r5-c{i:06d}', cache)
        core = encode.decode(line)
        for (u, v), color in encode.fixed(core).items():
            audit.require(task.fixed[tuple(sorted((embedding[u], embedding[v])))] == color, 'Fixed-edge embedding')
        for clause in encode.physical_clauses(core):
            color = int(clause[0] < 0)
            vertices = set()
            physical = []
            for literal in clause:
                u, v = encode.FREE[abs(literal) - 1]
                vertices.update((embedding[u], embedding[v]))
                physical.append(task.variables[tuple(sorted((embedding[u], embedding[v])))] * (1 if literal > 0 else -1))
            audit.require(len(vertices) == (4 if color else 5) and min(vertices) >= 20, 'Forbidden-set embedding')
            # The parent adds every blue-five clause globally, and every red-four
            # clause on 4r..42. Here 4r=20, exactly the embedded residual.
            original = task.forbid(sorted(vertices), color)
            audit.require(original is not None and sorted(original) == sorted(physical), 'Parent physical clause mismatch')
            count += 1
    return {'status': 'VERIFIED_ALL_640_PHYSICAL_TASK_EMBEDDINGS', 'tasks': 640,
            'mapped_source_clauses': count, 'physical_vertices': list(range(20, 43)),
            'tail_ordering_appended_to_parent': False}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--parent-root', required=True)
    p.add_argument('--cache', required=True)
    a = p.parse_args()
    print(json.dumps(run(a.parent_root, a.cache), sort_keys=True))
