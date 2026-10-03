"""Once-only complete pre-native workflow for genuinely coupled six-run inputs."""
import json
from pathlib import Path
import sys
import time
from symbolic6_common import ROOT,pins,require,sha,write
from symbolic6_stage import stage

PYTHON=ROOT/'solver-env/bin/python'
WORK=ROOT/'symbolic6-models'


def main():
    pins();attempt=ROOT/'symbolic6-job-attempt.json'
    require(not attempt.exists(),'once-only symbolic job is frozen')
    record=dict(agent='six-vdw-2',role='researcher',status='REGISTERED_ONCE_BEFORE_MODEL_GENERATION',
                started=time.time(),source_manifest_sha256=sha(ROOT/'symbolic6-source-pins.json'),mathematical_exclusion=False)
    write(attempt,record)
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            stage('phase-'+mode,[PYTHON,*flags,ROOT/'phase_cover.py',ROOT/('phase-'+mode+'.json')],55)
        require((ROOT/'phase-normal.json').read_bytes()==(ROOT/'phase-optimized.json').read_bytes(),'whole phase cover normal/O differs')
        stage('generate',[PYTHON,ROOT/'symbolic6_generate.py','--work',WORK],55)
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            stage('audit-'+mode,[PYTHON,*flags,ROOT/'symbolic6_audit.py','--work',WORK],55)
            stage('guards-'+mode,[PYTHON,*flags,ROOT/'symbolic6_guards.py','--work',WORK,'--output',ROOT/('symbolic6-guards-'+mode)],55)
        audit_paths=[WORK/('audit-'+mode+'.json') for mode in ('normal','optimized')]
        guard_paths=[ROOT/('symbolic6-guards-'+mode)/'result.json' for mode in ('normal','optimized')]
        require(audit_paths[0].read_bytes()==audit_paths[1].read_bytes() and guard_paths[0].read_bytes()==guard_paths[1].read_bytes(),
                'entire paired pre-native receipt bytes differ')
        write(WORK/'pre-native-complete.json',dict(agent='six-vdw-2',role='researcher',
            status='WHOLE_PHYSICAL_SIGNED_AUXILIARY_METADATA_CONTROLS_NORMAL_O_COMPLETE',
            source_manifest_sha256=sha(ROOT/'symbolic6-source-pins.json'),audit_sha256=sha(audit_paths[0]),
            guards_sha256=sha(guard_paths[0]),mathematical_exclusion=False))
        from symbolic6_propose import main as propose
        propose()
        # The controller runs here; only the serial intensive children are bounded stages.
        result=json.loads((ROOT/'symbolic6-result.json').read_text())
        record.update(status=result['status'],exact_negative_models=result['exact_negative_models'],
                      mathematical_exclusion=result['longest_minority_run6_exclusion'])
    except BaseException as error:
        record.update(status='FIRST_INCOMPLETE_STAGE_STOPPED_NO_NEW_EXCLUSION',failure=type(error).__name__)
        raise
    finally:
        record['finished']=time.time();write(attempt,record)
    print(json.dumps(record),flush=True)


if __name__=='__main__':main()
