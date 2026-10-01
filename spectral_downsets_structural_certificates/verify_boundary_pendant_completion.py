"""Independent literal boundary blocks/trades, complete Schur/gaps and full LDL.

Finite evidence validates implementation, not the separate all-order proof.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import argparse

import boundary_pendant_completion as build
import verify_linear_pendant_completion as linear_check
from affine_pendant_completion import geometry, add_pendants
from verify import check, psd_ldl, require
from verify_linear_pendant_completion import labeled_three_point_downsets


def construct(D, c):
    s, S, B = geometry(D, c)
    E = [0] + B
    t = len(E)
    require(t > s >= 1, 'Strictly unbalanced input required')
    r = t
    k, b, n = s + t, 2*t, len(D) + 2*t
    delta = t - s
    p = [1 << (max(D).bit_length() + j) for j in range(t)]
    z = [a | (1 << c) for a in p]
    family = add_pendants(D, c, t)
    ix = {a:i for i,a in enumerate(family)}
    u, v, w = F(1,t), F(k,b*t), F(delta,b*(t-1))
    mu = F(delta,b)
    g = F(8,15)
    Rbound = 2*s+4*(t-1)
    kappa = F(4*s*k,t*(t+3*s))
    eps = min(g*kappa/(8*b*Rbound**2),v/(2*s),u/2,mu/(2*t))
    tau = b*eps*kappa/2
    M0 = [[F(0)]*n for _ in family]
    def put(a,d,value):
        M0[ix[a]][ix[d]] = M0[ix[d]][ix[a]] = value
    for a in S:
        for q in p: put(a,q,u)
    for q in z:
        for a in E: put(q,a,v)
    for i in range(t):
        for j in range(t):
            if i!=j: put(z[i],p[j],w)
    for a in E:
        for q in p: put(a,q,mu/t)
    R = [[F(0)]*n for _ in family]
    def trade(a,d,amount):
        R[ix[a]][ix[d]] += amount
        if a!=d: R[ix[d]][ix[a]] += amount
    for a in S:
        for x,d,amount in ((0,a,1),(z[0],p[1],1),(a,p[1],-1),(z[0],0,-1)):
            trade(x,d,amount)
    for a in E[1:]:
        for x,d,amount in ((0,a,1),(0,p[0],1),(p[0],a,-1),(0,0,-2)):
            trade(x,d,amount)
    M = [[M0[i][j]+eps*R[i][j] for j in range(n)] for i in range(n)]
    H = [2*t if a in S else -2*s if a in z else k if a in E else -k for a in family]
    meta = dict(original_N=len(D),original_s=s,t=t,r=t,k=k,b=b,N=n,delta=delta,
                u=u,v=v,w=w,mu=mu,g=g,Rbound=Rbound,kappa=kappa,epsilon=eps,lower_gap=tau)
    return family,M0,R,M,H,meta


def audit(D,c):
    family,M0,R,M,H,meta = construct(D,c)
    producer = build.completion(D,c)
    require(producer['family']==family, 'Closed/literal geometry differs')
    require(build.dense_entries(producer,'raw')==M0
            and build.dense_entries(producer,'repair')==R
            and build.dense_entries(producer)==M,
            'Complete raw/repair/final oracle replay differs')
    require(producer['lower_gap']==meta['lower_gap']
            and producer['epsilon']==meta['epsilon'], 'Quantitative producer constants differ')
    n,k,b,t,s = (meta[x] for x in ('N','k','b','t','original_s'))
    star = [i for i,a in enumerate(family) if a>>c&1]
    outside = [i for i in range(n) if i not in star]
    oldE = [j for j,i in enumerate(outside) if family[i] in D]
    newP = [j for j in range(b) if j not in oldE]
    one = [1]*n
    q = [b if i in star else -k for i in range(n)]
    def mv(A,x): return [sum(a*d for a,d in zip(row,x)) for row in A]
    def quadratic(A,x): return sum(a*d for a,d in zip(x,mv(A,x)))
    PZ = [[F(i==j)-F(int(i in star and j in star),k)
           -F(int(i in outside and j in outside),b) for j in range(n)] for i in range(n)]
    Hnorm = sum(a*a for a in H)
    require(Hnorm==2*t*k*(t+3*s), 'Boundary kernel norm differs')
    require(sum(H)==sum(a*d for a,d in zip(H,q))==0,'Boundary mode not in Z0')
    PH = [[F(H[i]*H[j],Hnorm) for j in range(n)] for i in range(n)]
    L0 = [[b*M0[i][j]+F(k*(i==j)) for j in range(n)] for i in range(n)]
    require(mv(L0,H)==[0]*n and mv(L0,q)==[0]*n,'Raw lower kernel differs')
    require(check(family,M0,k,upper=True)==n-2,'Raw lower rank differs')
    require(psd_ldl([[F(i==j)-M0[i][j] for j in range(n)] for i in range(n)])==n-1,
            'Raw upper rank differs')
    psd_ldl([[L0[i][j]-meta['g']*(PZ[i][j]-PH[i][j]) for j in range(n)] for i in range(n)])
    X = [[M0[i][j] for j in outside] for i in star]
    Y = [[F(int((i in oldE and j in newP) or (j in oldE and i in newP)),t)
          for j in range(b)] for i in range(b)]
    Q = [[F(k*(i==j))+meta['delta']*Y[i][j]
          -F(b*b,k)*sum(X[a][i]*X[a][j] for a in range(k))
          for j in range(b)] for i in range(b)]
    PE = [[F(i==j and i in oldE)-F(int(i in oldE and j in oldE),t)
           for j in range(b)] for i in range(b)]
    PP = [[F(i==j and i in newP)-F(int(i in newP and j in newP),t)
           for j in range(b)] for i in range(b)]
    psi = k-F(meta['delta']**2,(t-1)**2*k)
    require(Q==[[k*PE[i][j]+psi*PP[i][j] for j in range(b)] for i in range(b)],
            'Complete singular Schur identity differs')
    require(psi>=F(8,3) and psd_ldl(Q)==b-2,'Complete Schur rank/gap differs')
    psd_ldl([[Q[i][j]-F(8,3)*(PE[i][j]+PP[i][j]) for j in range(b)] for i in range(b)])
    require(mv(R,one)==mv(R,q)==[0]*n,'Repair changes endpoints')
    require(max(sum(abs(x) for x in row) for row in R)<=meta['Rbound'],'Repair norm differs')
    require(quadratic(R,H)==8*s*k*k==meta['kappa']*Hnorm,'Boundary rank-lifting mass differs')
    require(check(family,M,k,upper=True)==n-1,'Final lower rank differs')
    require(psd_ldl([[F(i==j)-M[i][j] for j in range(n)] for i in range(n)])==n-1,
            'Final upper rank differs')
    require(all(M[i][j]>=0 for i in range(n) for j in range(i+1,n)), 'Negative off-diagonal')
    require(min(M[0][1:])>=meta['epsilon'],'Empty margin differs')
    for A in (M0,M):
        require(mv(A,one)==one and mv(A,q)==[-F(k,b)*x for x in q],'Endpoints differ')
    psd_ldl([[b*M[i][j]+F(k*(i==j))-meta['lower_gap']*PZ[i][j]
              for j in range(n)] for i in range(n)])
    psd_ldl([[F(i==j)-M[i][j]-meta['epsilon']*(F(i==j)-F(1,n))
              for j in range(n)] for i in range(n)])
    # Literal addition of the omitted new-P triangles tests the old repair failure.
    oldR = [row[:] for row in R]
    newpoints = [family[outside[i]] for i in newP]
    ix = {a:i for i,a in enumerate(family)}
    for a in newpoints[1:]:
        for x,d,amount in ((0,a,1),(0,newpoints[0],1),(newpoints[0],a,-1),(0,0,-2)):
            oldR[ix[x]][ix[d]] += amount
            if x!=d: oldR[ix[d]][ix[x]] += amount
    oldmass = quadratic(oldR,H)
    require(oldmass==8*k*k*(1-meta['delta']), 'Old-repair obstruction mass differs')
    require(oldmass<0 or (oldmass==0 and any(mv(oldR,H))),'Old-repair obstruction missing')
    record = {key:(str(value) if isinstance(value,F) else value) for key,value in meta.items()}
    record.update(center=c,original_family=D,raw_lower_rank=n-2,final_lower_rank=n-1,
                  upper_rank=n-1,empty_margin=str(min(M[0][1:])),H_squared_norm=Hnorm,
                  old_repair_H_quadratic=str(oldmass),full_singular_Schur_and_buffer=True,
                  complete_raw_repair_final_entry_replays=3*n*n,
                  whole_raw_final_and_buffered_LDL=True,
                  matrix_sha256=hashlib.sha256(json.dumps([[str(a) for a in row] for row in M],
                                                        separators=(',',':')).encode()).hexdigest())
    return record


def audit_above(D,c,r):
    independent = linear_check.audit(D,c,r)
    family,raw,repair,final,meta = linear_check.construct(D,c,r)
    producer = build.completion(D,c,r)
    require(producer['construction']=='above-boundary' and producer['family']==family,
            'Above-boundary dispatch differs')
    require(build.dense_entries(producer,'raw')==raw
            and build.dense_entries(producer,'repair')==repair
            and build.dense_entries(producer)==final, 'Above-boundary literal/oracle replay differs')
    n=meta['N']; eps=meta['epsilon']
    require(all(final[i][j]>=0 for i in range(n) for j in range(i+1,n)),
            'Above-boundary off-diagonal sign differs')
    psd_ldl([[F(i==j)-final[i][j]-eps*(F(i==j)-F(1,n))
              for j in range(n)] for i in range(n)])
    independent.update(final_empty_star_upper_gap=str(eps),full_empty_star_upper_buffer=True)
    return independent


def rejection_controls():
    controls=[lambda:build.completion([0,1,2],0,1),
              lambda:build.completion([0,1,2],0,True),
              lambda:build.completion([0,1,2],0,2.0),
              lambda:build.completion([0,1,2],0,-1),
              lambda:build.completion([0,1],0),
              lambda:build.completion(list(range(4)),0,3),
              lambda:build.completion([0,1,3,4],0),
              lambda:build.completion([0,1,2,3,4],2),
              lambda:build.completion([0,1,2],2),
              lambda:build.completion([0,1,2],True)]
    good=build.completion([0,1,2],0)
    controls.extend([lambda:good['entry'](0,True),lambda:good['entry'](0,32),
                     lambda:build.dense_entries(good,'unknown'),
                     lambda:build.dense_entries(good,limit=2)])
    for f in controls:
        try:f()
        except ValueError:pass
        else:raise ValueError('Invalid boundary-recipe input accepted')
    return len(controls)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true')
    args=parser.parse_args();cohort=[];inputs=0
    for D in labeled_three_point_downsets():
        s=max(sum(bool(a>>c&1) for a in D) for c in range(3))
        if len(D)==2*s: continue
        inputs+=1
        for c in range(3):
            if sum(bool(a>>c&1) for a in D)==s: cohort.append(audit(D,c))
    require(inputs==8 and len(cohort)==18,'Complete nonbalanced input/center count differs')
    extras=[]
    for E0,E1 in [([0,1,2,4,5],[0,2,4]),
                  ([a for a in range(16) if a.bit_count()<=2],[0,1,2,4,8])]:
        D=sorted([a<<1 for a in E0]+[(a<<1)|1 for a in E1]);extras.append(audit(D,0))
    extras.append(audit(list(range(15)),0))
    extras.append(audit([0,1,8,16],4))
    above=[audit_above([0,1,2],0,3),audit_above(extras[0]['original_family'],0,6)]
    result=dict(agent='six-downset-1',role='researcher',
                theorem_scope='finite implementation validation for separate ordinary boundary proof',
                nonbalanced_three_point_inputs=inputs,maximum_center_choices=len(cohort),
                cohort=cohort,extra=extras,above_boundary=above,rejected_controls=rejection_controls())
    result['canonical_sha256']=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if args.check:
        expected=json.loads(Path(__file__).with_name('boundary_pendant_expected.json').read_text())
        require(result==expected,'Whole boundary-count output differs from frozen fixture')
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__': main()
