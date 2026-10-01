"""Meaningful adversarial controls for phase witnesses and union coverage."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,os,shutil,subprocess,sys

HERE=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,required=True)
    ap.add_argument('--work',type=Path,required=True);args=ap.parse_args()
    work=args.work.absolute();require(not work.exists(),'fresh control directory required')
    require(HERE not in (work,*work.parents),'controls must be outside source directory')
    work.mkdir(parents=True);original=json.loads(args.certificate.read_text())
    require(hashlib.sha256(args.certificate.read_bytes()).hexdigest()==
            json.loads((HERE/'expected.json').read_text())['certificate_sha256'],
            'controls need the exact checked baseline')
    pins=json.loads((HERE/'SOURCE_PINS.json').read_text())
    helper=HERE.parent/'order7-geometric-cut'/pins['file']
    require(hashlib.sha256(helper.read_bytes()).hexdigest()==pins['sha256'],'changed control helper')
    spec=importlib.util.spec_from_file_location('control_scope_generator',helper)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    full=(1<<44)-1
    canon=lambda m:min(((m>>s)|(m<<(44-s)))&full for s in range(44))
    base={canon(sum(1<<v for v in {x%44 for x in edge})) for edge in module.field_edges()}
    nonbase=next(int(r['phase_mask']) for r in original['records'] if int(r['phase_mask']) not in base)
    cases=[]
    bad=copy.deepcopy(original);bad['p']=619
    cases.append(('wrong-field',bad,'wrong mathematical parameters'))
    bad=copy.deepcopy(original);bad['records'][0]['witnesses'].pop()
    cases.append(('missing-phase',bad,'incomplete phase cube'))
    bad=copy.deepcopy(original);bad['records'][0]['witnesses'][0]=True
    cases.append(('boolean-word',bad,'invalid normalized witness words'))
    bad=copy.deepcopy(original);bad['records'][0]['witnesses'][0]=0
    cases.append(('constant-color-same-phase',bad,'monochromatic internal field AP'))
    bad=copy.deepcopy(original);bad['records']=[r for r in bad['records'] if int(r['phase_mask'])!=nonbase]
    cases.append(('missing-union',bad,'missing support union in cover'))
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
             MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    result=[]
    for name,data,message in cases:
        path=work/(name+'.json');path.write_text(json.dumps(data,separators=(',',':'))+'\n')
        for flags in ([],['-O']):
            r=subprocess.run([sys.executable,*flags,str(HERE/'audit.py'),str(path)],
                             capture_output=True,text=True,timeout=55,env=env)
            require(r.returncode!=0 and message in r.stderr,'control was not rejected: '+name)
            result.append({'name':name,'optimized':bool(flags),'status':'REJECTED_EXPECTED_GUARD'})
    # Own isolated helper copy; no mutation of the published helper.
    target=work/'isolated'/'order7-eight-coset-locality';target.mkdir(parents=True)
    sibling=target.parent/'order7-geometric-cut';sibling.mkdir()
    for name in ('encode.py','SOURCE_PINS.json'):shutil.copyfile(HERE/name,target/name)
    (sibling/pins['file']).write_bytes(helper.read_bytes()+b'\n# changed control helper\n')
    for flags in ([],['-O']):
        output=target/('never-optimized.json' if flags else 'never-normal.json')
        r=subprocess.run([sys.executable,*flags,str(target/'encode.py'),'--output',str(output)],
                         capture_output=True,text=True,timeout=55,env=env)
        require(r.returncode!=0 and 'changed pinned field generator' in r.stderr and
                not output.exists(),'changed helper reached certificate generation')
        result.append({'name':'changed-pinned-helper','optimized':bool(flags),
                       'status':'REJECTED_BEFORE_HELPER_IMPORT'})
    receipt={'status':'TWELVE_ADVERSARIAL_CONTROLS_PASSED','omitted_nonbase_union_mask':str(nonbase),
             'controls':result}
    (work/'result.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt),flush=True)

if __name__=='__main__':main()
