"""Exercise a real cohort input and the complete branch-to-queue protocol."""
import argparse
import hashlib
import json
from pathlib import Path

import basis
import certificate
import cohorts
import task_queue
import worker


def check(directory):
    d = Path(directory)
    tree = json.loads((d/'cohorts.json').read_text())
    row = cohorts.job(tree, 5, 0)
    job = dict(r=5, core_assumptions=row['assumptions'], edge_cube=[])
    path = d/'cohort-r5-000.worker.cnf'
    meta = worker.materialize(d, job, path)
    # Independent byte contract: identical body followed by precisely these units.
    base = (d/'q8-r5.cnf').read_bytes()
    header, body = base.split(b'\n', 1)
    _, _, nv, nc = header.decode().split()
    expected = f'p cnf {nv} {int(nc)+len(job["core_assumptions"])}\n'.encode()+body
    expected += ''.join(str(x)+' 0\n' for x in job['core_assumptions']).encode()
    if path.read_bytes() != expected or hashlib.sha256(expected).hexdigest() != meta['worker_sha256']:
        raise ValueError('Full physical worker input differs from its contract')
    words = task_queue.read_words(d/'cores.u64le')
    members = task_queue.matching(words, job['core_assumptions'])
    if len(members) != row['original_tasks']:
        raise ValueError('Worker assumptions do not identify the whole cohort')
    try:
        worker.materialize(d, job, path)
    except FileExistsError:
        pass
    else:
        raise ValueError('Existing physical input was overwritten')
    (d/'cohort-r5-000.job.json').write_text(json.dumps(job, indent=2)+'\n')
    # Test certificates use a red K4 in the variable core. The actual catalog
    # has no such core, so this must close zero real tasks throughout.
    control = json.loads((d/'empty-cover-control-r5.json').read_text())
    a = control['assumptions']
    positive = worker.wrap(dict(r=5, core_assumptions=a, edge_cube=[2]), control['proof'])
    negative = worker.wrap(dict(r=5, core_assumptions=a, edge_cube=[-2]), control['proof'])
    try:
        worker.as_cover(positive)
    except ValueError:
        pass
    else:
        raise ValueError('A single physical branch closed its parent')
    merged = worker.join(d, positive, negative)
    cover = worker.as_cover(merged)
    receipt = certificate.verify_cover(d, cover)
    if receipt['matching_tasks'] != 0 or receipt['status'] != 'VERIFIED_EMPTY_COVER':
        raise ValueError('Branch-combination test changed the real registry')
    (d/'joined-empty-cover-control.json').write_text(json.dumps(cover, indent=2)+'\n')
    result = task_queue.request('bo1-q8-r5-c000000', d, d/'joined-empty-cover-control.json')
    if result['status'] != 'UNKNOWN':
        raise ValueError('Invalid task status after branch join')
    return dict(real_cohort_input=meta, cohort_members=len(members), duplicate_write_refused=True,
                full_physical_branch_pair_joined=True, single_branch_parent_closure_refused=True,
                joined_cover=receipt, final_real_task_status=result['status'], target_solver_calls=0,
                task_exclusions=0, physical_candidates=0)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('directory'); a = p.parse_args()
    print(json.dumps(check(a.directory), indent=2))
