"""One bounded ordinary-AP numerical proposal, then separate exact replay."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import time

for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'
import verify
from proposal_lp import cover_lp

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=int,choices=(605,3405),required=True)
    p.add_argument('--outdir',type=Path,required=True);a=p.parse_args();start=time.monotonic();a.outdir.mkdir(parents=True,exist_ok=True)
    ctx=verify.context();N,P,C=verify.N,verify.P,verify.C
    squares={r*r%P for r in range(1,P)};colors=[]
    for x in range(N):
        r=(x-C+(611 if x<C else 7))%P
        colors.append(-1 if not r else int(r not in squares)^int(x>=C))
    vertices=[x for x in range(N) if x in ctx['V']];index={x:i for i,x in enumerate(vertices)}
    potential=sum(1<<x for x in range(N) if colors[x]==1 or x==a.root)
    aps=[];petals=[]
    for d in range(1,(N-1)//6+1):
        starts=(1<<(N-6*d))-1
        for j in range(7):starts&=potential>>(j*d)
        while starts:
            bit=starts&-starts;starts-=bit;aa=bit.bit_length()-1
            petal={index[aa+j*d] for j in range(7) if aa+j*d in index}
            if not petal:raise ValueError('Direct empty-petal terminal must be reported separately')
            aps.append([aa,d]);petals.append(petal)
    values,weights,native=cover_lp(petals,[1]*len(petals),len(vertices))
    summary={'agent':'six-vdw-3','role':'researcher','phase':611,'root':a.root,'only_capped_class':1,'cap':197,
             'other_class_cap':None,'native':native,'native_limit_seconds':15,'native_threads':1,
             'mandatory_proposed_APs':len(aps),'full_domain_size':len(vertices),'new_W_bound':False}
    if values is None:
        summary['operational_failure_no_exclusion']=True
        (a.outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        raise RuntimeError('Guide unavailable: stop without mathematical exclusion or resource escalation')
    D=1000000;nums=[max(0,math.floor(w*D)) for w in weights];loads=[0]*len(vertices)
    for petal,w in zip(petals,nums):
        for x in petal:loads[x]+=w
    D=max([D]+loads)
    data={'format':'QR617_SINGLECAP611_AP_PACK_1','phase':611,'root':a.root,
          'capped_original_class':1,'capped_class_cap':197,'base_sha256':verify.BASE_SHA,
          'denominator':D,'AP_weights':[ap+[w] for ap,w in zip(aps,nums) if w]}
    raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode();(a.outdir/'packing.json').write_bytes(raw)
    exact=verify.check_new_root(data,ctx,require_exclusion=False)
    summary.update(exact=exact,certificate_sha256=hashlib.sha256(raw).hexdigest(),seconds=time.monotonic()-start,
                   peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,proposal_only_until_exact_replay=True)
    (a.outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    if not exact['excluded']:raise RuntimeError('No strict positive certificate: bounded proposal inconclusive')
    print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
