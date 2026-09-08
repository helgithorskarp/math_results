#!/usr/bin/env python3
"""Full normal/-O replay using a mandatory, locally supplied pinned catalog."""
import argparse,copy,hashlib,json,os,resource,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run(args,expected_failure=None):
    r=subprocess.run(args,capture_output=True,text=True,cwd=ROOT)
    if expected_failure:
        if r.returncode==0 or expected_failure not in r.stderr:raise ValueError('incorrect negative control: '+r.stderr)
        return None
    if r.returncode or r.stderr:raise ValueError('replay failed: '+r.stdout+r.stderr)
    return json.loads(r.stdout)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--catalog',required=True);args=parser.parse_args()
    catalog=Path(args.catalog).resolve();t=time.monotonic()
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('manifest '+name)
    expected=json.loads((ROOT/'EXPECTED_CHECK.json').read_text());expected_controls=json.loads((ROOT/'EXPECTED_CONTROLS.json').read_text())
    with tempfile.TemporaryDirectory(prefix='r55-regular-overlap-') as tmp:
        d=Path(tmp)
        for flag in ([],['-O']):
            py=[sys.executable,*flag,'-B']
            run([*py,str(ROOT/'produce.py'),'--catalog',str(catalog),'--output-dir',str(d)])
            for name in ('CERTIFICATE.json','RETAINED.g6'):
                if (d/name).read_bytes()!=(ROOT/name).read_bytes():raise ValueError('producer '+name)
            cmd=[*py,str(ROOT/'check.py'),'--catalog',str(catalog),'--certificate',str(d/'CERTIFICATE.json'),'--retained',str(d/'RETAINED.g6')]
            if run(cmd)!=expected:raise ValueError('independent output')
            if run([*py,str(ROOT/'controls.py')])!=expected_controls:raise ValueError('control output')
            c=run([*py,str(ROOT/'interface.py'),str(ROOT/'FIXTURE.json')])
            if c!=json.loads((ROOT/'FIXTURE_CERTIFICATE.json').read_text()):raise ValueError('fixture output')
            if run([*py,str(ROOT/'verify_physical.py'),str(ROOT/'FIXTURE.json'),str(ROOT/'FIXTURE_CERTIFICATE.json')])!={'status':'VERIFIED_LITERAL_MONOCHROMATIC_FIVE','pairs':10}:raise ValueError('fixture check')
            wrong=copy.deepcopy(json.loads((d/'CERTIFICATE.json').read_text()));wrong['buckets'][0]['degree_budget']+=1
            (d/'wrong.json').write_text(json.dumps(wrong))
            bad=cmd.copy();bad[bad.index('--certificate')+1]=str(d/'wrong.json');run(bad,'certificate entry mismatch')
            (d/'bad.g6').write_bytes((d/'RETAINED.g6').read_bytes().splitlines()[0]+b'\n')
            bad=cmd.copy();bad[bad.index('--retained')+1]=str(d/'bad.g6');run(bad,'complete retained list')
            (d/'bad-catalog.g6').write_text('bad\n')
            bad=cmd.copy();bad[bad.index('--catalog')+1]=str(d/'bad-catalog.g6');run(bad,'catalog hash')
    print(json.dumps({'status':'REPRODUCED_COMPLETE_REGULAR18_AND24_EXCLUSION','modes':['normal','assertions_disabled'],'family_certificate_input_negative_controls_per_mode':3,'elapsed_seconds':time.monotonic()-t,'max_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},indent=2))
if __name__=='__main__':main()
