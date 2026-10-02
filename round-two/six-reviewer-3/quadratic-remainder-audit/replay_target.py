"""Late native validation replay with full source-byte gates and original per-child guards."""
import sys,json,subprocess,os,signal,time,resource
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from export_target import gate

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: replay_target.py IMMUTABLE_NATIVE_DIRECTORY OUTPUT_JSON')
    directory=Path(sys.argv[1]).resolve();gate(directory)
    original_validation=(directory/'VALIDATION.json').read_bytes()
    env=os.environ.copy()
    for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
    start=time.monotonic()
    child=subprocess.Popen([sys.executable,'-I','-B',str(directory/'validate.py')],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    try:
        try:stdout,stderr=child.communicate(timeout=100)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGTERM);child.communicate();raise RuntimeError('administrative native replay guard; no mathematical verdict')
        if child.returncode:raise RuntimeError('native validation failed: '+stderr[-2000:])
        data=json.loads((directory/'VALIDATION.json').read_text())
        if data.get('status')!='PASS' or data.get('positive_modes')!=2 or data.get('intended_external_fixture_rejections')!=18:raise ValueError('native full-record validation incomplete')
        summaries=[r['output'] for r in data['whole_runs'] if r.get('case')=='positive']
        if len(summaries)!=2 or summaries[0]!=summaries[1]:raise ValueError('whole native normal/O outputs differ')
        Path(sys.argv[2]).write_text(json.dumps(data,indent=2)+'\n')
        result={'native_summary':summaries[0],'all_native_external_fixture_rejections':18,'native_child_guard_seconds':45,'administrative_orchestration_guard_seconds':100,'serial_math_children':True,'native_threads':1,'scope':'unchanged1CPU2GiB','whole_replay_seconds':time.monotonic()-start,'peak_child_rss_kib':data['peak_child_rss_kib'],'source_bytes_checked_before_any_execution':True}
    finally:
        (directory/'VALIDATION.json').write_bytes(original_validation)
        gate(directory)
    print(json.dumps(result,sort_keys=True))
