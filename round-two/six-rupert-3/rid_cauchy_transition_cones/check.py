#!/usr/bin/env python3
"""Exact finite hypotheses for RID receiving cones crossing a Cauchy kink.

PROOF.md proves the continuum statement, including closed boundaries.
The full pinned prior wedge record and prerequisites are replayed first.
Python 3.11+ standard library; all new arithmetic is ordered Q(phi).
"""
from pathlib import Path
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
import argparse, hashlib, json, sys

HERE=Path(__file__).resolve().parent
U=Q(1,20)
SLOPE=Q(1,2)


def require(condition,message):
    if not condition:raise ValueError(message)


def replay():
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','PROOF.md','DEPENDENCIES.json','expected.json'},'prior wedge inventory differs')
    for name,digest in pin['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,'prior wedge source changed:'+name)
    require('field' not in sys.modules,'arithmetic loaded before verification')
    spec=spec_from_file_location('transition_wedge_dependency',directory/'check.py')
    w=module_from_spec(spec);spec.loader.exec_module(w)
    result=w.verify();output=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(output==(directory/'expected.json').read_bytes(),'whole prior wedge expected record differs')
    base=directory
    for unused in range(3):
        child=json.loads((base/'DEPENDENCIES.json').read_text())
        base=(base/child['directory']).resolve()
        for name,digest in child['sha256'].items():
            require(hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,'transitive source changed after replay:'+name)
    require(Path(sys.modules['field'].__file__).resolve()==base/'field.py','original verified arithmetic location differs')
    spec=spec_from_file_location('transition_original_geometry',base/'verify.py')
    b=module_from_spec(spec);spec.loader.exec_module(b)
    return b,w,{'whole_wedge_expected_bytes':len(output),'whole_wedge_expected_sha256':hashlib.sha256(output).hexdigest(),
                'source_commit':pin['source_commit'],'graph':pin['graph_ref'],
                'transitive_replay':'complete prior wedge, filter, fivefold and original brightness records'}


def tangent_data(b,C,transition=None,D_override=None):
    p,F,Z=b.PHI,b.F,b.ZERO
    D=[v for v in C if v[2]==Z] if D_override is None else D_override
    expected={(p-1,p,Z),(p-1,-p,Z),(1+3*p,2+p,Z),(1+3*p,-2-p,Z),(F(4),Z,Z),(Z,F(4),Z)}
    require(len(C)==31 and len(D)==6 and set(D)==expected,'actual physical tangent max inventory differs')
    signed=tuple(sum((v[i]*v[2].sign() for v in C if v[2]!=Z),Z) for i in range(3))
    require(signed==(Z,Z,12+28*p),'nonzero-height signed sum differs')
    first=(p-1)/p;second=(1+3*p)/(2+p)
    require(first==2-p and second==p,'physical Cauchy transitions differ')
    require(transition is None or transition==first,'damaged kink partition')
    require(Z<first<F(SLOPE)<second and F(SLOPE)<p-1,'new cone sign partition fails')
    low=(4+2*(p-1)+2*(1+3*p),F(4))
    middle=(4+2*(1+3*p),4+2*p)
    high=(8+4*p,F(4))  # coefficients in (major=y, minor=x) order
    require(low==(4+8*p,F(4)) and middle==(6+6*p,4+2*p),'x tangent coefficients differ')
    require(low[0]+low[1]*first==middle[0]+middle[1]*first,'Cauchy kink is discontinuous')
    families=[]
    for j,pieces in [(0,[low,middle]),(1,[high])]:
        gaps=[]
        for s,t in [(Q(0),Q(0)),(U,U*SLOPE),(U,-U*SLOPE)]:
            raw=[Z,Z,b.ONE];raw[j]=F(s);raw[1-j]=F(t)
            gaps.extend(v[2].sign()*b.dot(v,raw) for v in C if v[2]!=Z)
        require(len(gaps)==75 and min(gaps)>Z,'nonzero facet signs fail on entire receiving triangle')
        families.append({'major_axis':['x','y'][j],
                         'piece_coefficients':[[h.encode(),k.encode()] for h,k in pieces],
                         'nonzero_facet_sign_corner_comparisons':len(gaps),
                         'minimum_nonzero_facet_sign_corner_margin':min(gaps).encode()})
    return [ [low,middle],[high] ],{'tangent_original_vectors':[b.encode(v) for v in sorted(D,key=b.key)],
            'global_tangent_formula':'4|x|+4|y|+2max((phi-1)|x|,phi|y|)+2max((1+3phi)|x|,(2+phi)|y|)',
            'positive_xy_transitions':[first.encode(),second.encode()],'families':families}


def width_data(b,V,j,offset=Q(0)):
    F,p,Z=b.F,b.PHI,b.ZERO;B=3*p**2;S=p+2;old=Q(1,12)
    for m in [Z,p*old]:
        d=(p,b.ONE,-m);h=B+p*m+F(offset)
        require(all(b.dot(d,v)<=h for v in V),'physical affine width support failed')
        require(b.dot(d,(2*p,p**2,-p))==h,'actual original width witness differs')
    require(p*S-B*p*old>Z,'physical width derivative fails on entire support interval')
    require(p-SLOPE>Z and 1-p*SLOPE>Z,'new receiving width parameter can be negative')
    maximum=p*U if j==0 else F(U)
    value=4*(B+p*maximum)**2/(S+maximum*maximum)
    limit=(20+32*p)*(1-Q(10,11664))
    require(value<limit,'new entire cone fails full-source width filter')
    return {'affine_original_support_endpoint_comparisons':2*len(V),'maximum_width_parameter':maximum.encode(),
            'maximum_squared_directional_width':value.encode(),'squared_width_filter_margin':(limit-value).encode()}


def matching_data(b,epsilon=Q(11,20)):
    F,p,Z=b.F,b.PHI,b.ZERO;a=p**2;c=2+p;bmax=Q(9,2)
    zmin=Q(99,100);sing=Q(24,25);source=Q(3,25);frame=Q(4,15)
    norm2=1+(1+SLOPE*SLOPE)*U*U
    require(norm2==Q(321,320) and zmin*zmin*norm2<1,'new receiving norm/z brackets fail')
    require((1+SLOPE*SLOPE)*U*U<Q(1,11)**2,'new receiving normal chord fails')
    require(zmin*(1-bmax*U*(1+SLOPE))>Q(3,5),'new nonequatorial receiving height separation fails')
    require(Q(36,125)<Q(9,25) and Q(36,125)<epsilon*epsilon,'actual equatorial matching budget fails')
    require(1-source*source>sing*sing and zmin>sing,'equatorial singular bounds fail')
    require(2*a*sing>F(2*epsilon) and 2*c*sing-2*a>F(2*epsilon),'actual rectangle side separation fails')
    require(F(4*epsilon)*(a+c)+F(4*epsilon*epsilon)<4*a*c*sing,'proper rectangle determinant gate fails')
    roll=(epsilon+Q(9,256)+Q(9,484))/Q(22,5)
    require(Q(1,8)+roll<frame,'initially arbitrary roll/full frame budget fails')
    require(1-frame*frame/2>Q(9,10),'initial source minor-row positive diagonal fails')
    require(1-(U*SLOPE)**2/(1+zmin)>zmin,'new target minor-row diagonal fails')
    require(1+U/(1+zmin)<Q(21,20),'new target minor-row transverse factor fails')
    l1=Q(21,20)*U*SLOPE
    margin=(p**3-c)*zmin-(p**3-1)*l1
    require(l1==Q(21,800) and margin>Z,'expanded ACTUAL target minor-row exposed face fails')
    return {'receiving_raw_norm_squared_upper':str(norm2),'receiving_z_lower':str(zmin),'receiving_chord_upper':'1/11',
            'nonequatorial_original_height_lower':'3/5','match_error_upper':str(epsilon),'singular_value_lower':str(sing),
            'full_row_frame_error_upper':str(frame),'initial_roll_error_upper':str(roll),
            'target_minor_row_transverse_l1_upper':str(l1),'actual_target_minor_row_face_margin':margin.encode()}


def bootstrap_data(b,final_factor=Q(6,5),slope=SLOPE):
    F,p,Z=b.F,b.PHI,b.ZERO;bmax=Q(9,2);zmin=Q(99,100);m=U*SLOPE
    initial=Q(21,20)/(1-bmax*Q(4,15)/Q(19,10))
    require(initial==Q(399,140)<3,'initial actual minor-row localization fails')
    require(1-(3*m)**2>zmin*zmin,'first bootstrap positive diagonal fails')
    factor1=Q(21,20)/(1-bmax*(3*m)/(1+zmin))
    require(factor1==Q(4179,3305)<Q(13,10),'first exact bootstrap factor fails')
    factor2=Q(21,20)/(1-bmax*(Q(13,10)*m)/(1+zmin))
    require(factor2==Q(8358,7375)<final_factor,'second exact bootstrap factor fails')
    require(final_factor*m<=Q(3,100),'source minor outside comparison rectangles')
    gamma=[p**2,2+p];margins=[]
    for j in [0,1]:
        margin=gamma[j]-final_factor*slope*gamma[1-j]
        require(margin>Z and gamma[j]>slope*gamma[1-j],'wrong UNSQUARED summed radius branch can survive')
        margins.append(margin.encode())
    return {'actual_minor_row_initial_factor':str(initial),'subsequent_factors':[str(factor1),str(factor2)],
            'source_minor_factor_upper':str(final_factor),'source_minor_absolute_upper':'3/100',
            'wrong_branch_positive_margins':margins,'zero_minor_rule':'Y=0 forces q=y=0'}


def area_data(b,C,j,pieces,y_major_bound=Q(1,12)):
    F,p,Z=b.F,b.PHI,b.ZERO;A0=12+28*p;minor=Q(3,100);sing=Q(24,25)
    require(F(50)<A0<F(58) and 940+1520*p>F(Q(583,10)**2),'original physical area brackets fail')
    require(1-Q(3,25)**2-minor*minor>sing*sing,'whole source comparison rectangle root fails')
    for H,K in pieces:
        require(H-U*(A0+K*U*SLOPE)>Z and K-U*SLOPE*(A0+H*U)>Z,'whole raw receiving box derivative fails')
    raw=[Z,Z,b.ONE];raw[j]=F(U);raw[1-j]=F(U*SLOPE)
    H,K=pieces[-1];physical=b.brightness_raw(C,raw);norm2=F(1+(1+SLOPE*SLOPE)*U*U)
    require(physical==A0+H*U+K*U*SLOPE,'receiving upper-corner PHYSICAL area differs')
    corner=physical*physical/norm2;cap=Q(1171,20) if j==0 else Q(581,10)
    require(corner<F(cap*cap) and cap<=Q(583,10)+Q(1,4),'new area source-filter budget fails')
    cutoff=None
    if j==0:
        major=Q(3,25);lower=Q(8);upper=Q(10);rho=(2+p)/p**2
    else:
        Hy=8+4*p
        require(4-A0*minor/sing>Z and Hy-A0*Q(3,25)/sing>F(7),'y source lower bound monotonicity fails')
        threshold=F(cap)-Hy*Q(1,12)
        gate=A0*A0*(1-Q(1,12)**2)-threshold*threshold
        require(threshold>Z and gate>Z,'area comparison cannot confine source y-major tilt below1/12')
        major=y_major_bound;lower=Q(9);upper=Q(6);rho=p**2/(2+p)
        cutoff={'source_major_upper':'1/12','receiver_area_upper':str(cap),
                'positive_comparison_rhs':threshold.encode(),'positive_squared_cutoff_margin':gate.encode()}
    margins=[]
    for H,K in pieces:
        major_margin=H-A0*major/sing-F(lower)
        minor_margin=F(upper)-K-A0*minor/sing
        require(major_margin>Z and minor_margin>Z,'piecewise whole-source derivative/Lipschitz domination fails')
        margins.append({'major_derivative_margin':major_margin.encode(),'minor_Lipschitz_margin':minor_margin.encode()})
    require(lower*rho>F(upper),'paired radius tilt order does not dominate physical area change')
    return {'receiving_corner_squared_area':corner.encode(),'receiving_area_upper':str(cap),'y_major_cutoff':cutoff,
            'source_comparison_major_upper':str(major),'source_comparison_minor_upper':str(minor),
            'major_derivative_lower':str(lower),'minor_Lipschitz_upper':str(upper),'paired_radius_ratio':rho.encode(),
            'strict_area_domination_margin':(lower*rho-upper).encode(),'piece_derivative_margins':margins}


def example(b,V,C,G,pieces):
    F,Z,O=b.F,b.ZERO,b.ONE;r=(F(U),F(U*SLOPE),O);N=b.dot(r,r)
    physical=b.brightness_raw(C,r);direct,corners=b.direct_shadow_raw(V,r)
    require(physical==direct and corners==16,'independent physical seed hull differs')
    require(physical>A0_raw(b,pieces[0][0],U,U*SLOPE),'seed does not cross physical old tangent formula')
    members=[];candidates=[]
    for g in G:
        q=b.act(tuple(zip(*g)),r)
        for j in [0,1]:
            if q[2]>Z and Z<=q[j]<=q[2]/12 and 20*abs(q[1-j])<=q[j]:members.append((g,j))
            ss=[Z,F(Q(1,12))]
            if q[2]!=Z:
                critical=q[j]/q[2]
                if Z<critical<F(Q(1,12)):ss.append(critical)
            for s in ss:
                numerator=q[2]+s*q[j]
                if numerator>Z:candidates.append((numerator**2/(N*(O+s*s)),j,s))
    require(not members,'new seed covered by ANY proper prior wedge image')
    cos2,j,s=max(candidates,key=lambda item:item[0])
    require(cos2==F(Q(1604,1605)) and j==0 and s==F(U),'complete proper mirror maximum differs')
    radius=Q(1,50)
    require(cos2<F((1-radius*radius/2)**2),'seed within stated whole-mirror chord bound')
    caps={}
    for label,refs,radius in [('twofold',[(Z,Z,O)],Q(1,270)),
                              ('endpoint',[(O,Z,F(12)),(Z,O,F(12))],Q(1,15000)),
                              ('fivefold',[(Z,b.PHI,O)],Q(1,1500))]:
        scores=[]
        for g in G:
            for ref in refs:
                q=b.act(g,ref);d=b.dot(q,r)
                if d>Z:scores.append(d*d/(b.dot(q,q)*N))
        maximum=max(scores)
        require(maximum<F((1-radius*radius/2)**2),'seed covered by specified '+label+' caps')
        caps[label]={'chord_radius':str(radius),'maximum_positive_squared_cosine':maximum.encode()}
    f2=min(b.dot(v,r)**2/N for v in V)
    require(f2<F(Q(83,200)**2),'seed covered by specified prior height band')
    return {'receiving_raw_normal':b.encode(r),'physical_squared_area':(physical*physical/N).encode(),
            'original_shadow_hull_corners':corners,'all_proper_prior_wedge_members':len(members),
            'old_single_x_chamber_formula_strict_shortfall':(physical-A0_raw(b,pieces[0][0],U,U*SLOPE)).encode(),
            'complete_mirror_maximum_positive_squared_cosine':cos2.encode(),'nearest_mirror_parameter':s.encode(),
            'complete_mirror_chord_distance_lower':'1/50','outside_specified_prior_caps':caps,
            'minimum_original_height_squared':f2.encode(),'prior_cover_scope':'only the named wedges, mirror tube, caps and height band; no exhaustive literature cover assertion'}


def A0_raw(b,piece,s,t):
    H,K=piece
    return 12+28*b.PHI+H*s+K*abs(t)


def negative_controls(b,V,C,pieces):
    D=[v for v in C if v[2]==b.ZERO]
    cases=[lambda:tangent_data(b,C,D_override=D[:-1]),lambda:tangent_data(b,C,transition=b.F(Q(1,2))),
           lambda:require(b.brightness_raw(C,(b.F(U),b.F(U*SLOPE),b.ONE))==A0_raw(b,pieces[0][0],U,U*SLOPE),'old single chamber frozen across kink'),
           lambda:width_data(b,V,0,Q(-1,100)),lambda:matching_data(b,epsilon=Q(1)),
           lambda:bootstrap_data(b,final_factor=Q(1)),lambda:bootstrap_data(b,slope=Q(1)),
           lambda:area_data(b,C,1,pieces[1],y_major_bound=Q(3,25))]
    for case in cases:
        try:case()
        except ValueError:continue
        raise ValueError('damaged certificate or enlarged-domain control accepted')
    return len(cases)


def verify():
    b,w,pin=replay();V=b.vertices();planes,pc=b.complete_facets(V);C,records,cc=b.area_generators(V,planes)
    G=b.proper_group(V);Z,O=b.ZERO,b.ONE
    require(((-O,Z,Z),(Z,-O,Z),(Z,Z,O)) in G,'proper transverse half-turn absent')
    geometry=w.originals(b,V);pieces,tangent=tangent_data(b,C)
    families=[{'major_axis':['x','y'][j],**width_data(b,V,j),**area_data(b,C,j,pieces[j])} for j in [0,1]]
    return {'agent':'six-rupert-3','role':'researcher','arithmetic':'exact ordered Q(phi); no floating comparison',
            'proof_status':'complete written continuum proof with exact finite hypotheses; author-checked, unformalized, unreviewed',
            'global_RID_Rupert_status':'unresolved','receiving_set':'S=W union P; W pinned prior wedge; P all proper g images of normalized(s,t,1) and(t,s,1),0<=s<=1/20,abs(t)<=s/2',
            'closed_fit_classification':'every lambda>=1, arbitrary source/proper planar roll/physical translation: lambda=1,T=0,B1=sigma B2 g',
            'direct_prerequisite':pin,'original_vertices':len(V),'proper_body_group_order':len(G),
            'physical_facet_record_sha256':b.digest(records),'physical_area_generators':len(C),
            'physical_tangent_structure':tangent,'original_geometry':geometry,'full_frame_matching':matching_data(b),
            'actual_minor_row_bootstrap':bootstrap_data(b),'families':families,'new_receiving_example':example(b,V,C,G,pieces),
            'new_damaged_controls_rejected':negative_controls(b,V,C,pieces),**pc,**cc}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    output=(json.dumps(verify(),indent=2,sort_keys=True)+'\n').encode()
    if not args.emit:require(output==(HERE/'expected.json').read_bytes(),'new complete expected record differs')
    sys.stdout.buffer.write(output)


if __name__=='__main__':main()
