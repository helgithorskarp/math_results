"""six-vdw-3, researcher: discovery for exact spatial AP-weight cuts.

Positive certificates need no solver optimum or exhaustive AP enumeration.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time

P, N, C = 617, 3704, 1852


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


def discover(aps, lo, hi, cap, seconds):
    import highspy as hs
    import numpy as np
    h = hs.Highs()
    opts = {'threads':1,'parallel':'off','output_flag':False,'solver':'ipm',
            'run_crossover':'on','time_limit':seconds,'random_seed':0,
            'primal_feasibility_tolerance':1e-9,
            'dual_feasibility_tolerance':1e-9,'ipm_optimality_tolerance':1e-9}
    for k,v in opts.items():
        if h.setOptionValue(k,v) != hs.HighsStatus.kOk:
            raise RuntimeError('Solver option '+k)
    lp = hs.HighsLp()
    m = len(aps)
    lp.num_col_,lp.num_row_ = m+1,N
    lp.col_cost_ = np.array([-1.0]*m+[float(cap)])
    lp.col_lower_,lp.col_upper_ = np.zeros(m+1),np.full(m+1,hs.kHighsInf)
    lp.row_lower_ = np.full(N,-hs.kHighsInf)
    lp.row_upper_ = np.array([0.0 if lo <= x < hi else 1.0 for x in range(N)])
    lp.a_matrix_.format_ = hs.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.array([7*i for i in range(m+1)]+[7*m+N],dtype=np.int32)
    lp.a_matrix_.index_ = np.array([a+j*d for a,d in aps for j in range(7)]+list(range(N)),dtype=np.int32)
    lp.a_matrix_.value_ = np.array([1.0]*(7*m)+[-1.0]*N)
    if h.passModel(lp) != hs.HighsStatus.kOk:
        raise RuntimeError('Model load')
    h.run()
    sol = h.getSolution()
    if not sol.value_valid or not all(math.isfinite(x) for x in sol.col_value):
        raise RuntimeError('No finite guidance; no exclusion established')
    return sol.col_value,{'solver':h.version(),'numpy':np.__version__,
            'python':sys.version.split()[0],'options':opts,
            'status':h.modelStatusToString(h.getModelStatus()),
            'floating_objective':-h.getObjectiveValue(),
            'floating_mu':sol.col_value[-1]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('phase',type=int)
    ap.add_argument('certificate',type=Path)
    ap.add_argument('--inner',type=int,nargs=2,default=[1287,2417])
    ap.add_argument('--budget',type=int,default=196)
    ap.add_argument('--seconds',type=float,default=15)
    ap.add_argument('--guidance',type=Path)
    args = ap.parse_args()
    lo,hi = args.inner
    if not (0 <= args.phase < P and 0 <= lo < hi <= N and lo+hi == N
            and 0 <= args.budget <= N and 0 < args.seconds <= 60):
        raise ValueError('Phase, symmetric band, budget or bounded time')
    begin = time.monotonic()
    aps = edges(args.phase)
    vals,meta = discover(aps,lo,hi,args.budget,args.seconds)
    den = 1000000
    weights = [max(0,math.floor(v*den)) for v in vals[:-1]]
    loads = [0]*N
    for (a,d),num in zip(aps,weights):
        if num:
            for j in range(7):
                loads[a+j*d] += num
    mu = max(0,max(loads[lo:hi]),max(loads[:lo]+loads[hi:])-den
             if lo > 0 or hi < N else 0)
    cert = {'format':'QR617_SPATIAL_WEIGHTS_1','P':P,'N':N,'terms':7,'seam':C,
            's':args.phase,'t':(1-args.phase)%P,'g':1,'inner':[lo,hi],
            'denominator':den,'mu_numerator':mu,
            'color0_APs':sorted([a,d,num] for (a,d),num in zip(aps,weights) if num)}
    raw = (json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n').encode()
    tmp = args.certificate.with_suffix('.partial')
    tmp.write_bytes(raw);os.replace(tmp,args.certificate)
    meta.update({'agent':'six-vdw-3','role':'researcher','phase':args.phase,
                 'input_color0_APs':len(aps),'positive_color0_APs':len(cert['color0_APs']),
                 'discovery_budget':args.budget,'seconds':time.monotonic()-begin,
                 'certificate_sha256':hashlib.sha256(raw).hexdigest(),
                 'certificate_bytes':len(raw),'status_of_proof':'REQUIRES_EXACT_CHECK'})
    if args.guidance:
        args.guidance.write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta),flush=True)


if __name__ == '__main__':
    main()
