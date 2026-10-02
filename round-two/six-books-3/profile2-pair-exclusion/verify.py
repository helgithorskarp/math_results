"""Offline serial regeneration and independent replay of the complete profile.

Generated certificates, full records and child receipts stay in a private
work directory. Each producer/checker has its own unchanged2M/40s internal
guard and a45s child timeout. A timeout or any incomplete case is a failure
to establish the full profile, never a mathematical nonexistence premise.
"""
import argparse
import datetime
import hashlib
import json
import os
import resource
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def require(ok,message):
    if not ok:
        raise ValueError(message)


def stable(v):
    if isinstance(v,dict):return {k:stable(x) for k,x in v.items() if k!='seconds'}
    if isinstance(v,list):return [stable(x) for x in v]
    return v


def canonical(v):
    return json.dumps(v,sort_keys=True,separators=(',',':')).encode()


def run(directory):
    directory.mkdir(parents=True,exist_ok=True)
    require(not any(directory.iterdir()),'Use an empty private work directory')
    expected=json.loads((ROOT/'EXPECTED.json').read_text())
    env=dict(os.environ)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
        env[name]='1'
    receipts=[]

    def child(label,command):
        started=time.monotonic()
        try:
            result=subprocess.run(command,capture_output=True,env=env,timeout=45)
        except subprocess.TimeoutExpired as error:
            (directory/(label+'.stdout')).write_bytes(error.stdout or b'')
            (directory/(label+'.stderr')).write_bytes(error.stderr or b'')
            raise ValueError('Child timeout; no full-profile verdict: '+label) from error
        (directory/(label+'.stdout')).write_bytes(result.stdout)
        (directory/(label+'.stderr')).write_bytes(result.stderr)
        receipt=dict(label=label,exit_code=result.returncode,
            seconds=time.monotonic()-started,guard_seconds=45,native_threads=1,
            mathematical_children=1,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            stdout_sha256=hashlib.sha256(result.stdout).hexdigest())
        (directory/(label+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
        receipts.append(receipt)
        require(result.returncode==0,'Child failed; no full-profile verdict: '+label)
        return result.stdout

    inventory=[]
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        inventory.append(json.loads(child('inventory-'+mode,
            [sys.executable]+flags+[str(ROOT/'compare_inventory.py')])))
    require(inventory[0]==inventory[1],'Whole distinct inventory records differ normal/O')
    require(inventory[0]==json.loads((ROOT/'INVENTORY.json').read_text()), 'Expected whole inventory differs')
    rows=[]
    for t in range(40):
        packet=directory/('certificate'+str(t)+'.json')
        child('produce'+str(t),[sys.executable,str(ROOT/'generate.py'),
                               '--template',str(t),'--out',str(packet)])
        proposal=json.loads(packet.read_text())
        require(proposal['pending'] is None and proposal['status'] in
            ('CANDIDATE_INITIAL_EMPTY_UNCHECKED','CANDIDATE_PAIR_DOMAIN_EMPTY_UNCHECKED'),
            'Producer incomplete; no full-profile verdict: '+str(t))
        records=[]
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            output=directory/('checked'+str(t)+'-'+mode+'.json')
            child('check'+str(t)+'-'+mode,[sys.executable]+flags+
                [str(ROOT/'check.py'),'--packet',str(packet),'--out',str(output)])
            records.append(json.loads(output.read_text()))
        r=records[0]
        require(stable(r)==stable(records[1]),'Entire normal/O checker records differ')
        require(r['pending'] is None and r['claim_template_excluded'],
                'Checker incomplete; no full-profile verdict: '+str(t))
        mathematical=stable(r);mathematical.pop('packet_sha256')
        encoded=canonical(mathematical)
        row={k:r[k] for k in ('template','checked_stars','work_units','initial_empty','empty_targets')}
        row.update(whole_mathematical_sha256=hashlib.sha256(encoded).hexdigest(),
            whole_mathematical_bytes=len(encoded),producer_work=proposal['work_units'])
        require(row==expected['cases'][t],'Whole mathematical expected record differs: '+str(t))
        rows.append(row)
        print(json.dumps(dict(template=t,checked=True,deletions=r['checked_stars'],
            empty=r['empty_targets'],whole_mathematical_sha256=row['whole_mathematical_sha256'])),flush=True)
    controls=[]
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        controls.append(json.loads(child('controls-'+mode,[sys.executable]+flags+
            [str(ROOT/'controls.py'),'--packet',str(directory/'certificate0.json'),
             '--initial-packet',str(directory/'certificate7.json')])))
    require(controls[0]==controls[1],'Entire semantic control records differ normal/O')
    require(controls[0]==json.loads((ROOT/'CONTROLS.json').read_text()), 'Expected whole controls differ')
    record=dict(agent='six-books-3',role='researcher',status='COMPLETE_PROFILE2_PAIR_EXCLUSION',
        counts=expected['counts'],coverage=40,initial_empty=[7],pair_deleted_cases=39,
        checked_deletions=sum(r['checked_stars'] for r in rows),
        literal_work_one_mode=sum(r['work_units'] for r in rows),
        producer_work=sum(r['producer_work'] for r in rows),
        whole_case_summary_sha256=hashlib.sha256(canonical(rows)).hexdigest(),
        whole_inventory=inventory[0],whole_controls=controls[0],
        maximum_child_rss_kib=max(r['peak_child_rss_kib'] for r in receipts),
        all_child_receipts=receipts,formalized=False,independent_review=False,
        source_inputs_self_contained=True,old_private_certificates_required=False,
        generated_evidence_directory=str(directory))
    (directory/'RESULTS.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in
        ('all_child_receipts','whole_inventory','whole_controls')},sort_keys=True),flush=True)
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work-dir',type=Path);a=p.parse_args()
    directory=a.work_dir or Path(tempfile.mkdtemp(prefix='books-profile2-'))
    run(directory)
