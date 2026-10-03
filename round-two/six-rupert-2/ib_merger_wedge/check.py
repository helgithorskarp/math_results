"""Exact I/B finite collar coefficients and whole-wedge shadow equality.

The noneffective all-source corollary is an ordinary compactness proof in
PROOF.md with explicit external mathematical premises; it is not computed.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
import geometry as g
import algebra as p
Q,a=g.Q,g.a;HERE=Path(__file__).resolve().parent
def read_certificate():return json.loads((HERE/'certificate.json').read_text())
def stream(cs):return [[list(e),g.enc(v)] for e,v in cs]
def parameters(cert):
    delta,base,C,rho=[g.dec(cert[k]) for k in ('delta','strict_base_weight','quadratic_bound_C','closed_Cayley_radius')]
    g.require(delta>0 and base>0 and C>Q(F(1,2)) and rho>0,'positive finite domain, every base weight, quadratic bound and physical radius')
    masses=[max(cert['duals'][2*k]['mass_bound'],cert['duals'][2*k+1]['mass_bound']) for k in range(3)]
    absorb=C*C*rho*rho*sum(z*z for z in masses)
    g.require(absorb<1,'finite nonlinear absorption is strictly less than one')
    return delta,base,C,rho,absorb
def body_record():
    built=g.model.cupola_construction()[3]
    g.require(len(g.V)==len(set(g.V))==60 and built==set(g.V),'original named two-nonopposite-cupola J74 construction')
    for A in (g.I,g.H,g.B,g.G,g.mm(g.H,g.B)):g.proper(A)
    perms={}
    for name,A in (('H',g.H),('MX',g.MX),('MY',g.MY)):
        W=[g.act(A,v) for v in g.V]
        g.require(set(W)==set(g.V),'actual full-body '+name+' symmetry')
        perms[name]=[g.V.index(w) for w in W]
    R2=(11+4*g.S)/4
    g.require(all(a.dot(v,v)==R2 for v in g.V),'true original common spatial radius')
    antipodes=((0,7),(1,6),(2,5))
    g.require(all(a.add(g.V[i],g.V[j])==g.Z for i,j in antipodes) and a.dot(g.V[0],a.cross(g.V[1],g.V[2]))!=0,'three independent antipodes put zero in the interior without whole-body centrality')
    return {'actual_body_symmetry_permutations':perms,'original_common_R2':g.enc(R2),'interior_origin_antipodal_pairs':[list(z) for z in antipodes]}
def contact_data(cert,transcript):
    delta,base,C,rho,absorb=parameters(cert)
    corners=((Q(),Q()),(delta,Q()),(delta,delta));contacts=cert['contacts']
    g.require(len(contacts)==30 and len({tuple(z['edge'])+(z['endpoint'],) for z in contacts})==30,'thirty distinct original persistent endpoint contacts')
    for z in contacts:
        i,j=z['edge'];k=z['endpoint'];src=z['B_source']
        g.require(i in range(60) and j in range(60) and k in (i,j),'literal original endpoint contact')
        g.require(src in range(60) and g.act(g.B,g.V[src])==g.V[k],'literal actual B spatial preimage of endpoint')
    mats=[];heights=[];normal_y=[];gaps=[];ratios=[];rod=[]
    cv=tuple(p.P.variable(i) for i in range(3));c2=p.dot(cv,cv);R=p.rot_num(cv)
    for ep,et in corners:
        cols=[];hh=[];my=[]
        for z in contacts:
            i,j=z['edge'];k=z['endpoint'];V=g.V[k];m,h=g.support(i,j,ep,et)
            g.require(h>0,'strict positive selected support height including q')
            gg=[h-a.dot(m,v) for v in g.V];g.require(min(gg)>=0,'every60 genuine receiving supports at every closed wedge corner')
            gaps.extend(g.vec(gg));ratios.append((11+4*g.S)/4*a.dot(m,m)/(h*h))
            g.require(ratios[-1]<(2*C-1)*(2*C-1),'fresh literal nonlinear normalized-normal bound')
            cols.append(tuple(a.cross(V,m))+(m[0],m[2]));hh.append(h);my.append(m[1])
            lhs=p.dot(m,tuple(p.dot(row,V) for row in R))-(1+c2)*h
            rhs=p.dot(cv,a.cross(V,m))*2+p.dot(cv,m)*p.dot(cv,V)*2-c2*(2*h)
            g.require(lhs==rhs,'full original endpoint identity in three free physical Cayley variables')
            rod.append({'edge':z['edge'],'endpoint':k,'epsilon':g.enc(ep),'eta':g.enc(et),
                        'exact_coefficients':[[list(e),g.enc(x)] for e,x in sorted(lhs.terms.items())]})
        mats.append(tuple(zip(*cols)));heights.append(hh);normal_y.append(my)
    ALL=[[p.linear([M[r][k] for M in mats]) for k in range(30)] for r in range(5)]
    H=[p.linear([h[k] for h in heights]) for k in range(30)]
    MY=[p.linear([h[k] for h in normal_y]) for k in range(30)]
    # Two genuine selected normals already span the physical receiving plane.
    nx=[p.linear([g.support(13,31,ep,et)[0][k] for ep,et in corners]) for k in (0,2)]
    ny=[p.linear([g.support(31,43,ep,et)[0][k] for ep,et in corners]) for k in (0,2)]
    force_det=p.add(p.mul(nx[0],ny[1]),p.scale(p.mul(nx[1],ny[0]),-1))
    orient=1 if p.value(force_det,(Q(1),Q(),Q()))>0 else -1
    force_controls=p.controls(p.scale(force_det,orient),2)
    g.require(min(x for e,x in force_controls)>0,'selected physical force normals span the entire receiver plane')
    transcript.update(selected_receiving_every_gap=gaps,original_Rodrigues_every_coefficient=rod,force_span_controls=stream(force_controls))
    small={'contacts':contacts,'original_support_controls':len(gaps),'all_original_support_SHA256':g.digest(gaps),
           'maximum_corner_R2_normal_squared':g.enc(max(ratios)),'physical_force_span_controls':stream(force_controls),
           'full_three_free_variable_Rodrigues_identities':len(rod),'all_Rodrigues_coefficients_SHA256':g.digest(rod)}
    return (ALL,H,MY,base),small
def dual_record(proposal,data,transcript,damage=None):
    ALL,H,MY,base=data;indices=proposal['contact_indices'];axis,sign,bound=[proposal[k] for k in ('axis','sign','mass_bound')]
    g.require(axis in range(3) and sign in (-1,1) and type(bound) is int and bound>0,'literal signed torque and positive integral mass bound')
    g.require(len(indices)==len(set(indices))==5 and all(k in range(30) for k in indices),'five distinct original endpoint column indices')
    L=p.linear((Q(1),)*3);M=[[ALL[r][k] for k in indices] for r in range(5)]
    target=tuple(Q(sign*int(r==axis)) for r in range(5))
    if damage=='false_force_target':target=target[:3]+(Q(1),Q())
    shifted=[p.add(p.scale(L,target[r]),p.scale(p.sum_polys(ALL[r]),-base)) for r in range(5)]
    D=p.det(M);NUM=[p.det([[shifted[r] if c==k else M[r][c] for c in range(5)] for r in range(5)]) for k in range(5)]
    orientation=1 if p.value(D,(Q(1),Q(),Q()))>0 else -1
    D=p.scale(D,orientation);NUM=[p.scale(z,orientation) for z in NUM]
    if damage=='negative_cofactor':NUM[0]=p.scale(NUM[0],-1)
    dc=p.controls(D,5);nc=[p.controls(z,5) for z in NUM]
    g.require(min(z for e,z in dc)>0,'all21 finite determinant controls positive')
    g.require(min(z for zz in nc for e,z in zz)>0,'all105 finite excess-weight controls positive')
    U=[p.scale(D,base) for k in range(30)]
    for k,z in zip(indices,NUM):U[k]=p.add(U[k],z)
    for r in range(5):
        lhs=p.sum_polys(p.mul(ALL[r][k],U[k]) for k in range(30))
        g.require(lhs==p.scale(p.mul(L,D),Q(sign*int(r==axis))),'original signed torque and exactly zero two physical force components')
    g.require(p.sum_polys(p.mul(MY[k],U[k]) for k in range(30))=={},'third original spatial force is exactly zero as a polynomial')
    MASS=p.sum_polys(p.mul(H[k],U[k]) for k in range(30))
    bc=p.controls(p.add(p.scale(p.mul(D,L),bound),p.scale(MASS,-1)),6)
    g.require(min(z for e,z in bc)>0,'all28 strict normalized physical mass controls')
    fixtures=[]
    barycentrics=((Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)),(Q(F(1,3)),)*3)
    for bary in barycentrics:
        A=tuple(tuple(p.value(z,bary) for z in row) for row in M)
        target_direct=tuple(p.value(z,bary) for z in shifted);weights=g.act(p.inverse(A),target_direct)
        g.require(p.value(D,bary)==orientation*p.directdet(A),'independent full exact Gaussian determinant')
        g.require(tuple(p.value(z,bary)/p.value(D,bary) for z in NUM)==weights,'independent full exact inverse and all Cramer weights')
        fixtures.append({'barycentric':g.vec(bary),'exact_excess_weights':g.vec(weights)})
    cs=[stream(x) for x in (dc,*nc,bc)]
    rr={'axis':axis,'sign':sign,'contact_indices':indices,'strict_mass_upper':bound,'positive_control_count':154,
        'minimum_determinant_control':g.enc(min(z for e,z in dc)),
        'minimum_excess_weight_control':g.enc(min(z for zz in nc for e,z in zz)),
        'minimum_mass_control':g.enc(min(z for e,z in bc)),'all_controls_SHA256':g.digest(cs),
        'all_six_original_physical_polynomial_identities':True,'independent_full_direct_fixtures':fixtures}
    transcript.setdefault('every_original_dual_control',[]).append(cs)
    return rr,[p.value(z,(Q(1),Q(),Q()))/p.value(D,(Q(1),Q(),Q())) for z in U]
def q_geometry(cert,transcript):
    cycle=cert['q_cycle'];g.require(len(cycle)==len(set(cycle)),'distinct literal original q labels')
    gg=[];turns=[]
    for pos,i in enumerate(cycle):
        j=cycle[(pos+1)%len(cycle)];k=cycle[(pos+2)%len(cycle)];m,h=g.support(i,j)
        g.require(h>0,'actual positive q support')
        for A in (g.I,g.B):
            for u in g.V:
                z=h-a.dot(m,g.act(A,u))
                zz=g.det2(a.sub(g.projection(g.V[j],Q(),Q()),g.projection(g.V[i],Q(),Q())),a.sub(g.projection(g.act(A,u),Q(),Q()),g.projection(g.V[i],Q(),Q())))
                g.require(z==zz and z>=0,'actual complete q receiver/B spatial and planar containment')
                gg.append(g.enc(z))
        turn=g.det2(a.sub(g.projection(g.V[j],Q(),Q()),g.projection(g.V[i],Q(),Q())),a.sub(g.projection(g.V[k],Q(),Q()),g.projection(g.V[j],Q(),Q())))
        g.require(turn>0,'genuine strict q cycle, without fictitious18-corner degeneration');turns.append(g.enc(turn))
    qpoints=[g.projection(g.V[i],Q(),Q()) for i in cycle]
    g.require(len(set(qpoints))==len(cycle),'actual distinct q extreme projections')
    transcript.update(every_original_q_gap=gg)
    return {'actual_q_cycle':cycle,'all_receiver_and_B_q_controls':len(gg),'all_q_gap_SHA256':g.digest(gg),'all_q_strict_turns':turns,'distinct_original_q_projections':len({g.projection(v,Q(),Q()) for v in g.V})}
def phase_geometry(cert,transcript):
    delta,base,C,rho,absorb=parameters(cert)
    # This literal actual support witness derives the wall, instead of relying on a sample.
    def wallgap(ep,et):
        m,h=g.support(27,3,ep,et);return h-a.dot(m,g.V[55])
    w0=wallgap(Q(),Q());we=wallgap(Q(1),Q())-w0;wt=wallgap(Q(),Q(1))-w0
    g.require(w0==0 and wt!=0,'genuine affine receiver wall witness')
    alpha=-we/wt;g.require(alpha==g.t and Q()<alpha<Q(1),'actual fan wall eta=t epsilon')
    triangles=(((Q(),Q()),(delta,Q()),(delta,alpha*delta)),((Q(),Q()),(delta,alpha*delta),(delta,delta)))
    source=[g.act(g.B,v) for v in g.V];records=[];allgaps=[];allzero=[]
    for cycle,corners in zip(cert['cell_cycles'],triangles):
        g.require(len(cycle)==len(set(cycle))==18,'literal eighteen original receiving labels per open cell')
        pre=[source.index(g.V[i]) if g.V[i] in source else None for i in cycle]
        g.require(all(k is not None for k in pre),'all actual18 receiving corner spatial preimages under B')
        gaps=[];heights=[];turns=[]
        for i,j in zip(cycle,cycle[1:]+cycle[:1]):
            hh=[]
            for ep,et in corners:
                m,h=g.support(i,j,ep,et);hh.append(h)
                for A in (g.I,g.B):
                    for u in g.V:
                        W=g.act(A,u);z=h-a.dot(m,W)
                        zz=g.det2(a.sub(g.projection(g.V[j],ep,et),g.projection(g.V[i],ep,et)),a.sub(g.projection(W,ep,et),g.projection(g.V[i],ep,et)))
                        g.require(z==zz and z>=0,'every actual receiving AND full60 B closed-cell support control with direct spatial/planar comparison')
                        gaps.append(g.enc(z))
            g.require(min(hh)>=0 and max(hh)>0,'positive heights throughout the relative interior; retain true zero corner height')
            zero=g.support(i,j)[0]==g.Z
            if zero:allzero.append([i,j])
            heights.append({'edge':[i,j],'all_corner_heights':g.vec(hh),'true_zero_q_normal':zero})
        for pos,j in enumerate(cycle):
            i,k=cycle[pos-1],cycle[(pos+1)%len(cycle)]
            tt=[g.det2(a.sub(g.projection(g.V[j],ep,et),g.projection(g.V[i],ep,et)),a.sub(g.projection(g.V[k],ep,et),g.projection(g.V[j],ep,et))) for ep,et in corners]
            g.require(min(tt)>=0 and max(tt)>0,'every affine adjacent turn is strict throughout relative cell interior')
            turns.append({'triple':[i,j,k],'all_corner_controls':g.vec(tt)})
        records.append({'cycle':cycle,'closed_corners':[[g.enc(x) for x in v] for v in corners],
                        'literal_B_spatial_preimages':pre,'actual_edge_height_records':heights,'all_adjacent_turns':turns,
                        'complete_original_receiver_B_gap_count':len(gaps),'all_gap_SHA256':g.digest(gaps)})
        allgaps.extend(gaps)
    pairs=[];qcollisions=[]
    for i in range(60):
        for j in range(i+1,60):
            d=a.sub(g.V[j],g.V[i])
            if d[1]==0:
                g.require((d[0],d[2])!=(Q(),Q()),'distinct original spatial vertices')
                pairs.append({'pair':[i,j],'constant_nonzero_component':True});continue
            ep=g.qx-d[0]/d[1];et=-d[2]/d[1]-g.t
            if ep==et==0:qcollisions.append([i,j])
            g.require(not(Q()<ep<=delta and Q()<=et<=ep),'all60 projections distinct throughout epsilon>0 closed wedge')
            pairs.append({'pair':[i,j],'only_possible_epsilon':g.enc(ep),'only_possible_eta':g.enc(et)})
    transcript.update(every_original_whole_cell_gap=allgaps,all1770_original_pair_records=pairs)
    return {'genuine_wall_coefficients':g.vec((w0,we,wt)),'wall_eta_over_epsilon':g.enc(alpha),
            'closed_cells':records,'all_whole_cell_original_receiver_B_gap_controls':len(allgaps),'all_whole_cell_gap_SHA256':g.digest(allgaps),
            'all_original_pair_count':len(pairs),'all_pair_records_SHA256':g.digest(pairs),'retained_actual_q_pair_collisions':qcollisions,
            'true_zero_q_normals_retained':allzero,'whole_wedge_B_shadow_equality_via_supports_and_literal_preimages':True}
def companion_record(cert):
    delta,base,C,rho,absorb=parameters(cert);bases=(g.I,g.H,g.B,g.mm(g.B,g.H));permutation=[g.V.index(g.act(g.MY,v)) for v in g.V]
    comparisons=[]
    for ep,et in ((Q(),Q()),(delta,Q()),(delta,delta),(delta/2,delta/4)):
        for A in bases:
            Jr=g.companion(A,ep,et);g.proper(Jr)
            for k,V in enumerate(g.V):
                u=g.projection(g.act(Jr,V),ep,et);w=g.projection(g.act(A,g.V[permutation[k]]),ep,et)
                g.require(u==w,'whole original companion projected source identity preserving same scale and physical T')
                comparisons.append(g.vec(u))
        C0=g.rotation((rho/2,rho/3,-rho/4));Q0=g.mm(C0,g.B)
        old=g.mm(Q0,tuple(zip(*g.B)));other=g.mm(g.companion(Q0,ep,et),tuple(zip(*g.companion(g.B,ep,et))))
        g.require(sum(old[i][i] for i in range(3))==sum(other[i][i] for i in range(3)),'proper companion relative trace isometry')
    F=(g.I,g.H,g.B,g.mm(g.B,g.H),g.G,g.mm(g.G,g.H),g.mm(g.H,g.B),g.mm(g.mm(g.H,g.B),g.H))
    Mr=g.reflection(g.raw(Q(),Q()))
    old=set(F)|{g.mm(g.mm(Mr,A),g.MX) for A in F}
    current=set(F)|{g.companion(A,Q(),Q()) for A in F}
    g.require(old==current,'full old q fit SET matches current continuous center-family SET')
    return {'whole_original_companion_point_comparisons':len(comparisons),'full_companion_points_SHA256':g.digest(comparisons),
            'relative_trace_fixture_count':4,'actual_q_family_SET_matches_imported_q_registry':True,'distinct_q_centers':len(old)}
def record(cert=None,transcript=None):
    cert=read_certificate() if cert is None else cert;transcript={} if transcript is None else transcript
    delta,base,C,rho,absorb=parameters(cert);body=body_record();data,contact=contact_data(cert,transcript)
    g.require([(x['axis'],x['sign']) for x in cert['duals']]==[(k,s) for k in range(3) for s in (-1,1)],'all six original signed torque targets exactly once')
    duals=[];qweights=[]
    for proposal in cert['duals']:
        rr,weights=dual_record(proposal,data,transcript);duals.append(rr);qweights.append(weights)
    annihilator=[sum((w[k] for w in qweights),Q()) for k in range(30)]
    g.require(min(annihilator)>0,'strict positive q cone annihilator uses every original persistent contact')
    ALL,H,MY,b=data
    g.require(all(sum((p.value(row[k],(Q(1),Q(),Q()))*annihilator[k] for k in range(30)),Q())==0 for row in ALL),'all five original physical first-order annihilator coordinates')
    mass=sum((p.value(H[k],(Q(1),Q(),Q()))*annihilator[k] for k in range(30)),Q());g.require(mass>0,'strict positive original scale column')
    q=q_geometry(cert,transcript);receiving=phase_geometry(cert,transcript);companions=companion_record(cert)
    trace=3-4*rho*rho/(1+rho*rho);frob=8*rho*rho/(1+rho*rho)
    out={'agent':'six-rupert-2','role':'researcher','status':'author exact finite I/B collar data; ordinary proof unformalized and independently UNREVIEWED',
         'delta':g.enc(delta),'closed_Cayley_radius':g.enc(rho),'relative_trace_gate':g.enc(trace),'squared_Frobenius_gate':g.enc(frob),
         'quadratic_bound_C':g.enc(C),'axis_mass_bounds':[max(cert['duals'][2*k]['mass_bound'],cert['duals'][2*k+1]['mass_bound']) for k in range(3)],'nonlinear_absorption_squared':g.enc(absorb),
         'body':body,'contacts':contact,'duals':duals,'q_contact_cone':{'rank':5,'strict_positive_original_annihilator':g.vec(annihilator),'scale_mass':g.enc(mass),'all_three_rotation_both_physical_translation_and_nonnegative_scale_derivatives_forced_zero':True},
         'q_geometry':q,'whole_receiver_geometry':receiving,'companions':companions,
         'all_source_entry':'ordinary compactness in PROOF.md imports full q9918 and finite G10093/6,HB10107/0; delta_star>0 is NOT computed',
         'global_J74_status':'OPEN'}
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output');ap.add_argument('--transcript');ap.add_argument('--emit',action='store_true');args=ap.parse_args()
    tr={};rr=record(transcript=tr)
    if not args.emit:g.require(rr==json.loads((HERE/'EXPECTED.json').read_text()),'complete expected mathematical record')
    if args.output:Path(args.output).write_text(json.dumps(rr,indent=2)+'\n')
    if args.transcript:Path(args.transcript).write_text(json.dumps(tr,indent=2)+'\n')
    print(json.dumps({'agent':'six-rupert-2','role':'researcher','mathematical_record_SHA256':g.digest(rr),
                      'whole_original_transcript_SHA256':g.digest(tr),'original_endpoint_contacts':30,'strict_dual_controls':924,
                      'true_zero_q_normals_retained':rr['whole_receiver_geometry']['true_zero_q_normals_retained'],
                      'all_source_receiving_entry_radius':'exists positive, unspecified; ordinary dependent proof',
                      'global_J74_status':'OPEN'},indent=2))
if __name__=='__main__':main()
