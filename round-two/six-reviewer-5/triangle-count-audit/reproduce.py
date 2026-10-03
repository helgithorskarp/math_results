"""Portable serial reproduction; fresh work, pinned public inputs, whole outputs.

The optional cache is DATA, never a skip of the independent proof checker.
Every one of its273 native mathematical records is verified before reuse.
"""
import argparse,hashlib,json,os,pathlib,shutil,subprocess,sys,time,urllib.request

def need(ok,why):
    if not ok:raise ValueError(why)

def digest(b):return hashlib.sha256(b).hexdigest()

def mathematical(x):
    if isinstance(x,dict):return {k:mathematical(v) for k,v in x.items() if k not in ('seconds','peak_KiB','optimized')}
    if isinstance(x,list):return [mathematical(v) for v in x]
    return x

def phase_path(label,mode):
    if label.startswith('point-check:'):return 'newton/h'+label.split(':')[1]+'-checked.json'
    if label.startswith('point:'):return 'newton/h'+label.split(':')[1]+'.json'
    if label.startswith('original:'):
        _,h,n=label.split(':');return 'original-h'+h+'-n'+n+'.json'
    return {'raw':'raw-bounds.json','Newton':'newton-coefficients.json','Newton-check':'newton-checked-'+mode+'.json','semantic-damages':'newton-damages-'+mode+'.json','h2-signs':'h2-signs.json','h2-check':'h2-checked.json','complete-sector-controls':'sectors-controls.json'}[label]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=pathlib.Path,required=True);ap.add_argument('--native-cache',type=pathlib.Path);args=ap.parse_args()
    root=pathlib.Path(__file__).resolve().parent;work=args.work.resolve();need(not work.exists(),'fresh work required');work.mkdir(parents=True)
    inputs=json.loads((root/'SOURCE_INPUTS.json').read_text());expected=json.loads((root/'EXPECTED.json').read_text())
    env=os.environ.copy()
    for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'
    def barrier():
        pause=env.get('RESEARCH_PAUSE_DIR')
        need(not pause or not any((pathlib.Path(pause)/n).exists() for n in ['PAUSED','PAUSED.json','HANDOVER','HANDOVER.json']),'operational barrier')
    barrier()
    manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text())['files']
    for name,sha in manifest.items():need(digest((root/name).read_bytes())==sha,'entire reviewer defining source '+name)
    for f in root.iterdir():
        if f.is_file():shutil.copyfile(f,work/f.name)
    native=work/'native-normal';target=work/'target-source';native.mkdir();target.mkdir();cache=args.native_cache.resolve() if args.native_cache else None
    for row in inputs['files']:
        if cache:raw=(cache/row['name']).read_bytes()
        else:
            url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+inputs['commit']+'/'+inputs['prefix']+'/'+row['name']
            with urllib.request.urlopen(url,timeout=20) as response:raw=response.read()
        need(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'complete pinned public producer source '+row['name'])
        (native/row['name']).write_bytes(raw);(target/row['name']).write_bytes(raw)
    native_record=json.loads((native/'RESULTS.json').read_text());need(native_record['phase_count']==273,'entire native phase catalogue')
    if cache:
        need((cache/'work/FULL-RESULT.json').read_bytes()==(native/'RESULTS.json').read_bytes(),'entire native cached final record')
        cp=json.loads((cache/'work/DRIVER-CHECKPOINT.json').read_text());need(cp['complete'],'completed source-generated cache')
        need(cp['code_hashes']=={f.name:digest(f.read_bytes()) for f in sorted(native.glob('*.py'))},'entire cached defining source')
        mode=cp['mode'];stream=hashlib.sha256();count=0;(native/'work').mkdir()
        need(set(cp['finished'])=={r['phase'] for r in native_record['phase_records']},'complete finished273 phases')
        for r in native_record['phase_records']:
            path=phase_path(r['phase'],mode);raw=(cache/'work'/path).read_bytes()
            need(digest(raw)==cp['finished'][r['phase']]['file_sha256'],'every whole cached phase output')
            blob=json.dumps(mathematical(json.loads(raw)),sort_keys=True,separators=(',',':')).encode()
            need(len(blob)==r['mathematical_bytes'] and digest(blob)==r['mathematical_sha256'],'every mathematical cached phase')
            stream.update(r['phase'].encode()+b'\n'+blob+b'\n');count+=len(blob)
            out=native/'work'/phase_path(r['phase'],'normal');out.parent.mkdir(exist_ok=True,parents=True);out.write_bytes(raw)
        need(count==expected['native']['mathematical_bytes'] and stream.hexdigest()==expected['native']['mathematical_sha256'],'entire native cached stream')
        (native/'work/FULL-RESULT.json').write_bytes((native/'RESULTS.json').read_bytes())
    else:
        barrier();r=subprocess.run([sys.executable,'-B','verify.py','--check','RESULTS.json'],cwd=native,env=env,timeout=1200)
        need(r.returncode==0,'complete source-only native regeneration')
    need(digest((native/'work/FULL-RESULT.json').read_bytes())==expected['native']['sha256'],'whole native result pin')
    packages=env.get('REVIEW_SYMPY_PATH')
    cmd=[sys.executable,'-I','-B']
    if packages:cmd+=['-c',"import sys,runpy;sys.path.insert(0,sys.argv.pop(1));runpy.run_path(sys.argv.pop(1),run_name='__main__')",packages,str(work/'canonical.py')]
    else:cmd+=[str(work/'canonical.py')]
    barrier();r=subprocess.run(cmd,env=env,capture_output=True,timeout=55);need(r.returncode==0,'cold defining reconstruction '+r.stderr.decode()[-1000:])
    need(len(r.stdout)==expected['primary']['bytes'] and digest(r.stdout)==expected['primary']['sha256'],'whole sealed cold primary');(work/'canonical.stdout').write_bytes(r.stdout)
    for name in ['verify.py','extra.py']:
        barrier();r=subprocess.run([sys.executable,'-B',str(work/name)],env=env,timeout=1200);need(r.returncode==0,'full cold reviewer '+name)
    own=json.loads((work/'own-replay.json').read_text());extra=json.loads((work/'supplement.json').read_text())
    need(own['complete'] and own['entire_modes_equal'] and extra['complete'] and extra['entire_modes_equal'],'all cold modes complete')
    seal=json.loads((work/'PRIMARY_SEAL.json').read_text())
    for row in seal['files'][:3]:need(digest((work/row['path']).read_bytes())==row['sha256'],'pre-access defining source unchanged')
    output=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',complete=True,source_only_reviewer=True,native_source_regenerated=not bool(cache),native_cache_entire273phases_checked=bool(cache),own_children=len(own['receipts']),extra_children=len(extra['receipts']),entire_normal_optimized_equal=True,independent_stream_sha256=own['mode_summary'][0]['stream_sha256'],supplement_stream_sha256=extra['whole_stream_sha256'],serial_math_children=True,threads=1)
    (work/'COLD-RESULT.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output),flush=True)
if __name__=='__main__':main()
