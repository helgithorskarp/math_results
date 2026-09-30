"""One-thread LP proposals with original, activated, three- and five-AP rows.

Numerical guidance only. No timeout, lack of a witness or nonpositive gap
proves mathematical exclusion. Domain restrictions need exact chain replay.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import time
import verify

for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[k]='1'


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=int,default=1427)
    p.add_argument('--domain',type=Path,required=True);p.add_argument('--plans',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True)
    p.add_argument('--state',type=Path);p.add_argument('--trial-opposite',type=int)
    p.add_argument('--denominator',type=int,default=1_000_000)
    a=p.parse_args();begin=time.monotonic()
    sq={r*r%617 for r in range(1,617)}
    colors=[]
    for x in range(3704):
        r=(x-1852+(201 if x<1852 else 417))%617
        colors.append(-1 if not r else int(r not in sq)^int(x>=1852))
    if not(0<=a.root<3704 and colors[a.root]==0):raise ValueError('Original0 root required')
    vertices=sorted(json.loads(a.domain.read_text())['permitted_screen'])
    if len(set(vertices))!=len(vertices) or any(colors[x]!=1 for x in vertices):raise ValueError('Distinct original1 domain')
    index={x:i for i,x in enumerate(vertices)}
    aps=[(aa,d) for d in range(1,618) for aa in range(max(0,1852-6*d),min(1852,3704-6*d))
         if all(colors[aa+j*d]==1 for j in range(7))]
    original=len(aps)
    for d in range(1,618):
        for j in range(7):
            aa=a.root-j*d
            if 0<=aa<aa+6*d<3704 and all(colors[aa+k*d]==1 for k in range(7) if k!=j):aps.append((aa,d))
    rows=[{index[x] for x in (aa+j*d for j in range(7)) if x in index} for aa,d in aps]
    if any(not r for r in rows):
        i=next(i for i,r in enumerate(rows) if not r)
        out={'format':'QR617_PHASE201_EMPTY_PETAL_1','phase':201,'root':a.root,
             'domain_sha256':verify.domain_sha(vertices),'AP':list(aps[i])}
        a.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
        a.summary.write_text(json.dumps({'root':a.root,'direct_empty_petal':True,'AP':list(aps[i])})+'\n')
        print(json.dumps(out));return
    plans=json.loads(a.plans.read_text());lookup={ap:i for i,ap in enumerate(aps)}
    proposed=([[[3703-aa-6*d,d] for aa,d in t] for t in plans.get('cover2_triples',[])]+
              plans.get('opposite_cover2_triples',[])+plans.get('opposite_cover3_quintuples',[]))
    bundles=[];rhs=[1]*len(aps);seen=set()
    for bundle in proposed:
        key=tuple(sorted(tuple(ap) for ap in bundle))
        if key in seen:continue
        if len(key) not in (3,5) or len(set(key))!=len(key) or any(ap not in lookup for ap in key):raise ValueError('Invalid planned bundle')
        ps=[rows[lookup[ap]] for ap in key]
        union=set.union(*ps)
        valid=not set.intersection(*ps) if len(key)==3 else all(sum(x in r for r in ps)<=2 for x in union)
        if not valid:continue
        seen.add(key);bundles.append([list(ap) for ap in key]);rows.append(union);rhs.append(2 if len(key)==3 else 3)
    trial=index[a.trial_opposite] if a.trial_opposite is not None else None
    residual_rhs=[b-int(trial is not None and trial in r) for b,r in zip(rhs,rows)]
    kept=[i for i,b in enumerate(residual_rhs) if b>0]
    solve_rows=[rows[i] for i in kept]
    cols=[[] for _ in vertices]
    for i,r in enumerate(solve_rows):
        for x in r:cols[x].append(i)
    starts,indices=[0],[]
    for col in cols:indices.extend(col);starts.append(len(indices))
    import highspy as hs
    import numpy as np
    h=hs.Highs();opts={'threads':1,'parallel':'off','output_flag':False,'solver':'ipm','run_crossover':'on',
                      'time_limit':15.0,'random_seed':0,'primal_feasibility_tolerance':1e-9,
                      'dual_feasibility_tolerance':1e-9,'ipm_optimality_tolerance':1e-9}
    for k,v in opts.items():
        if h.setOptionValue(k,v)!=hs.HighsStatus.kOk:raise RuntimeError('Solver option')
    lp=hs.HighsLp();lp.num_col_,lp.num_row_=len(vertices),len(solve_rows)
    upper=np.ones(len(vertices))
    if trial is not None:upper[trial]=0.0
    lp.col_cost_,lp.col_lower_,lp.col_upper_=np.ones(len(vertices)),np.zeros(len(vertices)),upper
    lp.row_lower_,lp.row_upper_=np.array([residual_rhs[i] for i in kept],dtype=float),np.full(len(solve_rows),hs.kHighsInf)
    lp.a_matrix_.format_=hs.MatrixFormat.kColwise
    lp.a_matrix_.start_,lp.a_matrix_.index_=np.array(starts,dtype=np.int32),np.array(indices,dtype=np.int32)
    lp.a_matrix_.value_=np.ones(len(indices))
    if h.passModel(lp)!=hs.HighsStatus.kOk:raise RuntimeError('Solver model')
    h.run();sol=h.getSolution()
    if not(sol.value_valid and sol.dual_valid) or not all(math.isfinite(w) for w in sol.row_dual):raise RuntimeError('Incomplete guide, no exclusion')
    D=a.denominator
    if not(1<=D<=1_000_000_000):raise ValueError('Bounded positive rounding denominator')
    nums=[0]*len(rows)
    for i,w in zip(kept,sol.row_dual):nums[i]=max(0,math.floor(w*D))
    load=[0]*len(vertices)
    for r,w in zip(rows,nums):
        for x in r:load[x]+=w
    W=sum(b*w for b,w in zip(rhs,nums));nu=sum(max(0,l-D) for l in load)
    out={'format':'QR617_PHASE201_DOMAIN_PACK_1','phase':201,'root':a.root,'denominator':D,
         'domain_sha256':verify.domain_sha(vertices),
         'AP_weights':[[aa,d,w] for (aa,d),w in zip(aps,nums) if w],
         'bundle_weights':[[b,w] for b,w in zip(bundles,nums[len(aps):]) if w],
         'surcharges':[[x,l-D] for x,l in zip(vertices,load) if l>D]}
    encoded=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode()
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(encoded)
    if a.state:
        a.state.write_text(json.dumps({'APs':aps,'petals':[sorted(r) for r in rows[:len(aps)]],
                                      'point_values':list(sol.col_value),'vertices':vertices,
                                      'existing_bundles':bundles},separators=(',',':'))+'\n')
    summary={'agent':'six-vdw-3','role':'researcher','root':a.root,'domain_size':len(vertices),
             'original_mono_APs':original,'activated_APs':len(aps)-original,'valid_triples':sum(len(b)==3 for b in bundles),
             'valid_five_bundles':sum(len(b)==5 for b in bundles),'numerical_objective':h.getObjectiveValue(),
             'weighted_numerator':W,'surcharge_numerator':nu,'gap_to_cap_numerator':W-nu-197*D,
             'solver_status':h.modelStatusToString(h.getModelStatus()),'options':opts,'seconds':time.monotonic()-begin,
             'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'certificate_sha256':hashlib.sha256(encoded).hexdigest(),
             'proposal_only':True,'nonpositive_gap_proves_no_exclusion':True,
             'proposal_opposite_trial':a.trial_opposite,
             'residual_weight_numerator':sum(b*w for b,w in zip(residual_rhs,nums))}
    a.summary.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
