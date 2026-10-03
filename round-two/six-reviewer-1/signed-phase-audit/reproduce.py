"""Bounded serial independent replay; optional LATE data-only correspondence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from independent import need, canon, digest

BASE=Path(__file__).resolve().parent
NATIVE=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
        'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--native-record',type=Path)
    args=ap.parse_args()
    seal=json.loads((BASE/'PRIMARY_SEAL.json').read_text())
    need(len(seal['files'])==4,'primary file census')
    need(all(hashlib.sha256((BASE/n).read_bytes()).hexdigest()==v for n,v in seal['files'].items()),
         'all four primary files byte-identical')
    env=os.environ.copy()
    env.update({n:'1'for n in NATIVE})
    children=0
    def run(base,name,opt=False,extra=(),success=True):
        nonlocal children
        cmd=[sys.executable,'-B']+(['-O']if opt else[])+[str(base/name),*extra]
        p=subprocess.run(cmd,cwd=base,env=env,capture_output=True,timeout=45)
        children+=1
        need((p.returncode==0)==success,'unexpected mathematical child result '+p.stderr.decode(errors='replace'))
        return p.stdout
    streams={}
    for opt in (False,True):
        for name in ('independent.py','primary_controls.py'):
            data=run(BASE,name,opt)
            if name in streams:
                need(data==streams[name],'ENTIRE normal/optimized records')
            streams[name]=data
        for damage in ('general-a','majorant','phase-eight','phase-four','path-rms','endpoint'):
            run(BASE,'independent.py',opt,('--damage',damage),False)
    with tempfile.TemporaryDirectory(prefix='signed-phase-primary-')as temp:
        cold=Path(temp)
        for name in ('independent.py','primary_controls.py','PROOF.md'):
            shutil.copyfile(BASE/name,cold/name)
        for opt in (False,True):
            for name in streams:
                need(run(cold,name,opt)==streams[name],'ENTIRE cold source-only record')
    summary=json.loads(run(BASE,'independent.py',extra=('--summary',)))
    summary['gaussian_controls']={'count':6,'balanced_closed_endpoints':2,
        'whole_record_sha256':hashlib.sha256(streams['primary_controls.py']).hexdigest(),
        'bytes':len(streams['primary_controls.py'])}
    expected=json.loads((BASE/'expected.json').read_text())
    need(canon(summary)==canon(expected),'whole canonical expected summary')
    late=None
    if args.native_record:
        # Absolute path survives the child's cwd and is never treated as executable code.
        record=args.native_record.resolve()
        normal=run(BASE,'compare_native.py',extra=(str(record),))
        need(run(BASE,'compare_native.py',True,(str(record),))==normal,'whole late normal/O comparison')
        late=json.loads(normal)
    print(canon({'agent':'six-reviewer-1','role':'independent mathematical reviewer',
        'all_primary_seals_unchanged':True,'serial_children':children,'child_guard_seconds':45,
        'native_threads':1,'primary_whole_record_sha256':summary['whole_record_sha256'],
        'primary_coefficients':{'general_a':45,'mixed':36,'phase':3025},
        'all_four_endpoint_gaps_positive':True,'source_only_normal_O_complete_match':True,
        'mathematical_damages_rejected_per_mode':6,'late_native_correspondence':late,
        'scope':'Ordinary unformalized universal proof and finite corroboration; no wider actual window or global first-power resolution'}))


if __name__=='__main__':
    main()
