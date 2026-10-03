"""Exact enlarged RID gates and full closed source frustum.

No solver, floating arithmetic, source forest or external runtime input.
The ordinary proof is in PROOF.md. Public10074 supplies only the
fixed-source converse; it is a mathematical citation, not a runtime import.
"""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction as Q
import argparse,hashlib,json,resource,sys,time

HERE=Path(__file__).resolve().parent
sys.dont_write_bytecode=True

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def verify_pins():
    expected=json.loads((HERE/'MANIFEST.json').read_text())['declared_inputs']
    actual={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in expected}
    need(actual==expected,'declared runtime source changed before or after checking')
    return actual

PINS=verify_pins()
sys.path.insert(0,str(HERE))
from field import F,ZERO as Z,ONE as O,PHI as phi,dot,cross,sub,vertices,encode,act,matmul,determinant

def source_geometry():
    V=vertices()
    need(len(V)==60 and digest(list(map(encode,V)))=='fc20f041ee0dd3cb289807af1feb564186d66cc713bf256acc520c93aa26e1b1',
         'literal named RID source vertices differ')
    normals=set()
    seed=(Z,O/2,(phi-1)/2)
    for signs in product((-1,1),repeat=3):
        w=tuple(s*x for s,x in zip(signs,seed))
        for k in range(3):normals.add(w[k:]+w[:k])
    normals=sorted(normals);height=O-phi/2
    need(len(normals)==12 and height>Z,'full source linear forms differ')
    D=set()
    for a,b,c in combinations(normals,3):
        det=dot(a,cross(b,c))
        if det==Z:continue
        w=tuple(height*(cross(b,c)[i]+cross(c,a)[i]+cross(a,b)[i])/det for i in range(3))
        if all(dot(n,w)<=height for n in normals):D.add(w)
    D=sorted(D)
    need(len(D)==20,'twelve-form source polytope vertex enumeration differs')
    face=[(phi-2,Z,5-3*phi),(3-2*phi,3-2*phi,2*phi-3),
          (Z,3*phi-5,2-phi),(Z,5-3*phi,2-phi),(3-2*phi,2*phi-3,2*phi-3)]
    ids=[D.index(w) for w in face]
    need(ids==[1,3,9,11,5],'literal full source pentagon differs')
    normal=(F(Q(1,2),Q(-1,2)),Z,O/2);ni=normals.index(normal)
    need([i for i,w in enumerate(D) if dot(normal,w)==height]==sorted(ids),'source pentagon is not the complete facet')
    need(all(dot(normal,cross(sub(face[(i+1)%5],face[i]),sub(face[j],face[i])))>Z
             for i in range(5) for j in range(5) if j not in [i,(i+1)%5]),
         'literal facet cycle is not strictly convex')
    return {'V':V,'normals':normals,'height':height,'D':D,'record':{'literal_faces':{ni:ids}}}

def rotate(c,v):
    a=dot(c,c);b=dot(c,v);x=cross(c,v)
    return tuple(((O-a)*v[j]+2*c[j]*b+2*x[j])/(O+a) for j in range(3))
def transpose(M):return tuple(zip(*M))
def halfturn(v):return tuple(tuple(2*v[i]*v[j]-(O if i==j else Z) for j in range(3)) for i in range(3))
def matrix(c):
    basis=[tuple(O if i==j else Z for i in range(3)) for j in range(3)]
    return transpose([rotate(c,v) for v in basis])
def evaluate(a,z):return sum((a[i]*z**i for i in range(len(a))),Z)
def multiply(a,b):
    c=[Z]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c
def bernstein2(a,lo,hi):
    delta=hi-lo;v=evaluate(a,lo);l=delta*(a[1]+2*a[2]*lo);q=delta*delta*a[2]
    return [v,v+l/2,v+l+q]
def projection(v,x):return (v[0]-x*v[2],v[1])

def prove(alpha=Q(1,3),wrong_symmetry=False):
    data=source_geometry();V=data['V'];I=tuple(tuple(O if i==j else Z for j in range(3)) for i in range(3))
    p=(F(Q(4,5),Q(-3,5)),Z,F(Q(3,5),Q(-1,5)));A=O+dot(p,p)
    M=matrix(p);moving=[act(M,v) for v in V]
    need(matmul(M,transpose(M))==I and determinant(M)==O,'original parent is not proper')
    lo,hi=2*phi-3,2-phi;U=(Z,O,Z);h=1+2*phi
    need(set(V)=={tuple(-x for x in v) for v in V},'actual source centrality differs')
    u=(F(Q(-2,5),Q(4,5)),Z,F(Q(1,5),Q(-2,5)))
    v=(F(Q(1,5),Q(-2,5)),Z,F(Q(2,5),Q(-4,5)))
    need(dot(u,u)==dot(v,v)==O and dot(u,v)==dot(u,U)==dot(v,U)==Z,'actual square frame differs')
    square=[]
    for name,body,labels in [('receiving',V,[18,19,46,47]),('moving',moving,[35,39,47,53])]:
        gaps=[h-sign*dot(U,w) for sign in (-1,1) for w in body]
        need(all(x>=Z for x in gaps),'full original square paired support fails')
        actual=[i for i,w in enumerate(body) if dot(U,w)==h]
        need(actual==labels,'actual positive square labels differ')
        corners={tuple(h*U[j]+a*u[j]+b*v[j] for j in range(3)) for a,b in product((-1,1),repeat=2)}
        if name=='moving':need(set(body[i] for i in actual)==corners,'literal unit-inradius moving square differs')
        square.append({'body':name,'positive_original_labels':actual,'all120_full_paired_support_gaps':encode(gaps)})
    tight=[i for i,n in enumerate(data['normals']) if dot(n,p)==data['height']]
    need(len(tight)==1,'actual source parent is not on a unique complete facet')
    ni=tight[0];ids=data['record']['literal_faces'][ni];face=[data['D'][i] for i in ids]
    need(len(face)==5 and all(dot(c,p)==dot(p,p) for c in face),'actual complete parent facet plane differs')
    need(tuple(sum((c[j] for c in face),Z)/5 for j in range(3))==p,
         'actual parent is not the full facet centroid')
    vertices=face+[tuple(F(alpha)*x for x in c) for c in face]
    gates=[]
    for c in vertices:
        D=O+dot(c,p);N=sub(sub(c,p),cross(c,p))
        need(D>Z,'full frustum physical relative scalar nonpositive')
        transverse=N[0]*N[0]+N[2]*N[2]
        gap=D*D-h*h*transverse
        need(gap>Z,'whole-frustum transverse cusp entry fails')
        lower=D/4+N[1];upper=D/4-N[1]
        need(lower>=Z and upper>=Z,'full frustum relative yaw bound exceeds1/4')
        need(dot(N,N)+D*D==A*(O+dot(c,c)),'original Cayley metric identity differs')
        source_gaps=[data['height']-dot(n,c) for n in data['normals']]
        need(all(g>=Z for g in source_gaps),'actual frustum vertex leaves the original source quotient')
        relative=tuple(x/D for x in N)
        for basis in ((O,Z,Z),(Z,O,Z),(Z,Z,O)):
            need(rotate(relative,act(M,basis))==rotate(c,basis),
                 'original physical LEFT composition differs at a frustum vertex')
        gates.append({'source_vertex':encode(c),'physical_D':D.encode(),'physical_N':encode(N),
                      'strict_transverse_cusp_gap':gap.encode(),'yaw_lower_gap':lower.encode(),'yaw_upper_gap':upper.encode(),
                      'relative_Cayley':encode(relative),'all12_original_source_membership_gaps':encode(source_gaps),
                      'all3_basis_physical_LEFT_compositions_checked':True})
    # The source-axis line is on the OUTER original facet, not its interior shell.
    direction=(p[2],O,-p[0]);need(dot(direction,p)==Z,'original source yaw line not on the outer facet')
    limits=[];lower=[];upper=[]
    for normal in data['normals']:
        intercept=data['height']-dot(normal,p);slope=dot(normal,direction)
        need(intercept>=Z,'actual c* outside source D')
        if slope>Z:upper.append(intercept/slope)
        elif slope<Z:lower.append(intercept/slope)
        limits.append({'normal':encode(normal),'remaining_at_parent':intercept.encode(),'yaw_slope':slope.encode()})
    zlo,zhi=max(lower),min(upper)
    need(zlo==-(2*phi-3) and zhi==(2-phi)/2,'full actual source-facet yaw interval differs')
    axis_endpoints=[tuple(p[i]+z*direction[i] for i in range(3)) for z in (zlo,zhi)]
    need(axis_endpoints[0]==face[1] and
         axis_endpoints[1]==tuple((face[3][i]+face[4][i])/2 for i in range(3)),
         'actual source yaw endpoint convex membership differs')
    def beta(x):return (2*x-O)/(x+2)
    need(Z<lo<hi<F(Q(1,2)) and beta(lo)==zlo and zlo<beta(hi)<Z<zhi,
         'actual companion membership over the entire receiver interval differs')
    midpoint=(lo+hi)/2
    edges=[(48,36),(36,54)];support_records=[]
    for ia,ib in edges:
        row=[]
        for x in (lo,hi):
            m=cross(sub(V[ib],V[ia]),(x,Z,O));H=dot(m,V[ia])
            gaps=[H-sign*dot(m,w) for sign in (-1,1) for w in V]
            need(H>Z and all(g>=Z for g in gaps),'actual original receiving width support fails')
            row.append({'x':x.encode(),'normal':encode(m),'height':H.encode(),'all120_paired_original_gaps':encode(gaps)})
        support_records.append({'actual_edge':[ia,ib],'all2_endpoint_records':row})
    polynomials={};fixtures=[]
    for name,si,source in [('32',0,32),('40',0,40),('96',1,36)]:
        ia,ib=edges[si];E=sub(V[ib],V[ia]);w=moving[source];values=[]
        for x in (Z,O):
            m=cross(E,(x,Z,O));H=dot(m,V[ia]);q=dot(m,w)
            values.append([A*(q-H),2*A*dot(cross(w,m),U),A*(-q-H+2*dot(m,U)*dot(w,U))])
        b=values[0];a=[values[1][j]-b[j] for j in range(3)];polynomials[name]=(a,b)
        for x in (lo,hi):
            m=cross(E,(x,Z,O));H=dot(m,V[ia])
            for z in (-F(Q(1,4)),Z,F(Q(1,4))):
                literal=A*(O+z*z)*(dot(m,rotate(tuple(z*j for j in U),w))-H)
                need(literal==x*evaluate(a,z)+evaluate(b,z),'full original width polynomial direct identity differs')
                fixtures.append({'row':name,'x':x.encode(),'z':z.encode(),'actual_literal_cleared_width':literal.encode()})
    a32,b32=polynomials['32'];k=F(Q(8,5))*(2*phi-1)
    need(a32==[Z,2*k,-k] and b32==[Z,-k,-2*k] and k>Z,'actual32 branch factor differs')
    a40,b40=polynomials['40'];a96,b96=polynomials['96'];rho=F(Q(1,12))
    neg40=bernstein2(a40,Z,rho);pos96=[a96[1],a96[1]+a96[2]*rho]
    need(a96[0]==Z and all(c<Z for c in neg40) and all(c>Z for c in pos96),'positive tiny-yaw two-width signs fail')
    determinant_poly=[x-y for x,y in zip(multiply(b40,a96),multiply(b96,a40))]
    C=F(Q(64,5))*(3-phi)
    need(determinant_poly==[Z,Z,C,Z,C] and C>Z,'full actual40/96 elimination determinant differs')
    farther=[]
    for x in (lo,hi):
        p40=[x*a40[i]+b40[i] for i in range(3)]
        controls=bernstein2(p40,rho,F(Q(1,4)))
        need(all(g>Z for g in controls),'entire larger positive yaw interval is not excluded by actual40')
        farther.append({'x':x.encode(),'all3_positive_actual40_Bernstein_controls':encode(controls)})
    Hv=halfturn(U if wrong_symmetry else v)
    g=matmul(matmul(transpose(M),Hv),M)
    need(matmul(g,transpose(g))==I and determinant(g)==O and matmul(g,g)==I,'candidate companion action is not a proper involution')
    permutation=[V.index(act(g,w)) for w in V]
    need(len(set(permutation))==60,'candidate companion action is not an actual body symmetry')
    # Complete degree-two polynomial covariance, not sampled evidence.
    zero=[Z,Z,Z];one=[O,Z,O]
    Hrnum=[[[ -O,Z,O],zero,[Z,2*O,Z]],[zero,[-O,Z,-O],zero],[[Z,2*O,Z],zero,[O,Z,-O]]]
    cos=[F(Q(3,5)),F(Q(8,5)),F(Q(-3,5))]
    sin=[F(Q(-4,5)),F(Q(6,5)),F(Q(4,5))]
    expected=[[cos,zero,sin],[zero,one,zero],[[-a for a in sin],zero,cos]]
    coefficients=[]
    for i in range(3):
        for j in range(3):
            actual=[sum((Hrnum[i][l][k]*Hv[l][j] for l in range(3)),Z) for k in range(3)]
            need(actual==expected[i][j],'full proper companion yaw covariance polynomial differs')
            coefficients.append({'matrix_entry':[i,j],'all3_coefficients':encode(actual)})
    transport=[]
    for x in (lo,midpoint,hi):
        b=beta(x);cp=tuple(p[i]+b*direction[i] for i in range(3));r=(x,Z,O)
        need(all(rotate(cp,w)==rotate(tuple(b*j for j in U),act(M,w)) for w in [(O,Z,Z),(Z,O,Z),(Z,Z,O)]),
             'actual companion source Cayley formula differs')
        tests=[]
        for j,w in enumerate(V):
            q=projection(rotate(cp,w),x);opposite=projection(moving[permutation[j]],x)
            need(all(q[i]==-opposite[i] for i in range(2)),'full original proper companion shadow transport differs')
            tests.append({'source_original':j,'body_image_original':permutation[j],'companion_projection':encode(q)})
        membership=[data['height']-dot(n,cp) for n in data['normals']]
        need(all(t>=Z for t in membership),'actual original companion source-facet membership differs')
        transport.append({'x':x.encode(),'companion_z':b.encode(),'companion_original_c':encode(cp),
                          'all12_actual_source_D_gaps':encode(membership),'all60_actual_projected_vertex_transports':tests})
    translation=[]
    for x in (lo,hi):
        r=(x,Z,O);m=cross(sub(V[36],V[48]),r);H=dot(m,V[48])
        need(dot(m,moving[32])==H and cross(m,U)==r,'persistent ORIGINAL translation closure differs')
        translation.append({'x':x.encode(),'actual_normal':encode(m),'height':H.encode(),'normal_cross_U':encode(cross(m,U))})
    return {'agent':'six-rupert-3','role':'researcher','actual_original_model_and_twelve_source_forms_rebuilt':True,
        'parent':encode(p),'parent_rotation':list(map(encode,M)),'original_source_facet':{'index':ni,'normal':encode(data['normals'][ni]),'height':data['height'].encode(),'original_D_vertex_labels':ids,'full5_cyclic_vertices':list(map(encode,face))},
        'source_S':'ENTIRE CLOSED conv(F/3,F); no initial relative source-norm gate','source_radial_alpha':str(alpha),
        'all10_exact_source_vertex_transverse_entry_and_yaw_controls':gates,'all240_actual_paired_square_supports':square,
        'actual_unit_inradius_moving_square_u':encode(u),'actual_unit_inradius_moving_square_v':encode(v),
        'all12_original_facet_yaw_line_inequalities':limits,'whole_source_yaw_interval':encode((zlo,zhi)),
        'source_axis_endpoint_original_convex_membership':[
            {'yaw':zlo.encode(),'original_c':encode(axis_endpoints[0]),'original_D_labels':[ids[1]],'weights':['1']},
            {'yaw':zhi.encode(),'original_c':encode(axis_endpoints[1]),'original_D_labels':[ids[3],ids[4]],'weights':['1/2','1/2']}],
        'whole_closed_receiver_interval':encode((lo,hi)),
        'companion_membership_entire_closed_receiver_interval':True,
        'companion_beta_endpoint_values':encode((beta(lo),beta(hi))),
        'companion_beta_monotonicity_identity':'beta(y)-beta(x)=5*(y-x)/((x+2)*(y+2)); both denominators positive',
        'all480_actual_receiving_paired_width_controls':support_records,'all3_fresh_actual_width_polynomials':{k:{'x_coefficients':encode(a),'constant_coefficients':encode(b)} for k,(a,b) in polynomials.items()},
        'all18_direct_physical_full_width_polynomial_fixtures':fixtures,'all3_negative_small_positive_yaw40_controls':encode(neg40),
        'all2_positive_small_yaw96_over_z_controls':encode(pos96),'full40_96_elimination_polynomial':encode(determinant_poly),
        'all6_strict_positive40_controls_for_yaw1_over12_to1_over4':farther,
        'actual_proper_body_companion_symmetry':list(map(encode,g)),'all60_original_body_vertex_images':permutation,
        'all27_exact_continuum_proper_companion_matrix_coefficients':coefficients,
        'all180_original_companion_projected_vertex_transports':transport,'all2_original_translation_and_spanning_identities':translation,
        'complete_ordinary_claim':'For EVERY original c in the ENTIRE closed S, every r=(x,0,1), ell<=x<=s, every original physical t in r-perp and lambda>=1: lambda P_rR(c)K+t subseteq P_rK IFF lambda1,t0 and either c=c* or c=c*+beta(x)*(c*_z,1,-c*_x), beta(x)=(2x-1)/(x+2). BOTH source branches belong to S for EVERY receiver, including both endpoints. All source fits are on the actual OUTER facet; no strict passage.',
        'only_mathematical_dependency':'public10074 supplies ONLY the parent converse on the ENTIRE closed midpoint receiver segment; sourceentry, larger positive-yaw exclusion, actual body action and moving companion membership are rebuilt',
        'source_forest_or_proposal_or_private_predecessor_runtime_input':False,
        'full_SO3_or_global_nonRupert_claimed':False,'proof_status':'Complete ordinary intermediate proof; author checked/unformalized/independently UNREVIEWED'}

def scalar_bridges(radius=Q(1,5)):
    ell,s,h=2*phi-3,2-phi,1+2*phi;delta=F(radius)
    need(h*ell==O and Z<delta<ell<F(Q(1,4)),
         'uniform metric gate does not enter the strict transverse/yaw cylinder')
    beta=lambda x:(2*x-O)/(x+2)
    chi=F(Q(3,11));rho=(2*phi-3)/(4-phi)
    need(ell<chi<s and beta(chi)==-delta and beta(ell)==-ell and beta(s)==-rho,
         'actual centered radius-one-fifth companion membership differs')
    need(F(Q(1,12))<F(Q(1,11))<rho<delta,'prior single-center threshold ordering differs')
    trace=(3-delta*delta)/(O+delta*delta);distance=8*delta*delta/(O+delta*delta)
    need(trace==F(Q(37,13)) and distance==F(Q(4,13)),
         'closed radius-one-fifth physical metric conversion differs')
    open_trace=(3-ell*ell)/(O+ell*ell);open_distance=8*ell*ell/(O+ell*ell)
    need(open_trace==(O+8*phi)/5 and open_distance==(28-16*phi)/5,
         'open radius-ell physical metric conversion differs')
    rejected=False
    try:
        bad=F(Q(1,4))
        need(bad<ell,'uniform metric gate does not enter the strict transverse/yaw cylinder')
    except ValueError as e:
        need(str(e)=='uniform metric gate does not enter the strict transverse/yaw cylinder',
             'unexpected scalar false control failure')
        rejected=True
    need(rejected,'unsupported radius-one-quarter cylinder certificate accepted')
    return {'ell':ell.encode(),'body_support_height_h':h.encode(),'exact_h_times_ell_is_one':True,
        'closed_companion_SET_radius':delta.encode(),'closed_trace_lower_bound':trace.encode(),
        'closed_squared_Frobenius_upper_bound':distance.encode(),
        'centered_one_fifth_companion_receiver_entry':chi.encode(),
        'prior_independent_sharp_single_center_rho':rho.encode(),
        'open_companion_SET_radius':ell.encode(),'strict_trace_lower_bound':open_trace.encode(),
        'strict_squared_Frobenius_upper_bound':open_distance.encode(),
        'false_one_quarter_transverse_metric_certificate_rejected':True,
        'one_quarter_region_falsity_or_SET_radius_optimality_claimed':False}

def full_record():
    return {'agent':'six-rupert-3','role':'researcher',
            'complete_common_geometric_record':prove(),
            'complete_scalar_bridges':scalar_bridges(),
            'claim_scope':'Conditional anisotropic gate, closed centered and companion-SET 1/5 gates, open companion-SET ell gate, and entire closed source conv(F/3,F), over the whole closed receiver segment. Original translation and lambda>=1 retained.',
            'only_mathematical_dependency':'public10074 fixed-source converse on the whole receiver segment',
            'prior_review_credit':'Independent10093/10 sharp open single-center rho and endpoint body action are prior art; its verdict is not transferred to this result.',
            'full_SO3_arbitrary_source_or_receiver_coverage_claimed':False,
            'global_nonRupert_claimed':False,
            'proof_status':'Complete ordinary intermediate proof; author checked/unformalized/independently UNREVIEWED'}

def negative_controls():
    cases=[]
    for name,operation,message in [
        ('unsupported-full-frustum-alpha-one-quarter',lambda:prove(alpha=Q(1,4)),
         'whole-frustum transverse cusp entry fails'),
        ('wrong-proper-body-halfturn-HU',lambda:prove(wrong_symmetry=True),
         'full proper companion yaw covariance polynomial differs'),
        ('unsupported-uniform-metric-one-quarter',lambda:scalar_bridges(radius=Q(1,4)),
         'uniform metric gate does not enter the strict transverse/yaw cylinder')]:
        caught=None
        try:operation()
        except ValueError as error:caught=str(error)
        need(caught==message,'semantic false geometry accepted or rejected for the wrong reason: '+name)
        cases.append({'fixture':name,'rejection':caught,'rejected':True})
    return {'agent':'six-rupert-3','role':'researcher','semantic_false_controls':cases,
            'larger_gate_falsity_or_mathematical_nonexistence_inferred':False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    if args.output:need(not args.output.exists(),'fresh output required')
    start=time.monotonic();mathematical=negative_controls() if args.controls else full_record()
    pins=verify_pins()
    expected=json.loads((HERE/'EXPECTED.json').read_text())['controls' if args.controls else 'production']
    actual={name:digest(value) for name,value in mathematical.items()}
    need(actual==expected['all_section_sha256'],'complete declared section record differs')
    need(digest(mathematical)==expected['whole_mathematical_sha256'],'complete mathematical record differs')
    if not args.controls:
        need({name:digest(value) for name,value in mathematical['complete_common_geometric_record'].items()}==expected['all_geometric_section_sha256'],
             'complete declared geometric section record differs')
    record={'mathematical':mathematical,'declared_inputs_sha256':pins,'optimized':not __debug__,
            'seconds':round(time.monotonic()-start,3),'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'python_version':sys.version.split()[0]}
    if args.output:args.output.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'whole_mathematical_sha256':digest(mathematical),'declared_inputs_sha256':pins,
                      'controls':args.controls,'seconds':record['seconds'],'peak_kib':record['peak_kib']},sort_keys=True))

if __name__=='__main__':main()
