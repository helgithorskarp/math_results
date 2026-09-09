"""Deterministic ASan/UBSan coverage across catalogue sizes and core positions."""
from pathlib import Path
import argparse,json,subprocess
def need(ok,why):
    if not ok:raise ValueError(why)
def run(data,baseline,out,producer,checker):
    data,baseline,out=map(Path,(data,baseline,out));out.mkdir();records=profiles=0;parts=[]
    for n,total in ((3,4),(7,362),(11,546356),(15,640)):
        ranges=[(0,total)] if n!=11 else [(0,128),(total//2,total//2+128),(total-128,total)]
        expected=(baseline/str(n)/'COUNTS.tsv').read_text().splitlines()
        for lo,hi in ranges:
            dest=out/f'{n}-{lo}-{hi}';dest.mkdir();table=dest/'COUNTS.tsv';profile=dest/'PROFILES.bin'
            for name,cmd in [('producer',[producer,n,data/f'r44_{n}.g6',lo,hi,table,profile]),('independent',[checker,n,table,profile])]:
                r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True);(dest/(name+'.log')).write_text(r.stdout+r.stderr)
                need(r.returncode==0,'sanitized stage failed: '+str(dest));result=json.loads(r.stdout)
                need(result['records']==hi-lo and result['profiles']==(hi-lo)*(1<<n),'sanitized coverage')
            need(table.read_text().splitlines()==expected[lo:hi],'sanitized count rows differ')
            with (baseline/str(n)/'PROFILES.bin').open('rb') as f:
                f.seek(lo*(2<<n));expected_profile=f.read((hi-lo)*(2<<n))
            need(profile.read_bytes()==expected_profile,'sanitized profile entries differ')
            records+=hi-lo;profiles+=(hi-lo)*(1<<n);parts.append(dict(order=n,start=lo,end=hi))
    return dict(status='SANITIZED_RESIDUAL_CENSUS_COVERAGE_PASS',records=records,profile_entries=profiles,partitions=parts,
                scope='All orders 3,7,15; first/middle/last 128 order-11 cores. Full release census independently compared separately.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('baseline');p.add_argument('out');p.add_argument('producer');p.add_argument('checker');a=p.parse_args()
    r=run(a.data,a.baseline,a.out,a.producer,a.checker);(Path(a.out)/'SANITIZED.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
