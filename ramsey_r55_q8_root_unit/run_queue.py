"""Execute the complete q8,r8 routing gate. No target SAT call is made."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import struct
import sys
import time

import bridge
sys.path.insert(0, str(bridge.PARENT))
import cohorts
import task_queue

RECORD = struct.Struct('<IQh')


def execute(directory, cert, output):
    start = time.monotonic()
    d, out = Path(directory), Path(output)
    out.mkdir(exist_ok=False)
    expected = json.loads((bridge.PARENT/'EXPECTED.json').read_text())
    for name, digest in [('cores.u64le', expected['queue']['files']['cores.u64le']['sha256']),
                         ('cohorts.json', expected['cohorts']['cohort_sha256'])]:
        if bridge.sha(d/name) != digest:
            raise ValueError('Actual parent queue identity')
    words = task_queue.read_words(d/'cores.u64le')
    tree = json.loads((d/'cohorts.json').read_text())
    membership = cohorts.audit(words, tree)
    if membership['membership_digest'] != expected['cohorts']['membership_digest']:
        raise ValueError('Actual entire catalog partition')
    old = [json.loads(s) for s in (d/'cohort-jobs.jsonl').read_text().splitlines()]
    wanted = [cohorts.job(tree,r,k) for r in range(5,9) for k in range(len(tree['leaves']))]
    if old != wanted:
        raise ValueError('Actual preexisting cohort queue differs')
    router = bridge.Dispatcher(d, cert)
    base = (d/'q8-r8.cnf').read_bytes()
    _, body = base.split(b'\n',1)
    materializations, untouched = [], 0
    with (out/'active-cohort-jobs.jsonl').open('x') as active, (out/'closed-physical-branches.jsonl').open('x') as closed:
        for row in old:
            if row['r'] != 8:
                active.write(json.dumps(dict(parent=row, worker_job=dict(r=row['r'],
                    core_assumptions=row['assumptions'], edge_cube=[]), status='UNKNOWN'),separators=(',',':'))+'\n')
                untouched += 1
                continue
            leaf = row['cohort']
            job = dict(r=8, core_assumptions=row['assumptions'], edge_cube=[-119])
            forbidden_output = out/f'negative-{leaf:03d}.cnf'
            receipt = router.dispatch(job, forbidden_output)
            if forbidden_output.exists() or receipt['materialized']:
                raise ValueError('Closed branch reached materializer')
            closed.write(json.dumps(dict(cohort=leaf, original_tasks=row['original_tasks'],
                base_sha256=bridge.BASE_SHA, receipt=receipt),separators=(',',':'))+'\n')
            job = dict(r=8, core_assumptions=row['assumptions'], edge_cube=[119])
            path = out/f'positive-{leaf:03d}.cnf'
            receipt = router.dispatch(job, path)
            raw = path.read_bytes()
            assumptions = row['assumptions']+[119]
            header = f'p cnf 946 {1502521+len(assumptions)}\n'.encode()
            wanted_raw = header+body+''.join(f'{x} 0\n' for x in assumptions).encode()
            if raw != wanted_raw or hashlib.sha256(raw).hexdigest() != receipt['worker_sha256']:
                raise ValueError('Actual complete physical materialization mismatch')
            materializations.append(dict(cohort=leaf, core_tasks=row['original_tasks'],
                bytes=len(raw), sha256=receipt['worker_sha256'], clauses=receipt['clauses']))
            active.write(json.dumps(dict(parent=row, worker_job=job, status='UNKNOWN',
                input_sha256=receipt['worker_sha256'], unit_certificate='branch-certificate.json'),separators=(',',':'))+'\n')
            (out/f'positive-{leaf:03d}.job.json').write_text(json.dumps(job,separators=(',',':'))+'\n')
            # Keep the endpoint inputs. All other exact bodies are regenerable;
            # their literal bytes, not merely headers, have just been compared.
            if leaf not in (0, len(tree['leaves'])-1):
                path.unlink()
            if leaf % 40 == 0 or leaf == len(tree['leaves'])-1:
                print(json.dumps(dict(completed_cohorts=leaf+1, seconds=time.monotonic()-start)),flush=True)
    stream = out/'q8r8-dispatch.records'
    ids = hashlib.sha256()
    with stream.open('xb') as f:
        f.write(b'Q8UNIT1\n'+struct.pack('<I', len(words)))
        for c, word in enumerate(words):
            f.write(RECORD.pack(c, word, 119))
            ids.update(f'bo1-q8-r8-c{c:06d}\n'.encode())
    # Separate complete stream consumer: every old identity and every physical
    # assumption must survive the dispatched stream, in exact original order.
    raw = stream.read_bytes()
    if raw[:12] != b'Q8UNIT1\n'+struct.pack('<I',len(words)) or len(raw) != 12+14*len(words):
        raise ValueError('Entire original-task dispatch framing')
    for c, (index,word,unit) in enumerate(RECORD.iter_unpack(raw[12:])):
        if index != c or word != words[c] or unit != 119:
            raise ValueError('Entire original-task dispatch identity')
    if router.closed != 239 or router.materialized != 239 or untouched != 717:
        raise ValueError('Complete cohort routing totals')
    result = dict(status='COMPLETE_NEGATIVE_BRANCH_AND_QUEUE_GATE',
        original_q8_tasks=4*len(words), affected_original_q8r8_tasks=len(words),
        active_cohort_jobs=956, constrained_positive_workers=239,
        certified_negative_physical_workers=239, unchanged_other_q8_cohorts=717,
        actual_positive_materializations=len(materializations),
        materialized_bytes=sum(x['bytes'] for x in materializations),
        negative_materializations=0, original_task_exclusions=0, candidates=0,
        all_original_statuses='UNKNOWN', target_solver_calls=0,
        affected_ids_sha256=ids.hexdigest(), original_dispatch_stream_sha256=bridge.sha(stream),
        core_membership_digest=membership['membership_digest'],
        original_task_stream_bytes=stream.stat().st_size,
        seconds=time.monotonic()-start, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        materializations=materializations)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    return {k:v for k,v in result.items() if k != 'materializations'}


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('certificate');p.add_argument('output')
    a=p.parse_args()
    print(json.dumps(execute(a.directory,json.loads(Path(a.certificate).read_text()),a.output),indent=2))
