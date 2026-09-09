"""Complete pinned catalogue census; bulky profiles remain outside Git."""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, subprocess, time
HERE=Path(__file__).resolve().parent

def need(ok, why):
    if not ok: raise ValueError(why)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return h.hexdigest()

def run(data,out,producer,checker):
    data,out=Path(data).resolve(),Path(out).resolve();out.mkdir();start=time.monotonic()
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    for pin in inputs:
        need(sha(data/pin['file'])==pin['sha256'],'catalogue identity')
        need(len((data/pin['file']).read_bytes().splitlines())==pin['count'],'catalogue count')
    def one(pin):
        n=pin['order'];dest=out/str(n);dest.mkdir()
        commands=[('producer',[producer,n,data/pin['file'],0,pin['count'],dest/'COUNTS.tsv',dest/'PROFILES.bin']),
                  ('independent',[checker,n,dest/'COUNTS.tsv',dest/'PROFILES.bin'])]
        for name,cmd in commands:
            r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True)
            (dest/(name+'.log')).write_text(r.stdout+r.stderr)
            need(r.returncode==0,name+' failed; inspect '+str(dest))
            result=json.loads(r.stdout);need(result['records']==pin['count'] and result['profiles']==pin['count']*(1<<n),'complete census')
            print(json.dumps(dict(order=n,stage=name,**result)),flush=True)
        return dict(order=n,records=pin['count'],profile_entries=pin['count']*(1<<n),
                    count_sha256=sha(dest/'COUNTS.tsv'),profile_sha256=sha(dest/'PROFILES.bin'),
                    producer=json.loads((dest/'producer.log').read_text()),independent=json.loads((dest/'independent.log').read_text()))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(one,inputs))
    result=dict(status='COMPLETE_INDEPENDENT_MAXIMAL_RESIDUAL_CENSUS',catalogues=results,
                records=sum(p['records'] for p in results),profile_entries=sum(p['profile_entries'] for p in results),seconds=time.monotonic()-start)
    (out/'CENSUS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('out');p.add_argument('producer');p.add_argument('checker');a=p.parse_args()
    print(json.dumps(run(a.data,a.out,a.producer,a.checker),sort_keys=True))
