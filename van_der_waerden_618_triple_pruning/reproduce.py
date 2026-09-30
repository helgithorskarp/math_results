"""Sequential, bounded reproduction with an independent definition-level AP check."""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

from check_coloring import cyclic_report, interval_report
from triple_pruning import compact_evidence

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--builddir',type=Path,default=ROOT/'build')
    args = parser.parse_args()
    build = args.builddir.resolve()
    build.mkdir(parents=True,exist_ok=True)
    env = dict(os.environ)
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:
        env[key] = '1'
    expected = json.loads((ROOT/'expected.json').read_text())
    ap_expected = json.loads((ROOT/'ap_expected.json').read_text())
    summaries = {}
    start = time.monotonic()
    for name in ['preferred584','gate585']:
        path = build/(name+'.json')
        command = [sys.executable,str(ROOT/'triple_pruning.py'),'--case',name,
                   '--output',str(path),'--expected',str(ROOT/'expected.json'),
                   '--seconds','30']
        child = subprocess.run(command,env=env,capture_output=True,text=True,timeout=45)
        if child.returncode:
            raise RuntimeError('Incomplete or failed exact check; no exclusion. '+child.stderr)
        document = json.loads(path.read_text())
        assert compact_evidence(document) == expected[name]
        halfword = list(map(int,path.with_suffix('.bits').read_text().strip()))
        assert len(halfword)==309
        period = halfword+[1-v for v in halfword]
        cyclic = cyclic_report(period)
        integer = interval_report([period[t%618] for t in range(3704)])
        actual_ap = {'cyclic':cyclic,'integer':integer}
        assert actual_ap == ap_expected[name]
        assert cyclic['monochromatic_cyclic_pairs']==4*document['results']['initial_long_cost']
        assert not integer['verified']
        summaries[name] = {'bound_and_residual_checked':True,
                           'integer_monochromatic_APs':integer['monochromatic_interval_progressions'],
                           'cyclic_monochromatic_pairs':cyclic['monochromatic_cyclic_pairs'],
                           'native_summary':json.loads(child.stdout)}
        print(json.dumps({'case':name,**summaries[name]}),flush=True)
    partial = build/'incomplete.json'
    assert not partial.exists() and not partial.with_suffix('.bits').exists()
    child = subprocess.run([sys.executable,str(ROOT/'triple_pruning.py'),'--case','preferred584',
                            '--output',str(partial),'--seconds','0.000000000001'],
                           env=env,capture_output=True,text=True,timeout=45)
    assert child.returncode != 0 and 'Incomplete computation' in child.stderr
    assert not partial.exists() and not partial.with_suffix('.bits').exists()
    summary = {'agent':'six-vdw-1','role':'researcher','status':'VERIFIED_TRIPLE_PRUNING_APPLICATIONS',
               'cases':summaries,'fail_closed_deadline_control':True,'threads':1,
               'length3704_witness':False,'no_template_family_exclusion':True,
               'seconds':time.monotonic()-start,
               'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (build/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='cases'}))


if __name__=='__main__':
    main()
