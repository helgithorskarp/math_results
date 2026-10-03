#!/usr/bin/env python3
"""Exact original HB labels and a fresh complete continuum boundary hull.

The finite selected-point necessity argument is an explicit ordinary
dependency of the published G-merger proof, not replayed by this file.
No old source forest, hull/contact cache, LP or float is imported.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, json
import geometry as g
import polynomial as p
Q,a=g.Q,g.a
HERE=Path(__file__).resolve().parent
B=((-g.aa,-Q(1)/2,-g.bb),(Q(1)/2,-g.bb,g.aa),(-g.bb,-g.aa,Q(1)/2))
HB=g.mm(g.H,B)
AX=((Q(1),Q(),Q()),(Q(),Q(-1),Q()),(Q(),Q(),Q(-1)))
USED=[13,15,31,10,8,28,41,38,43,36,29]
G_ROWS=[([43,7],28,Q(F(5,2),F(-11,10))),([7,27],28,Q(F(-1,2),F(3,10))),
        ([39,47],29,Q(-4,F(9,5))),([0,4],13,Q(1,F(-2,5))),([0,4],15,Q(1,F(-2,5)))]

def projected(v,epsilon):
    return (v[0]-(g.qx-epsilon)*v[1],v[2]+g.t*v[1])
def turn(v,w,z):
    e=a.sub(w,v);f=a.sub(z,v)
    return e[0]*f[1]-e[1]*f[0]
def qnum(v):return tuple(p.P(w,n=2) for w in v)

def source_configuration(data,source,claim_full_action=False):
    _,caps,_,built,axes=g.model.cupola_construction()
    g.require(len(g.V)==len(set(g.V))==60 and built==set(g.V) and len(caps)==2
              and a.cross(axes[0],axes[1])!=g.Z,'original named J74: two NONOPPOSITE cupola gyrations')
    for M in (g.G,g.H,B,source):g.proper(M)
    for M in (g.H,g.MY):
        g.require({g.act(M,v) for v in g.V}==set(g.V),'ALL60 actual original H/My body images')
    g.require(g.det(g.MY)==-1 and g.mm(g.MY,g.MY)==g.I,'actual improper involution My')
    g.require(g.mm(tuple(zip(*g.G)),source)==AX,'actual proper relative G-transpose HB')
    g.require(g.mm(AX,g.MY)==g.mm(g.MY,AX) and g.mm(AX,g.H)==g.mm(g.H,AX),
              'relative Ax commutes with actual My and H')
    nonimages=[i for i,v in enumerate(g.V) if g.act(AX,v) not in set(g.V)]
    if claim_full_action:g.require(not nonimages,'false full-body Ax action')
    g.require(len(nonimages)==20,'Ax is NOT a full-body symmetry; no whole-solid transport')
    WG=[g.act(g.G,v) for v in g.V];WA=[g.act(source,v) for v in g.V]
    selected=data['source_mapping']
    g.require([i for i,_ in selected]==USED,'complete exact source inventory of the published necessity argument')
    g.require(len({j for _,j in selected})==11,'eleven distinct original HB labels')
    point_records=[]
    for i,j in selected:
        g.require(0<=j<60 and WG[i]==WA[j],'EVERY labelled shared source vertex in original coordinates')
        point_records.append([i,j,g.vec(WG[i])])
    mapping=dict(selected);h=(7+g.S)/4
    face=data['positive_triangle_pairs']
    g.require(face==[[mapping[13],mapping[10]],[mapping[15],mapping[8]],[mapping[31],mapping[28]]],
              'complete actual paired triangle inventory')
    for i,j in face:
        g.require(a.add(WA[i],WA[j])==g.Z and a.dot(g.U,WA[i])==h,'genuine original opposite triangle vertices')
    triangle=[WA[i] for i,_ in face]
    center=tuple(sum(v[k] for v in triangle)/3 for k in range(3))
    g.require(center==a.scale(h/g.U2,g.U) and h>0,'exact source centroid and positive height')
    distances=[]
    for v,w in zip(triangle,triangle[1:]+triangle[:1]):
        e=a.sub(w,v);d=a.sub(center,v);ee=a.dot(e,e)
        dd=a.dot(d,d)-a.dot(d,e)*a.dot(d,e)/ee
        g.require(ee==1 and dd==Q(F(1,12)),'ALL triangle sides and disk inradius')
        distances.append(g.enc(dd))
    pairs=data['width_pairs']
    g.require(pairs==[[mapping[31],mapping[28]],[mapping[41],mapping[38]],[mapping[43],mapping[36]]],
              'complete actual three width-pair inventory')
    for i,j in pairs:g.require(a.add(WA[i],WA[j])==g.Z,'each width uses a genuine antipodal pair')
    rows=data['stress_contacts'];g.require(len(rows)==5,'five actual stress rows')
    for row,(edge,i,weight) in zip(rows,G_ROWS):
        g.require(row['edge']==edge and row['source']==mapping[i] and g.dec(row['weight'])==weight>0,
                  'identical original receiving row, actual selected source, and positive exact weight')
        g.require(WA[row['source']]==WG[i],'FULL source coordinates in every stress row, not first-order equality')
    return {'actual_selected_source_points':point_records,'source_triangle_pairs':face,
            'source_triangle_centroid':g.vec(center),'all_three_inradius_squared':distances,
            'original_width_pairs':pairs,'original_stress_contacts':rows,
            'actual_Ax_nonoriginal_image_labels':nonimages,'G_and_HB_whole_vertex_sets_equal':set(WG)==set(WA),
            'common_full_original_rotated_points':len(set(WG)&set(WA)),
            'source_subset_transfer_scope':'pointwise inclusion ONLY; complete finite G necessity argument is an explicit ordinary dependency; no whole-body equality or replay of its stress bound'}

def companions(source,factor):
    g.require(g.det(factor)==-1 and g.mm(factor,factor)==g.I,'right companion factor must be an improper involution')
    g.require({g.act(factor,v) for v in g.V}==set(g.V),'actual right-factor body action')
    epsilon,eta=[p.P.variable(i,n=2) for i in range(2)]
    r=(p.P(g.qx)-epsilon,p.P(1),p.P(-g.t)-eta);rr=p.dot(r,r)
    M=tuple(tuple(rr*int(i==j)-2*r[i]*r[j] for j in range(3)) for i in range(3))
    Proj=tuple(tuple(rr*int(i==j)-r[i]*r[j] for j in range(3)) for i in range(3))
    g.require(p.mm(M,M)==tuple(tuple(rr*rr*int(i==j) for j in range(3)) for i in range(3))
              and p.det(M)==-rr*rr*rr,'FREE two-variable receiving reflection')
    g.require(p.mm(Proj,M)==tuple(tuple(v*rr for v in row) for row in Proj),
              'FREE projected companion preserves SAME original translation and scale')
    den=p.P(4*g.t)-epsilon*g.qx+eta*g.t;w=(-eta,epsilon*g.t+eta*g.qx,epsilon)
    numerator=tuple(tuple((den*den-p.dot(w,w))*int(i==j)+2*w[i]*w[j]+2*den*p.skew(w)[i][j]
                          for j in range(3)) for i in range(3))
    src=tuple(qnum(row) for row in source);my=tuple(qnum(row) for row in factor)
    left=p.mm(p.mm(M,src),my);right=p.mm(numerator,src);dn=den*den+p.dot(w,w)
    g.require(tuple(tuple(v*dn for v in row) for row in left)==tuple(tuple(v*rr for v in row) for row in right),
              'FREE full-wedge ACTUAL Jr(HB)=R(w/den)HB, including merger; not Cr(HB)')
    tests=[]
    for epsilon0,eta0,c,T,scale in [(Q(),Q(),(Q(),Q(),Q()),(Q(2),Q(-3),Q(1)),Q(1)),
                                   (Q(F(1,100)),Q(F(1,200)),(Q(F(1,7)),Q(F(-1,11)),Q(F(1,13))),
                                    (Q(-1),Q(2),Q(3)),Q(F(7,6)))]:
        r0=g.raw(g.qx-epsilon0,g.t+eta0);rr0=a.dot(r0,r0);Mr=g.reflection(r0)
        project=lambda v:a.sub(v,a.scale(a.dot(r0,v)/rr0,r0))
        base=g.mm(g.rotation(c),source);J=lambda motion:g.mm(g.mm(Mr,motion),factor)
        g.proper(J(base));g.require(J(J(base))==base,'actual original companion is an involution')
        g.require(J(g.mm(base,g.H))==g.mm(J(base),g.H),'commutes with actual right H')
        for v in g.V:
            leftv=a.add(a.scale(scale,project(g.act(J(base),v))),T)
            rightv=a.add(a.scale(scale,project(g.act(base,g.act(factor,v)))),T)
            g.require(leftv==rightv,'EVERY spatial original companion image with same arbitrary T/scale')
            tests.append(g.vec(leftv))
    return {'free_receiving_variables':2,'whole_companion_identity_entries':9,
            'actual_Jr_HB_Cayley_numerator':['-eta','t*epsilon+qx*eta','epsilon'],
            'positive_denominator':'4t-qx*epsilon+t*eta','same_T_scale_direct_controls':len(tests),
            'whole_direct_image_SHA256':g.digest(tests),'direct_fixture_scope':'identity checks only; second fixture is outside the theorem gate'}

def hull(data,source,transcript):
    delta=g.dec(data['receiver_wedge_delta']);C=data['open_receiving_cycle'];QC=data['q_receiving_cycle']
    g.require(len(C)>=3 and len(set(C))==len(C) and all(0<=i<60 for i in C),'distinct original open-cycle labels')
    g.require(len(QC)>=3 and len(set(QC))==len(QC) and all(0<=i<60 for i in QC),'distinct original merger-cycle labels')
    WA=[g.act(source,v) for v in g.V];r0=g.raw(g.qx,g.t);r1=(Q(-1),Q(),Q())
    turns=[];pair_records=[];receiver=[];moving=[];support_records=[];direct=[]
    for k,i in enumerate(C):
        j=C[(k+1)%len(C)];l=C[(k+2)%len(C)];e=a.sub(g.V[j],g.V[i])
        n0=a.cross(r0,e);n1=a.cross(r1,e);h0=a.dot(n0,g.V[i]);h1=a.dot(n1,g.V[i])
        c0=h0-a.dot(n0,g.V[l]);c1=h1-a.dot(n1,g.V[l]);cd=c0+delta*c1
        g.require(c0>=0 and cd>0,'strict adjacent receiving turn on ENTIRE0<epsilon<=delta')
        turns.append([i,j,l,g.enc(c0),g.enc(c1),g.enc(cd)])
        for label,body,stream in [('receiver',g.V,receiver),('HB',WA,moving)]:
            gaprows=[]
            for source_label,v in enumerate(body):
                b0=h0-a.dot(n0,v);b1=h1-a.dot(n1,v);bd=b0+delta*b1
                g.require(b0>=0 and bd>=0,'EVERY actual '+label+' continuum support gap endpoint')
                row=[i,j,source_label,g.enc(b0),g.enc(b1),g.enc(bd)]
                stream.append(row);gaprows.append(row)
                for epsilon in (Q(),delta/2,delta):
                    spatial=b0+epsilon*b1
                    planar=turn(projected(g.V[i],epsilon),projected(g.V[j],epsilon),projected(v,epsilon))
                    g.require(spatial==planar,'EVERY full spatial support affine vs direct projected determinant')
                    direct.append([label,i,j,source_label,g.enc(epsilon),g.enc(spatial)])
            support_records.append({'edge':[i,j],'body':label,'all60_affine_gap_SHA256':g.digest(gaprows)})
    for k,i in enumerate(C):
        for j in C[k+1:]:
            v0=a.sub(projected(g.V[i],Q()),projected(g.V[j],Q()))
            vd=a.sub(projected(g.V[i],delta),projected(g.V[j],delta))
            g.require(v0[1]==vd[1],'fixed second quotient coordinate')
            g.require(v0[1]!=0 or (vd[0]!=0 and (v0[0]==0 or v0[0]*vd[0]>0)),
                      'ALL nonconsecutive cycle pairs distinct on ENTIRE open edge')
            pair_records.append([i,j,g.vec(v0),g.vec(vd)])
    qreceiver=[];qmoving=[];qturns=[];qrecords=[]
    qpoints=[projected(g.V[i],Q()) for i in QC]
    g.require(len(set(qpoints))==len(QC),'actual merger cycle has distinct projected points')
    for k,i in enumerate(QC):
        j=QC[(k+1)%len(QC)];l=QC[(k+2)%len(QC)]
        ct=turn(projected(g.V[i],Q()),projected(g.V[j],Q()),projected(g.V[l],Q()))
        g.require(ct>0,'strict ALL merger receiving turns after true degeneracies removed')
        qturns.append([i,j,l,g.enc(ct)])
        for label,body,stream in [('receiver',g.V,qreceiver),('HB',WA,qmoving)]:
            gaps=[]
            for source_label,v in enumerate(body):
                val=turn(projected(g.V[i],Q()),projected(g.V[j],Q()),projected(v,Q()))
                g.require(val>=0,'EVERY actual merger '+label+' point in the complete receiving polygon')
                row=[i,j,source_label,g.enc(val)];stream.append(row);gaps.append(row)
            qrecords.append({'edge':[i,j],'body':label,'all60_original_gap_SHA256':g.digest(gaps)})
    if transcript is not None:
        transcript.update(all_open_receiver_affine_gaps=receiver,all_open_HB_affine_gaps=moving,
                          all_q_receiver_gaps=qreceiver,all_q_HB_gaps=qmoving,all_spatial_planar_comparisons=direct)
    return {'open_receiving_cycle':C,'all_open_adjacent_turn_coefficients':turns,
            'zero_q_turns_of_open_cycle':sum(g.dec(row[3])==0 for row in turns),
            'all_open_cycle_pair_separation_records':pair_records,
            'whole_open_receiver_affine_gap_SHA256':g.digest(receiver),'whole_open_HB_affine_gap_SHA256':g.digest(moving),
            'original_open_endpoint_controls':2*(len(receiver)+len(moving)),'all_open_support_records':support_records,
            'q_receiving_cycle':QC,'actual_q_distinct_original_projections':len({projected(v,Q()) for v in g.V}),
            'all_q_adjacent_turn_records':qturns,'all_q_support_records':qrecords,'original_q_support_controls':len(qreceiver)+len(qmoving),
            'whole_q_receiver_gap_SHA256':g.digest(qreceiver),'whole_q_HB_gap_SHA256':g.digest(qmoving),
            'whole_spatial_planar_comparisons':len(direct),'whole_spatial_planar_SHA256':g.digest(direct),
            'continuum_bridge':'affinity of ALL gaps and turns; pair separation; complete exposed receiving polygon on open edge; fresh complete nondegenerate polygon at q, not a sampled-feasibility theorem'}

def record(data=None,transcript=None,source_override=None,claim_full_action=False,companion_factor=None):
    if data is None:data=json.loads((HERE/'certificate.json').read_text())
    g.require(data['schema']==1 and data['agent']=='six-rupert-2' and data['role']=='researcher','literal schema/author')
    source=HB if source_override is None else source_override
    factor=g.MY if companion_factor is None else companion_factor
    rho=g.dec(data['physical_Cayley_radius']);delta=g.dec(data['receiver_wedge_delta'])
    g.require(rho==Q(F(1,1000)) and 0<delta<=rho,'physical gate and closed receiver interval')
    beta=Q(F(1,4),F(-3,20));KJ,CR=99930012,805116900
    upper=beta+(KJ+CR)*delta
    g.require(upper<0,'strict FINITE upper from explicit published selected-point dependency, not an infinitesimal sign')
    g.require(delta<=Q(F(1,905077199000)),'within the ACTUAL closed receiving domain of the imported necessity argument')
    conf=source_configuration(data,source,claim_full_action)
    comp=companions(source,factor)
    boundary=hull(data,source,transcript)
    return {'agent':'six-rupert-2','role':'researcher','scope':'finite CONDITIONAL HB companion collar on closed J74 q wedge, all original T/lambda>=1; reusable eleven-point necessity',
            'physical_Cayley_radius':g.enc(rho),'closed_receiver_delta':g.enc(delta),
            'trace_gate':g.enc(3-4*rho*rho/(1+rho*rho)),'Frobenius_squared_gate':g.enc(8*rho*rho/(1+rho*rho)),
            'source_configuration':conf,'proper_companions':comp,'fresh_boundary_hull':boundary,
            'ordinary_finite_necessity_dependency':{'source_commit':'c6c32dc036534de446baa559d7456418198785e6',
                'file':'../halfturn_merger_wedge/PROOF.md','scope':'ONLY the selected-point necessity argument and its full finite constants; not whole G theorem transport or old fixedG sufficiency',
                'replayed_here':False,'committed_artifact_ref':'bafkreicl6zoh3xixpcj2ddkec3hdazsfqwrdzys4ur7ba2aspdtxawvm5i','graph_position_at_creation':[10093,6]},
            'selected_dependency_strict_finite_upper':g.enc(upper),'no_arbitrary_source_entry':True,
            'global_J74_status':'OPEN','independent_review':False,'formalized':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');parser.add_argument('--output');parser.add_argument('--transcript');args=parser.parse_args()
    full={};result=record(transcript=full)
    if not args.emit:g.require(result==json.loads((HERE/'expected.json').read_text()),'ENTIRE compact expected mathematical record')
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    if args.transcript:
        full['whole_mathematical_record']=result
        Path(args.transcript).write_text(json.dumps(full,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'agent':'six-rupert-2','role':'researcher','WHOLE_record_SHA256':g.digest(result),
                      'all_original_endpoint_controls':result['fresh_boundary_hull']['original_open_endpoint_controls'],
                      'all_original_q_controls':result['fresh_boundary_hull']['original_q_support_controls'],
                      'global_J74_status':'OPEN'},indent=2))
