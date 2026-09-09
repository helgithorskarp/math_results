"""Read the resulting queue; prove its coverage by independent core bitsets."""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def audit(directory, output):
    d,out=Path(directory),Path(output)
    raw=(d/'cores.u64le').read_bytes()
    if hashlib.sha256(raw).hexdigest() != 'ca6d60b50d01ae460941cffa4e843a81fcbe33a8e5d37ea6e1fe568e2f5c95cc':
        raise ValueError('Independent original catalog identity')
    n=546356
    if raw[:12] != b'Q8CORE1\n'+struct.pack('<I',n) or len(raw)!=12+8*n:
        raise ValueError('Independent original framing')
    words=[x[0] for x in struct.iter_unpack('<Q',raw[12:])]
    old=[json.loads(s) for s in (d/'cohort-jobs.jsonl').read_text().splitlines()]
    active=[json.loads(s) for s in (out/'active-cohort-jobs.jsonl').read_text().splitlines()]
    closed=[json.loads(s) for s in (out/'closed-physical-branches.jsonl').read_text().splitlines()]
    if len(old)!=956 or len(active)!=956 or len(closed)!=239:
        raise ValueError('Independent whole queue sizes')
    for i,(before,after) in enumerate(zip(old,active)):
        expected=dict(r=before['r'],core_assumptions=before['assumptions'],edge_cube=[119] if before['r']==8 else [])
        if before!=after['parent'] or after['status']!='UNKNOWN' or after['worker_job']!=expected:
            raise ValueError('Original scope/status changed')
        if i<717 and set(after)!={'parent','worker_job','status'}:
            raise ValueError('Unchanged q8,r5..7 jobs altered')
    # Build physical core columns and intersect each guard. This does not
    # traverse the producer's decision tree or invoke its membership auditor.
    columns=[bytearray((n+7)//8) for _ in range(55)]
    for c,w in enumerate(words):
        while w:
            b=(w&-w).bit_length()-1;columns[b][c//8]|=1<<(c%8);w&=w-1
    columns=[int.from_bytes(c,'little') for c in columns]
    universe=(1<<n)-1;covered=0
    for k,(row,parent) in enumerate(zip(closed,old[717:])):
        receipt=row['receipt'];job=receipt['job']
        if (row['cohort']!=k or row['original_tasks']!=parent['original_tasks']
            or row['base_sha256']!='ba96586572a831dbc6a12329515cad3d11779a1ea01b3242e981a2c1f539c2d1'
            or job!=dict(r=8,core_assumptions=parent['assumptions'],edge_cube=[-119])
            or receipt['status']!='CERTIFIED_UNSAT_USING_IMPORTED_RAMSEY_THEOREM'
            or receipt['materialized'] is not False or receipt['original_task_status']!='UNKNOWN'):
            raise ValueError('Independent physical child disposition')
        members=universe
        for lit in parent['assumptions']:
            col=columns[abs(lit)-802]
            members &= col if lit>0 else universe^col
        if members.bit_count()!=row['original_tasks'] or members&covered:
            raise ValueError('Independent nonempty/disjoint cohort membership')
        covered |= members
    if covered!=universe:
        raise ValueError('Incomplete original registry cover')
    stream=(out/'q8r8-dispatch.records').read_bytes()
    if stream[:12]!=b'Q8UNIT1\n'+struct.pack('<I',n) or len(stream)!=12+14*n:
        raise ValueError('Independent actual dispatch framing')
    for c,(idx,w,unit) in enumerate(struct.iter_unpack('<IQh',stream[12:])):
        if (idx,w,unit)!=(c,words[c],119):
            raise ValueError('Independent actual dispatched record')
    for k in (0,238):
        actual=(out/f'positive-{k:03d}.cnf').read_bytes()
        base=(d/'q8-r8.cnf').read_bytes().split(b'\n',1)[1]
        a=old[717+k]['assumptions']+[119]
        wanted=f'p cnf 946 {1502521+len(a)}\n'.encode()+base+''.join(f'{x} 0\n' for x in a).encode()
        if actual!=wanted or hashlib.sha256(actual).hexdigest()!=active[717+k]['input_sha256']:
            raise ValueError('Independent retained full input')
    if list(out.glob('negative-*.cnf')):
        raise ValueError('A closed child reached materialization')
    return dict(status='VERIFIED', original_q8r8_ids_covered=n,
                independently_disjoint_nonempty_negative_cohorts=239,
                active_positive_cohorts=239, unchanged_cohorts=717,
                complete_original_dispatch_records_checked=n,
                retained_full_worker_inputs_checked=2, original_task_exclusions=0,
                all_original_statuses='UNKNOWN')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('output')
    a=p.parse_args();print(json.dumps(audit(a.directory,a.output),indent=2))
