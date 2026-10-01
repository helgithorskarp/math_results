"""Exact post-proof branch checker; imports no proposal implementation.

The shared proof is replayed before any branch assumption is made. A smaller
finite cap is a stronger hypothesis; None in the shared proof is uncapped.
All APs use actual interval positions and every failed trial has local scope.
"""
import argparse
import hashlib
import json
from pathlib import Path
import base_verify
import check_probe

N=3704
need=base_verify.need


class Context:
    def __init__(self,base,shared,caps):
        raw=base.read_bytes();data=json.loads(raw)
        self.base_sha=hashlib.sha256(raw).hexdigest()
        shared_raw=shared.read_bytes();trace=json.loads(shared_raw)
        self.shared_sha=hashlib.sha256(shared_raw).hexdigest()
        need(type(caps) is list and len(caps)==2 and all(k is None or type(k) is int and k>=0 for k in caps),'Explicit nonnegative or uncapped branch caps')
        need(trace['root']==-1,'Shared proof has no branch assumption')
        old=trace['caps']
        need(all(old[c] is None or caps[c] is not None and caps[c]<=old[c] for c in (0,1)),'Only stronger caps may inherit the shared proof')
        self.shared_check=check_probe.check(base,trace)
        need(not self.shared_check['excluded'],'Open shared proof, before post-proof branching')
        self.colors,_,summary=base_verify.base_premise(base)
        self.phase=summary['phase'];self.D=data['denominator'];self.S=summary['base_weight_numerator']
        self.loads=[0]*N
        for a,d,w in data['color0_APs']:
            for aa in (a,N-1-a-6*d):
                for x in base_verify.actual_ap(aa,d):self.loads[x]+=w
        self.caps=caps
        self.budgets=[None if k is None else k*self.D-self.S for k in caps]
        need(all(b is None or b>=0 for b in self.budgets),'Nonnegative branch packing budgets')
        self.known=dict(self.shared_check['known_candidate_values'])
        self.additional_screen=[]
        for x,c in enumerate(self.colors):
            if c>=0 and caps[c] is not None and self.D-self.loads[x]>self.budgets[c]:
                need(x not in self.known or self.known[x]==c,'Consistent stronger initial budget screen')
                if x not in self.known:self.additional_screen.append(x);self.known[x]=c

    def forced(self,known,c):
        return {x for x,b in known.items() if self.colors[x]==c and b!=c}

    def can_budget_fix(self,known,x,b):
        c=self.colors[x]
        if c<0 or c!=b or self.caps[c] is None:return False
        E=self.forced(known,c);cost=sum(self.D-self.loads[y] for y in E)
        return len(E)>=self.caps[c] or self.D-self.loads[x]>self.budgets[c]-cost

    def terminal(self,node,known,required):
        if node is None:
            need(not required,'A failed literal needs an actual contradiction');return False
        need(type(node) is dict and 'kind' in node,'Terminal schema')
        if node['kind']=='mono_AP':
            need(set(node)=={'kind','AP'} and type(node['AP']) is list and len(node['AP'])==2,'Actual terminal progression')
            A=base_verify.actual_ap(*node['AP'])
            need(all(x in known for x in A) and len({known[x] for x in A})==1,'All seven actual positions have the same fixed value')
        else:
            need(set(node)=={'kind','class'} and type(node['class']) is int and node['class'] in (0,1),'Original-class terminal schema')
            c=node['class'];need(self.caps[c] is not None,'Uncapped class cannot yield a finite-budget terminal')
            E=self.forced(known,c)
            if node['kind']=='class_cap':need(len(E)>self.caps[c],'Strict forced original-class edit count')
            elif node['kind']=='base_defect':need(sum(self.D-self.loads[x] for x in E)>self.budgets[c],'Strict exact nonnegative defect sum')
            else:raise ValueError('Unknown terminal')
        return True

    def replay(self,rows,known,counts,trial=False):
        need(type(rows) is list and len(rows)<=N,'At most one fresh fact per actual position in each scope')
        for row in rows:
            need(type(row) is dict and row.get('kind') in ('unit','budget_fix','failed_literal'),'Known implication kind')
            kind=row['kind'];x=row.get('point');b=row.get('value')
            need(type(x) is int and 0<=x<N and x not in known and type(b) is int and b in (0,1),'One fresh binary fact')
            if kind=='unit':
                need(set(row)=={'kind','AP','point','value'} and type(row['AP']) is list and len(row['AP'])==2,'Unit AP schema')
                A=base_verify.actual_ap(*row['AP'])
                need(x in A and all(y in known and known[y]==1-b for y in A-{x}),'All six actual predecessors have the opposite bit')
            elif kind=='budget_fix':
                need(set(row)=={'kind','point','value'},'Budget fix schema')
                c=self.colors[x];need(c>=0 and c==b and self.caps[c] is not None,'Finite original class only')
                need(self.can_budget_fix(known,x,b),'An extra edit strictly violates a cap or packing budget')
            else:
                need(not trial and set(row)=={'kind','point','value','trial'},'No nested failed literal')
                sub=row['trial'];need(type(sub) is dict and set(sub)=={'assumption','steps','terminal'},'Trial has explicit assumption, proof and contradiction')
                need(type(sub['assumption']) is list and sub['assumption']==[x,1-b] and all(type(v) is int for v in sub['assumption']),'Assume exactly the negation of this fact')
                local=known.copy();local[x]=1-b
                self.replay(sub['steps'],local,counts,True);self.terminal(sub['terminal'],local,True)
            counts[('trial_' if trial else '')+kind]+=1
            known[x]=b

    def check(self,trace):
        schema={'format','phase','caps','root','base_certificate_sha256','shared_trace_sha256','steps','terminal','next_cursor'}
        need(type(trace) is dict and set(trace)==schema,'Post-proof branch schema')
        need(trace['format']=='QR617_POST_SHARED_BRANCH_TRACE_1','Post-proof branch format')
        need(type(trace['phase']) is int and trace['phase']==self.phase and trace['caps']==self.caps,'Actual phase and inherited cap hypothesis')
        need(all(k is None or type(k) is int for k in trace['caps']),'Caps are exact native integers')
        need(trace['base_certificate_sha256']==self.base_sha and trace['shared_trace_sha256']==self.shared_sha,'Replay exact pinned base and shared proof')
        root=trace['root'];known=self.known.copy()
        need(type(root) is int and 0<=root<N and self.colors[root]==0 and root not in known,'A fresh original0 edit AFTER the shared proof')
        known[root]=1
        counts={'unit':0,'budget_fix':0,'failed_literal':0,'trial_unit':0,'trial_budget_fix':0}
        self.replay(trace['steps'],known,counts);excluded=self.terminal(trace['terminal'],known,False)
        need(type(trace['next_cursor']) is int and 0<=trace['next_cursor']<=2*N,'Operational cursor has no coverage meaning')
        E=[self.forced(known,c) for c in (0,1)]
        return {'agent':'six-vdw-3','role':'researcher','phase':self.phase,'caps':self.caps,'root':root,
                'base_certificate_sha256':self.base_sha,'shared_trace_sha256':self.shared_sha,
                'base_denominator':self.D,'base_weight_numerator':self.S,'base_defect_budgets':self.budgets,
                'shared_fixed_positions':len(self.known),'additional_screen_positions':self.additional_screen,
                'steps_checked':counts,'terminal':trace['terminal'],'excluded':excluded,
                'forced_original_class_edits':[len(e) for e in E],
                'consumed_base_defects':[sum(self.D-self.loads[x] for x in e) for e in E],
                'known_candidate_values':[[x,known[x]] for x in sorted(known)],
                'candidate_symmetry_assumed':False,'solver_trusted':False,'new_W_bound':False}

    def anchor_roots(self,anchor):
        need(type(anchor) is list and len(anchor)==2,'One actual anchor progression')
        A=base_verify.actual_ap(*anchor)
        need(all(self.colors[x]==0 for x in A),'Every actual anchor position is original0, without poles')
        need(all(self.known[x]==0 for x in A if x in self.known),'Anchor has no already fixed edit')
        roots=sorted(A-set(self.known));need(roots,'Open anchor has at least one undecided position')
        return roots


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--shared',type=Path,required=True)
    p.add_argument('--trace',type=Path,required=True);p.add_argument('--output',type=Path)
    a=p.parse_args();trace=json.loads(a.trace.read_text());ctx=Context(a.base,a.shared,trace['caps']);out=ctx.check(trace)
    if a.output:a.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='known_candidate_values'}),flush=True)


if __name__=='__main__':main()
