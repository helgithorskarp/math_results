"""Bounded bit-mask failed-literal and packing-budget proposals.

The trace checker must reconstruct actual APs and scope each trial independently.
No failed probe, exhausted budget, or incomplete closure establishes exclusion.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

N,P,C=3704,617,1852


class Proposal:
    def __init__(self,raw,caps,use_zero_loss=False):
        base=json.loads(raw);self.phase=base['s'];self.D=base['denominator']
        self.S=sum(w for _,_,w in base['color0_APs'])
        squares={r*r%P for r in range(1,P)}
        self.colors=[]
        for x in range(N):
            r=(x-C+(self.phase if x<C else (1-self.phase)%P))%P
            self.colors.append(-1 if not r else int(r not in squares)^int(x>=C))
        self.loads=[0]*N
        for a,d,w in base['color0_APs']:
            for aa in [a,N-1-a-6*d]:
                for j in range(7):self.loads[aa+j*d]+=w
        self.caps=caps;self.budget=[None if k is None else k*self.D-self.S for k in caps]
        self.use_zero_loss=use_zero_loss
        self.starts=[(1<<(N-6*d))-1 for d in range(1,(N-1)//6+1)]

    def initial(self):
        known=[-1]*N
        for x,c in enumerate(self.colors):
            if c>=0 and self.caps[c] is not None and self.D-self.loads[x]>self.budget[c]:known[x]=c
            if c>=0 and self.use_zero_loss and self.caps[c]==197 and self.loads[x]==0:known[x]=c
        return known

    def close(self,known,max_rounds=16):
        known=known.copy();masks=[0,0];edits=[0,0];cost=[0,0];steps=[];terminal=None
        for x,b in enumerate(known):
            if b<0:continue
            masks[b]|=1<<x;c=self.colors[x]
            if c>=0 and b!=c:edits[c]+=1;cost[c]+=self.D-self.loads[x]
        def contradiction():
            for c in [0,1]:
                if self.caps[c] is not None:
                    if edits[c]>self.caps[c]:return {'kind':'class_cap','class':c}
                    if cost[c]>self.budget[c]:return {'kind':'base_defect','class':c}
            return None
        def assign(x,b):
            known[x]=b;masks[b]|=1<<x;c=self.colors[x]
            if c>=0 and b!=c:edits[c]+=1;cost[c]+=self.D-self.loads[x]
        terminal=contradiction()
        if terminal:return known,steps,terminal
        for unused in range(max_rounds):
            before=len(steps)
            # Every fixed edit consumes nonnegative aggregate packing defect.
            for x,c in enumerate(self.colors):
                if known[x]<0 and c>=0 and self.caps[c] is not None and (
                        self.D-self.loads[x]>self.budget[c]-cost[c] or edits[c]>=self.caps[c]):
                    steps.append({'kind':'budget_fix','point':x,'value':c});assign(x,c)
            for d,starts in enumerate(self.starts,1):
                for c in [0,1]:
                    shifted=[masks[c]>>(j*d) for j in range(7)]
                    full=starts
                    for v in shifted:full&=v
                    if full:
                        a=(full&-full).bit_length()-1
                        return known,steps,{'kind':'mono_AP','AP':[a,d]}
                    for j in range(7):
                        candidates=starts
                        for k in range(7):
                            if k!=j:candidates&=shifted[k]
                        candidates&=~shifted[j]
                        while candidates:
                            bit=candidates&-candidates;candidates-=bit;a=bit.bit_length()-1;x=a+j*d
                            if known[x]==1-c:continue
                            if known[x]==c:return known,steps,{'kind':'mono_AP','AP':[a,d]}
                            steps.append({'kind':'unit','AP':[a,d],'point':x,'value':1-c});assign(x,1-c)
                            terminal=contradiction()
                            if terminal:return known,steps,terminal
            if len(steps)==before:return known,steps,None
        return known,steps,None


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True)
    p.add_argument('--seconds',type=float,default=8);p.add_argument('--max-probes',type=int,default=400)
    p.add_argument('--root',type=int,default=-1);p.add_argument('--caps',type=int,nargs=2,default=[197,-1])
    p.add_argument('--resume',type=Path);p.add_argument('--zero-tree',type=Path);a=p.parse_args();started=time.monotonic()
    raw=a.base.read_bytes();caps=[None if k==-1 else k for k in a.caps]
    if any(k is not None and k<0 for k in caps):raise ValueError('Nonnegative caps, or -1 explicitly uncapped')
    zero_sha=None if a.zero_tree is None else hashlib.sha256(a.zero_tree.read_bytes()).hexdigest()
    prop=Proposal(raw,caps,a.zero_tree is not None);known=prop.initial();steps=[];probes=0;failed=0;cursor=0;term=None
    if a.root!=-1:
        if not 0<=a.root<N or prop.colors[a.root]!=0 or known[a.root]>=0:raise ValueError('Fresh original0 root')
        known[a.root]=1
    if a.resume:
        previous=json.loads(a.resume.read_text())
        if previous['phase']!=prop.phase or previous['caps']!=caps or previous['root']!=a.root or previous['base_certificate_sha256']!=hashlib.sha256(raw).hexdigest():raise ValueError('Resume premise differs')
        if previous.get('zero_tree_sha256')!=zero_sha:raise ValueError('Resume zero-loss premise differs')
        # Checked externally before resuming: only proven top-level facts are retained.
        for row in previous['steps']:
            if known[row['point']]>=0:raise ValueError('Fresh resume fact')
            known[row['point']]=row['value']
        steps=previous['steps'];cursor=previous.get('next_cursor',0)
        if previous['terminal'] is not None:raise ValueError('Already excluded')
    known,new,term=prop.close(known);steps.extend(new)
    # Probe each remaining point in a fixed alternating trial-colour order.
    # A complete scan is not claimed; any accepted failed literal has a certificate.
    while term is None and cursor<2*N and probes<a.max_probes and time.monotonic()-started<a.seconds:
        x=cursor//2;b=cursor%2;cursor+=1
        if known[x]>=0:continue
        trial=known.copy();trial[x]=b;probes+=1
        _,trial_steps,trial_term=prop.close(trial)
        if trial_term is None:continue
        failed+=1
        steps.append({'kind':'failed_literal','point':x,'value':1-b,'trial':{'assumption':[x,b],'steps':trial_steps,'terminal':trial_term}})
        known[x]=1-b
        known,new,term=prop.close(known);steps.extend(new)
    out={'format':'QR617_SCOPED_UNIT_TRACE_1','phase':prop.phase,'caps':caps,'root':a.root,
         'base_certificate_sha256':hashlib.sha256(raw).hexdigest(),'steps':steps,'terminal':term,'next_cursor':cursor}
    if zero_sha is not None:out['zero_tree_sha256']=zero_sha
    encoded=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();a.output.write_bytes(encoded)
    summary={'agent':'six-vdw-3','role':'researcher','phase':prop.phase,'caps':caps,'root':a.root,
             'steps':len(steps),'failed_literals_this_run':failed,'probes_this_run':probes,'next_cursor':cursor,
             'terminal':term,'proposal_only':True,'no_contradiction_proves_no_exclusion':True,
             'fixed_candidate_colors':[known.count(c) for c in [0,1]],
             'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'certificate_sha256':hashlib.sha256(encoded).hexdigest()}
    a.summary.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
