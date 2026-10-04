"""Bounded serial whole replays and semantic/source damage controls; no solver."""
import argparse,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,tempfile,time
THREADS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')

def require(ok,msg):
    if not ok:raise ValueError(msg)


def reseal(root):
    (root/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(root.iterdir()) if p.is_file() and p.name!='SHA256SUMS'))


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--second-python');a=p.parse_args();root=pathlib.Path(__file__).resolve().parent;output=pathlib.Path(a.out).resolve()
    require(root not in output.parents,'validation output must be outside source');env=os.environ.copy();env.update({k:'1' for k in THREADS});rows=[];begin=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='sharp-q18-audit-') as td:
        temp=pathlib.Path(td);cold=temp/'cold';shutil.copytree(root,cold,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        def run(label,source,optimized=False,damage=None,expect='PASS',python=sys.executable):
            command=[python,'-I','-B']+(['-O'] if optimized else [])+[str(source/'verify.py')];out=temp/(label+'.json')
            command+=['--out',str(out)]
            if damage:command+=['--damage',damage]
            started=time.monotonic()
            try:r=subprocess.run(command,capture_output=True,text=True,env=env,timeout=45)
            except subprocess.TimeoutExpired:raise ValueError('INCOMPLETE fixed45-second child '+label) from None
            seconds=time.monotonic()-started
            if expect=='PASS':
                require(r.returncode==0,'positive child '+label+' '+r.stderr[-1200:]);m=json.loads(r.stdout);require(m['status']=='PASS' and m['complete'],'complete positive '+label);require(out.read_bytes()==(root/'FRESH-BASE.json').read_bytes(),'whole positive bytes '+label)
            else:
                require(r.returncode!=0 and 'ValueError: '+expect in r.stderr,'intended exited rejection '+label+' '+r.stderr[-1200:]);require(not out.exists(),'failed check produced final record')
                m=None
            rows.append(dict(label=label,optimized=optimized,status='PASS' if expect=='PASS' else 'REJECTED',expected_failure=None if expect=='PASS' else expect,seconds=round(seconds,6),python=python,record=m))
            print(json.dumps({k:v for k,v in rows[-1].items() if k!='record'}),flush=True)
        for source,label in ((root,'local'),(cold,'cold')):
            for optimized in (False,True):run(label+('-O' if optimized else '-normal'),source,optimized)
        if a.second_python:
            for optimized in (False,True):run('second'+('-O' if optimized else '-normal'),cold,optimized,python=a.second_python)
        mathematical=('coefficient','factor','scalar','residual-den','dual','star','upper','empty','slope','range','stability','action');schema=('float','boolean','key','triangle')
        for damage in mathematical+schema:
            for optimized in (False,True):run(damage+('-O' if optimized else '-normal'),cold,optimized,damage,expect='')
        for label in ('float-N','boolean-N','drop-block','alter-bound'):
            dest=temp/label;shutil.copytree(cold,dest);f=dest/'FRESH-BASE.json';v=json.loads(f.read_text())
            if label=='float-N':v['carrier']['N']=float(v['carrier']['N'])
            elif label=='boolean-N':v['carrier']['N']=True
            elif label=='drop-block':v['point_certificates']['blocks'].pop('TT_lower')
            else:v['enlarged_uniform_proper_floor']='1/63'
            f.write_text(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n');reseal(dest);run('fixture-'+label,dest,expect='whole fixture')
        for label in ('changed-arithmetic','omitted-manifest-row'):
            dest=temp/label;shutil.copytree(cold,dest)
            if label=='changed-arithmetic':f=dest/'geometry.py';f.write_text(f.read_text()+'\n# altered source\n')
            else:f=dest/'SHA256SUMS';f.write_text(''.join(s+'\n' for s in f.read_text().splitlines() if not s.endswith('  geometry.py')))
            run('source-'+label,dest,expect='preimport')
    v=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',complete=True,positive_replays=4+2*bool(a.second_python),mathematical_rejects=2*len(mathematical),input_schema_rejects=2*len(schema),whole_fixture_rejects=4,preimport_source_rejects=2,total_rejects=2*(len(mathematical)+len(schema))+6,serial_child_limit=1,native_threads={k:1 for k in THREADS},fixed_child_seconds=45,resource_settings_unchanged=True,all_whole_positive_bytes_equal=True,max_child_seconds=max(r['seconds'] for r in rows),peak_child_rss_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,total_seconds=round(time.monotonic()-begin,6),checks=rows)
    output.write_text(json.dumps(v,indent=2)+'\n');print(json.dumps({k:v for k,v in v.items() if k!='checks'}))

if __name__=='__main__':main()
