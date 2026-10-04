"""Source-only independent audit: whole normal/O/cold records and semantic rejects.
Generated whole records stay temporary, never act as mathematical source inputs."""
from pathlib import Path
import argparse,hashlib,json,os,resource,shutil,subprocess,sys,tempfile,time
def need(ok,label):
    if not ok:raise ValueError(label)
def verify(out):
    here=Path(__file__).resolve().parent
    primary=json.loads((here/'PRIMARY_SEAL.json').read_text())['primary_files']
    need(len(primary)==5,'complete five primary mathematical files')
    for name,pin in primary.items():
        raw=(here/name).read_bytes()
        need(len(raw)==pin['bytes']and hashlib.sha256(raw).hexdigest()==pin['sha256'],'unchanged primary file '+name)
    expected=json.loads((here/'EXPECTED.json').read_text())['records']
    need(set(expected)=={'actual.py','sectors.py','literal.py','input_check.py'},'whole four-route expectations')
    env=dict(os.environ)
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[name]='1'
    files=['arithmetic.py','actual.py','sectors.py','literal.py','input_check.py','INPUT.json','TARGET_INPUT.json']
    failures={
      'actual.py':['mass-factor','last-numerator','denominator-factor','critical-slot','odd-coefficient'],
      'sectors.py':['negative-terminal','tensor-negative','tensor-zero-omitted','closed-cut','endpoint-strictness','sharp-leading'],
      'literal.py':['seven-slot','literal-mass','raw-normalization'],
      'input_check.py':['target-terminal','target-input-factor','target-domain','target-boolean']}
    allruns=[];start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='opposite-audit-')as temp:
        tmp=Path(temp);cold=tmp/'cold';cold.mkdir()
        for name in files:shutil.copyfile(here/name,cold/name)
        for label,source,opt in [('local',here,False),('local',here,True),('cold',cold,False),('cold',cold,True)]:
            for script,pin in expected.items():
                record=tmp/(label+str(opt)+script+'.json');cmd=[sys.executable,'-I','-B']+(['-O']if opt else[])+[str(source/script),'--record',str(record)]
                before=time.monotonic();p=subprocess.run(cmd,capture_output=True,env=env,timeout=50)
                need(p.returncode==0,'positive '+label+' '+script+' '+p.stderr.decode(errors='replace')[-700:])
                raw=record.read_bytes();digest=hashlib.sha256(raw).hexdigest()
                need(len(raw)==pin['bytes']and digest==pin['sha256'],'entire expected record '+script)
                if script=='literal.py':verified_literal=json.loads(raw)
                first=tmp/(script+'.baseline')
                if first.exists():need(first.read_bytes()==raw,'whole record equality across all normal/O/cold modes')
                else:first.write_bytes(raw)
                allruns.append({'source':label,'optimized':opt,'script':script,'defect':None,'exit':0,'seconds':round(time.monotonic()-before,6),'record_bytes':len(raw),'record_sha256':digest})
        for opt in [False,True]:
            for script,damages in failures.items():
                for damage in damages:
                    record=tmp/('damaged-'+script+'.json')
                    if record.exists():record.unlink()
                    cmd=[sys.executable,'-I','-B']+(['-O']if opt else[])+[str(here/script),'--record',str(record),'--damage',damage]
                    before=time.monotonic();p=subprocess.run(cmd,capture_output=True,env=env,timeout=50)
                    error=p.stderr.decode(errors='replace')
                    need(p.returncode>0 and 'ValueError:'in error and not record.exists(),'intended mathematical/schema rejection '+script+' '+damage)
                    gate=error.split('ValueError:')[-1].strip().splitlines()[0]
                    allruns.append({'source':'local','optimized':opt,'script':script,'defect':damage,'exit':p.returncode,'seconds':round(time.monotonic()-before,6),'gate':gate})
    # Exact positive-sector control obstructs transferring sharp16 across sectors.
    from fractions import Fraction
    # Whole literal data was compared in all four modes before temp cleanup;
    # preserve the verified baseline object, not a precomputed control input.
    need(Fraction(verified_literal['profiles'][2]['C'])>16,'actual positive-sector C strictly exceeds16')
    positive=[r for r in allruns if r['defect']is None];negative=[r for r in allruns if r['defect']is not None]
    need(len(positive)==16 and len(negative)==36,'all16 positive and36 required rejection children')
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','python':sys.version.split()[0],'native_threads':1,'CPU_intensive_children_concurrent':1,'fixed_child_seconds':45,'fixed_outer_child_seconds':50,'all_five_primary_files_unchanged':True,'actual_positive_sector_strict_C_above16':True,'positive_children':len(positive),'mathematical_and_schema_rejections':len(negative),'all_four_whole_records_equal_normal_O_local_cold':True,'expected_records':expected,'max_child_seconds':max(r['seconds']for r in allruns),'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'total_seconds':round(time.monotonic()-start,6),'runs':allruns}
    raw=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    if out:out.write_bytes(raw)
    print(json.dumps({k:v for k,v in result.items()if k not in ['runs','expected_records']},indent=2))
if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--out',type=Path);a=cli.parse_args();verify(a.out)
