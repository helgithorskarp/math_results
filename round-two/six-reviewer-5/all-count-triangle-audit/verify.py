"""Check complete public source before serial independent mathematical replay."""
import argparse,hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile,time
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    a=argparse.ArgumentParser();a.add_argument('--out',required=True);args=a.parse_args();root=pathlib.Path(__file__).resolve().parent
    need(root not in pathlib.Path(args.out).resolve().parents,'output must be outside public source')
    rows=[line.split('  ') for line in (root/'SHA256SUMS').read_text().splitlines()]
    need(all(len(row)==2 and '/' not in row[1] and row[1] not in ('','.','..','SHA256SUMS') for row in rows),'flat owned manifest')
    names=[row[1] for row in rows]
    need(all(not x.is_symlink() and x.is_file() for x in root.iterdir()),'only flat regular public source')
    need(len(names)==len(set(names)) and sorted(names+['SHA256SUMS'])==sorted(x.name for x in root.iterdir()),'complete public source census')
    for digest,name in rows:
        raw=(root/name).read_bytes();need(len(raw)<=100000,'compact public source');raw.decode('utf-8')
        need(hashlib.sha256(raw).hexdigest()==digest,'whole public source digest')
        if name.endswith('.json'):json.loads(raw)
    child=subprocess.run([sys.executable,'-B',str(root/'validate.py'),'--out',args.out],capture_output=True,text=True)
    need(child.returncode==0,child.stdout+child.stderr);v=json.loads(pathlib.Path(args.out).read_text())
    need(len(v['positive_children'])==18 and len(v['damage_children'])==28,'entire public mathematics')
    env=dict(os.environ)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[key]='1'
    gates=[]
    with tempfile.TemporaryDirectory(prefix='independent-no-pole-') as name:
        tmp=pathlib.Path(name)
        for f in ('bounds.py','five_check.py','FRESH-FIVE.json'):shutil.copyfile(root/f,tmp/f)
        for mode in ('normal','optimized','cold'):
            start=time.monotonic();at=tmp if mode=='cold' else root;out=tmp/'record.json'
            r=subprocess.run([sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(at/'bounds.py'),'--input',str(at/'FRESH-FIVE.json'),'--out',str(out)],env=env,capture_output=True,timeout=45)
            need(r.returncode==0,r.stderr.decode());need(out.read_bytes()==(root/'BOUNDS.json').read_bytes(),'entire no-pole/scalar record equality')
            gates.append(dict(mode=mode,exit_code=r.returncode,seconds=time.monotonic()-start,all_encoded_denominators=80))
        for mode in ('normal','optimized'):
            rec=json.loads((root/'FRESH-FIVE.json').read_text());rec['entries'][0][0]['d'][0][1]='-1';path=tmp/'damage.json';path.write_text(json.dumps(rec))
            r=subprocess.run([sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(root/'bounds.py'),'--input',str(path),'--out',str(tmp/'reject.json')],env=env,capture_output=True,timeout=45)
            need(r.returncode!=0 and b'every intermediate denominator positive' in r.stderr,'no-pole damage must reject')
            gates.append(dict(mode=mode,exit_code=r.returncode,damage='negative-intermediate-denominator',rejected=True))
    v.update(source_binding_complete=True,no_pole_gates=gates)
    pathlib.Path(args.out).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(complete=True,public_math_positives=18,public_math_rejections=28,no_pole_positives=3,no_pole_rejections=2,record_sha256=v['record_sha256'])))
if __name__=='__main__':main()
