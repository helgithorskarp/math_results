"""Literal full-formula comparison with the pinned h3887 q8 tasks."""
import argparse
import hashlib
from itertools import zip_longest
import json
from pathlib import Path
import sys
import time

import basis
import task_queue


def check_parents():
    root = basis.HERE.parent
    for p in json.loads((basis.HERE/'DEPENDENCIES.json').read_text())['parents']:
        d = root/p['directory']
        raw = (d/'SHA256SUMS').read_bytes()
        if hashlib.sha256(raw).hexdigest() != p['manifest_sha256'] or len(raw.splitlines()) != p['entries']:
            raise ValueError('Parent manifest identity')
        for line in raw.decode().splitlines():
            sha, name = line.split('  ', 1)
            if hashlib.sha256((d/name).read_bytes()).hexdigest() != sha:
                raise ValueError('Parent source changed: '+name)
    sys.path.insert(0, str(root/'ramsey_r55_maximal_block_order'))
    import ordered
    # Its own loader verifies the complete h3835/h3873/h3881 source manifests.
    ordered.dependencies.load()
    return ordered


def check(cache, directory):
    ordered = check_parents()
    words = task_queue.read_words(Path(directory)/'cores.u64le')
    rows = []
    for r, c in [(5, 0), (6, 12345), (7, 273178), (8, 546355)]:
        start = time.monotonic()
        name = f'bo1-q8-r{r}-c{c:06d}'
        task, plan, meta = ordered.build(name, cache, False)
        wanted = ordered.clauses(task, plan, meta)
        actual = (p for cl in basis.read_cnf(Path(directory)/f'q8-r{r}.cnf')
                  if (p := basis.project(cl, words[c])) is not None)
        digest = hashlib.sha256(f"p cnf {meta['variables']} {meta['clauses']}\n".encode())
        count = 0
        for lhs, rhs in zip_longest(wanted, actual):
            if lhs != rhs:
                raise ValueError(f'Physical projection mismatch {name} clause {count+1}')
            digest.update((' '.join(map(str, lhs))+' 0\n').encode())
            count += 1
        if count != meta['clauses']:
            raise ValueError('Parent projection length')
        rows.append(dict(task=name, variables=meta['variables'], clauses=count,
                         complete_parent_cnf_sha256=digest.hexdigest(), seconds=time.monotonic()-start))
    return dict(status='VERIFIED', full_literal_task_comparisons=rows,
                scope='Four representative full CNFs; universal proof plus all-base support audit covers every core')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('catalog_directory'); p.add_argument('run_directory')
    a = p.parse_args(); print(json.dumps(check(a.catalog_directory, a.run_directory), indent=2))
