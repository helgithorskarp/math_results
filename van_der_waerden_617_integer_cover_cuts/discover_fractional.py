"""Rational primal discovery for the screened original-monochromatic relaxation.

Numerical guidance is repaired and must be checked independently. This
produces no binary edit set or AP-free coloring.
"""
import argparse
import hashlib
import json
import math
import importlib.util
from pathlib import Path
import resource
import sys
import time


def build_instance():
    source=Path(__file__).resolve().parent/'base'
    raw=(source/'certificates/phase-184.json').read_bytes();base=json.loads(raw)
    spec=importlib.util.spec_from_file_location('base_exact',source/'verify.py')
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    _,loads=v.check(base,[196],return_loads=True)
    s,t=184,434;D,u=base['denominator'],base['mu_numerator'];lo,hi=base['inner']
    delta=196*u+55*D-sum(a[2] for a in base['color0_APs'])
    squares={r*r%617 for r in range(1,617)}
    colors=[];eligible=[];defects=[];far=[]
    for x in range(3704):
        r=(x-1852+(s if x<1852 else t))%617
        c=-1 if r==0 else int(r not in squares)^int(x>=1852);colors.append(c)
        if c==0:
            defect=u+(0 if lo<=x<hi else D)-loads[x]
            if defect<=delta:
                eligible.append(x);defects.append(defect);far.append(int(not lo<=x<hi))
    positions={x:i for i,x in enumerate(eligible)}
    aps=[(a,d) for d in range(1,618) for a in range(3704-6*d)
         if all(colors[a+j*d]==0 for j in range(7))]
    petals=[[positions[x] for x in [a+j*d for j in range(7)] if x in positions] for a,d in aps]
    if len(eligible)!=881 or len(aps)!=3065 or any(not p for p in petals):raise RuntimeError('Unexpected exact instance')
    return {'phase':s,'eligible':eligible,'defects':defects,'far_flags':far,'petals':petals,
            'aggregate_defect_budget':delta,'base_certificate_sha256':hashlib.sha256(raw).hexdigest()}


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    args=p.parse_args()
    args.work.mkdir(parents=True,exist_ok=True)
    instance=build_instance()
    eligible=instance['eligible'];defects=instance['defects'];far=instance['far_flags']
    petals=instance['petals'];n,m=len(eligible),len(petals);begin=time.monotonic()
    import highspy as hs
    import numpy as np
    h=hs.Highs();options={'threads':1,'parallel':'off','output_flag':False,'solver':'ipm',
         'run_crossover':'on','time_limit':15.0,'random_seed':0,
         'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9,
         'ipm_optimality_tolerance':1e-9}
    for k,v in options.items():
        if h.setOptionValue(k,v)!=hs.HighsStatus.kOk:raise RuntimeError('Option '+k)
    columns=[[] for _ in range(n)]
    for ri,petal in enumerate(petals):
        for ci in petal:columns[ci].append((ri,1.0))
    for ci in range(n):
        columns[ci].append((m,1.0))
        if far[ci]:columns[ci].append((m+1,1.0))
        if defects[ci]:columns[ci].append((m+2,float(defects[ci])))
    start=[0];index=[];value=[]
    for col in columns:
        for ri,v in col:index.append(ri);value.append(v)
        start.append(len(index))
    lp=hs.HighsLp();lp.num_col_=n;lp.num_row_=m+3
    lp.col_cost_=np.ones(n);lp.col_lower_=np.zeros(n);lp.col_upper_=np.ones(n)
    lp.row_lower_=np.array([1.0]*m+[-hs.kHighsInf,54.99,-hs.kHighsInf])
    lp.row_upper_=np.array([hs.kHighsInf]*m+[195.99,54.99,float(instance['aggregate_defect_budget'])])
    lp.a_matrix_.format_=hs.MatrixFormat.kColwise;lp.a_matrix_.start_=np.array(start,dtype=np.int32)
    lp.a_matrix_.index_=np.array(index,dtype=np.int32);lp.a_matrix_.value_=np.array(value)
    if h.passModel(lp)!=hs.HighsStatus.kOk:raise RuntimeError('Model load')
    h.run();sol=h.getSolution()
    if not sol.value_valid or not all(math.isfinite(v) for v in sol.col_value):
        raise RuntimeError('No finite guidance;no feasibility claim')
    D=100000000;nums=[min(D,max(0,math.ceil(v*D))) for v in sol.col_value]
    repaired=0
    for petal in petals:
        missing=D-sum(nums[i] for i in petal)
        if missing<=0:continue
        for i in sorted(petal,key=lambda i:(far[i],defects[i],eligible[i])):
            add=min(missing,D-nums[i]);nums[i]+=add;missing-=add;repaired+=add
            if missing==0:break
        if missing:raise RuntimeError('Rational AP repair failed')
    def fill(kind,target):
        current=sum(nums[i] for i in range(n) if far[i]==kind)
        missing=target-current
        if missing<0:raise RuntimeError('Rational budget already exceeded')
        for i in sorted((i for i in range(n) if far[i]==kind),key=lambda i:(defects[i],eligible[i])):
            add=min(missing,D-nums[i]);nums[i]+=add;missing-=add
            if missing==0:break
        if missing:raise RuntimeError('Insufficient point capacity to fill target')
    fill(1,55*D);fill(0,141*D)
    witness={'format':'QR617_FRACTIONAL_HITTING_1','phase':instance['phase'],
         'class_sum':196,'far_sum':55,'denominator':D,
         'base_certificate_sha256':instance['base_certificate_sha256'],
         'position_weights':[[x,num] for x,num in zip(eligible,nums) if num]}
    raw=(json.dumps(witness,sort_keys=True,separators=(',',':'))+'\n').encode()
    (args.work/'fractional-witness.json').write_bytes(raw)
    report={'agent':'six-vdw-3','role':'researcher','status':'REQUIRES_EXACT_INDEPENDENT_CHECK',
            'solver_status':h.modelStatusToString(h.getModelStatus()),'solver':h.version(),
            'numpy':np.__version__,'python':sys.version.split()[0],'options':options,
            'floating_class_objective':h.getObjectiveValue(),'rational_AP_repair_units':repaired,
            'positive_weights':len(witness['position_weights']),'certificate_bytes':len(raw),
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-begin,
            'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'binary_edit_set_claim':False,'AP_free_coloring_claim':False,'solver_trusted':False}
    (args.work/'guidance.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)


if __name__=='__main__':main()
