"""Whole-source reproduction with bounded serial exact children.

--native downloads pinned PUBLIC producer source only after own reconstruction.
--cas-packages points at an existing SymPy1.14.0/mpmath1.3.0 installation.
"""
import argparse,hashlib,json,os,pathlib,subprocess,sys,tempfile,time,urllib.request
P=pathlib.Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)

def main():
    args=argparse.ArgumentParser()
    args.add_argument('--cas-packages',type=pathlib.Path,required=True)
    args.add_argument('--native',action='store_true')
    a=args.parse_args();cas=a.cas_packages.resolve()
    manifest=json.loads((P/'SOURCE_MANIFEST.json').read_text())
    for name,sha in manifest['files'].items():
        need(hashlib.sha256((P/name).read_bytes()).hexdigest()==sha,'whole public source '+name)
    seal=json.loads((P/'primary-seal.json').read_text())
    for name in ['primary.py','budgets.py','primary.py.out.json','budgets.py.out.json']:
        pin=next(r for r in seal['files'] if r['path']==name)
        need(hashlib.sha256((P/name).read_bytes()).hexdigest()==pin['sha256'],'original pre-native seal '+name)
    env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
    rows=[]
    def run(path,optimized=False,extra=(),cas_mode=False,expected_status=0):
        cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])
        if cas_mode:cmd+=['-c',"import sys,runpy;sys.path.insert(0,sys.argv.pop(1));runpy.run_path(sys.argv.pop(1),run_name='__main__')",str(cas),str(path)]
        else:cmd+=[str(path)]
        cmd+=list(extra);t=time.monotonic();r=subprocess.run(cmd,env=env,capture_output=True,timeout=55)
        need(r.returncode==expected_status,'child status '+str(path)+': '+r.stderr.decode())
        rows.append(dict(file=path.name,optimized=optimized,status=r.returncode,seconds=time.monotonic()-t,sha256=hashlib.sha256(r.stdout).hexdigest()))
        return r
    for f in ['primary.py','budgets.py']:
        expected=(P/(f+'.out.json')).read_bytes()
        for optimized in (False,True):need(run(P/f,optimized,cas_mode=f=='primary.py').stdout==expected,'whole regenerated coefficient record '+f)
    controls=run(P/'controls.py',extra=[str(cas)])
    need(json.loads(controls.stdout)==json.loads((P/'CONTROLS.json').read_text()),'entire six mathematical controls per mode')
    if a.native:
        # Fetch only after own output and damage controls have succeeded.
        with tempfile.TemporaryDirectory(dir=P) as temp:
            tmp=pathlib.Path(temp);(tmp/'producer').mkdir()
            pins=json.loads((P/'producer-pin.json').read_text())
            for pin in pins['files']:
                with urllib.request.urlopen(pin['url'],timeout=20) as response:raw=response.read()
                need(len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'],'entire pinned native source '+pin['name'])
                (tmp/'producer'/pin['name']).write_bytes(raw)
            for f in ['compare_native.py','primary.py.out.json','primary-seal.json']:(tmp/f).write_bytes((P/f).read_bytes())
            results=[]
            for optimized in (False,True):
                native=run(tmp/'producer/verify.py',optimized)
                need(json.loads(native.stdout)['record_sha256']=='98eccc29981554fe0fea426e410d6f849ea2d70e12c2a8bfe7714c4e03a73423','entire native typed record')
                comparison=run(tmp/'compare_native.py',optimized)
                need(json.loads(comparison.stdout)==json.loads((P/'LATE-COMPARISON.json').read_text()),'all ten whole native maps')
                fixture=json.loads((tmp/'producer/expected.json').read_text())
                fixture['whole_maps']['Phi'][11][-1][1]=str(__import__('fractions').Fraction(fixture['whole_maps']['Phi'][11][-1][1])+1)
                damaged=tmp/'damaged.json';damaged.write_text(json.dumps(fixture))
                r=run(tmp/'producer/verify.py',optimized,extra=['--expected',str(damaged)],expected_status=1)
                need(b'ENTIRE typed mathematical record differs' in r.stderr,'last K5 corruption rejected by entire native record')
                results.append(json.loads(native.stdout))
            need(results[0]==results[1],'whole native normal/O typed output')
    print(json.dumps(dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',complete=True,native=a.native,all_four_primary_whole_records_equal=True,all_six_damages_per_mode_rejected=True,all_ten_native_maps_equal=a.native,children=rows),sort_keys=True))

if __name__=='__main__':main()
