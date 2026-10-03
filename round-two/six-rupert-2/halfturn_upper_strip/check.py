#!/usr/bin/env python3
"""Whole exact evidence for the ordinary upper-strip conditional collar proof.

No search, LP solver, old source tree or floating data is used. A compact
literal certificate is checked against the actual original coordinates.
All requirements survive python3 -O. See PROOF.md for the ordinary bridge.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
import geometry as g
import polynomial as p
Q,a=g.Q,g.a
HERE=Path(__file__).resolve().parent
P=lambda q:p.P(q,n=7)
ORDER=['xi','eta','c_x','c_y','c_z','tau_x','tau_z']

def parameters(data):
    g.require(data['agent']=='six-rupert-2' and data['role']=='researcher' and data['schema']==1,'literal author/schema')
    g.require(data['variable_order']==ORDER,'original variable meaning and order')
    rho,dx,dy=[g.dec(data[k]) for k in ['physical_Cayley_radius','receiver_half_width','receiver_upper_height']]
    x0=g.dec(data['receiver_base_x'])
    g.require(x0==g.x0 and 0<rho<=Q(F(1,8)) and dx>0 and dy>0,'original receiving base and positive closed domains')
    g.require(g.ell<x0-dx<x0+dx<g.qx,'boundary entirely inside the prior feasible top edge')
    return rho,dx,dy,x0

def original_geometry(data,dx,dy,x0):
    _,caps,_,built,axes=g.model.cupola_construction()
    g.require(len(g.V)==len(set(g.V))==60 and built==set(g.V) and len(caps)==2 and a.cross(axes[0],axes[1])!=g.Z,
              'original unit-edge two NONOPPOSITE cupola construction')
    pairs=data['exact_origin_interior_pairs']
    g.require(pairs==[[0,7],[1,6],[2,5]],'three original interior pairs')
    for i,j in pairs:g.require(a.add(g.V[i],g.V[j])==g.Z,'genuine original antipodal pair')
    g.require(a.dot(g.V[0],a.cross(g.V[1],g.V[2]))!=0,'origin INTERIOR without whole-body centrality')
    g.proper(g.G);g.proper(g.H)
    g.require(g.det(g.MX)==g.det(g.MY)==-1 and g.mm(g.H,g.MX)==g.MY,'two actual improper body actions compose with properH')
    for M in (g.H,g.MX,g.MY):
        g.require({g.act(M,v) for v in g.V}==set(g.V),'all60 original full-body action')
    h=a.dot(g.U,g.V[0]);images=[g.act(g.G,v) for v in g.V]
    streams=[h-sign*a.dot(g.U,v) for sign in (-1,1) for v in g.V]
    streams += [h-sign*a.dot(g.U,v) for sign in (-1,1) for v in images]
    g.require(h>0 and min(streams)>=0 and a.dot(g.U,images[31])==h,'actual positive boundary height and original scale closure')
    edges=[tuple(e) for e in data['receiving_edges']]
    g.require(len(edges)==len(set(edges))>0 and all(len(e)==2 and all(0<=i<60 for i in e) and e[0]!=e[1] for e in edges),
              'literal nonduplicate original receiving edges')
    support_stream=[];endpoint_records=[]
    for i,j in edges:
        e=a.sub(g.V[j],g.V[i])
        for x in (x0-dx,x0+dx):
            for y in (g.t,g.t+dy):
                n=a.cross(g.raw(x,y),e);h0=a.dot(n,g.V[i])
                gaps=[h0-a.dot(n,v) for v in g.V]
                g.require(h0>0 and min(gaps)>=0,'EVERY actual original support on each closed rectangle corner')
                support_stream+=list(map(g.enc,gaps))
                endpoint_records.append({'edge':[i,j],'receiver':g.vec((x,y)),'positive_height':g.enc(h0),
                                         'all60_gap_sha256':g.digest(list(map(g.enc,gaps)))})
    rows=[(tuple(row['receiver_edge']),row['source']) for row in data['source_contacts']]
    g.require(len(rows)==len(set(rows)) and all(e in edges and 0<=k<60 for e,k in rows),'original contact labels')
    original_zeros=[];source_base_stream=[]
    for i,j in edges:
        n=a.cross(g.raw(x0,g.t),a.sub(g.V[j],g.V[i]));hh=a.dot(n,g.V[i])
        source_gaps=[hh-a.dot(n,v) for v in images]
        g.require(min(source_gaps)>=0,'all original baseG points obey these actual selected supports')
        source_base_stream+=list(map(g.enc,source_gaps))
        original_zeros += [((i,j),k) for k,v in enumerate(images) if a.dot(n,v)==hh]
    g.require(rows==original_zeros,'COMPLETE actual zero contacts of the selected supports at the base, no hull completeness assertion')
    return {'original_vertices':60,'receiving_edges':len(edges),'literal_contact_count':len(rows),
            'actual_rectangle_support_controls':len(support_stream),'whole_support_sha256':g.digest(support_stream),
            'all_rectangle_support_records':endpoint_records,'original_boundary_width_controls':len(streams),
            'selected_baseG_support_controls':len(source_base_stream),'all_selected_baseG_support_sha256':g.digest(source_base_stream),
            'whole_boundary_width_sha256':g.digest(list(map(g.enc,streams))),
            'origin_interior_determinant':g.enc(a.dot(g.V[0],a.cross(g.V[1],g.V[2])))}

def contact_polynomials(data,x0,dx,dy,rho):
    xi,eta,*d=[p.P.variable(i,n=7) for i in range(7)]
    c=d[:3];tau=(d[3],P(0),d[4]);N=1+p.dot(c,c);Rn=p.rot_num(c)
    r=(P(x0)+xi,P(1),P(-g.t)-eta)
    rows=[];direct=[]
    fixtures=[(-dx,Q(),(rho,Q(),Q()),(rho,-rho)),
              (dx,dy,(Q(),-rho,Q()),(Q(2),Q(-3))),
              (Q(),dy/2,(rho/3,rho/4,-rho/5),(Q(),Q())),
              (dx/2,Q(),(Q(F(1,7)),Q(F(-1,11)),Q(F(1,13))),(Q(-1),Q(2)))]
    for entry in data['source_contacts']:
        i,j=entry['receiver_edge'];k=entry['source'];e=a.sub(g.V[j],g.V[i]);W=g.act(g.G,g.V[k])
        nn=p.cross(r,tuple(P(v) for v in e));h=p.dot(nn,tuple(P(v) for v in g.V[i]))
        f=N*h-p.dot(nn,p.act(Rn,tuple(P(v) for v in W)))-p.dot(nn,tau)
        n0=a.cross(g.raw(x0,g.t),e);n1=a.cross((Q(),Q(),Q(-1)),e)
        A=tuple(2*q for q in a.cross(W,n0))+(n0[0],n0[2]);b=a.dot(n1,a.sub(g.V[i],W))
        rem=f+sum((v*aa for v,aa in zip(d,A)),P(0))-eta*b
        # All constant/receiving-only and unaccounted linear coefficients must vanish.
        l1_categories(rem)
        rows.append({'A':A,'b':b,'f':f,'remainder':rem,'source':k,'edge':[i,j]})
        for xx,yy,cc,tt in fixtures:
            x,y=x0+xx,g.t+yy;normal=a.cross(g.raw(x,y),e);height=a.dot(normal,g.V[i]);RR=g.rotation(cc);g.proper(RR)
            norm=1+a.dot(cc,cc);RW=g.act(RR,W);lift=(tt[0]/norm,Q(),tt[1]/norm)
            spatial=norm*(height-a.dot(normal,a.add(RW,lift)))
            project=lambda v:(v[0]-x*v[1],v[2]+y*v[1])
            pe=project(e);pv=a.add(project(RW),(tt[0]/norm,tt[1]/norm));pi=project(g.V[i]);z=a.sub(pv,pi)
            planar=norm*(pe[0]*z[1]-pe[1]*z[0])
            value=f.at((xx,yy,*cc,*tt))
            g.require(value==spatial==planar,'direct original 3D AND quotient-plane determinant compare to WHOLE polynomial')
            direct.append([k,g.vec((xx,yy,*cc,*tt)),g.enc(value)])
    return rows,{'free_variables':7,'all_contact_polynomials_sha256':g.digest([r['f'].coefficients() for r in rows]),
                 'all_linear_rows_sha256':g.digest([{'A':g.vec(r['A']),'b':g.enc(r['b'])} for r in rows]),
                 'actual_3D_and_planar_comparisons':len(direct),'all_direct_comparisons_sha256':g.digest(direct)}

def l1_categories(poly):
    out={k:Q() for k in ['c2','xi_linear','eta_linear','xi_c2','eta_c2']}
    for e,v in poly.terms.items():
        sx,se=e[:2];dc,dt=sum(e[2:5]),sum(e[5:])
        if sx==se==dt==0 and dc==2:key='c2'
        elif sx==1 and se==0 and dc+dt==1:key='xi_linear'
        elif se==1 and sx==0 and dc+dt==1:key='eta_linear'
        elif sx==1 and se==dt==0 and dc==2:key='xi_c2'
        elif se==1 and sx==dt==0 and dc==2:key='eta_c2'
        else:raise ValueError('unproved nonlinear remainder monomial: '+str(e))
        out[key]+=v if v>=0 else -v
    return out

def weights(entries,rows):
    w=[Q()]*len(rows);seen=set()
    for entry in entries:
        i=entry['row_index'];v=g.dec(entry['weight'])
        g.require(isinstance(i,int) and 0<=i<len(rows) and i not in seen and v>0,'literal distinct strictly positive stored weights')
        seen.add(i);w[i]=v
    g.require(seen,'nonempty exact dual')
    return w

def duals_and_bounds(data,rows,rho,dx,dy):
    frames=[];coverage=set();allpolys=[]
    for entry in data['signed_coordinate_duals']:
        k,sign=entry['coordinate'],entry['sign']
        g.require(k in range(5) and sign in (-1,1) and (k,sign) not in coverage,'original signed coordinate directions')
        coverage.add((k,sign));w=weights(entry['nonnegative_weights'],rows)
        for j in range(5):g.require(sum((v*r['A'][j] for v,r in zip(w,rows)),Q())==Q(sign if j==k else 0),
                                    'EVERY original signed dual coefficient')
        b=sum((v*r['b'] for v,r in zip(w,rows)),Q());rem=sum((r['remainder']*v for r,v in zip(rows,w)),P(0))
        cat=l1_categories(rem)
        B=cat['c2']*rho+cat['xi_linear']*dx+cat['eta_linear']*dy+cat['xi_c2']*dx*rho+cat['eta_c2']*dy*rho
        frames.append({'coordinate':k,'sign':sign,'beta':b,'B':B,'l1':cat,'remainder':rem})
        allpolys.append(rem.coefficients())
    g.require(coverage=={(k,s) for k in range(5) for s in (-1,1)},'ALL ten original source/translation directions covered')
    mu=weights(data['separating_dual'],rows)
    for j in range(5):g.require(sum((v*r['A'][j] for v,r in zip(mu,rows)),Q())==0,'original separating dual annihilates source AND translation')
    x0=g.x0
    normalization=sum((v*a.dot(a.cross(g.raw(x0,g.t),a.sub(g.V[r['edge'][1]],g.V[r['edge'][0]])),g.V[r['edge'][0]]) for v,r in zip(mu,rows)),Q())
    g.require(normalization==1,'actual positive scale normalization, not a scale-one premise')
    beta=sum((v*r['b'] for v,r in zip(mu,rows)),Q())
    g.require(beta==g.dec(data['separating_beta_claim'])<0,'actual strictly negative separating receiving coefficient')
    rem=sum((r['remainder']*v for r,v in zip(rows,mu)),P(0));cat=l1_categories(rem);allpolys.append(rem.coefficients())
    M=max([Q()]+[f['beta'] for f in frames]);K=2*M;B=max(f['B'] for f in frames)
    g.require(M>0 and B<Q(F(1,2)),'WHOLE finite coercivity bound B<1/2')
    C2=cat['c2']+dx*cat['xi_c2']+dy*cat['eta_c2']
    upper=beta+cat['xi_linear']*dx*K+(C2*K*K+cat['eta_linear']*K)*dy
    g.require(upper<0,'WHOLE finite upper-sector exclusion; infinitesimal sign alone is insufficient')
    return {'original_coordinate_directions':10,'coordinate_coefficient_identities':50,'separating_source_translation_identities':5,
            'M':g.enc(M),'K':g.enc(K),'maximum_coercivity_B':g.enc(B),'strict_margin_to_half':g.enc(Q(F(1,2))-B),
            'negative_separating_beta':g.enc(beta),'strict_finite_upper_coefficient':g.enc(upper),
            'separating_l1_categories':{k:g.enc(v) for k,v in cat.items()},
            'ALL_weighted_remainders_sha256':g.digest(allpolys),
            'coordinate_records':[{'coordinate':f['coordinate'],'sign':f['sign'],'beta':g.enc(f['beta']),'B':g.enc(f['B']),
                'l1_categories':{k:g.enc(v) for k,v in f['l1'].items()},'whole_remainder_sha256':g.digest(f['remainder'].coefficients())} for f in frames]}

def actions_and_cayley():
    c=[p.P.variable(i,n=3) for i in range(3)];N=1+p.dot(c,c);Rn=p.rot_num(c)
    g.require(p.mm(p.transpose(Rn),Rn)==tuple(tuple(N*N*int(i==j) for j in range(3)) for i in range(3)) and p.det(Rn)==N*N*N,'FREE original Cayley properness')
    g.require(sum((Rn[i][i] for i in range(3)),0)==3-p.dot(c,c),'exact physical Cayley trace gate')
    plus=tuple(tuple(Rn[i][j]+N*int(i==j) for j in range(3)) for i in range(3))
    g.require(p.mm(plus,p.skew(c))==tuple(tuple(Rn[i][j]-N*int(i==j) for j in range(3)) for i in range(3)) and p.det(plus)==8*N*N,
              'entire original Cayley inverse and positive denominator')
    X,Y,Tx,Ty,Tz=[p.P.variable(i,n=5) for i in range(5)]
    raw=(X,p.P(1,n=5),-Y);original=(Tx,Ty,Tz);lift=(Tx-X*Ty,p.P(0,n=5),Tz+Y*Ty)
    g.require(tuple(v-w for v,w in zip(original,lift))==tuple(v*Ty for v in raw),'all free original physical translation lift identities')
    x=p.P.variable(0,n=2)+g.x0;y=p.P.variable(1,n=2)+g.t;r=(x,p.P(1),-y);rr=p.dot(r,r)
    M=tuple(tuple(rr*int(i==j)-r[i]*r[j]*2 for j in range(3)) for i in range(3))
    Proj=tuple(tuple(rr*int(i==j)-r[i]*r[j] for j in range(3)) for i in range(3))
    g.require(p.mm(M,M)==tuple(tuple(rr*rr*int(i==j) for j in range(3)) for i in range(3)) and p.det(M)==-rr*rr*rr,'actual original receiving reflection identities')
    g.require(p.mm(Proj,M)==tuple(tuple(v*rr for v in row) for row in Proj),'moving receiving action preserves projected source SET')
    return {'free_Cayley_variables':3,'proper_orthogonality_entries':9,'proper_determinant_identities':1,'trace_gate_identity':1,'Cayley_inverse_entries':9,'positive_inverse_denominator_identity':1,
            'free_original_translation_variables':5,'translation_lift_identity_entries':3,
            'free_receiving_variables':2,'reflection_involution_entries':9,'reflection_determinant_identity':1,'projection_preservation_entries':9}

def record(data=None):
    if data is None:data=json.loads((HERE/'certificate.json').read_text())
    rho,dx,dy,x0=parameters(data)
    original=original_geometry(data,dx,dy,x0)
    rows,polys=contact_polynomials(data,x0,dx,dy,rho)
    result=duals_and_bounds(data,rows,rho,dx,dy)
    return {'agent':'six-rupert-2','role':'researcher','scope':'ordinary CONDITIONAL original-source collar on an ENTIRE CLOSED upper receiving rectangle; arbitrary original physical translation and lambda>=1',
            'certificate_SHA256':g.digest(data),'rectangle_corners':list(map(g.vec,((x,y) for x in (x0-dx,x0+dx) for y in (g.t,g.t+dy)))),
            'physical_Cayley_radius':g.enc(rho),'exact_relative_trace_gate':g.enc(3-4*rho*rho/(1+rho*rho)),
            'exact_relative_Frobenius_squared_gate':g.enc(8*rho*rho/(1+rho*rho)),
            'original_geometry':original,'whole_polynomial_checks':polys,'nonlinear_duals':result,'proper_actions':actions_and_cayley(),
            'translation_scope':'tau=(1+c^2)*(Tx-x*Ty,Tz+y*Ty) unrestricted; no centering premise',
            'scale_reduction':'original0 is interior; a fitted lambda>=1 source contains the unit source with SAME translation; boundary positive support then forces lambda1',
            'boundary_sufficiency_dependency':'LEMMA9961/0 supplies original fixedG boundary feasibility; old full ray/width certificate NOT replayed here',
            'global_J74_status':'OPEN','independent_review':False,'formalized':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');parser.add_argument('--output');args=parser.parse_args()
    r=record()
    if not args.emit:g.require(r==json.loads((HERE/'expected.json').read_text()),'ENTIRE expected mathematical record required')
    if args.output:Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'agent':r['agent'],'role':r['role'],'WHOLE_record_SHA256':g.digest(r),'scope':r['scope'],'global_J74_status':'OPEN'},indent=2))
