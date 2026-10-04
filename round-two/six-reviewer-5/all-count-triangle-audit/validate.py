"""Independent whole source/record replay and fourteen semantic damages.

Fixed45s children, native1, serial1. No current author executable inputs.
"""
import argparse,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,tempfile,time
def need(ok,msg):
    if not ok:raise ValueError(msg)
CASES=((3,5,2),(5,3,2),(3,6,2),(3,6,3))
ORIGINAL_DAMAGE=('missing-private-row','wrong-empty','omitted-heavy-mean','wrong-light-full-score','wrong-dual-energy','false-endpoint','wrong-update-empty','missing-spread-pair')
CERT_DAMAGE=('entry','pivot','local-update','coverage','last-pivot-term','duplicate-coefficient')
def main():
    a=argparse.ArgumentParser();a.add_argument('--out',required=True);a.add_argument('--seal',action='store_true');arg=a.parse_args()
    root=pathlib.Path(__file__).resolve().parent;env=dict(os.environ)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[key]='1'
    receipt=dict(interpreter=sys.version,native_threads=1,serial_children=1,fixed_guard_seconds=45,positive_children=[],damage_children=[])
    expected=None if arg.seal else (root/'RECORD.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='independent-unrestricted-triangle-') as tmpname:
        tmp=pathlib.Path(tmpname)
        for name in ('forms.py','original.py','five_generate.py','five_check.py','FRESH-FIVE.json'):shutil.copyfile(root/name,tmp/name)
        def run(mode,code,args,source=None):
            at=source or (tmp if mode=='cold' else root)
            cmd=[sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(at/code),*args]
            start=time.monotonic();r=subprocess.run(cmd,capture_output=True,env=env,timeout=45)
            return r,dict(mode=mode,code=code,seconds=time.monotonic()-start,exit_code=r.returncode,peak_child_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        for mode in ('normal','optimized','cold'):
            gen=tmp/'generated.json';r,row=run(mode,'five_generate.py',['--out',str(gen)]);need(r.returncode==0,r.stderr.decode());need(gen.read_bytes()==(root/'FRESH-FIVE.json').read_bytes(),'whole fresh certificate equality');receipt['positive_children'].append(row)
            out=tmp/'five.json';r,row=run(mode,'five_check.py',['--input',str(gen),'--out',str(out)]);need(r.returncode==0,r.stderr.decode());five=json.loads(out.read_text());receipt['positive_children'].append(row)
            originals=[]
            for n,h,l in CASES:
                out=tmp/f'original-{n}-{h}-{l}.json';r,row=run(mode,'original.py',['--n',str(n),'--h',str(h),'--l',str(l),'--out',str(out)]);need(r.returncode==0,r.stderr.decode());originals.append(json.loads(out.read_text()));receipt['positive_children'].append(row)
            data=(json.dumps(dict(five=five,original=originals),sort_keys=True,separators=(',',':'))+'\n').encode()
            if expected is None:expected=data;(root/'RECORD.json').write_bytes(data)
            need(data==expected,'entire independent mathematical record equality')
            print('completed six full mathematical children: '+mode,flush=True)
        for mode in ('normal','optimized'):
            for damage in ORIGINAL_DAMAGE:
                r,row=run(mode,'original.py',['--n','3','--h','5','--l','2','--out',str(tmp/'reject.json'),'--damage',damage]);need(r.returncode!=0 and b'ValueError: ' in r.stderr,'mathematical original damage must reject '+damage)
                row.update(damage=damage,rejected=True,reason=r.stderr.decode().strip().splitlines()[-1]);receipt['damage_children'].append(row)
            for damage in CERT_DAMAGE:
                rec=json.loads((root/'FRESH-FIVE.json').read_text())
                if damage=='entry':rec['entries'][0][0]['n'][0][1]=str(int(rec['entries'][0][0]['n'][0][1])+1)
                elif damage=='pivot':rec['pivots'][0]['n'][0][1]=str(int(rec['pivots'][0]['n'][0][1])+1)
                elif damage=='local-update':rec['stages'][0]['updates'][0]['value']['n'][0][1]=str(int(rec['stages'][0]['updates'][0]['value']['n'][0][1])+1)
                elif damage=='coverage':rec['stages'][0]['updates'].pop()
                elif damage=='last-pivot-term':rec['pivots'][-1]['n'].pop()
                elif damage=='duplicate-coefficient':rec['entries'][0][0]['n'].append(rec['entries'][0][0]['n'][0])
                path=tmp/'damage.json';path.write_text(json.dumps(rec));r,row=run(mode,'five_check.py',['--input',str(path),'--out',str(tmp/'reject.json')]);need(r.returncode!=0 and b'ValueError: ' in r.stderr,'mathematical coefficient damage must reject '+damage)
                row.update(damage=damage,rejected=True,reason=r.stderr.decode().strip().splitlines()[-1]);receipt['damage_children'].append(row)
            print('completed fourteen mathematical damage rejections: '+mode,flush=True)
    receipt.update(complete=True,record_bytes=len(expected),record_sha256=hashlib.sha256(expected).hexdigest(),fresh_certificate_bytes=(root/'FRESH-FIVE.json').stat().st_size,fresh_certificate_sha256=hashlib.sha256((root/'FRESH-FIVE.json').read_bytes()).hexdigest())
    pathlib.Path(arg.out).write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(json.dumps(dict(complete=True,positive_children=len(receipt['positive_children']),damages=len(receipt['damage_children']),record_sha256=receipt['record_sha256'])))
if __name__=='__main__':main()
