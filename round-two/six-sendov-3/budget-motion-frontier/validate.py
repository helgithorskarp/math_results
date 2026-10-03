"""Bounded serial same-author validation, standard library only."""
from pathlib import Path
import argparse, copy, datetime, json, os, resource, shutil, subprocess, sys, tempfile, time

HERE=Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    parser.add_argument('--baseline-root',type=Path)
    args=parser.parse_args();start=time.monotonic();env=os.environ.copy()
    for name in THREADS:env[name]='1'
    rows=[];positive=[]
    def run(folder,optimized,extra,should_pass,description):
        command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(folder/'verify.py')]+extra
        t=time.monotonic()
        result=subprocess.run(command,cwd=folder,env=env,capture_output=True,text=True,timeout=45)
        if (result.returncode==0)!=should_pass:
            raise RuntimeError(description+' unexpected outcome '+result.stdout+' '+result.stderr)
        row={'description':description,'optimized':optimized,'expected_pass':should_pass,
             'returncode':result.returncode,'seconds':time.monotonic()-t,'child_guard_seconds':45}
        if should_pass:
            summary=json.loads(result.stdout)
            if summary['status']!='PASS' or len(summary['mathematical_damages'])!=10:
                raise RuntimeError('incomplete positive damage coverage')
            row['summary']=summary;positive.append(summary)
        else:
            if 'REJECTED:' not in result.stderr:raise RuntimeError('negative case did not reject through normal checker')
            row['reason']=result.stderr.strip()
        rows.append(row)
    for optimized in (False,True):
        extra=['--validation-batch']+(['--baseline-root',str(args.baseline_root.resolve())] if args.baseline_root else [])
        run(HERE,optimized,extra,True,'normal sources full record and ten mathematical damages')
    with tempfile.TemporaryDirectory(prefix='sendov-budget-cold-') as td:
        cold=Path(td)/'source';cold.mkdir()
        for p in HERE.iterdir():
            if p.is_file() and p.name!='VALIDATION.json':shutil.copyfile(p,cold/p.name)
        for optimized in (False,True):
            run(cold,optimized,['--validation-batch'],True,'cold source-only full record and ten mathematical damages')
        expected=json.loads((HERE/'EXPECTED.json').read_text())
        cases=[]
        data=copy.deepcopy(expected);data['field_polynomial_identities'][-1]['all_coefficients'][0][5]='1';cases.append(('alter LAST field coefficient',data))
        data=copy.deepcopy(expected);data['all_ordered_three_value_counts'].pop();cases.append(('remove last multiplicity case',data))
        data=copy.deepcopy(expected);data['all_nine_harmonics'][0]['label']=False;cases.append(('bool for integer label',data))
        data=copy.deepcopy(expected);data['ordinary_analytic_bridges_unformalized']=1;cases.append(('integer for boolean',data))
        data=copy.deepcopy(expected);data['unknown_field']=0;cases.append(('extra whole-record key',data))
        data=copy.deepcopy(expected);data['all_nine_harmonics'][8]['squared_norm'][0][5]='0';cases.append(('alter last harmonic norm',data))
        for name,data in cases:
            damaged=Path(td)/'fixture.json';damaged.write_text(json.dumps(data))
            for optimized in (False,True):
                run(HERE,optimized,['--fixture',str(damaged)],False,name)
        (cold/'curve.py').write_bytes(b'\n'+(cold/'curve.py').read_bytes())
        run(cold,False,[],False,'one source byte alteration')
    for p in positive:
        if p['whole_record_sha256']!=positive[0]['whole_record_sha256'] or p['manifest_sha256']!=positive[0]['manifest_sha256']:
            raise RuntimeError('positive whole record/seal mismatch')
    out={'agent':'six-sendov-3','role':'researcher','status':'PASS',
         'whole_summary':positive[0],'manifest_sha256':positive[0]['manifest_sha256'],
         'positive_modes':4,'mathematical_damage_cases_per_positive':10,
         'whole_external_fixture_rejections':12,'source_byte_rejections':1,
         'native_threads':1,'max_cpu_intensive_jobs':1,'child_guard_seconds':45,
         'scope':'existing1CPU2GiB unchanged','whole_seconds':time.monotonic()-start,
         'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
         'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'children':rows,'ordinary_proof_unformalized':True,'independent_review':False}
    if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('children','whole_summary')},sort_keys=True))


if __name__=='__main__':main()
