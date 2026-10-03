#!/usr/bin/env python3
"""Exact evidence for the ordinary finite J74 companion-merger wedge proof.

Every geometric support and polynomial is rebuilt from original model8551.
No private LP, old contact inventory, source forest or floating input is used.
Explicit requirements survive -O. The ordinary continuum bridges are in PROOF.md.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, json
import geometry as g
import polynomial as p
Q,a=g.Q,g.a
HERE=Path(__file__).resolve().parent
ORDER=['epsilon','eta','e_x','e_y','z','tau_x','tau_z']
P=lambda v:p.P(v,n=7)

def rational_abs_bound(v):return abs(v.a)+3*abs(v.b)
def ceil_fraction(v):return -(-v.numerator//v.denominator)
def l1(poly):return sum((rational_abs_bound(v) for v in poly.terms.values()),F())
def axis(poly):
    return p.P({e:v for e,v in poly.terms.items() if e[1]==e[2]==e[3]==e[5]==e[6]==0},n=7)
def eta_error(poly,C0):
    g.require(all(any(e[i] for i in (1,2,3)) for e in poly.terms),'each width-error monomial contains eta or a transverse rotation')
    return ceil_fraction(C0*l1(poly))

def original_geometry(data):
    _,caps,_,built,axes=g.model.cupola_construction()
    g.require(len(g.V)==len(set(g.V))==60 and built==set(g.V) and len(caps)==2 and a.cross(axes[0],axes[1])!=g.Z,
              'original unit-edge TWO NONOPPOSITE cupola gyrations')
    pairs=data['exact_origin_interior_pairs']
    g.require(pairs==[[0,7],[1,6],[2,5]],'three actual origin-interior pairs')
    for i,j in pairs:g.require(a.add(g.V[i],g.V[j])==g.Z,'literal antipodal pair, not full centrality')
    interior=a.dot(g.V[0],a.cross(g.V[1],g.V[2]));g.require(interior!=0,'origin strictly interior to the original K')
    g.proper(g.G);g.proper(g.H)
    g.require(g.det(g.MX)==g.det(g.MY)==-1 and g.mm(g.H,g.MX)==g.MY,'actual improper body factors')
    for M in (g.H,g.MX,g.MY):g.require({g.act(M,v) for v in g.V}==set(g.V),'ALL60 original body images')
    W=[g.act(g.G,v) for v in g.V];h=(7+g.S)/4
    stream=[h-sign*a.dot(g.U,v) for sign in (-1,1) for v in list(g.V)+W]
    g.require(h==a.dot(g.U,g.V[0])>0 and min(stream)>=0,'both actual U supports and positive scale closure height')
    face=data['paired_source_triangle'];g.require(len(face)==3 and len({k for k,_ in face})==3,'genuine three-point source triangle')
    for k,j in face:g.require(a.add(W[k],W[j])==g.Z and a.dot(g.U,W[k])==h,'actual positive source face and its original antipodes')
    verts=[W[k] for k,_ in face];center=tuple(sum(v[j] for v in verts)/3 for j in range(3))
    g.require(center==a.scale(h/g.U2,g.U),'centroid is perpendicular foot on source face')
    distances=[]
    for v,w in zip(verts,verts[1:]+verts[:1]):
        e=a.sub(w,v);q=a.sub(center,v);ee=a.dot(e,e)
        ds=a.dot(q,q)-a.dot(q,e)*a.dot(q,e)/ee
        g.require(ee==1 and ds==Q(F(1,12)),'ALL unit triangle sides and inradius squared1/12')
        distances.append(g.enc(ds))
    widthpairs=data['paired_source_widths'];g.require(widthpairs==[[31,28],[41,38],[43,36]],'three actual width pairs')
    for k,j in widthpairs:g.require(a.add(W[k],W[j])==g.Z,'each original width pair really is antipodal')
    return {'original_vertices':60,'origin_interior_determinant':g.enc(interior),
            'actual_U_support_controls':len(stream),'whole_U_gap_stream_SHA256':g.digest(g.vec(stream)),
            'source_centroid':g.vec(center),'all_three_side_inradius_squared':distances,
            'unit_source_triangle_pairs':face,'actual_paired_width_sources':widthpairs},center

def free_bridges():
    c=[p.P.variable(i,n=3) for i in range(3)];N=1+p.dot(c,c);Rn=p.rot_num(c)
    identity=tuple(tuple(N*N*int(i==j) for j in range(3)) for i in range(3))
    g.require(p.mm(p.transpose(Rn),Rn)==identity and p.det(Rn)==N*N*N,'FREE3 physical Cayley properness')
    g.require(sum((Rn[i][i] for i in range(3)),0)==3-p.dot(c,c),'FREE3 physical relative trace identity')
    plus=tuple(tuple(Rn[i][j]+N*int(i==j) for j in range(3)) for i in range(3))
    g.require(p.mm(plus,p.skew(c))==tuple(tuple(Rn[i][j]-N*int(i==j) for j in range(3)) for i in range(3)) and p.det(plus)==8*N*N,
              'FREE3 Cayley inverse and positive denominator')
    U=tuple(p.P(v,n=3) for v in g.U);diff=tuple(v-N*u for v,u in zip(p.act(Rn,U),U))
    g.require(p.dot(diff,diff)==4*N*p.dot(p.cross(c,U),p.cross(c,U)),'FREE3 exact transverse angular identity')
    X,Y,Tx,Ty,Tz=[p.P.variable(i,n=5) for i in range(5)]
    raw=(X,p.P(1,n=5),-Y);original=(Tx,Ty,Tz);lift=(Tx-X*Ty,p.P(0,n=5),Tz+Y*Ty)
    g.require(tuple(v-w for v,w in zip(original,lift))==tuple(v*Ty for v in raw),'all FREE5 original translation lift identities')
    eps,eta=[p.P.variable(i,n=2) for i in range(2)]
    r=(p.P(g.qx)-eps,p.P(1),p.P(-g.t)-eta);rr=p.dot(r,r)
    M=tuple(tuple(rr*int(i==j)-2*r[i]*r[j] for j in range(3)) for i in range(3))
    Proj=tuple(tuple(rr*int(i==j)-r[i]*r[j] for j in range(3)) for i in range(3))
    g.require(p.mm(M,M)==tuple(tuple(rr*rr*int(i==j) for j in range(3)) for i in range(3)) and p.det(M)==-rr*rr*rr,'FREE2 receiving reflection')
    g.require(p.mm(Proj,M)==tuple(tuple(v*rr for v in row) for row in Proj),'FREE2 projected source companion preserves SAME T and lambda')
    B=p.P(4*g.t)-eps*g.qx+eta*g.t;w=(-eta,eps*g.t+eta*g.qx,eps)
    numerator=tuple(tuple((B*B-p.dot(w,w))*int(i==j)+2*w[i]*w[j]+2*B*p.skew(w)[i][j] for j in range(3)) for i in range(3))
    gg=tuple(tuple(p.P(v) for v in row) for row in g.G);my=tuple(tuple(p.P(v) for v in row) for row in g.MY)
    left=p.mm(p.mm(M,gg),my);right=p.mm(numerator,gg);dn=B*B+p.dot(w,w)
    g.require(tuple(tuple(v*dn for v in row) for row in left)==tuple(tuple(v*rr for v in row) for row in right),
              'FREE2 Jr(G) is the ACTUAL proper companion with Cayley w/B, including q merger')
    n=(p.P(0),p.P(g.t)+eta,p.P(1));U2=p.P(g.U2)
    g.require(p.dot(tuple(p.P(v) for v in g.U),n)==U2+eta*g.t and p.cross(tuple(p.P(v) for v in g.U),n)==(-eta,p.P(0),p.P(0)),
              'FREE2 exact camera-axis angle tangent denominator')
    return {'Cayley_variables':3,'properness_entries':9,'determinant_trace_inverse_checked':True,
            'transverse_norm_identity':True,'original_translation_variables':5,'translation_lift_entries':3,
            'receiving_variables':2,'reflection_projection_entries':18,
            'actual_Jr_not_Cr_companion_entries':9,'camera_axis_cross_dot_identities':True}

def record(data=None,transcript=None):
    if data is None:data=json.loads((HERE/'certificate.json').read_text())
    g.require(data['schema']==1 and data['agent']=='six-rupert-2' and data['role']=='researcher','literal schema/author')
    g.require(data['variable_order']==ORDER,'original variable meanings and order')
    rho=g.dec(data['physical_Cayley_radius']);delta=g.dec(data['receiver_wedge_delta'])
    C0=data['constant_claims']['C0']
    g.require(C0==4*8+2,'angular proof derived constant32+2, not an arbitrary small bound')
    geometry,centroid=original_geometry(data)
    ep,et,ex,ey,z,tx,tz=[p.P.variable(i,n=7) for i in range(7)]
    c=(ex,ey+z*g.t,z);tau=(tx,P(0),tz);N=1+p.dot(c,c);Rn=p.rot_num(c)
    r=(P(g.qx)-ep,P(1),P(-g.t)-et);h=(7+g.S)/4
    normal=(P(0),P(g.t)+et,P(1));Fp=tuple(P(v) for v in centroid)
    centroid_error=p.dot(normal,p.act(Rn,Fp))-N*h
    g.require(axis(centroid_error)==0,'complete axis centroid identity')
    Cn=eta_error(centroid_error,C0)
    edge=a.sub(g.V[36],g.V[0]);m=p.cross(tuple(P(v) for v in edge),r)
    g.require(m==(P(g.t)-et*g.aa,ep*F(1,2)+et*g.bb,P(g.qx)+ep*g.aa),'FREE7 original m formula')
    hm=p.dot(m,tuple(P(v) for v in g.V[0]));D=P(4*g.t)-ep*g.qx;J=z*(ep-D*z)
    expected_widths={31:J*(-g.t),
       41:-2*(D*z-ep)*(P(F(1,4))+z*((g.S-5)/8)),
       43:-2*z*(P(-g.t)+ep*F(1,2)+(P(2*g.S-5)+ep*((3*g.S-7)/4))*z)}
    widths={};errors={};C_each={}
    for k,target in expected_widths.items():
        W=tuple(P(v) for v in g.act(g.G,g.V[k]));f=N*hm-p.dot(m,p.act(Rn,W))
        g.require(axis(f)==target,'entire original two-variable merging-branch width')
        widths[k]=f;errors[k]=f-target;C_each[k]=eta_error(errors[k],C0)
    Cw=max(1,*C_each.values());Kz=1+4*Cw;KJ=4*Cw*Kz;Ct=4*(Cw+1+2*(Cn+4))
    MU=data['positive_original_stress'];g.require(len(MU)==5,'five genuine positive stress rows')
    stress=P(0);entries=[];polynomials=[];rows=[]
    r0=g.raw(g.qx,g.t);re=(Q(-1),Q(),Q());rh=(Q(),Q(),Q(-1))
    cols=[Q()]*6;be=Q();bt=Q()
    for entry in MU:
        i,j=entry['edge'];k=entry['source'];mu=g.dec(entry['weight'])
        g.require(mu>0 and i!=j and all(0<=v<60 for v in (i,j,k)),'positive literal actual source stress')
        e=a.sub(g.V[j],g.V[i]);nn=p.cross(r,tuple(P(v) for v in e));hh=p.dot(nn,tuple(P(v) for v in g.V[i]))
        W=g.act(g.G,g.V[k]);f=N*hh-p.dot(nn,p.act(Rn,tuple(P(v) for v in W)))-p.dot(nn,tau)
        stress+=f*mu;polynomials.append(f);rows.append(((i,j),k))
        n0,ne,nh=[a.cross(rv,e) for rv in (r0,re,rh)];h0=a.dot(n0,g.V[i])
        g.require(a.dot(n0,W)==h0,'actual original q contact')
        row=tuple(2*v for v in a.cross(W,n0))+(n0[0],n0[2],h0)
        cols=[v+mu*w for v,w in zip(cols,row)]
        be+=mu*a.dot(ne,a.sub(g.V[i],W));bt+=mu*a.dot(nh,a.sub(g.V[i],W))
        entries.append({'edge':[i,j],'source':k,'weight':g.enc(mu),'polynomial_coefficients':f.coefficients()})
    g.require(len(set(rows))==5,'distinct five actual edge/source rows')
    beta=Q(F(1,4),F(-3,20));lc=Q(F(3,2),F(-7,10))
    g.require(cols==[Q()]*5+[Q(1)] and be==0 and bt==beta,'ALL original source/translation/scale AND receiving columns')
    g.require(g.dec(data['beta'])==beta and g.dec(data['axis_stress_coefficient'])==lc,'claimed exact finite stress coefficients')
    g.require(axis(stress)==J*lc,'COMPLETE axis stress vanishes at BOTH branches')
    remainder=stress-J*lc-et*beta
    g.require(remainder.coefficients()==data['full_stress_remainder_coefficients'],'EVERY reconstructed original remainder coefficient, including translation')
    weights=[1,1,C0,C0,Kz,Ct,Ct];weighted=F()
    for e,v in remainder.terms.items():
        g.require(sum(e)>=2 and any(e[i] for i in (1,2,3,5,6)),'no unproved receiving-only, pure-axis or first-order stress remainder')
        mass=1
        for ki,power in zip(weights,e):
            for _ in range(power):mass*=ki
        weighted+=rational_abs_bound(v)*mass
    CR=ceil_fraction(weighted)
    constants={'C0':C0,'Cw':Cw,'Cn':Cn,'Kz':Kz,'KJ':KJ,'Ct':Ct,'CR':CR}
    g.require(data['constant_claims']==constants,'ALL claimed constants derived from whole original polynomials')
    g.require(0<delta<=rho<Q(F(1,8)) and delta<g.L,'closed wedge inside original feasible boundary')
    g.require(beta<Q(F(-1,20)) and -1<lc<0,'strict exact stress signs')
    g.require((KJ+CR)*delta<Q(F(1,1000)) and beta+(KJ+CR)*delta<0,'FINITE absorption, not infinitesimal sign')
    for Ki in (Kz,KJ,Ct):g.require(Ki*delta<1,'derived source/translation boxes and paired slack')
    g.require((2*rho)/(1-rho*rho)<Q(F(1,64)),'uniform angular half-angle margin')
    g.require(Q(F(1,3))<g.t<Q(F(1,2)) and 1<g.U2<4 and h<3,'ordinary angular norm prerequisites')
    g.require((5+g.S)/8<1 and (3+g.S)/4<2 and Q(F(1,12))>Q(F(1,16)),'actual asymmetric width and triangular disk bounds')
    height_coeff=[g.dec(v) for v in data['asymmetric_receiving_eta_height_coefficients']]
    g.require(len(height_coeff)==2,'two original opposite height coefficients')
    corners=[(Q(),Q()),(delta,Q()),(delta,delta)];support_stream=[];supports=[]
    for eps,eta in corners:
        rr=g.raw(g.qx-eps,g.t+eta);nn=(Q(),g.t+eta,Q(1));mm=a.cross(edge,rr);hh=a.dot(mm,g.V[0])
        tests=[('n+',nn,h+height_coeff[0]*eta),('n-',a.scale(-1,nn),h+height_coeff[1]*eta),
               ('m+',mm,hh),('m-',a.scale(-1,mm),hh)]
        for entry in MU:
            i,j=entry['edge'];force=a.cross(rr,a.sub(g.V[j],g.V[i]));tests.append(('stress'+str((i,j)),force,a.dot(force,g.V[i])))
        for label,force,height in tests:
            gaps=[height-a.dot(force,v) for v in g.V]
            g.require(a.dot(force,rr)==0 and height>0 and min(gaps)==0,'EVERY genuine original support at closed wedge corners')
            support_stream+=g.vec(gaps);supports.append({'corner':g.vec((eps,eta)),'label':label,'height':g.enc(height),'all60_gap_SHA256':g.digest(g.vec(gaps))})
        g.require(mm[0]>Q(F(1,4)) and 0<mm[2]<2,'actual translation inverse bound')
    ab=[];bb=[]
    for eps in (Q(),delta):
        for zz in (-rho,rho):
            A=Q(F(1,4))+(g.S-5)*zz/8;B=-g.t+eps/2+(2*g.S-5+(3*g.S-7)*eps/4)*zz
            g.require(Q(F(1,8))<A<Q(F(1,2)) and -1<B<Q(F(-1,4)),'ALL closed scalar-width corners')
            ab.append(g.enc(A));bb.append(g.enc(B))
        g.require(1<4*g.t-g.qx*eps<2,'entire positive branch denominator')
    direct=[]
    fixtures=[(Q(),Q(),(rho,Q(),Q()),(Q(),Q())),
              (delta,delta,(Q(),-rho,Q()),(Q(2),Q(-3))),
              (delta,delta/2,(rho/3,rho/4,-rho/5),(Q(),Q())),
              (delta/2,Q(),(Q(F(1,7)),Q(F(-1,11)),Q(F(1,13))),(Q(-1),Q(2)))]
    for eps,eta,cc,tt in fixtures:
        x,y=g.qx-eps,g.t+eta;rr=g.raw(x,y);R=g.rotation(cc);g.proper(R);norm=1+a.dot(cc,cc)
        value_at=(eps,eta,cc[0],cc[1]-g.t*cc[2],cc[2],*tt)
        project=lambda v:(v[0]-x*v[1],v[2]+y*v[1])
        for entry,f in zip(MU,polynomials):
            i,j=entry['edge'];k=entry['source'];e=a.sub(g.V[j],g.V[i]);nn=a.cross(rr,e);height=a.dot(nn,g.V[i]);RW=g.act(R,g.act(g.G,g.V[k]))
            spatial=norm*(height-a.dot(nn,a.add(RW,(tt[0]/norm,Q(),tt[1]/norm))))
            pe=project(e);pv=a.add(project(RW),(tt[0]/norm,tt[1]/norm));zz=a.sub(pv,project(g.V[i]));planar=norm*(pe[0]*zz[1]-pe[1]*zz[0])
            actual=f.at(value_at);g.require(actual==spatial==planar,'WHOLE contact polynomial vs direct3D AND planar determinant')
            direct.append([entry['edge'],k,g.vec(value_at),g.enc(actual)])
        mm=a.cross(edge,rr);hm0=a.dot(mm,g.V[0]);nn=(Q(),g.t+eta,Q(1))
        for k,f in widths.items():
            actual=f.at(value_at);spatial=norm*(hm0-a.dot(mm,g.act(R,g.act(g.G,g.V[k]))))
            g.require(actual==spatial,'WHOLE paired width vs original physical rotation')
            direct.append(['width',k,g.vec(value_at),g.enc(actual)])
        actual=centroid_error.at(value_at);spatial=norm*(a.dot(nn,g.act(R,centroid))-h)
        g.require(actual==spatial,'WHOLE source centroid error vs original physical rotation')
        direct.append(['centroid',g.vec(value_at),g.enc(actual)])
    if transcript is not None:transcript['all_original_support_gaps']=support_stream
    return {'agent':'six-rupert-2','role':'researcher','scope':'ordinary CONDITIONAL original-source collar on ENTIRE CLOSED q-merger wedge; EVERY original physical T and lambda>=1',
        'certificate_SHA256':g.digest(data),'variable_order':ORDER,'physical_Cayley_radius':g.enc(rho),'receiver_wedge_delta':g.enc(delta),
        'relative_trace_gate':g.enc(3-4*rho*rho/(1+rho*rho)),'relative_Frobenius_squared_gate':g.enc(8*rho*rho/(1+rho*rho)),
        'original_geometry':geometry,'free_bridges':free_bridges(),'constants':constants,'individual_width_error_bounds':{str(k):v for k,v in C_each.items()},
        'beta':g.enc(beta),'axis_stress_coefficient':g.enc(lc),'strict_finite_upper':g.enc(beta+(KJ+CR)*delta),
        'all_original_stress_columns':g.vec(cols),'receiving_epsilon_coefficient':g.enc(be),'receiving_eta_coefficient':g.enc(bt),
        'source_stress_contacts_and_whole_polynomials':entries,'actual_support_controls':len(support_stream),
        'whole_support_stream_SHA256':g.digest(support_stream),'all_support_records':supports,
        'source_centroid_error_l1':str(l1(centroid_error)),'whole_source_centroid_error_coefficients':centroid_error.coefficients(),
        'whole_width_coefficients':{str(k):widths[k].coefficients() for k in widths},'whole_width_error_coefficients':{str(k):errors[k].coefficients() for k in errors},
        'whole_stress_coefficients':stress.coefficients(),'whole_stress_SHA256':g.digest(stress.coefficients()),
        'whole_remainder_coefficients':remainder.coefficients(),'whole_remainder_SHA256':g.digest(remainder.coefficients()),
        'weighted_remainder_l1_rational':str(weighted),'scalar_A_corner_controls':ab,'scalar_B_corner_controls':bb,
        'direct_spatial_and_quotient_comparisons':len(direct),'all_direct_comparison_records':direct,
        'boundary_sufficiency_dependency':'LEMMA9961/0 supplies fixedG unit/T0 boundary sufficiency ONLY; old full ray/width certificate NOT replayed',
        'global_J74_status':'OPEN','independent_review':False,'formalized':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');parser.add_argument('--output');parser.add_argument('--transcript');args=parser.parse_args()
    full={};r=record(transcript=full)
    if not args.emit:g.require(r==json.loads((HERE/'expected.json').read_text()),'ENTIRE expected mathematical record required')
    if args.output:Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    if args.transcript:
        full['whole_mathematical_record']=r
        Path(args.transcript).write_text(json.dumps(full,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'agent':r['agent'],'role':r['role'],'WHOLE_record_SHA256':g.digest(r),'scope':r['scope'],'global_J74_status':'OPEN'},indent=2))
