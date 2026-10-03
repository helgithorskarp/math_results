#!/usr/bin/env python3
"""Complete exact evidence for the ordinary branch-aware collar proof.

Run with python3 check.py (or python3 -O check.py). Full records must match.
The ordinary face-width and angle implications are explained in PROOF.md;
public9961 is the explicit prior sufficiency theorem for fixed G on this edge.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
import geometry as g
import polynomial as p
Q,a=g.Q,g.a
HERE=Path(__file__).resolve().parent
def parameters(data):
    g.require(data['agent']=='six-rupert-2' and data['role']=='researcher' and data['schema']==1,'literal author/schema')
    g.require(data['receiving_endpoints']==list(map(g.vec,g.ENDS)),'BOTH exact endpoints of the entire closed top edge')
    g.require(data['face_source_indices']==[13,15,31] and data['actual_antipodes']==[10,8,28],'three complete genuine paired faces')
    g.require(data['line_source_indices']==[31,41,43] and data['line_antipodes']==[28,38,36],'three actual paired source rows')
    g.require(g.dec(data['physical_Cayley_radius'])==g.rho,'exact closed physical radius1/8')
    g.require(data['source_line_bound']==g.enc(g.rho),'proved source line coordinate bound')
    return data
def geometry(data):
    _,caps,_,built,axes=g.model.cupola_construction()
    g.require(len(g.V)==len(set(g.V))==60 and built==set(g.V) and len(caps)==2 and
              a.cross(axes[0],axes[1])!=g.Z,'original two NONOPPOSITE cupola model')
    R2=(11+4*g.S)/4
    g.require(all(a.dot(v,v)==R2 for v in g.V),'original common sphere')
    g.require(all(a.add(g.V[i],g.V[j])==g.Z for i,j in ((0,7),(1,6),(2,5))) and
              a.dot(g.V[0],a.cross(g.V[1],g.V[2]))!=0,'origin interior without centrality')
    g.proper(g.G);g.proper(g.H)
    g.require(g.det(g.MX)==g.det(g.MY)==-1 and g.mm(g.H,g.MX)==g.MY,'actual improper body reflections')
    for M in (g.H,g.MX,g.MY):
        g.require({g.act(M,v) for v in g.V}==set(g.V),'all60 original full-body permutations')
    g.require(g.qx*g.qx==g.t and g.U2==3*g.t>1 and 0<g.L<g.qx,'literal receiver/source bounds')
    h=a.dot(g.U,g.V[0]);images=[g.act(g.G,v) for v in g.V]
    positive=[images[k] for k in data['face_source_indices']]
    g.require(a.dot(g.U,g.V[4])==h>0,'actual receiving constant supporting edge')
    stream=[h-sign*a.dot(g.U,v) for sign in (-1,1) for v in g.V]
    source_stream=[h-sign*a.dot(g.U,v) for sign in (-1,1) for v in images]
    g.require(min(stream)>=0 and min(source_stream)>=0,'every original actual +/-U support')
    g.require({k for k,v in enumerate(images) if a.dot(g.U,v)==h}==set(data['face_source_indices']) and
              {k for k,v in enumerate(g.V) if a.dot(g.U,v)==h}=={0,4},'complete original positive source face and receiving edge labels')
    for k,j in zip(data['face_source_indices'],data['actual_antipodes']):
        g.require(a.add(g.V[k],g.V[j])==g.Z and a.dot(g.U,images[k])==h,'literal original antipodes and positive source face')
    foot=a.scale(h/g.U2,g.U)
    g.require(tuple(sum((v[i] for v in positive),Q())/3 for i in range(3))==foot,'positive centroid at perpendicular foot')
    side_records=[]
    for i,j in ((0,1),(1,2),(2,0)):
        e=a.sub(positive[j],positive[i]);v=a.sub(foot,positive[i]);cv=a.cross(e,v)
        distance2=a.dot(cv,cv)/a.dot(e,e)
        g.require(a.dot(e,e)==1 and distance2==Q(F(1,12)),'unit equilateral paired face, every exact inradius squared')
        side_records.append({'source_edge':[data['face_source_indices'][i],data['face_source_indices'][j]],'length_squared':g.enc(a.dot(e,e)),'foot_side_distance_squared':g.enc(distance2)})
    ratio=Q(F(1,12))*g.U2/(h*h)
    g.require(ratio==Q(F(29,121),F(-12,121))>g.rho*g.rho,'strict full collar face-width cusp bound')
    e=a.sub(g.V[36],g.V[0]);receiving=[]
    for eps in (Q(),g.L):
        r=g.raw(eps);m=a.cross(e,r);hm=a.dot(m,g.V[0]);D=4*g.t-g.qx*eps
        vals=[hm-sign*a.dot(m,v) for sign in (-1,1) for v in g.V]
        g.require(hm>0 and min(vals)>=0 and a.dot(g.U,r)==0 and D>3*g.t>0,'both closed endpoints, all actual opposite edge0->36 supports, positive denominators')
        g.require(a.cross(g.U,m)==a.scale(g.t,r),'two independent physical receiving normals on the WHOLE edge')
        for k,j in zip(data['line_source_indices'],data['line_antipodes']):
            g.require(a.add(g.V[k],g.V[j])==g.Z,'actual source antipode for every width row')
        g.require(images[31]==g.V[0] and images[43]==g.V[36],'two actual persistent original spatial preimages')
        receiving.append({'epsilon':g.enc(eps),'raw_receiver':g.vec(r),'support_height':g.enc(hm),'minimum_original_gap':g.enc(min(vals)),'support_controls':len(vals),'complete_support_stream_sha256':g.digest(list(map(g.enc,vals)))})
    return {'original_vertices':60,'source_face_indices':data['face_source_indices'],'actual_source_antipodes':data['actual_antipodes'],'constant_U':g.vec(g.U),'U_squared':g.enc(g.U2),'height_h':g.enc(h),'centroid_foot':g.vec(foot),'equilateral_side_records':side_records,'receiving_U_support_controls':len(stream),'source_U_support_controls':len(source_stream),'full_U_stream_sha256':g.digest(list(map(g.enc,stream+source_stream))),'cusp_squared_ratio':g.enc(ratio),'strict_margin_over_radius_squared':g.enc(ratio-g.rho*g.rho),'closed_edge_receiver_supports':receiving}
def general_rotation():
    c=[p.P.variable(i,n=3) for i in range(3)];N=1+p.dot(c,c);Rn=p.rot_num(c);K=p.skew(c)
    g.require(p.mm(p.transpose(Rn),Rn)==tuple(tuple(N*N*int(i==j) for j in range(3)) for i in range(3)) and p.det(Rn)==N*N*N,'all free three-variable proper rotation polynomial identities')
    lhs=p.mm(tuple(tuple(Rn[i][j]+N*int(i==j) for j in range(3)) for i in range(3)),K)
    g.require(lhs==tuple(tuple(Rn[i][j]-N*int(i==j) for j in range(3)) for i in range(3)),'all Cayley fixed-axis inverse identities')
    g.require(p.det(tuple(tuple(Rn[i][j]+N*int(i==j) for j in range(3)) for i in range(3)))==N*N*8,'positive cleared I+R determinant')
    return {'free_Cayley_variables':3,'orthogonality_entries':9,'determinant_identities':2,'fixed_axis_inverse_entries':9,'whole_coefficient_record_sha256':g.digest([v.coefficients() for row in Rn for v in row])}
def circle():
    eps,z=p.P.variable(0),p.P.variable(1)
    U=tuple(p.P(x) for x in g.U);c=tuple(z*x for x in g.U);N=1+z*z*g.U2;Rn=p.rot_num(c)
    r=(p.P(g.qx)-eps,p.P(1),p.P(-g.t));e=tuple(p.P(v) for v in a.sub(g.V[36],g.V[0]));m=p.cross(e,r);hm=p.dot(m,tuple(p.P(v) for v in g.V[0]));D=p.P(4*g.t)-eps*g.qx
    expected={31:z*(eps-D*z)*(g.t/2),
        41:(D*z-eps)*(p.P(F(1,4))+z*((g.S-5)/8)),
        43:z*(p.P(-g.t)+eps*Q(F(1,2))+z*(p.P(2*g.S-5)+eps*((3*g.S-7)/4)))}
    rows=[]
    fixtures=[]
    for k in (31,41,43):
        W=tuple(p.P(v) for v in g.act(g.G,g.V[k]));f=(p.dot(m,p.act(Rn,W))-hm*N)*Q(F(1,2))
        g.require(f==expected[k],'entire univariate-receiver/quadratic-source contact factor, source'+str(k))
        rows.append({'source_index':k,'coefficients':f.coefficients()})
        for ee in (Q(),g.L/2,g.L):
            for zz in (-g.rho,Q(),g.rho,ee/(4*g.t-g.qx*ee)):
                rr=g.raw(ee);mm=a.cross(a.sub(g.V[36],g.V[0]),rr);hh=a.dot(mm,g.V[0]);R=g.rotation(a.scale(zz,g.U));v=g.act(g.G,g.V[k])
                direct=(a.dot(mm,g.act(R,v))-hh)*(1+zz*zz*g.U2)/2
                g.require(direct==f.at((ee,zz)),'independent direct physical rotation/contact coefficient comparison')
                fixtures.append([k,g.enc(ee),g.enc(zz),g.enc(direct)])
    # The signs extend by convex/bilinear interpolation over the entire rectangle.
    f43=[];f41=[]
    for ee in (Q(),g.L):
        for zz in (-g.rho,g.rho):
            f43.append(-g.t+ee/2+zz*(2*g.S-5+ee*(3*g.S-7)/4))
            f41.append(Q(F(1,4))+zz*(g.S-5)/8)
    g.require(max(f43)<0 and min(f41)>0,'ALL closed rectangle factor signs, including each endpoint')
    return {'literal_width_rows':rows,'whole_factor_coefficients_sha256':g.digest(rows),'closed_factor_controls':8,'maximum_negative_row43_factor':g.enc(max(f43)),'minimum_positive_row41_factor':g.enc(min(f41)),'direct_exact_contact_comparisons':len(fixtures),'direct_fixture_stream_sha256':g.digest(fixtures),'source_line_bound':g.enc(g.rho),'closed_top_edge_length':g.enc(g.L)}
def companion():
    eps=p.P.variable(0);r=(p.P(g.qx)-eps,p.P(1),p.P(-g.t));rr=p.dot(r,r);D=p.P(4*g.t)-eps*g.qx;c=tuple(eps*u for u in g.U);cc=p.dot(c,c);Ku=p.skew(c)
    Cn=tuple(tuple((D*D-cc)*int(i==j)+c[i]*c[j]*2+Ku[i][j]*D*2 for j in range(3)) for i in range(3));W=D*D+cc
    M=tuple(tuple(rr*int(i==j)-r[i]*r[j]*2 for j in range(3)) for i in range(3));P=tuple(tuple(rr*int(i==j)-r[i]*r[j] for j in range(3)) for i in range(3))
    GP=tuple(tuple(p.P(v) for v in row) for row in g.G);MY=tuple(tuple(p.P(v) for v in row) for row in g.MY)
    left=p.mm(p.mm(M,GP),MY);right=p.mm(Cn,GP)
    g.require(tuple(tuple(v*W for v in row) for row in left)==tuple(tuple(v*rr for v in row) for row in right),'all exact whole-edge proper companion/Cayley identities')
    g.require(W==rr*(4*g.t),'positive two-reflection denominator identity')
    g.require(p.mm(M,M)==tuple(tuple(rr*rr*int(i==j) for j in range(3)) for i in range(3)) and p.det(M)==-rr*rr*rr,'actual whole-edge improper receiving reflection')
    g.require(p.mm(P,M)==tuple(tuple(v*rr for v in row) for row in P),'whole moving reflection preserves projected source set')
    physical=[]
    for ee in (Q(),Q(F(1,100)),g.L/2,g.L):
        r0=g.raw(ee);M0=g.reflection(r0);J=g.mm(g.mm(M0,g.G),g.MY);kap=ee/(4*g.t-g.qx*ee);R=g.rotation(a.scale(kap,g.U));g.proper(J)
        g.require(J==g.mm(R,g.G) and g.mm(g.mm(M0,J),g.MY)==g.G,'literal proper companion and involution at exact fixtures')
        Proj=tuple(tuple(g.I[i][j]-r0[i]*r0[j]/a.dot(r0,r0) for j in range(3)) for i in range(3))
        g.require({g.act(Proj,g.act(J,v)) for v in g.V}=={g.act(Proj,g.act(g.G,v)) for v in g.V},'all60 genuine projected-source set preservation')
        g.require((J==g.G)==(ee==0),'retained actual branch merger at q')
        physical.append({'epsilon':g.enc(ee),'companion_relative_Cayley':g.vec(a.scale(kap,g.U)),'distinct_from_G':ee!=0})
    return {'whole_edge_Cayley_companion_entries':9,'reflection_involution_entries':9,'reflection_determinant_identity':1,'projection_preservation_entries':9,'positive_denominator_identity':1,'genuine_projection_fixture_points':60*len(physical),'physical_fixtures':physical}
def record(data=None):
    if data is None:data=json.loads((HERE/'certificate.json').read_text())
    data=parameters(data)
    return {'agent':'six-rupert-2','role':'researcher','scope':'ordinary CONDITIONAL branch-aware original-source collar on ENTIRE closed top edge; lambda>=1, arbitrary physical T retained','certificate_sha256':g.digest(data),'geometry':geometry(data),'general_rotation':general_rotation(),'source_circle':circle(),'whole_companion_action':companion(),'physical_Cayley_radius':g.enc(g.rho),'relative_trace_gate':g.enc(3-4*g.rho*g.rho/(1+g.rho*g.rho)),'relative_Frobenius_squared_gate':g.enc(8*g.rho*g.rho/(1+g.rho*g.rho)),'prior_whole_edge_G_sufficiency':'LEMMA9961/0, bafkreicf4uiglabu2wi2rpbutlucr5babhngbu643cmzd6i3yty2nyglg4; mathematical dependency, full9961 ray/width certificate NOT replayed here','global_J74_status':'OPEN','formalized':False,'independent_review':False}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');parser.add_argument('--output');args=parser.parse_args()
    r=record()
    if not args.emit:g.require(r==json.loads((HERE/'expected.json').read_text()),'ENTIRE expected mathematical record required')
    text=json.dumps(r,indent=2)+'\n'
    if args.output:Path(args.output).write_text(text)
    print(json.dumps({'agent':r['agent'],'role':r['role'],'whole_record_sha256':g.digest(r),'scope':r['scope'],'global_J74_status':'OPEN'},indent=2))
