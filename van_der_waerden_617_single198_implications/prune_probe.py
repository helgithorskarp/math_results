"""Propose scoped proof pruning by actual implication dependencies.

Every pruned output must be replayed by check_probe.py. No minimality is claimed.
"""
import argparse
import copy
import json
from pathlib import Path
import base_verify


def prune(base,trace):
    colors,_,premise=base_verify.base_premise(base);data=json.loads(base.read_text())
    D=data['denominator'];S=premise['base_weight_numerator'];N=base_verify.N
    loads=[0]*N
    for a,d,w in data['color0_APs']:
        for aa in [a,N-1-a-6*d]:
            for x in base_verify.actual_ap(aa,d):loads[x]+=w
    caps=trace['caps'];budget=[None if k is None else k*D-S for k in caps]
    initial={x:c for x,c in enumerate(colors) if c>=0 and caps[c] is not None and D-loads[x]>budget[c]}
    if trace['root']!=-1:initial[trace['root']]=1

    def forced(known,c):return [x for x,b in known.items() if colors[x]==c and b!=c]

    def defect_subset(vertices,threshold):
        chosen=set();cost=0
        for x in sorted(vertices,key=lambda x:(-(D-loads[x]),x)):
            if cost>threshold:break
            chosen.add(x);cost+=D-loads[x]
        if cost<=threshold:raise ValueError('Missing strict defect contradiction')
        return chosen

    def terminal_support(terminal,known):
        if terminal is None:raise ValueError('Prune only completed exclusions')
        if terminal['kind']=='mono_AP':return base_verify.actual_ap(*terminal['AP'])
        c=terminal['class'];vertices=forced(known,c)
        if terminal['kind']=='base_defect':return defect_subset(vertices,budget[c])
        if terminal['kind']=='class_cap':
            if len(vertices)<=caps[c]:raise ValueError('Missing strict count contradiction')
            return set(sorted(vertices)[:caps[c]+1])
        raise ValueError('Unknown terminal')

    def scope(rows,terminal,inherited):
        known=inherited.copy();reasons={};revised=[]
        for row0 in rows:
            row=copy.deepcopy(row0);kind=row['kind'];x=row['point'];b=row['value']
            if x in known:raise ValueError('Fresh facts required')
            if kind=='unit':reason=base_verify.actual_ap(*row['AP'])-{x}
            elif kind=='budget_fix':
                c=colors[x];vertices=forced(known,c);options=[]
                if sum(D-loads[y] for y in vertices)>budget[c]-(D-loads[x]):
                    options.append(defect_subset(vertices,budget[c]-(D-loads[x])))
                if len(vertices)>=caps[c]:options.append(set(sorted(vertices)[:caps[c]]))
                if not options:raise ValueError('Unsupported budget fix')
                reason=min(options,key=lambda v:(len(v),sorted(v)))
            elif kind=='failed_literal':
                trial=row['trial'];local=known.copy();local[x]=1-b
                trimmed,external=scope(trial['steps'],trial['terminal'],local)
                trial['steps']=trimmed;reason=external-{x}
                if not reason<=set(known):raise ValueError('Trial facts leaked out of scope')
            else:raise ValueError('Unknown proof step')
            if not reason<=set(known):raise ValueError('Every dependency must already be known')
            reasons[x]=reason;known[x]=b;revised.append(row)
        needed=set(terminal_support(terminal,known));pending=list(needed)
        while pending:
            x=pending.pop()
            for y in reasons.get(x,set()):
                if y not in needed:needed.add(y);pending.append(y)
        kept=[row for row in revised if row['point'] in needed]
        external=needed-set(reasons)
        if not external<=set(inherited):raise ValueError('All proof leaves must be actual inherited facts')
        return kept,external

    out=copy.deepcopy(trace);out['steps'],external=scope(trace['steps'],trace['terminal'],initial)
    return out,{'initial_fact_dependencies':len(external),'original_top_steps':len(trace['steps']),'pruned_top_steps':len(out['steps'])}


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--trace',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    out,info=prune(a.base,json.loads(a.trace.read_text()))
    a.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(info))


if __name__=='__main__':main()
