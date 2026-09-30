"""Guidance for a screened spatial dual with explicit three-AP cover cuts."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time


def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


P,N,C=617,3704,1852

def edges(s):
    sq = {r*r % P for r in range(1, P)}
    t = (1-s) % P
    col = []
    for x in range(N):
        r = (x-C+(s if x < C else t)) % P
        col.append(-1 if r == 0 else int(r not in sq) ^ int(x >= C))
    return [(a,d) for d in range(1,(N-1)//6+1)
            for a in range(max(0,C-6*d),min(C,N-6*d))
            if all(col[a+j*d] == 0 for j in range(7))]


def main():
    p=argparse.ArgumentParser();p.add_argument('--cuts',type=Path,required=True)
    p.add_argument('--certificate',type=Path,required=True);p.add_argument('--guidance',type=Path)
    args=p.parse_args();guide=json.loads(args.cuts.read_text());s=guide['phase'];B,L=guide['class_cap'],guide['far_cap']
    source=Path(__file__).resolve().parent/'base'
    raw=(source/'certificates'/f'phase-{s:03d}.json').read_bytes();base=json.loads(raw)
    v=module(source/'verify.py','base_integer_capacities');_,load=v.check(base,[B],return_loads=True)
    u,D=base['mu_numerator'],base['denominator'];lo,hi=base['inner'];t=base['t']
    delta=B*u+L*D-sum(e[2] for e in base['color0_APs']);assert delta>=0
    allowed=set()
    for x in range(3704):
        r=(x-1852+(s if x<1852 else t))%617
        if r and (v.q[r]^int(x>=1852))==0 and u+(0 if lo<=x<hi else D)-load[x]<=delta:allowed.add(x)
    aps=edges(s)
    columns=[[a+j*d for j in range(7) if a+j*d in allowed] for a,d in aps]
    triples=[]
    for item in guide['cuts']:
        triple=item['triple_APs'];assert len(triple)==3
        petals=[{a+j*d for j in range(7) if a+j*d in allowed} for a,d in triple]
        assert all(petals) and not set.intersection(*petals)
        triples.append(triple);columns.append(sorted(set.union(*petals)))
    begin=time.monotonic()
    import highspy as hs
    import numpy as np
    h=hs.Highs();options={'threads':1,'parallel':'off','output_flag':False,'solver':'ipm',
         'run_crossover':'on','time_limit':15.0,'random_seed':0,
         'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9,'ipm_optimality_tolerance':1e-9}
    for k,value in options.items():assert h.setOptionValue(k,value)==hs.HighsStatus.kOk
    starts=[0];index=[]
    for c in columns:index+=c;starts.append(len(index))
    starts.append(len(index)+3704);m=len(aps);k=len(triples)
    lp=hs.HighsLp();lp.num_col_=m+k+1;lp.num_row_=3704
    lp.col_cost_=np.array([-1.0]*m+[-2.0]*k+[float(B)])
    lp.col_lower_=np.zeros(m+k+1);lp.col_upper_=np.full(m+k+1,hs.kHighsInf)
    lp.row_lower_=np.full(3704,-hs.kHighsInf);lp.row_upper_=np.array([0.0 if lo<=x<hi else 1.0 for x in range(3704)])
    lp.a_matrix_.format_=hs.MatrixFormat.kColwise;lp.a_matrix_.start_=np.array(starts,dtype=np.int32)
    lp.a_matrix_.index_=np.array(index+list(range(3704)),dtype=np.int32)
    lp.a_matrix_.value_=np.array([1.0]*len(index)+[-1.0]*3704)
    assert h.passModel(lp)==hs.HighsStatus.kOk;h.run();sol=h.getSolution()
    if not sol.value_valid or not all(math.isfinite(x) for x in sol.col_value):raise RuntimeError('No finite guidance;no exclusion')
    den=1000000;nums=[max(0,math.floor(x*den)) for x in sol.col_value[:-1]];loads=[0]*3704
    for col,w in zip(columns,nums):
        for x in col:loads[x]+=w
    mu=max(0,max(loads[lo:hi]),max(loads[:lo]+loads[hi:])-den)
    cert={'format':'QR617_SCREENED_COVER2_DUAL_1','phase':s,'class_cap':B,'far_cap':L,
          'base_certificate_sha256':hashlib.sha256(raw).hexdigest(),'denominator':den,
          'mu_numerator':mu,'color0_APs':sorted([a,d,w] for (a,d),w in zip(aps,nums[:m]) if w),
          'color0_cover2':[[triple,w] for triple,w in zip(triples,nums[m:]) if w]}
    output=(json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n').encode();args.certificate.write_bytes(output)
    weight_sum=sum(nums[:m])+2*sum(nums[m:])
    report={'agent':'six-vdw-3','role':'researcher','phase':s,'class_cap':B,'far_cap':L,
            'options':options,'solver':h.version(),'numpy':np.__version__,'python':sys.version.split()[0],
            'status':h.modelStatusToString(h.getModelStatus()),'floating_objective':-h.getObjectiveValue(),
            'floating_mu':sol.col_value[-1],'discovery_cut_numerator':weight_sum-B*mu,
            'discovery_gap_numerator':weight_sum-B*mu-L*den,'D':den,
            'positive_APs':len(cert['color0_APs']),'positive_cover2_cuts':len(cert['color0_cover2']),
            'seconds':time.monotonic()-begin,'certificate_bytes':len(output),
            'certificate_sha256':hashlib.sha256(output).hexdigest(),'proof_status':'REQUIRES_EXACT_INDEPENDENT_CHECK'}
    if args.guidance:args.guidance.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
