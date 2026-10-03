"""Fresh exact closed phase4 conditional contact duals.

Reuses only pinned exact polynomial primitives from public local9677.
No old contacts, receiver cell, nonlinear bounds or source forest is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,importlib.util,time
import geometry as g
Q,a=g.Q,g.a
path=g.BASE/'whole_phase56_collar/algebra.py'
g.require(hashlib.sha256(path.read_bytes()).hexdigest()=='8a9939d9b6e5db7d2bb86fb656efcc43ca295afb82a24c209992aa51fa16486a','before-import exact polynomial primitive pin')
spec=importlib.util.spec_from_file_location('credited_9677_exact_polynomials',path);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
FANS=[[0,1,2]]
TARGETS=list(product(range(3),(-1,1)))

def basis_record(fan,axis,sign,contacts,bound=None):
    start=time.monotonic()
    g.require(type(fan) is int and fan in range(1) and (axis,sign) in TARGETS,'actual closed fan and signed physical torque target')
    g.require(len(contacts)==5 and len({tuple(c) for c in contacts})==5,'five distinct literal original contacts')
    for i,j,k in contacts:g.require((i,j) in g.EDGES and k in (i,j),'literal persistent endpoint of actual original support')
    tri=[g.PENT[i] for i in FANS[fan]];corners=[];height_corners=[];normal_z=[]
    for v in tri:
        normals=[a.cross(a.sub(g.V[j],g.V[i]),g.raw(v)) for i,j,k in contacts]
        corners.append(tuple(zip(*(tuple(a.cross(g.V[k],m))+tuple(m[:2]) for m,(i,j,k) in zip(normals,contacts)))))
        height_corners.append([a.dot(m,g.V[k]) for m,(i,j,k) in zip(normals,contacts)]);normal_z.append([m[2] for m in normals])
    g.require(all(h>0 for hs in height_corners for h in hs),'fresh closed-fan positive contact heights')
    M=[[p.linear([B[r][k] for B in corners]) for k in range(5)] for r in range(5)]
    hs=[p.linear([h[k] for h in height_corners]) for k in range(5)];mz=[p.linear([m[k] for m in normal_z]) for k in range(5)]
    D=p.det(M);target=tuple(Q(sign*int(k==axis)) for k in range(5));Ns=[]
    for k in range(5):
        C=[[({p.ZERO:target[r]} if target[r]!=0 else {}) if i==k else M[r][i] for i in range(5)] for r in range(5)];Ns.append(p.det(C))
    for r in range(5):
        lhs={}
        for k in range(5):lhs=p.add(lhs,p.mul(M[r][k],Ns[k]))
        g.require(lhs==p.scale(D,target[r]),'entire literal homogeneous torque and two-force identity')
    force_z={}
    for k in range(5):force_z=p.add(force_z,p.mul(mz[k],Ns[k]))
    g.require(force_z=={},'entire literal third spatial force polynomial identity')
    center=(Q(F(1,3)),)*3;d0=p.value(D,center);g.require(d0!=0,'nonzero exact point contact determinant')
    orientation=1 if d0>0 else -1;D=p.scale(D,orientation);Ns=[p.scale(N,orientation) for N in Ns]
    dc=p.controls(D,5);nc=[p.controls(N,4) for N in Ns]
    g.require(min(z for e,z in dc)>0,'all21 closed-fan determinant Bernstein controls strict')
    g.require(min(z for cs in nc for e,z in cs)>=0,'all75 closed-fan cofactor controls nonnegative including boundary ties')
    mass={}
    for N,h in zip(Ns,hs):mass=p.add(mass,p.mul(N,h))
    if bound is None:
        # Exact integer ceiling search on literal coefficients, never rounded ratios.
        bound=1
        while min(z for e,z in p.controls(p.add(p.scale(D,bound),p.scale(mass,-1)),5))<=0:
            bound+=1
            g.require(bound<=100,'bounded mass construction budget exhausted: not mathematical infeasibility')
    g.require(type(bound) is int and bound>0,'positive literal normalized-mass bound')
    bc=p.controls(p.add(p.scale(D,bound),p.scale(mass,-1)),5)
    g.require(min(z for e,z in bc)>0,'all21 strict normalized closed-fan mass controls')
    fixtures=[(Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)),center,
              (Q(F(1,2)),Q(F(1,2)),Q()),(Q(),Q(F(1,2)),Q(F(1,2))),(Q(F(1,2)),Q(),Q(F(1,2)))]
    for t in fixtures:
        B=tuple(tuple(sum((t[v]*corners[v][r][k] for v in range(3)),Q()) for k in range(5)) for r in range(5));dd=p.directdet(B)
        g.require(p.value(D,t)==orientation*dd,'independent direct Gaussian determinant comparison')
        weights=g.act(p.inverse(B),target)
        g.require(tuple(p.value(N,t)/p.value(D,t) for N in Ns)==weights,'independent full exact inverse/Cramer comparison')
        normals=[a.cross(a.sub(g.V[j],g.V[i]),g.raw(tuple(sum((t[v]*tri[v][k] for v in range(3)),Q()) for k in range(2)))) for i,j,k in contacts]
        g.require(tuple(sum((weights[k]*normals[k][j] for k in range(5)),Q()) for j in range(3))==g.Z,'independent literal three spatial-force point comparison')
    controls=[[[list(e),g.enc(z)] for e,z in cs] for cs in [dc,*nc,bc]]
    return {'agent':'six-rupert-2','role':'researcher','closed_fan':fan,'closed_fan_vertex_indices':FANS[fan],'axis':axis,'sign':sign,
            'literal_original_contacts':contacts,'strict_normalized_mass_upper':bound,'exact_control_count':117,
            'all_six_literal_spatial_polynomial_identities':True,'control_stream_sha256':g.digest(controls),
            'minimum_determinant_control':g.enc(min(z for e,z in dc)),'minimum_cofactor_control':g.enc(min(z for cs in nc for e,z in cs)),
            'minimum_strict_mass_bound_control':g.enc(min(z for e,z in bc)),
            'zero_cofactor_controls':[[k,list(e)] for k,cs in enumerate(nc) for e,z in cs if z==0],
            'independent_direct_matrix_fixtures':len(fixtures),'wall_seconds':time.monotonic()-start}
