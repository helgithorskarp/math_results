#!/usr/bin/env python3
"""Exact finite hypotheses for the global parametric RID source filter.

PROOF.md supplies the continuum and inverse-branch arguments. The complete
published prerequisites are hash verified and replayed. Ordered Q(phi)
and rational squared gates suffice; no approximate root evaluation is used.
"""
from pathlib import Path
from fractions import Fraction as Q
from importlib.util import module_from_spec,spec_from_file_location
import argparse,hashlib,json,sys

HERE=Path(__file__).resolve().parent

def require(condition,message):
    if not condition:raise ValueError(message)

def replay():
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','PROOF.md','DEPENDENCIES.json','expected.json'},'filter inventory differs')
    for name,digest in pin['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,'published filter changed:'+name)
    require('field' not in sys.modules,'arithmetic loaded before verification')
    spec=spec_from_file_location('parametric_filter_dependency',directory/'check.py')
    f=module_from_spec(spec);spec.loader.exec_module(f)
    result=f.verify();output=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(output==(directory/'expected.json').read_bytes(),'whole filter expected record differs')
    five=json.loads((directory/'DEPENDENCIES.json').read_text());fold=(directory/five['directory']).resolve()
    original=json.loads((fold/'DEPENDENCIES.json').read_text());base=(fold/original['directory']).resolve()
    require(Path(sys.modules['field'].__file__).resolve()==base/'field.py','verified arithmetic location differs')
    for name,digest in original['sha256'].items():
        require(hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,'original source changed after replay:'+name)
    spec=spec_from_file_location('parametric_original_geometry',base/'verify.py')
    b=module_from_spec(spec);spec.loader.exec_module(b)
    return b,{'filter_whole_expected_bytes':len(output),'filter_whole_expected_sha256':hashlib.sha256(output).hexdigest(),
              'source_commit':pin['source_commit'],'graph':pin['graph_ref'],
              'transitive_replay':'complete filter, fivefold and original brightness records'}

def contact_order(b, V, w):
    p2 = (7-4*b.PHI)/5
    s = b.dot(w, w)
    J = [v for v in V if b.dot(w, v)**2/s == p2]
    u = (-b.PHI, b.ZERO, b.ZERO)
    t = b.cross(w, u)
    by_point = {(b.dot(u, v), b.dot(t, v)):v for v in J}
    require(len(by_point) == len(J) == 10, 'original contact projection collision')
    points = sorted(by_point)
    def turn(a, c, d):
        return (c[0]-a[0])*(d[1]-a[1])-(c[1]-a[1])*(d[0]-a[0])
    def half(seq):
        result = []
        for q in seq:
            while len(result)>1 and turn(result[-2], result[-1], q)<=b.ZERO:
                result.pop()
            result.append(q)
        return result
    hull = half(points)[:-1]+half(reversed(points))[:-1]
    require(len(hull) == 10, 'reference contact polygon is not a decagon')
    return [by_point[q] for q in hull]


def edge_geometry(b, V, ring, w, radius=Q(1, 20)):
    F, phi, zero = b.F, b.PHI, b.ZERO
    sn = b.dot(w, w)
    p2 = (7-4*phi)/5
    require(len(ring) == len(set(ring)) == 10 and set(ring)
            == {v for v in V if b.dot(w, v)**2/sn == p2},
            'contact loop is not ten distinct complete actual originals')
    require(all(b.neg(v) in ring for v in ring), 'contact loop is not centrally symmetric')
    require(0 < radius <= Q(1, 20), 'contact proof radius outside declared domain')
    p_upper, tangent_upper = Q(1, 3), Q(7, 5)
    require(p2 < F(p_upper*p_upper) and (3+4*phi)/5 < F(tangent_upper*tangent_upper),
            'positive height/halfedge root bounds fail')
    require(2-(p_upper+tangent_upper*radius)**2 > Q(9, 5),
            'projected edge denominator not above9/5')
    cosines = []
    identities = 0
    samples = [w, (F(Q(1, 100)), phi, b.ONE),
               (b.ZERO, phi+F(Q(1, 100)), b.ONE),
               (F(Q(1, 100)), phi+F(Q(1, 100)), b.ONE+F(Q(1, 100)))]
    for i, vi in enumerate(ring):
        vj = ring[(i+1)%10]
        M = tuple((vi[k]+vj[k])/2 for k in range(3))
        T = tuple((vj[k]-vi[k])/2 for k in range(3))
        require(b.dot(M, w) == zero and b.dot(M, M) == phi**6,
                'opposite-height equatorial midpoint identity fails')
        require(b.dot(M, T) == zero and b.dot(T, T) == F(2),
                'orthogonal midpoint/halfedge identity fails')
        require(b.dot(T, w)**2/sn == p2 and b.dot(T, T)-p2 == (3+4*phi)/5,
                'halfedge height/tangent identity fails')
        for vk in ring:
            if vk in (vi, vj):
                continue
            L = b.cross(b.sub(vj, vi), b.sub(vk, vi))
            ref = b.dot(w, L)
            require(ref > zero, 'contact loop has nonpositive orientation')
            ratio = ref*ref/(sn*b.dot(L, L))
            require(ratio > F(radius*radius), 'contact order unstable on whole chord cap')
            cosines.append(ratio)
        for r in samples:
            r2 = b.dot(r, r)
            PM = tuple(M[k]-r[k]*b.dot(r, M)/r2 for k in range(3))
            PT = tuple(T[k]-r[k]*b.dot(r, T)/r2 for k in range(3))
            pt2 = b.dot(PT, PT)
            require(pt2 > zero, 'sample projected edge is degenerate')
            direct = (b.dot(PM, PM)*pt2-b.dot(PM, PT)**2)/pt2
            reduced = phi**6-2*b.dot(r, M)**2/(2*r2-b.dot(r, T)**2)
            require(direct == reduced, 'physical Gram/edge-distance identity differs')
            identities += 1
    require(len(cosines) == 80 and identities == 40, 'edge check counts differ')
    return dict(original_contact_edges=10, robust_convexity_comparisons=80,
                minimum_normalized_boundary_dot_squared=min(cosines).encode(),
                contact_order_chord=str(radius), original_antipodal_contacts=10,
                edge_midpoint_squared_radius=(phi**6).encode(),
                edge_halfdifference_squared_length='2',
                edge_tangent_squared_radius=((3+4*phi)/5).encode(),
                physical_edge_distance_identity_checks=identities,
                projected_edge_squared_length_lower='9/5',
                contact_width_squared_lower='(20+32phi)*(1-(10/9)*d^2)')


def scalar_gates(b, first_coefficient=Q(8), second_coefficient=Q(9)):
    F,p,Z=b.F,b.PHI,b.ZERO
    A0=12+28*p; A0sq=A0**2
    A1sq=940+1520*p; A2sq=960+1536*p
    rho0sq=(288+464*p)/5;rho5sq=48+64*p
    require(Z<A0sq<A1sq<A2sq,'first three positive polar levels not ordered')
    require(F(Q(583,10)**2)<A1sq<F(Q(11661,200)**2),'positive A1 root bracket fails')
    eta_upper=Q(2,5)
    cross=A2sq-A1sq-F(eta_upper**2)
    margin=4*A1sq*eta_upper**2-cross**2
    require(cross>Z and margin>Z,'third-minus-second area gap is not below2/5')
    require(2*eta_upper/58<Q(3,25)**2,'initial fivefold chord not below3/25')
    require(rho5sq>F(12**2) and A1sq<F(59**2),'fivefold root brackets fail')
    require(Q(499,500)**2<1-Q(3,25)**2/4,'first chord square-root bracket fails')
    first=12*Q(499,500)-59*Q(3,25)/2
    require(first>first_coefficient and first_coefficient>=8,'first fivefold coercivity fails')
    require(eta_upper/first_coefficient<=Q(1,20),'first bootstrap not in second chord domain')
    require(Q(999,1000)**2<1-Q(1,20)**2/4,'second chord square-root bracket fails')
    second=12*Q(999,1000)-59*Q(1,20)/2
    require(second>second_coefficient and second_coefficient>=9,'second fivefold coercivity fails')
    require(eta_upper/second_coefficient<=Q(2,45)<Q(1,20),'fivefold root outside contact cap')
    branch=[]
    for name,Asq,rsq in [('twofold',A0sq,rho0sq),('fivefold',A1sq,rho5sq)]:
        S=Asq+rsq;rmax2=1-Asq/A2sq
        require(S>A2sq>Asq>Z and rsq>Z,'inverse radicand or positive branch fails:'+name)
        require(Z<rmax2<rsq/S,'tangent function not increasing throughout polar interval:'+name)
        branch.append({'orbit':name,'axis_area_squared':Asq.encode(),'tangent_inradius_squared':rsq.encode(),
                       'S':S.encode(),'strict_subthird_radicand_lower':(S-A2sq).encode(),
                       'polar_transverse_squared_upper':rmax2.encode(),
                       'increasing_interval_squared_limit':(rsq/S).encode()})
    return {'A0':A0.encode(),'A1_squared':A1sq.encode(),'A2_squared':A2sq.encode(),
            'A1_positive_root_bracket':['583/10','11661/200'],
            'strict_A2_minus_A1_upper':str(eta_upper),'gap_positive_cross':cross.encode(),
            'gap_positive_root_margin':margin.encode(),'inverse_branches':branch,
            'fivefold_initial_chord_upper':'3/25','first_coercivity_lower':str(first_coefficient),
            'first_coercivity_rational':str(first),'second_chord_upper':'1/20',
            'second_coercivity_lower':str(second_coefficient),'second_coercivity_rational':str(second),
            'fivefold_inverse_chord_strict_upper':'(T-A1)/9<2/45<1/20',
            'fivefold_parametric_width_threshold':'(20+32phi)*(1-(20/9)*(1-zeta5(T)))'}


def twofold_cutoff(b,budget_squared,rstar,chordstar,label):
    F,p,Z=b.F,b.PHI,b.ZERO;A0=12+28*p;rho2=(288+464*p)/5
    require(0<rstar<1 and 0<chordstar<1,'invalid positive cutoff')
    maxr2=1-A0**2/budget_squared
    require(F(rstar*rstar)<maxr2<rho2/(A0**2+rho2),'cutoff outside increasing polar interval')
    cross=budget_squared-A0**2*(1-rstar*rstar)-rho2*rstar*rstar
    margin=4*A0**2*rho2*rstar*rstar*(1-rstar*rstar)-cross**2
    require(cross>Z and margin>Z,'false positive-root transverse cutoff:'+label)
    require(rstar*rstar<chordstar*chordstar*(1-chordstar*chordstar/4),'false chord consequence:'+label)
    return {'label':label,'budget_squared':budget_squared.encode(),'source_transverse_strict_upper':str(rstar),
            'source_normal_chord_strict_upper':str(chordstar),'positive_cross':cross.encode(),
            'positive_root_margin':margin.encode()}


def uniform_corollaries(b):
    F,p,Z=b.F,b.PHI,b.ZERO;A1sq=940+1520*p;A2sq=960+1536*p
    records=[]
    for eta,rstar,chordstar in [(Q(1,4),Q(3,25),Q(1,8)),(Q(3,8),Q(13,100),Q(2,15))]:
        upper=Q(11661,200)+eta
        require(A1sq<F(Q(11661,200)**2) and F(upper**2)<A2sq,'corollary not subthird')
        row=twofold_cutoff(b,F(upper**2),rstar,chordstar,'eta<='+str(eta))
        row.update({'eta_upper':str(eta),'rational_area_upper':str(upper),
                    'simple_receiving_width_threshold':'(20+32phi)*(1-10*eta^2/729)'})
        records.append(row)
    records.append(twofold_cutoff(b,A2sq,Q(2,15),Q(7,50),'whole A1<T<A2'))
    return records


def receiving_band(b,V,C,width_sign=-1):
    F,p,Z,O=b.F,b.PHI,b.ZERO,b.ONE;k=(2+p)/5;U=Q(7,100);delta=Q(3,10);eta=Q(3,8)
    A0=12+28*p;D0=8+8*p;D1=4+2*p;alpha=D0-D1*k
    lo,hi=k-F(delta),k+F(delta)
    corners=[(Z,Z,O),(F(U),lo*U,O),(F(U),hi*U,O)];records=[]
    for r in corners:
        raw=b.brightness_raw(C,r);direct,count=b.direct_shadow_raw(V,r)
        envelope=A0+alpha*r[0]+D1*r[1]
        require(raw==direct==envelope,'original Cauchy/physical corner area differs')
        require(count==(12 if r[0]==Z else 16),'complete projected hull corner count differs')
        records.append({'raw_corner':b.encode(r),'direct_raw_shadow_area':direct.encode(),
                        'hull_vertices':count,'raw_Cauchy_area':raw.encode(),'envelope':envelope.encode()})
    require(Z<lo and alpha>Z and D1>Z,'receiving raw area coefficient signs fail')
    du=D0-D1*delta-A0*(1+hi**2)*U
    dt=D1*(1+U**2)-(A0*U+alpha*U**2)*hi
    require(du>Z and dt>Z,'normalized receiving area envelope monotonicity fails')
    rawmax=A0+(D0+D1*delta)*U;normmax2=1+(1+hi**2)*U**2
    L=Q(583,10)+eta;area_margin=F(L**2)*normmax2-rawmax**2
    require(area_margin>Z and F(Q(583,10)**2)<940+1520*p,'whole band area not below A1+3/8')
    B=3*p**2;S=p+2;mmax=(p-k+F(delta))*U
    require(Z<p-k-F(delta) and Z<mmax<p/12,'whole band width parameter interval fails')
    supports=[];attainer=(2*p,-p**2,-p)
    require(attainer in V,'width attainer is not an original')
    for m in [Z,mmax]:
        d=(p,-O,F(width_sign)*m);h=B+p*m
        require(max(b.dot(d,v) for v in V)==h and b.dot(d,attainer)==h,
                'whole affine width support endpoint differs')
        supports.append({'m':m.encode(),'direction':b.encode(d),'actual_support':h.encode(),
                         'support_attainer':b.encode(attainer)})
    require(p*S-B*mmax>Z,'physical directional width not increasing in m')
    width2=4*(B+p*mmax)**2/(S+mmax**2)
    limit=(20+32*p)*(1-Q(10,729)*eta**2)
    require(width2<limit,'whole receiving band does not satisfy simple width corollary')
    examples=[]
    for u in [Q(1,15),U]:
        r=(F(u),hi*u,O);r2=b.dot(r,r);direct,count=b.direct_shadow_raw(V,r)
        m=p*r[0]-r[1];d=(p,-O,F(width_sign)*m)
        require(b.dot(r,d)==Z,'example physical width direction is not perpendicular')
        oldupper=Q(11661,200)+Q(1,4)
        excess=direct**2-F(oldupper**2)*r2
        require(excess>Z,'example does not exceed original A1+1/4 filter hypothesis')
        transverse2=(r[0]**2+r[1]**2)/r2
        require(transverse2<F(Q(13,100)**2),'known identity source violates transverse conclusion')
        require(O/r2>(1-F(Q(2,15)**2)/2)**2,'known identity source violates chord conclusion')
        examples.append({'raw_major_u':str(u),'slope_offset':'3/10','raw_receiver':b.encode(r),
                         'complete_shadow_vertices':count,'direct_raw_area':direct.encode(),
                         'area_squared':(direct**2/r2).encode(),
                         'old_filter_area_excess_squared_margin':excess.encode(),
                         'identity_fit_inside_new_source_cap':True})
    return {'closed_raw_receiving_band':'r=(u,(k+rho)u,1),0<=u<=7/100,|rho|<=3/10',
            'corner_independent_complete_hulls':records,'affine_raw_envelope_coefficients':b.encode((A0,alpha,D1)),
            'normalized_envelope_u_derivative_lower':du.encode(),'outer_slope_derivative_lower':dt.encode(),
            'physical_area_strict_rational_upper':str(L),'physical_area_squared_margin':area_margin.encode(),
            'maximum_width_parameter':mmax.encode(),'complete_original_support_endpoints':supports,
            'directional_width_squared_upper':width2.encode(),'simple_width_threshold':limit.encode(),
            'width_squared_margin':(limit-width2).encode(),'old_filter_failure_examples':examples,
            'fit_status':'necessary all-source localization only; identity closed fits remain; rigidity and strict passage unresolved here'}


def negative_controls(b,V,C,ring,w):
    F,p=b.F,b.PHI
    cases=[('missing contact',lambda:edge_geometry(b,V,ring[:-1],w)),
           ('duplicate contact',lambda:edge_geometry(b,V,ring[:-1]+[ring[0]],w)),
           ('reversed projected orientation',lambda:edge_geometry(b,V,list(reversed(ring)),w)),
           ('false first coercivity9',lambda:scalar_gates(b,first_coefficient=Q(9))),
           ('false second coercivity11',lambda:scalar_gates(b,second_coefficient=Q(11))),
           ('false whole-range transverse13/100',lambda:twofold_cutoff(b,960+1536*p,Q(13,100),Q(2,15),'damaged')),
           ('false old-range transverse1/10',lambda:twofold_cutoff(b,F(Q(11711,200)**2),Q(1,10),Q(1,8),'damaged')),
           ('wrong physical width direction',lambda:receiving_band(b,V,C,width_sign=1))]
    results=[]
    for name,case in cases:
        try:case()
        except ValueError as e:results.append({'control':name,'rejected':True,'reason':str(e)});continue
        raise ValueError('damaged mathematical control accepted:'+name)
    return results


def verify():
    b,dependency=replay();V=b.vertices();w=(b.ZERO,b.PHI,b.ONE)
    ring=contact_order(b,V,w);edges=edge_geometry(b,V,ring,w)
    planes,counts=b.complete_facets(V);C,_,_=b.area_generators(V,planes)
    require(len(V)==60 and len(planes)==62 and len(C)==31,'complete named physical geometry inventory differs')
    require(set(V)=={b.neg(v) for v in V},'named original body not centrally symmetric')
    G=b.proper_group(V)
    require(len(G)==60,'proper body group count differs')
    return {'agent':'six-rupert-3','role':'researcher','arithmetic':'exact ordered Q(phi) and rational squared root gates',
            'proof_status':'complete written global source-localization theorem; author-checked, unformalized, independently unreviewed',
            'global_RID_Rupert_status':'unresolved','source_scope':'every orthonormal source frame, arbitrary proper planar roll, actual physical translation and lambda>=1',
            'parametric_filter':'A1<T<A2; A(receiver)<=T; mu(receiver)^2<=(20+32phi)*(1-(20/9)*(1-zeta5(T)))',
            'inverse_functions':'A_5=A_1; j=0,5; S_j=A_j^2+rho_j^2; zeta_j=(A_j*T+rho_j*sqrt(S_j-T^2))/S_j; r_j=(rho_j*T-A_j*sqrt(S_j-T^2))/S_j',
            'conclusion':'some directed twofold axis m has transverse<=r0(T), chord squared<=2*(1-zeta0(T)); full-range transverse<2/15,chord<7/50',
            'dependency_replay':dependency,'original_geometry':{'vertices':60,'physical_facets':62,'Cauchy_generators':31,'proper_group':60,'fresh_facet_enumeration':counts},
            'contact_loop_sha256':b.digest([b.encode(v) for v in ring]),'larger_fivefold_contact_cap':edges,
            'whole_subthird_scalar_gates':scalar_gates(b),'uniform_corollaries':uniform_corollaries(b),
            'whole_larger_receiving_band_application':receiving_band(b,V,C),
            'old_annular_example_retained':'full original8732 expected record replayed; (1,0,12)/sqrt145 retains source chord strictly between1/17 and1/8',
            'damaged_controls':negative_controls(b,V,C,ring,w)}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    output=json.dumps(verify(),indent=2,sort_keys=True)+'\n'
    if not args.emit:require(output==(HERE/'expected.json').read_text(),'whole new expected record differs')
    print(output,end='')


if __name__=='__main__':main()
