"""Exact local/support preflight for a proposed two-parameter J74 region.

This is not a complete source exclusion: no joint quaternion cut cover is
replayed here. The original published model and six-pose certificate are used.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse, importlib.util, json, sys, time

HERE=Path(__file__).resolve().parent
DEPENDENCIES=json.loads((HERE/'DEPENDENCIES.json').read_text())
for relative,digest in DEPENDENCIES['sha256'].items():
    if __import__('hashlib').sha256((HERE/relative).read_bytes()).hexdigest()!=digest:
        raise ValueError('before-import pinned source changed: '+relative)
P=HERE.parent/'full_source_cap/check.py'
spec=importlib.util.spec_from_file_location('j74_rectangle_original',P)
c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
a,Q=c.a,c.Q
ZERO=c.ZERO
EX=(Q(1),Q(),Q());EY=(Q(),Q(1),Q())

def absvec(v):return tuple(c.absolute(x) for x in v)
def matsum(A,B):return tuple(tuple(x+y for x,y in zip(r,s)) for r,s in zip(A,B))
def norminf(A):return max(sum((c.absolute(x) for x in r),Q()) for r in A)

def preflight(eta,data_override=None):
    started=time.monotonic();data=json.loads((P.parent/'certificate.json').read_text()) if data_override is None else data_override
    c.require(eta==Q(F(1,1000)),'fixed entire raw rectangle halfwidth1/1000')
    u,cycle,N,R2=c.original_geometry()
    s=Q(0,1);aa=(s-1)/4;bb=(s+1)/4;cc=Q(1)/2;Z=Q()
    H=((Q(-1),Z,Z),(Z,Q(-1),Z),(Z,Z,Q(1)))
    A=((bb,aa,cc),(-aa,-cc,bb),(cc,-bb,-aa));B=((-aa,-cc,-bb),(cc,-bb,aa),(-bb,-aa,cc))
    named={c.IDENTITY,H,A,c.matmul(A,H),B,c.matmul(B,H)}
    c.require({c.matrix(x['proper_matrix_rows']) for x in data['poses']}==named,'literal six named base poses')
    c.require(u==((16*s-26)/44,(53-15*s)/44,(-11-s)/44),'literal stated receiving center')
    u2=a.dot(u,u);c.require(u[2]<0 and u[2]*u[2]>u2/4,'unit center has z<-1/2')
    phi=(1+s)/2
    axes=((Q(1),Q(),Q()),(Q(),Q(1),Q()))+tuple(a.scale(1/(2*phi),(Q(1),e*phi,d*phi*phi)) for e,d in ((-1,-1),(-1,1),(1,-1),(1,1)))
    c.require(all(a.dot(v,v)==1 for v in axes),'six original minimum axes are unit')
    c.require(all(a.dot(u,v)*a.dot(u,v)<Q(F(119*119,128*128))*u2 for v in axes),'center projective chord>3/8 from all minimum axes')
    c.require(Q(F(3,8))-3*eta>Q(F(1,3)),'entire normalized rectangle separated from minimum axes')
    c.require(9*Q(F(1,10**9))<eta,'entire old projective chord cap maps inside raw rectangle')
    raw=a.scale(-1/u[2],u)
    c.require(raw[2]==-1,'receiving raw chart z=-1')
    c.local_hypotheses(data,u,cycle,N,R2)
    corners=[a.add(raw,(sx*eta,sy*eta,Q())) for sx,sy in product((-1,1),repeat=2)]
    edges=[a.sub(c.V[j],c.V[i]) for i,j in zip(cycle,cycle[1:]+cycle[:1])]
    m0=[a.cross(e,raw) for e in edges]
    mx=[a.cross(e,EX) for e in edges];my=[a.cross(e,EY) for e in edges]
    h0=[a.dot(m,c.V[i]) for m,i in zip(m0,cycle)]
    hx=[a.dot(m,c.V[i]) for m,i in zip(mx,cycle)]
    hy=[a.dot(m,c.V[i]) for m,i in zip(my,cycle)]
    least_gap=None;source_comparisons=0;full_support_comparisons=0
    quadratic_ratio=Q();height_lower=[]
    for edge,i,j in zip(edges,cycle,cycle[1:]+cycle[:1]):
        heights=[];lengths=[]
        for r in corners:
            m=a.cross(edge,r);h=a.dot(m,c.V[i])
            c.require(h>0,'positive actual support height on proposed rectangle')
            c.require(all(a.dot(m,v)<=h for v in c.V),'full actual receiver support on proposed rectangle')
            full_support_comparisons+=60;heights.append(h);lengths.append(a.dot(m,m))
        height_lower.append(min(heights))
        floor=min(heights)
        quadratic_ratio=max(quadratic_ratio,R2*max(lengths)/(floor*floor))
    for item in data['poses']:
        g=c.matrix(item['proper_matrix_rows']);images=[c.act(g,v) for v in c.V]
        for i in cycle:c.require(c.V[i] in images,'literal persistent source preimage')
        for r in corners:
            for edge,i,j in zip(edges,cycle,cycle[1:]+cycle[:1]):
                m=a.cross(edge,r)
                for p in images:
                    if p in (c.V[i],c.V[j]):continue
                    gap=a.dot(m,a.sub(c.V[i],p))
                    c.require(gap>0,'strict actual offendpoint support on proposed rectangle')
                    least_gap=min(least_gap,gap) if least_gap is not None else gap
                    source_comparisons+=1
    C=Q(F(5,4))
    c.require(quadratic_ratio<(2*C-1)*(2*C-1),'uniform actual contact quadratic constant5/4')
    inverse_cache={};families=[];mass_max=[Q(),Q(),Q()];least_weight=None;largest_rho=Q()
    for pose_index,item in enumerate(data['poses']):
        g=c.matrix(item['proper_matrix_rows']);images=[c.act(g,v) for v in c.V]
        for dual_index,dual in enumerate(item['coordinate_duals']):
            indices=[i for i,k in dual['actual_contact_rows']]
            points=[images[k] for i,k in dual['actual_contact_rows']]
            def basis(normals):
                return tuple(zip(*(tuple(a.cross(p,normals[i]))+tuple(normals[i][:2]) for i,p in zip(indices,points))))
            B0,Bx,By=basis(m0),basis(mx),basis(my)
            key=(B0,Bx,By)
            if key not in inverse_cache:
                inv=c.load_collar().inverse(c,B0)
                Kx,Ky=c.matmul(inv,Bx),c.matmul(inv,By)
                D=tuple(tuple(eta*(c.absolute(x)+c.absolute(y)) for x,y in zip(r,s)) for r,s in zip(Kx,Ky))
                rho=norminf(D)
                c.require(rho<1,'component Neumann matrix on proposed rectangle')
                I=tuple(tuple(Q(int(i==j)) for j in range(5)) for i in range(5))
                repair=c.load_collar().inverse(c,tuple(tuple(x-y for x,y in zip(r,s)) for r,s in zip(I,D)))
                c.require(all(x>=0 for row in repair for x in row),'nonnegative comparison inverse')
                inverse_cache[key]=(Kx,Ky,repair,rho)
            Kx,Ky,repair,rho=inverse_cache[key];largest_rho=max(largest_rho,rho)
            c.require(rho<Q(F(1,20)),'simple whole-box component Neumann bound1/20')
            w0=tuple(c.field(x)/h0[i] for x,i in zip(dual['weights'],indices))
            target=tuple(Q(dual['sign']*int(i==dual['axis'])) for i in range(5))
            c.require(c.act(B0,w0)==target,'original exact raw dual target')
            b=tuple(eta*(c.absolute(x)+c.absolute(y)) for x,y in zip(c.act(Kx,w0),c.act(Ky,w0)))
            errors=c.act(repair,b)
            lower=tuple(x-e for x,e in zip(w0,errors))
            c.require(min(lower)>Q(F(1,2000)),'uniform repaired raw dual weight floor1/2000')
            least_weight=min(least_weight,min(lower)) if least_weight is not None else min(lower)
            mass0=sum((w*h0[i] for w,i in zip(w0,indices)),Q())
            mass=mass0+sum((e*h0[i]+eta*(w+e)*(c.absolute(hx[i])+c.absolute(hy[i]))
                            for w,e,i in zip(w0,errors,indices)),Q())
            c.require(mass<Q((6,7,8)[dual['axis']]),'simple whole-box contact mass6,7,8')
            mass_max[dual['axis']]=max(mass_max[dual['axis']],mass)
            families.append({'pose':pose_index,'dual':dual_index,'axis':dual['axis'],'sign':dual['sign'],
                'point_raw_weights':[c.enc(x) for x in w0],'component_error_bounds':[c.enc(x) for x in errors],
                'whole_box_weight_lower_bounds':[c.enc(x) for x in lower],'whole_box_contact_mass_upper':c.enc(mass)})
    c.require(Q(F(3725,4096))<1,'simple uniform local closure3725/4096')
    gate=Q(F(1,16));factor=C*C*sum((x*x for x in mass_max),Q())*gate*gate
    c.require(factor<1,'uniform local Cayley absorption on proposed rectangle')
    c.require(Q(F(8,75))+6*eta<Q(F(3,25)) and Q(F(9,625))<Q(F(4,257)),
              'all old source holes enter the actual moving-pose gate on proposed rectangle')
    Mn=tuple(tuple(c.IDENTITY[i][j]-2*u[i]*u[j]/u2 for j in range(3)) for i in range(3))
    Mx=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
    poses=[]
    for item in data['poses']:
        g=c.matrix(item['proper_matrix_rows']);poses.extend((g,c.matmul(c.matmul(Mn,g),Mx)))
    sep=min(sum(((g[i][j]-h[i][j])*(g[i][j]-h[i][j]) for i in range(3) for j in range(3)),Q()) for k,g in enumerate(poses) for h in poses[k+1:])
    c.require(sep>Q(F(1,100)) and 18*eta<Q(F(1,10)),'twelve equality branches remain distinct on entire rectangle')
    circuits=c.force_circuits(N);persistent_pairs=0;positive_triples=0;failed_circuits=[]
    used={leaf[4] for leaf in data['leaves'] if leaf[3]=='C'}
    for number,(rows,weights) in enumerate(circuits):
        if len(rows)==2:
            if a.add(edges[rows[0]],edges[rows[1]])==ZERO:persistent_pairs+=1
            else:failed_circuits.append({'circuit':number,'kind':'point pair not opposite spatial edges','used':number in used})
        else:
            cof=[a.cross(edges[rows[1]],edges[rows[2]]),a.cross(edges[rows[2]],edges[rows[0]]),a.cross(edges[rows[0]],edges[rows[1]])]
            w=[a.dot(v,raw) for v in cof]
            sign=1 if min(w)>0 else -1
            if all(sign*a.dot(v,r)>0 for r in corners for v in cof):positive_triples+=1
            else:failed_circuits.append({'circuit':number,'kind':'cofactor sign fails receiver corner','used':number in used})
    return {'agent':'six-rupert-2','role':'researcher','scope':'exact entire-receiver-box supports, equality and conditional local dual preflight; joint all-source cuts NOT yet certified',
        'raw_rectangle_center':[c.enc(x) for x in raw],'raw_rectangle_halfwidth':c.enc(eta),
        'complete_receiving_cycle':cycle,'actual_receiver_corner_support_comparisons':full_support_comparisons,
        'actual_source_corner_offendpoint_comparisons':source_comparisons,'minimum_strict_raw_offendpoint_gap':c.enc(least_gap),
        'whole_box_contact_R_squared_normal_ratio_upper':c.enc(quadratic_ratio),'uniform_contact_quadratic_constant':c.enc(C),
        'distinct_exact_raw_comparison_inverses':len(inverse_cache),'maximum_component_Neumann_infinity':c.enc(largest_rho),
        'minimum_uniform_raw_weight_lower':c.enc(least_weight),'uniform_coordinate_contact_mass_upper':[c.enc(x) for x in mass_max],
        'conditional_relative_Cayley_Euclidean_gate':c.enc(gate),'squared_uniform_local_absorption':c.enc(factor),
        'persistent_opposite_spatial_edge_pairs':persistent_pairs,'whole_box_strict_positive_cofactor_triples':positive_triples,
        'failing_point_circuits':failed_circuits,'local_families':families,'wall_seconds':time.monotonic()-started}
