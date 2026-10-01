"""Bounded bit-mask closure with a checked AP/triple packing defect budget."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import check_transfer
import probe_units

N=3704


class Proposal(probe_units.Proposal):
    def __init__(self,base,ctx):
        super().__init__(base.read_bytes(),ctx.caps)
        self.pc=ctx.packing_class;self.pD=ctx.new_D;self.pB=ctx.new_budget
        self.pV=ctx.new_V;self.pL=ctx.new_loads

    def close(self,known,max_rounds=16):
        known=known.copy();steps=[]
        for unused in range(max_rounds):
            before=len(steps)
            cost=sum(self.pD-self.pL[x] for x in self.pV if known[x]>=0 and known[x]!=self.pc)
            if cost>self.pB:return known,steps,{'kind':'packing_defect','class':self.pc}
            for x in sorted(self.pV):
                if known[x]<0 and self.pD-self.pL[x]>self.pB-cost:
                    known[x]=self.pc;steps.append({'kind':'budget_fix','point':x,'value':self.pc})
            known,new,term=super().close(known,max_rounds);steps.extend(new)
            if term is not None:return known,steps,term
            cost=sum(self.pD-self.pL[x] for x in self.pV if known[x]>=0 and known[x]!=self.pc)
            if cost>self.pB:return known,steps,{'kind':'packing_defect','class':self.pc}
            if len(steps)==before:return known,steps,None
        return known,steps,None


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--shared',type=Path,required=True)
    p.add_argument('--packing',type=Path,required=True);p.add_argument('--outdir',type=Path,required=True)
    p.add_argument('--root',type=int,default=-1);p.add_argument('--resume',type=Path)
    p.add_argument('--seconds',type=float,default=8);p.add_argument('--max-probes',type=int,default=400)
    a=p.parse_args();a.outdir.mkdir(parents=True,exist_ok=True);started=time.monotonic()
    ctx=check_transfer.Context(a.base,a.shared,a.packing);prop=Proposal(a.base,ctx)
    known=[ctx.known.get(x,-1) for x in range(N)];steps=[];cursor=0;probes=failed=0
    if a.root!=-1:
        if not 0<=a.root<N or prop.colors[a.root]!=0 or known[a.root]>=0:raise ValueError('Fresh original0 root')
        known[a.root]=1
    if a.resume:
        previous=json.loads(a.resume.read_text());checked=ctx.check(previous)
        if checked['excluded'] or previous['root']!=a.root:raise ValueError('Only the same open checked premise can resume')
        known=[-1]*N
        for x,b in checked['known_candidate_values']:known[x]=b
        steps=list(previous['steps']);cursor=previous['next_cursor']
    known,new,term=prop.close(known);steps.extend(new)
    while term is None and cursor<2*N and probes<a.max_probes and time.monotonic()-started<a.seconds:
        x=cursor//2;b=cursor%2;cursor+=1
        if known[x]>=0:continue
        trial=known.copy();trial[x]=b;probes+=1
        _,trial_steps,trial_term=prop.close(trial)
        if trial_term is None:continue
        failed+=1;steps.append({'kind':'failed_literal','point':x,'value':1-b,
                               'trial':{'assumption':[x,b],'steps':trial_steps,'terminal':trial_term}})
        known[x]=1-b;known,new,term=prop.close(known);steps.extend(new)
    trace={'format':'QR617_PACKING_TRANSFER_TRACE_1','phase':ctx.phase,'caps':ctx.caps,'root':a.root,
           'base_certificate_sha256':ctx.base_sha,'shared_trace_sha256':ctx.shared_sha,'packing_sha256':ctx.packing_sha,
           'steps':steps,'terminal':term,'next_cursor':cursor}
    raw=(json.dumps(trace,sort_keys=True,separators=(',',':'))+'\n').encode();(a.outdir/'trace.json').write_bytes(raw)
    summary={'agent':'six-vdw-3','role':'researcher','phase':ctx.phase,'caps':ctx.caps,'root':a.root,
             'packing_defect_budget':ctx.new_budget,'steps':len(steps),'failed_literals_this_run':failed,
             'probes_this_run':probes,'next_cursor':cursor,'terminal':term,'fixed_positions':sum(b>=0 for b in known),
             'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'certificate_sha256':hashlib.sha256(raw).hexdigest(),'proposal_only':True,'no_exhaustive_probe_coverage_claimed':True}
    (a.outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
