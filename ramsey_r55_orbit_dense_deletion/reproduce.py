#!/usr/bin/env python3
"""Replay the exact finite certificates and literal receiving interface."""
import argparse,hashlib,json,resource,subprocess,sys,tempfile,time
from pathlib import Path
import family

ROOT=Path(__file__).resolve().parent


def run(args):
    result=subprocess.run(args,capture_output=True,text=True)
    if result.returncode or result.stderr:raise ValueError('replay failed: '+result.stdout+result.stderr)
    return json.loads(result.stdout) if result.stdout else None


def main():
    argparse.ArgumentParser().parse_args();start=time.monotonic()
    files=[]
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);files.append(name)
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('source manifest '+name)
    if set(files)!={p.name for p in ROOT.iterdir() if p.is_file() and p.name!='SHA256SUMS'}:
        raise ValueError('source manifest file coverage')
    expected=json.loads((ROOT/'EXPECTED_CHECK.json').read_text())
    controls=json.loads((ROOT/'EXPECTED_CONTROLS.json').read_text())
    fixtures=json.loads((ROOT/'FIXTURES.json').read_text())
    physical=json.loads((ROOT/'EXPECTED_PHYSICAL.json').read_text())
    if len(fixtures)!=len(physical):raise ValueError('fixture count')
    if family.inventory()!=json.loads((ROOT/'REDUCTION.json').read_text()):raise ValueError('reduction inventory')
    with tempfile.TemporaryDirectory(prefix='r55-orbit-deletion-') as tmp:
        temp=Path(tmp)
        for flag in ([],['-O']):
            py=[sys.executable,*flag,'-B']
            run([*py,str(ROOT/'produce.py'),'--output',str(temp/'certificate.json')])
            if (temp/'certificate.json').read_bytes()!=(ROOT/'CERTIFICATE.json').read_bytes():raise ValueError('certificate reproduction')
            if run([*py,str(ROOT/'check.py'),str(temp/'certificate.json')])!=expected:raise ValueError('independent certificate check')
            if run([*py,str(ROOT/'controls.py')])!=controls:raise ValueError('control check')
            for i,(row,wanted) in enumerate(zip(fixtures,physical)):
                path=temp/f'input-{i}.json';path.write_text(json.dumps(family.instantiate(row)))
                cert=run([*py,str(ROOT/'interface.py'),str(path)])
                if cert!=wanted['certificate']:raise ValueError('physical certificate '+str(i))
                out=temp/f'physical-{i}.json';out.write_text(json.dumps(cert))
                if run([*py,str(ROOT/'check.py'),str(out),'--input',str(path)])!=wanted['independent_check']:
                    raise ValueError('literal physical witness '+str(i))
    print(json.dumps({'status':'REPRODUCED_COMPLETE_ORBIT_DENSE_DELETION_CERTIFICATES',
                      'modes':['normal','assertions_disabled'],'physical_fixtures_per_mode':len(fixtures),
                      'literal_physical_pairs_per_mode':10*len(fixtures),
                      'paley_physical_jobs_excluded':expected['paley_physical_jobs_excluded'],
                      'two_orbit_physical_parameter_jobs_excluded':expected['two_orbit_physical_parameter_jobs_excluded'],
                      'new_solver_calls':0,'target43_found':False,'elapsed_seconds':time.monotonic()-start,
                      'max_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},indent=2))


if __name__=='__main__':main()
