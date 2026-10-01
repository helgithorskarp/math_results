"""Frozen exact replay; optional bounded fresh generation and proof comparison."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import compact
import controls
import check_core
import check_probe
import prune_probe
import verify

HERE=Path(__file__).absolute().parent


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--fresh',action='store_true');a=p.parse_args()
    started=time.monotonic();work=a.work.absolute()
    verify.need(not(work==HERE or HERE in work.parents),'Generated work must stay outside source')
    work.mkdir(parents=True,exist_ok=True)
    actual=verify.all_cases();expected=json.loads((HERE/'expected.json').read_text())
    verify.need(actual==expected,'Full exact frozen results equal published expected results')
    tests=controls.run();fresh=[]
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    def invoke(cmd):subprocess.run(cmd,check=True,env=env,stdout=subprocess.DEVNULL)
    if a.fresh:
        manifest=json.loads((HERE/'manifest.json').read_text())
        for row in manifest['cases']:
            s=row['phase'];base=HERE/row['base'];frozen=HERE/row['proof']
            if row['kind']=='forcing_core':
                path=work/f'phase{s}-units.json';guide=work/f'phase{s}-units-guide.json'
                if not path.exists():invoke([sys.executable,str(HERE/'generate_units.py'),'--base',str(base),'--output',str(path),'--summary',str(guide)])
                proposed=compact.forcing_core(json.loads(path.read_text()));check_core.check(proposed)
            else:
                chosen=None
                for window in range(1,5):
                    path=work/f'phase{s}-probe-{window:02}.json';guide=path.with_name(path.stem+'-guide.json')
                    cmd=[sys.executable,str(HERE/'probe_units.py'),'--base',str(base),'--output',str(path),'--summary',str(guide)]
                    if window>1:
                        previous=work/f'phase{s}-probe-{window-1:02}.json'
                        prior=check_probe.check(base,json.loads(previous.read_text()))
                        verify.need(not prior['excluded'],'No proposal resumes a completed contradiction')
                        cmd.extend(['--resume',str(previous)])
                    if not path.exists():invoke(cmd)
                    trace=json.loads(path.read_text());checked=check_probe.check(base,trace)
                    if checked['excluded']:chosen=trace;break
                    if trace['next_cursor']>=7408:break
                verify.need(chosen is not None,'INCOMPLETE: bounded fresh search proves no exclusion; preserve work and inspect')
                pruned,unused=prune_probe.prune(base,chosen);check_probe.check(base,pruned);proposed=compact.encode(pruned)
            output=work/f'phase{s}-compact.json';output.write_text(json.dumps(proposed,sort_keys=True,separators=(',',':'))+'\n')
            result=verify.case(base,output,row['kind'])
            verify.need(result['proved_individual_floor']==198,'Every regenerated proof establishes the same bound')
            verify.need(output.read_bytes()==frozen.read_bytes(),'Fresh canonical proof differs; inspect before claiming identical reproduction')
            fresh.append({'phase':s,'proof_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'bytes_match':True})
    out={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_TEN_SINGLE_CLASS198_IMPLICATION_BOUNDS',
         'python':sys.version.split()[0],'frozen_results_match':True,'controls':tests,'fresh_cases':fresh,
         'fresh_all_ten_identical':len(fresh)==10,'seconds':time.monotonic()-started,
         'self_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'children_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'all_jobs_serial':True,'threads':1}
    (work/'reproduction.json').write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(out,sort_keys=True),flush=True)


if __name__=='__main__':main()
