"""Serial source-only reproduction with unchanged 55-second child guards."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
           BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
           PYTHONHASHSEED='0')


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def operations_allow():
    name = os.environ.get('RESEARCH_OPERATIONS_STATE')
    if not name:
        return
    root = Path(name)
    for directory in (root,root/'monitor'):
        if any((directory/marker).exists() for marker in ('PAUSED','PAUSED.json')):
            raise ValueError('Operations pause: no new computation')
        handover = directory/'HANDOVER.json'
        if handover.exists() and json.loads(handover.read_text()).get('phase') != 'completed':
            raise ValueError('Incomplete handover: no new computation')
    health = json.loads((root/'monitor/health.json').read_text())
    if health['campaign_state'] != 'running' or health['credit_budget']['status'] != 'authorized':
        raise ValueError('Operations state/budget barrier: no new computation')


def main():
    operations_allow()
    if WORK.exists() and any(WORK.iterdir()):
        raise ValueError('Cold reproduction needs an absent or empty work directory; use a fresh source copy')
    WORK.mkdir(exist_ok=True)
    start = time.monotonic();stages=[];producer=[]
    for script,optimized in [('generate.py',False),('verify.py',False),
                             ('generate.py',True),('verify.py',True),('check_controls.py',False)]:
        operations_allow()
        cmd=[sys.executable]+(['-O'] if optimized else [])+[str(ROOT/script)]
        before=time.monotonic()
        result=subprocess.run(cmd,env=ENV,capture_output=True,text=True,timeout=55)
        (WORK/(script+('-O' if optimized else '')+'.log')).write_text(result.stdout+result.stderr)
        if result.returncode:
            raise ValueError('Incomplete child is no mathematical negative: '+script+'\n'+result.stderr)
        summary=json.loads(result.stdout)
        if script == 'generate.py':
            p=json.loads((WORK/'proposal.json').read_text())
            if digest(p['finite']) != p['finite_sha256']:
                raise ValueError('Producer complete binding differs')
            producer.append(p['finite'])
        stages.append({'script':script,'optimized':optimized,'returncode':result.returncode,
                       'seconds':time.monotonic()-before,'finite_sha256':summary['finite_sha256']})
    checked=json.loads((WORK/'checked.json').read_text());other=json.loads((WORK/'checked-O.json').read_text())
    controls=json.loads((WORK/'controls.json').read_text());proposal=json.loads((WORK/'proposal.json').read_text())
    if producer[0] != producer[1] or checked['finite'] != other['finite']:
        raise ValueError('Entire normal/optimized mathematical records differ')
    if (WORK/'samples.json').read_bytes() != (WORK/'samples-O.json').read_bytes():
        raise ValueError('Entire normal/optimized original sample records differ')
    finite={'producer_finite_sha256':proposal['finite_sha256'],'scalar_finite_sha256':checked['finite_sha256'],
            'controls_finite_sha256':controls['finite_sha256'],
            'entire_producer_scalar_normal_O_records_match':True,'cold_source_only_complete':True,
            'all16_semantic_rejections_pass':True,'six_routes_each_three_fixed_and_at_least_four_head_tail_cuts':True,
            'actual_head_moves_checked':checked['finite']['actual_moved_head_sample_count'],
            'arbitrary_preparation_length_and_suffix_depth_allowed':True,
            'whole_route_or_global_size44_exclusion_claimed':False,
            'external_person_review_claimed':False,'formalized':False}
    result={'agent':'six-sorting-1','role':'researcher','status':'COMPLETE_SCOPED_SIX_ROUTE_AUTHOR_CERTIFICATE',
            'finite':finite,'finite_sha256':digest(finite),'stages':stages,
            'seconds':time.monotonic()-start,'max_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'python_version':sys.version}
    (WORK/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
