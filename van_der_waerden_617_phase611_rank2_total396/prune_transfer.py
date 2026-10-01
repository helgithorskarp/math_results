"""Untrusted logical dependency pruning; every output is checked independently."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import resource
import time
import base_verify
import check_probe
import check_rank2
import check_transfer
import prune_probe


def prune(ctx,trace):
    def forced(known,c):return [x for x,b in known.items() if ctx.colors[x]==c and b!=c]

    def subset(vertices,delta,threshold):
        chosen=set();cost=0
        for x in sorted(vertices,key=lambda x:(-delta(x),x)):
            if cost>threshold:break
            chosen.add(x);cost+=delta(x)
        if cost<=threshold:raise ValueError('Missing strict defect support')
        return chosen

    def terminal_support(node,known):
        if node['kind']=='mono_AP':return base_verify.actual_ap(*node['AP'])
        c=node['class'];E=forced(known,c)
        if node['kind']=='base_defect':return subset(E,lambda x:ctx.D-ctx.loads[x],ctx.budgets[c])
        if node['kind']=='packing_defect':return subset([x for x in E if x in ctx.new_V],lambda x:ctx.new_D-ctx.new_loads[x],ctx.new_budget)
        if node['kind']=='class_cap':return set(sorted(E)[:ctx.caps[c]+1])
        raise ValueError('Unknown terminal support')

    def scope(rows,terminal,inherited):
        # Stop at the first independently available packing contradiction.
        # The proposer may have continued its ordinary AP closure beyond it.
        probe=inherited.copy();cost=ctx.packing_cost(probe);prefix=0
        if cost<=ctx.new_budget:
            for prefix,row in enumerate(rows,1):
                x=row['point'];b=row['value'];probe[x]=b
                if x in ctx.new_V and b!=ctx.packing_class:cost+=ctx.new_D-ctx.new_loads[x]
                if cost>ctx.new_budget:break
        if cost>ctx.new_budget:
            rows=rows[:prefix];terminal={'kind':'packing_defect','class':ctx.packing_class}
        known=inherited.copy();reasons={};revised=[]
        for row0 in rows:
            row=copy.deepcopy(row0);x=row['point'];b=row['value'];kind=row['kind']
            if x in known:raise ValueError('Fresh proof facts required')
            if kind=='unit':reason=base_verify.actual_ap(*row['AP'])-{x}
            elif kind=='budget_fix':
                c=ctx.colors[x];E=forced(known,c);options=[]
                threshold=ctx.budgets[c]-(ctx.D-ctx.loads[x])
                if sum(ctx.D-ctx.loads[y] for y in E)>threshold:
                    options.append(subset(E,lambda y:ctx.D-ctx.loads[y],threshold))
                if len(E)>=ctx.caps[c]:options.append(set(sorted(E)[:ctx.caps[c]]))
                if x in ctx.new_V:
                    F=[y for y in E if y in ctx.new_V];threshold=ctx.new_budget-(ctx.new_D-ctx.new_loads[x])
                    if sum(ctx.new_D-ctx.new_loads[y] for y in F)>threshold:
                        options.append(subset(F,lambda y:ctx.new_D-ctx.new_loads[y],threshold))
                if not options:raise ValueError('Unsupported unchanged fact')
                reason=min(options,key=lambda v:(len(v),sorted(v)))
            elif kind=='failed_literal':
                sub=row['trial'];local=known.copy();local[x]=1-b
                sub['steps'],external,sub['terminal']=scope(sub['steps'],sub['terminal'],local);reason=external-{x}
            else:raise ValueError('Unknown deduction kind')
            if not reason<=set(known):raise ValueError('Only prior actual facts can support a deduction')
            reasons[x]=reason;known[x]=b;revised.append(row)
        needed=set(terminal_support(terminal,known));pending=list(needed)
        while pending:
            x=pending.pop()
            for y in reasons.get(x,set()):
                if y not in needed:needed.add(y);pending.append(y)
        external=needed-set(reasons)
        if not external<=set(inherited):raise ValueError('A local fact escaped its scope')
        return [row for row in revised if row['point'] in needed],external,terminal

    if trace['root']!=-1:raise ValueError('Root-free transfer proof required')
    out=dict(trace)
    # Each proposed pruned terminal is independently checked. Use a strict
    # packing contradiction when available; otherwise retain the actual one.
    checked=ctx.check(trace);known=dict(checked['known_candidate_values'])
    if not checked['excluded']:raise ValueError('An actual checked exclusion is required')
    if ctx.packing_cost(known)>ctx.new_budget:out['terminal']={'kind':'packing_defect','class':ctx.packing_class}
    ctx.terminal(out['terminal'],known,True)
    out['steps'],external,out['terminal']=scope(trace['steps'],out['terminal'],ctx.known)
    return out,external


def encode(path,data):
    raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--shared',type=Path,required=True)
    p.add_argument('--packing',type=Path,required=True);p.add_argument('--trace',type=Path,required=True);p.add_argument('--outdir',type=Path,required=True)
    a=p.parse_args();a.outdir.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    ctx=check_transfer.Context(a.base,a.shared,a.packing);trace=json.loads(a.trace.read_text())
    if trace['root']!=-1:raise ValueError('This reduction has no root hypothesis')
    reduced,external=prune(ctx,trace);cert=json.loads(a.packing.read_text());H=set(external)
    full_loads=[0]*3704
    for aa,d,w in cert['AP_weights']:
        A=base_verify.actual_ap(aa,d)
        if not all(ctx.colors[x]==0 for x in A):raise ValueError('Original0 AP premise required here')
        for x in A:full_loads[x]+=w
    common=set()
    for triple,w in cert['triple_weights']:
        sets=[base_verify.actual_ap(*ap) for ap in triple]
        if not all(ctx.colors[x]==0 for A in sets for x in A):raise ValueError('Original0 triple premise required here')
        common|=set.intersection(*sets)
        for x in set.union(*sets):full_loads[x]+=w
    overloaded={x for x,L in enumerate(full_loads) if L>cert['denominator']}
    H|=common|overloaded
    if not H<=set(ctx.known):raise ValueError('Every needed shared fact was actually proved')
    old_shared=json.loads(a.shared.read_text());shared,info=prune_probe.prune(a.base,old_shared,targets=H)
    shared_path=a.outdir/'shared.json';shared_sha=encode(shared_path,shared)
    shared_result=check_probe.check(a.base,shared)
    for x in H:
        if dict(shared_result['known_candidate_values']).get(x)!=ctx.known[x]:raise ValueError('Required actual shared fact lost')
    cert['shared_trace_sha256']=shared_sha;packing_path=a.outdir/'packing.json';packing_sha=encode(packing_path,cert)
    reduced['shared_trace_sha256']=shared_sha;reduced['packing_sha256']=packing_sha
    trace_path=a.outdir/'trace.json';trace_sha=encode(trace_path,reduced)
    new=check_transfer.Context(a.base,shared_path,packing_path);result=new.check(reduced)
    if not result['excluded']:raise ValueError('Pruned proof must still actually contradict the box')
    (a.outdir/'exact.json').write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    summary={'agent':'six-vdw-3','role':'researcher','required_shared_fact_targets':len(H),'transfer_shared_leaves':len(external),
             'triple_common_positions':len(common),'full_domain_overloaded_positions':len(overloaded),
             'shared_pruning':info,'shared_fixed_positions':len(new.known),'pruned_transfer_top_rows':len(reduced['steps']),
             'shared_sha256':shared_sha,'packing_sha256':packing_sha,'trace_sha256':trace_sha,
             'bytes':{p.name:p.stat().st_size for p in [shared_path,packing_path,trace_path]},
             'exact_steps':result['steps_checked'],'excluded':result['excluded'],
             'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'no_logical_minimality_claim':True}
    (a.outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
