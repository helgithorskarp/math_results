"""Exact defect-budget consequences of a replayed integer AP/triple packing.

The shared implication proof is checked first, the packing on its FULL remaining
domain second, and new deductions third. No new deduction is a packing premise.
"""
import argparse
import hashlib
import json
from pathlib import Path
import base_verify
import check_branch
import check_rank2

need=base_verify.need
N=3704


class Context(check_branch.Context):
    def __init__(self,base,shared,packing):
        raw=packing.read_bytes();cert=json.loads(raw)
        super().__init__(base,shared,cert['caps'])
        self.packing_sha=hashlib.sha256(raw).hexdigest()
        self.packing_check=check_rank2.check(base,shared,cert,context=self)
        need(not self.packing_check['excluded'],'An excluded packing is already a direct contradiction')
        self.packing_class=cert['original_class'];self.new_D=cert['denominator']
        self.new_S=self.packing_check['weighted_numerator']
        self.new_budget=self.packing_check['remaining_cap']*self.new_D-self.new_S
        self.new_V={x for x in range(N) if self.colors[x]==self.packing_class and x not in self.known}
        self.new_loads={x:0 for x in self.new_V}
        for a,d,w in cert['AP_weights']:
            for x in base_verify.actual_ap(a,d)-set(self.known):self.new_loads[x]+=w
        for triple,w in cert['triple_weights']:
            U=set.union(*(base_verify.actual_ap(*ap)-set(self.known) for ap in triple))
            for x in U:self.new_loads[x]+=w
        need(all(0<=L<=self.new_D for L in self.new_loads.values()),'Recomputed full-domain nonnegative packing defects')

    def packing_cost(self,known):
        return sum(self.new_D-self.new_loads[x] for x in self.new_V if x in known and known[x]!=self.packing_class)

    def can_budget_fix(self,known,x,b):
        if super().can_budget_fix(known,x,b):return True
        return x in self.new_V and b==self.packing_class and self.new_D-self.new_loads[x]>self.new_budget-self.packing_cost(known)

    def terminal(self,node,known,required):
        if type(node) is dict and node.get('kind')=='packing_defect':
            need(set(node)=={'kind','class'} and type(node['class']) is int and node['class']==self.packing_class,'Actual checked packing class')
            need(self.packing_cost(known)>self.new_budget,'Strict nonnegative defect budget from the independently checked AP/triple packing')
            return True
        return super().terminal(node,known,required)

    def check(self,trace):
        schema={'format','phase','caps','root','base_certificate_sha256','shared_trace_sha256','packing_sha256','steps','terminal','next_cursor'}
        need(type(trace) is dict and set(trace)==schema and trace['format']=='QR617_PACKING_TRANSFER_TRACE_1','Packing transfer trace schema')
        need(type(trace['phase']) is int and trace['phase']==self.phase and trace['caps']==self.caps and all(k is None or type(k) is int for k in trace['caps']),'Actual inherited phase and integer caps')
        need(trace['base_certificate_sha256']==self.base_sha and trace['shared_trace_sha256']==self.shared_sha and trace['packing_sha256']==self.packing_sha,'Shared proof and full-domain packing checked BEFORE any new fact')
        known=self.known.copy();root=trace['root']
        need(type(root) is int,'Explicit native integer root or none')
        if root!=-1:
            need(0<=root<N and self.colors[root]==0 and root not in known,'Fresh original0 edit after both shared proof and packing replay')
            known[root]=1
        counts={'unit':0,'budget_fix':0,'failed_literal':0,'trial_unit':0,'trial_budget_fix':0}
        self.replay(trace['steps'],known,counts);excluded=self.terminal(trace['terminal'],known,False)
        need(type(trace['next_cursor']) is int and 0<=trace['next_cursor']<=2*N,'Operational cursor has no exhaustive coverage meaning')
        E=[self.forced(known,c) for c in (0,1)]
        return {'agent':'six-vdw-3','role':'researcher','phase':self.phase,'caps':self.caps,'root':root,
                'base_certificate_sha256':self.base_sha,'shared_trace_sha256':self.shared_sha,'packing_sha256':self.packing_sha,
                'shared_positions':len(self.known),'total_positions':len(known),'new_positions':len(known)-len(self.known),
                'steps_checked':counts,'excluded':excluded,'terminal':trace['terminal'],
                'packing_class':self.packing_class,'packing_denominator':self.new_D,'packing_numerator':self.new_S,
                'packing_defect_budget':self.new_budget,'consumed_packing_defect':self.packing_cost(known),
                'forced_original_class_edits':[len(e) for e in E],
                'known_candidate_values':[[x,known[x]] for x in sorted(known)],
                'candidate_symmetry_assumed':False,'native_solver_trusted':False,'new_W_bound':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--shared',type=Path,required=True)
    p.add_argument('--packing',type=Path,required=True);p.add_argument('--trace',type=Path,required=True);p.add_argument('--output',type=Path)
    a=p.parse_args();ctx=Context(a.base,a.shared,a.packing);out=ctx.check(json.loads(a.trace.read_text()))
    if a.output:a.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='known_candidate_values'}),flush=True)


if __name__=='__main__':main()
