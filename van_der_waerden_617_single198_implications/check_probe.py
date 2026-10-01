"""Definition-level scoped AP implication checker; no proposer imports."""
import argparse
import hashlib
import json
from pathlib import Path
import base_verify

N=3704
need=base_verify.need


def check(base,trace,zero_tree=None):
    colors,_,summary=base_verify.base_premise(base,zero_tree)
    raw=base.read_bytes();data=json.loads(raw);D=data['denominator'];S=summary['base_weight_numerator']
    schema={'format','phase','caps','root','base_certificate_sha256','steps','terminal','next_cursor'}
    if zero_tree is not None:schema.add('zero_tree_sha256')
    need(type(trace) is dict and set(trace)==schema,'Scoped trace schema')
    if zero_tree is not None:need(trace['zero_tree_sha256']==hashlib.sha256(zero_tree.read_bytes()).hexdigest(),'Actual checked complete zero-loss tree')
    need(trace['format']=='QR617_SCOPED_UNIT_TRACE_1' and type(trace['phase']) is int and trace['phase']==summary['phase'],'Exact scoped trace phase')
    need(trace['base_certificate_sha256']==hashlib.sha256(raw).hexdigest(),'Actual checked base dependency')
    caps=trace['caps'];need(type(caps) is list and len(caps)==2 and all(c is None or type(c) is int and c>=0 for c in caps),'Caps with None explicitly uncapped')
    loads=[0]*N
    for a,d,w in data['color0_APs']:
        for aa in [a,N-1-a-6*d]:
            for x in base_verify.actual_ap(aa,d):loads[x]+=w
    budgets=[None if c is None else c*D-S for c in caps]
    need(all(b is None or b>=0 for b in budgets),'Nonnegative screened packing budgets')
    known={x:c for x,c in enumerate(colors) if c>=0 and caps[c] is not None and D-loads[x]>budgets[c]}
    if zero_tree is not None:
        need(any(k==197 for k in caps),'The zero-loss premise applies only to a capped197 class')
        for c in [0,1]:
            if caps[c]==197:
                for x in summary['zero_loss_premise']['fixed_positions'][c]:known[x]=c
    initial=len(known);root=trace['root']
    need(type(root) is int and (root==-1 or 0<=root<N and colors[root]==0 and root not in known),'Permitted original0 root or none')
    if root!=-1:known[root]=1
    counts={'unit':0,'budget_fix':0,'failed_literal':0,'scoped_trial_unit':0,'scoped_trial_budget_fix':0}

    def forced(known,c):return {x for x,b in known.items() if colors[x]==c and b!=c}

    def terminal(node,known,required):
        if node is None:
            need(not required,'Every failed literal needs a proved contradiction');return False
        need(type(node) is dict and 'kind' in node,'Exact terminal schema')
        if node['kind']=='mono_AP':
            need(set(node)=={'kind','AP'} and type(node['AP']) is list and len(node['AP'])==2,'Actual terminal AP')
            A=base_verify.actual_ap(*node['AP'])
            need(all(x in known for x in A) and len({known[x] for x in A})==1,'Actual monochromatic fixed AP')
        else:
            need(set(node)=={'kind','class'} and type(node['class']) is int and node['class'] in [0,1],'Original-class terminal schema')
            c=node['class'];need(caps[c] is not None,'Unrestricted class cannot yield a cap terminal')
            E=forced(known,c)
            if node['kind']=='class_cap':need(len(E)>caps[c],'Strict forced original-class count')
            elif node['kind']=='base_defect':need(sum(D-loads[x] for x in E)>budgets[c],'Strict aggregate nonnegative packing defect')
            else:raise ValueError('Unknown terminal')
        return True

    def replay(rows,known,trial_scope=False):
        need(type(rows) is list and len(rows)<=N,'Bounded fresh implication sequence')
        for row in rows:
            need(type(row) is dict and row.get('kind') in ['unit','budget_fix','failed_literal'],'Known implication schema')
            kind=row['kind'];x=row.get('point');b=row.get('value')
            need(type(x) is int and 0<=x<N and x not in known and type(b) is int and b in [0,1],'One fresh literal')
            if kind=='unit':
                need(set(row)=={'kind','AP','point','value'} and type(row['AP']) is list and len(row['AP'])==2,'Actual unit AP schema')
                A=base_verify.actual_ap(*row['AP'])
                need(x in A and all(y in known and known[y]==1-b for y in A-{x}),'All six ACTUAL AP predecessors have the opposite value')
            elif kind=='budget_fix':
                need(set(row)=={'kind','point','value'},'Packing fix schema')
                c=colors[x];need(c==b and c>=0 and caps[c] is not None,'Finite original class only')
                E=forced(known,c);cost=sum(D-loads[y] for y in E)
                need(len(E)>=caps[c] or D-loads[x]>budgets[c]-cost,'One more edit strictly violates the count or aggregate defect')
            else:
                need(not trial_scope and set(row)=={'kind','point','value','trial'},'No nested or unscoped trial')
                sub=row['trial'];need(type(sub) is dict and set(sub)=={'assumption','steps','terminal'},'Exact trial scope')
                need(sub['assumption']==[x,1-b] and all(type(v) is int for v in sub['assumption']),'Only the negation of this literal is assumed')
                local=known.copy();local[x]=1-b
                replay(sub['steps'],local,True);terminal(sub['terminal'],local,True)
                # Only the opposite trial assumption is discharged into global facts.
            counts[('scoped_trial_' if trial_scope else '')+kind]+=1
            known[x]=b

    replay(trace['steps'],known);excluded=terminal(trace['terminal'],known,False)
    need(type(trace['next_cursor']) is int and 0<=trace['next_cursor']<=2*N,'Bounded operational cursor, no mathematical coverage inferred')
    E=[forced(known,c) for c in [0,1]]
    return {'agent':'six-vdw-3','role':'researcher','phase':summary['phase'],'caps':caps,'root':root,
            'base_certificate_sha256':summary['base_certificate_sha256'],'base_denominator':D,'base_weight_numerator':S,
            'base_defect_budgets':budgets,'initial_fixed_positions':initial,'steps_checked':counts,
            'terminal':trace['terminal'],'excluded':excluded,'forced_original_class_edits':[len(e) for e in E],
            'consumed_base_defects':[sum(D-loads[x] for x in e) for e in E],
            'forced_poles':sum(colors[x]<0 for x in known),'known_candidate_values':[[x,known[x]] for x in sorted(known)],
            'candidate_symmetry_assumed':False,'new_W_bound':False,'solver_trusted':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--trace',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--zero-tree',type=Path)
    a=p.parse_args();out=check(a.base,json.loads(a.trace.read_text()),a.zero_tree)
    if a.output:a.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='known_candidate_values'}))


if __name__=='__main__':main()
