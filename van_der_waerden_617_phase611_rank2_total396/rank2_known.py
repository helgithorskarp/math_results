"""Numerical guides for exact AP/triple packing on checked inherited domains.

Each native solve is serial, one-thread and limited to15 seconds. Selection
keeps at most20000 violated three-AP rows, with an eight-second loop budget.
No solver status or failure establishes a mathematical exclusion.
"""
import argparse
import hashlib
import heapq
import json
import math
from pathlib import Path
import resource
import time
import highspy
import check_branch

N,P,C=3704,617,1852


def cover_lp(petals,rhs,n):
    columns=[[] for _ in range(n)]
    for i,row in enumerate(petals):
        for x in row:columns[x].append(i)
    starts=[0];indices=[]
    for col in columns:indices.extend(col);starts.append(len(indices))
    lp=highspy.HighsLp();lp.num_col_=n;lp.num_row_=len(petals)
    lp.col_cost_=[1.0]*n;lp.col_lower_=[0.0]*n;lp.col_upper_=[highspy.kHighsInf]*n
    lp.row_lower_=[float(b) for b in rhs];lp.row_upper_=[highspy.kHighsInf]*len(petals)
    matrix=highspy.HighsSparseMatrix();matrix.format_=highspy.MatrixFormat.kColwise
    matrix.num_col_=n;matrix.num_row_=len(petals);matrix.start_=starts;matrix.index_=indices;matrix.value_=[1.0]*len(indices)
    lp.a_matrix_=matrix;h=highspy.Highs()
    for key,value in {'threads':1,'parallel':'off','output_flag':False,'solver':'ipm','run_crossover':'on','time_limit':15.0}.items():
        if h.setOptionValue(key,value)!=highspy.HighsStatus.kOk:raise RuntimeError('Native solver option rejected')
    if h.passModel(lp)!=highspy.HighsStatus.kOk:raise RuntimeError('Native model rejected')
    start=time.monotonic();h.run();elapsed=time.monotonic()-start
    sol=h.getSolution();status=h.getModelStatus();obj=h.getObjectiveValue()
    data={'status':str(status),'objective':obj if math.isfinite(obj) else None,'seconds':elapsed,
          'value_valid':bool(sol.value_valid),'dual_valid':bool(sol.dual_valid)}
    good=status==highspy.HighsModelStatus.kOptimal and sol.value_valid and sol.dual_valid
    if not good:return None,None,data
    values=list(sol.col_value);weights=list(sol.row_dual)
    if len(values)!=n or len(weights)!=len(petals) or not all(math.isfinite(v) for v in values+weights):raise RuntimeError('Incomplete or nonfinite guide')
    return values,weights,data


def select_triples(petals,values,max_triples=20000,seconds=8,candidate_limit=2000000):
    start=time.monotonic();epsilon=1e-7
    # A violated triple cannot include a vertex with value>=1: some one of
    # its three APs misses that vertex, and that AP already has weight>=1.
    active=[i for i,p in enumerate(petals) if all(values[x]<1-epsilon for x in p) and sum(values[x] for x in p)<2-epsilon]
    incidence={}
    for i in active:
        for x in petals[i]:
            if values[x]>epsilon:incidence.setdefault(x,[]).append(i)
    adjacency={i:set() for i in active}
    for rows in incidence.values():
        group=set(rows)
        for i in rows:adjacency[i].update(group-{i})
    masks=[sum(1<<x for x in p) for p in petals];heap=[];tested=valid=violated=0;limited=False
    for i in active:
        if limited:break
        for j in sorted(x for x in adjacency[i] if x>i):
            if limited:break
            for k in sorted(x for x in adjacency[i]&adjacency[j] if x>j):
                if tested>=candidate_limit or time.monotonic()-start>=seconds:limited=True;break
                tested+=1
                if masks[i]&masks[j]&masks[k]:continue
                valid+=1;union=masks[i]|masks[j]|masks[k];bits=union;cost=0.0
                while bits:
                    bit=bits&-bits;bits-=bit;cost+=values[bit.bit_length()-1]
                if cost>=2-epsilon:continue
                violated+=1;item=(-cost,-union.bit_count(),-i,-j,-k)
                if len(heap)<max_triples:heapq.heappush(heap,item)
                elif item>heap[0]:heapq.heapreplace(heap,item)
    chosen=sorted([[-i,-j,-k] for _,_,i,j,k in heap])
    return chosen,{'active_APs':len(active),'positive_fractional_vertices':len(incidence),'triangle_candidates_tested':tested,
                   'valid_empty_intersection_triangles':valid,'violated_triangles':violated,'kept_triples':len(chosen),
                   'selection_limited':limited,'candidate_limit':candidate_limit,'seconds':time.monotonic()-start,
                   'no_mathematical_completeness_or_nonexistence_claim':True}


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--shared',type=Path,required=True)
    p.add_argument('--branch',type=Path);p.add_argument('--class',dest='color',type=int,choices=[0,1],default=0)
    p.add_argument('--rounds',type=int,choices=range(1,5),default=1)
    p.add_argument('--outdir',type=Path,required=True);a=p.parse_args();a.outdir.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();ctx=check_branch.Context(a.base,a.shared,[197,198]);c=a.color;root=-1;branch_sha=None
    known=ctx.known
    if a.branch:
        raw=a.branch.read_bytes();trace=json.loads(raw);checked=ctx.check(trace)
        if checked['excluded']:raise ValueError('Already excluded branch')
        known=dict(checked['known_candidate_values']);root=trace['root'];branch_sha=hashlib.sha256(raw).hexdigest()
    # Independent proposal geometry uses square enumeration and bit shifts.
    phase=json.loads(a.base.read_text())['s'];squares={r*r%P for r in range(1,P)};colors=[]
    for x in range(N):
        r=(x-C+(phase if x<C else (1-phase)%P))%P
        colors.append(-1 if not r else int(r not in squares)^int(x>=C))
    unknown=[x for x in range(N) if colors[x]==c and x not in known];index={x:i for i,x in enumerate(unknown)}
    forced=[x for x,b in known.items() if colors[x]==c and b!=c];residual=ctx.caps[c]-len(forced)
    potential=sum(1<<x for x in range(N) if known.get(x)==c or x in index)
    aps=[];petals=[]
    for d in range(1,(N-1)//6+1):
        mask=(1<<(N-6*d))-1
        for j in range(7):mask&=potential>>(j*d)
        while mask:
            bit=mask&-mask;mask-=bit;aa=bit.bit_length()-1
            petal={index[aa+j*d] for j in range(7) if aa+j*d in index}
            if not petal:raise ValueError('A direct fixed monochromatic AP needs an exact terminal instead of an LP')
            aps.append([aa,d]);petals.append(petal)
    values,weights,baseline=cover_lp(petals,[1]*len(petals),len(unknown))
    summary={'agent':'six-vdw-3','role':'researcher','phase':phase,'caps':ctx.caps,'root':root,'original_class':c,
             'unknown_vertices':len(unknown),'forced_edits':len(forced),'remaining_cap':residual,'mandatory_actual_APs':len(aps),
             'baseline':baseline,'native_limit_seconds':15,'threads':1,'proposal_only':True,'new_W_bound':False}
    if values is None:
        summary['solver_branch_paused']=True
        (a.outdir/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n');print(json.dumps(summary),flush=True);return
    (a.outdir/'baseline-guide.json').write_text(json.dumps({'values':values,'vertices':unknown,'APs':aps,'petals':[sorted(r) for r in petals]},separators=(',',':'))+'\n')
    triples=[];seen=set();rows=list(petals);rhs=[1]*len(aps);rounds=[];paused=False
    for r in range(a.rounds):
        proposed,selection=select_triples(petals,values,max_triples=20000-len(triples))
        fresh=[t for t in proposed if tuple(t) not in seen]
        entry={'round':r+1,'selection':selection,'fresh_triples':len(fresh)}
        rounds.append(entry)
        if not fresh:break
        proposed_rows=rows+[set.union(*(petals[i] for i in t)) for t in fresh]
        proposed_rhs=rhs+[2]*len(fresh)
        next_values,next_weights,augmented=cover_lp(proposed_rows,proposed_rhs,len(unknown));entry['native']=augmented
        if next_values is None:
            paused=True;break
        triples.extend(fresh);seen.update(tuple(t) for t in fresh)
        rows=proposed_rows;rhs=proposed_rhs;values=next_values;weights=next_weights
        if len(triples)>=20000:break
    summary['rounds']=rounds
    summary['augmented']=rounds[-1].get('native') if rounds else None
    (a.outdir/'latest-guide.json').write_text(json.dumps({'values':values,'vertices':unknown,'APs':aps,'petals':[sorted(r) for r in petals],'triples':triples},separators=(',',':'))+'\n')
    D=1000000;nums=[max(0,math.floor(w*D)) for w in weights];loads=[0]*len(unknown)
    for row,w in zip(rows,nums):
        for x in row:loads[x]+=w
    D=max([D]+loads);W=sum(b*w for b,w in zip(rhs,nums))
    certificate={'format':'QR617_KNOWN_RANK2_PACKING_1','phase':phase,'caps':ctx.caps,'root':root,'original_class':c,
                 'base_certificate_sha256':ctx.base_sha,'shared_trace_sha256':ctx.shared_sha,'branch_trace_sha256':branch_sha,
                 'denominator':D,'AP_weights':[ap+[w] for ap,w in zip(aps,nums[:len(aps)]) if w],
                 'triple_weights':[[[aps[i] for i in t],w] for t,w in zip(triples,nums[len(aps):]) if w]}
    encoded=(json.dumps(certificate,sort_keys=True,separators=(',',':'))+'\n').encode();(a.outdir/'packing.json').write_bytes(encoded)
    summary.update({'denominator':D,'weighted_numerator':W,'strict_gap':W-residual*D,
                    'positive_AP_weights':len(certificate['AP_weights']),'positive_triple_weights':len(certificate['triple_weights']),
                    'certificate_sha256':hashlib.sha256(encoded).hexdigest(),'total_seconds':time.monotonic()-start,
                    'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'solver_branch_paused':paused})
    (a.outdir/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
