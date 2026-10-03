"""Complete exact local RID certificate replay. CPython3.11+, stdlib only."""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, json, resource, sys, time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from primitives import F,Z,O,phi,vertices,dot,cross,sub,encode,rotate,need,digest,hull,projection,turn,matrix_det
import collar, bridge

def fixed_source_checks(cert,local):
    V=vertices();c=tuple(F(*a) for a in cert['source_cayley']);M=[rotate(c,v) for v in V]
    basis=[tuple(O if i==j else Z for i in range(3)) for j in range(3)]
    cols=[rotate(c,v) for v in basis];R=tuple(zip(*cols))
    need(all(dot(a,b)==(O if i==j else Z) for i,a in enumerate(cols) for j,b in enumerate(cols)), 'original proper source orthogonality fails')
    need(matrix_det(R)==O and sum((R[i][i] for i in range(3)),Z)==1+phi,'original36-degree source matrix differs')
    sphere=7+8*phi
    need(all(dot(v,v)==sphere for v in V),'original sphere radius differs')
    span=[(O,O,phi**3),(-O,O,phi**3),(O,-O,phi**3)]
    need(all(v in V and tuple(-q for q in v) in V for v in span) and matrix_det(span)!=Z,'original origin-interior witness fails')
    x0,x1=[F(*a) for a in local['whole_closed_receiving_x_interval']]
    theta=F(Q(cert['theta_upper']));corners=[(x,x*t,O) for x in (x0,x1) for t in (Z,theta)]
    E6=sub(V[18],V[46]);anchor=V[46];c2=dot(c,c)
    W=tuple((O+c2)*(M[53][j]-anchor[j]) for j in range(3));cut=cross(W,E6)
    need(cut==(Z,F(Q(16,5))*(2*phi-3),Z) and cut[1]>Z,'actual necessary source53 row differs')
    necessary=[]
    for r in corners:
        m=cross(E6,r);h=dot(m,anchor);gaps=[h-dot(m,v) for v in V]
        need(h>Z and all(a>=Z for a in gaps),'theta-eliminating row is not an actual support on the whole rectangle')
        need(dot(m,M[53])-h==dot(cut,r)/(O+c2),'literal theta-eliminating physical row differs')
        necessary.append({'r':encode(r),'height':h.encode(),'all60_original_support_controls':encode(gaps)})
    width=[];receiving=[];moving=[];hulls=[]
    ring=cert['ring'];E0=sub(V[36],V[48]);E7=sub(V[19],V[18])
    need(E0==(phi-1,O,-phi) and E7==(Z,Z,F(2)),'written original width edges differ')
    for x in (x0,x1):
        r=(x,Z,O);n0=cross(E0,r);n7=(Z,F(2),Z);h0=dot(n0,V[48]);h7=dot(n7,V[18])
        need(n0==(O,1-phi*(1+x),-x) and h0==3*phi+(1+3*phi)*x and h7==2+4*phi,'permanent width formulas differ')
        need(dot(n0,M[32])==h0 and dot(n7,M[47])==h7 and h0>Z and h7>Z,'actual permanent positive source contacts differ')
        width_gaps=[h-dot(n,v) for n,h in ((n0,h0),(n7,h7)) for v in V]
        need(all(a>=Z for a in width_gaps),'permanent width row is not an original support')
        determinant=dot(r,cross(n0,n7));need(determinant==2*dot(r,r) and determinant!=Z,'original physical translation span fails')
        width.append({'r':encode(r),'normals':[encode(n0),encode(n7)],'heights':encode((h0,h7)),'moving_contact_labels':[32,47],'all120_support_controls':encode(width_gaps),'spanning_determinant':determinant.encode()})
        for si,i in enumerate(ring):
            j=ring[(si+1)%len(ring)];m=cross(sub(V[j],V[i]),r);h=dot(m,V[i])
            rg=[h-dot(m,v) for v in V];mg=[h-dot(m,v) for v in M]
            need(h>Z and all(a>=Z for a in rg+mg),'full original endpoint receiving/moving ring control fails')
            receiving.extend(rg);moving.extend(mg)
        H=hull([projection(v,r) for v in V]);J=hull([projection(v,r) for v in M])
        need(H!=J and all(turn(a,b,p)>=Z for a,b in zip(H,H[1:]+H[:1]) for p in J),'genuine proper touching endpoint containment fails')
        hulls.append({'r':encode(r),'receiving_hull':[encode(p) for p in H],'moving_hull':[encode(p) for p in J]})
    rho=F(Q(cert['left_Cayley_radius']));trace=3-4*rho*rho/(O+rho*rho);distance=8*rho*rho/(O+rho*rho)
    need(trace==F(Q(18749999,6250001)) and distance==F(Q(8,6250001)),'actual physical trace/Frobenius gate differs')
    return {'actual_named_vertex_sha256':digest(list(map(encode,V))),'original_squared_sphere_radius':sphere.encode(),'literal_original_proper_matrix':[encode(row) for row in R],
            'actual_origin_interior_span':[encode(v) for v in span],'necessary_theta_row':encode(cut),'all4_actual_necessary_supports':necessary,'all2_original_permanent_width_pairs':width,
            'all2160_receiving_endpoint_controls':encode(receiving),'all2160_moving_endpoint_controls':encode(moving),'independent_full_endpoint_hulls':hulls,
            'physical_trace_gate':trace.encode(),'physical_squared_Frobenius_gate':distance.encode(),
            'published9896_dependency_use':'fixed-R* continuum sufficiency on its entire segment; original theta, lambda, t closure also checked here directly',
            'arbitrary_original_translation_and_enlargement_preserved':True}

def verify(cert):
    local=collar.verify(cert)
    literal=bridge.verify(local,cert)
    fixed=fixed_source_checks(cert,local)
    return {'local':local,'literal_nonlinear_bridge':literal,'fixed_source_and_physical_closure':fixed}

def summarize(mat):
    local=mat['local'];literal=mat['literal_nonlinear_bridge'];fixed=mat['fixed_source_and_physical_closure']
    return {'agent':'six-rupert-3','role':'researcher','whole_mathematical_record_sha256':digest(mat),
            'source_cayley':local['source_cayley'],'receiving_chart':local['receiving_chart'],
            'entire_closed_x_interval':local['whole_closed_receiving_x_interval'],'entire_closed_theta_interval':local['whole_closed_receiving_theta_interval'],
            'closed_physical_left_Cayley_radius':local['closed_physical_left_Cayley_radius'],
            'six_signed_mass_bounds':local['six_signed_mass_bounds'],'three_axis_mass_bounds':local['three_axis_mass_bounds'],
            'nonlinear_absorption':local['nonlinear_absorption'],'original_support_controls':1200,
            'complete_dual_tensor_controls':local['independent_complete_literal_tensor_coefficient_checks'],
            'independent_literal_Gaussian_grid_checks':local['independent_literal_Gaussian_grid_checks'],
            'literal_nonlinear_identities':literal['literal_contact_identity_control_count'],'actual_nonzero_rotation_controls':6,
            'additional_theta_eliminating_support_controls':240,'additional_width_support_controls':240,
            'additional_full_original_endpoint_support_controls':len(fixed['all2160_receiving_endpoint_controls'])+len(fixed['all2160_moving_endpoint_controls']),
            'original_named_vertex_sha256':fixed['actual_named_vertex_sha256'],'physical_trace_gate':fixed['physical_trace_gate'],'physical_squared_Frobenius_gate':fixed['physical_squared_Frobenius_gate'],
            'original_lambda_and_translation':'all lambda>=1 and t in r-perp quantified; fitting iff lambda1,t0,theta0,parent motion',
            'source_gate_is_a_hypothesis':True,'whole_source_cover_claimed':False,'new_group_enumeration_or_distinct_pose_count_claimed':False,
            'strict_Rupert_passage_claimed':False,'global_RID':'OPEN','proof_status':'author checked, unformalized, independently UNREVIEWED'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--compare',type=Path)
    args=p.parse_args();start=time.monotonic()
    if args.output:need(not args.output.exists(),'fresh output required')
    cert=json.loads((HERE/'certificate.json').read_text());mat=verify(cert);summary=summarize(mat)
    if args.compare:need(summary==json.loads(args.compare.read_text()),'full mathematical record fingerprint or scope differs')
    record={'mathematical':mat,'summary':summary,'seconds':round(time.monotonic()-start,3),'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':not __debug__,'threads':1,'external_child_guard_seconds':20,
            'runtime_source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ['check.py','collar.py','bridge.py','primitives.py','field.py','certificate.json']}}
    if args.output:args.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'summary':summary,'seconds':record['seconds'],'peak_kib':record['peak_kib'],'optimized':record['optimized']},sort_keys=True))

if __name__=='__main__':main()
