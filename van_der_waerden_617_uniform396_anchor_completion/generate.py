"""Serial numerical proposals for one missing anchor root, without private seeds."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import time

for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_name]='1'
import verify
from proposal_lp import cover_lp,select_triples


def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',type=int,required=True)
    p.add_argument('--root',type=int,required=True);p.add_argument('--outdir',type=Path,required=True)
    a=p.parse_args();start=time.monotonic();a.outdir.mkdir(parents=True,exist_ok=True)
    verify.need(a.phase in verify.NEW_ROOTS and a.root in verify.NEW_ROOTS[a.phase],'One declared new anchor case')
    ctx=verify.premise(a.phase);N,P,C=verify.N,verify.P,verify.C
    squares={r*r%P for r in range(1,P)};colors=[]
    for x in range(N):
        r=(x-C+(a.phase if x<C else (1-a.phase)%P))%P
        colors.append(-1 if not r else int(r not in squares)^int(x>=C))
    vertices=[x for x in range(N) if colors[x]==1 and x not in ctx['K'][1]]
    index={x:i for i,x in enumerate(vertices)}
    potential=sum(1<<x for x in range(N) if colors[x]==1 or x==a.root)
    aps=[];petals=[]
    for d in range(1,(N-1)//6+1):
        starts=(1<<(N-6*d))-1
        for j in range(7):starts&=potential>>(j*d)
        while starts:
            bit=starts&-starts;starts-=bit;aa=bit.bit_length()-1
            petal={index[aa+j*d] for j in range(7) if aa+j*d in index}
            if not petal:raise ValueError('A direct empty-petal proof must be reported separately')
            aps.append([aa,d]);petals.append(petal)
    values,weights,baseline=cover_lp(petals,[1]*len(petals),len(vertices))
    summary={'agent':'six-vdw-3','role':'researcher','phase':a.phase,'root':a.root,
             'only_capped_class':1,'cap':197,'other_class_cap':None,
             'baseline':baseline,'native_threads':1,'native_limit_seconds':15,
             'full_domain_size':len(vertices),'mandatory_proposed_APs':len(aps),'rounds':[]}
    if values is None:
        summary['paused_no_exclusion']=True;(a.outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        raise RuntimeError('Native guide unavailable: no mathematical exclusion')
    triples=[];seen=set();rows=list(petals);rhs=[1]*len(petals)
    for r in range(5):
        D=1000000;nums=[max(0,math.floor(w*D)) for w in weights];loads=[0]*len(vertices)
        for row,w in zip(rows,nums):
            for x in row:loads[x]+=w
        D=max([D]+loads)
        data={'format':'QR617_ANCHOR_COMPLETION_PACK_1','phase':a.phase,'root':a.root,
              'capped_original_class':1,'capped_class_cap':197,
              'base_sha256':hashlib.sha256(ctx['base'].read_bytes()).hexdigest(),
              'rigidity_sha256':hashlib.sha256(ctx['rigidity'].read_bytes()).hexdigest(),
              'denominator':D,'AP_weights':[ap+[w] for ap,w in zip(aps,nums[:len(aps)]) if w],
              'triple_weights':[[[aps[i] for i in t],w] for t,w in zip(triples,nums[len(aps):]) if w]}
        raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
        (a.outdir/'packing.json').write_bytes(raw)
        checked=verify.check_root(data,ctx,require_exclusion=False)
        if checked['excluded']:
            summary.update({'exact':checked,'certificate_sha256':hashlib.sha256(raw).hexdigest(),
                            'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                            'proposal_only_until_exact_replay':True,'new_W_bound':False})
            (a.outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True);return
        if r==4:break
        selected,selection=select_triples(petals,values,max_triples=20000-len(triples),seconds=8,candidate_limit=2000000)
        fresh=[t for t in selected if tuple(t) not in seen]
        entry={'round':r+1,'selection':selection,'fresh_triples':len(fresh)};summary['rounds'].append(entry)
        if not fresh:break
        proposed=rows+[set.union(*(petals[i] for i in t)) for t in fresh]
        proposed_rhs=rhs+[2]*len(fresh)
        nxt,nxt_weights,native=cover_lp(proposed,proposed_rhs,len(vertices));entry['native']=native
        if nxt is None:
            summary['paused_no_exclusion']=True;break
        triples.extend(fresh);seen.update(tuple(t) for t in fresh)
        rows=proposed;rhs=proposed_rhs;values=nxt;weights=nxt_weights
    summary['no_positive_certificate_found']=True
    (a.outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    raise RuntimeError('Bounded positive-certificate search unfinished: no exclusion or completeness claim')


if __name__=='__main__':main()
